# Copyright 2019 Google LLC. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Chicago taxi example using TFX."""

import datetime
import os
from typing import List
from fileinput import filename
import logging
import boto3
from botocore.exceptions import ClientError
import os
from dotenv import load_dotenv

import tensorflow_model_analysis as tfma
from tfx.components import FileBasedExampleGen
from tfx.components.base.executor_spec import ExecutorClassSpec
from tfx.components.example_gen.custom_executors import parquet_executor
from tfx.components import Evaluator
from tfx.components import ExampleValidator
from tfx.components import Pusher
from tfx.components import SchemaGen
from tfx.components import StatisticsGen
from tfx.components import Trainer
from tfx.dsl.components.common import resolver
from tfx.dsl.experimental import latest_blessed_model_resolver
from tfx.orchestration import data_types
from tfx.orchestration import metadata
from tfx.orchestration import pipeline
from tfx.orchestration.airflow.airflow_dag_runner import AirflowDagRunner
from tfx.orchestration.airflow.airflow_dag_runner import AirflowPipelineConfig
from tfx.proto import pusher_pb2
from tfx.proto import trainer_pb2
from tfx.types import Channel
from tfx.types.standard_artifacts import Model
from tfx.types.standard_artifacts import ModelBlessing

load_dotenv()

#Credentials aws
AWS_ACCESS_KEY= os.getenv('AWS_ACCESS_KEY')
AWS_SECERT_KEY= os.getenv('AWS_SECERT_KEY')

# dowload file from s3 bucket
bucket = 'delta-lake-mlops'
object_name = 'Test/data.gzip'
file_name = '/usr/local/airflow/data/data.gzip'

s3_client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECERT_KEY)
s3_client.download_file(bucket, object_name, file_name)


# TODO(jyzhao): rename to chicago_taxi_airflow.
_pipeline_name = 'police-uk-pipeline'

# This example assumes that the taxi data is stored in ~/taxi/data and the
# taxi utility function is in ~/taxi.  Feel free to customize this as needed.
_data_root = "/usr/local/airflow/data/"
# Python module file to inject customized logic into the TFX components. The
# Transform and Trainer both require user-defined functions to run successfully.
_module_file = '/usr/local/airflow/dags/police-uk_utils.py'
# Path which can be listened to by the model server.  Pusher will output the
# trained model here.
_serving_model_dir = "/usr/local/airflow/dags/police-uk-pipeline/pipeline/model"

# Directory and data locations.  This example assumes all of the chicago taxi
# example code and metadata library is relative to $HOME, but you can store
# these files anywhere on your local filesystem.
_pipeline_root = "/usr/local/airflow/dags/police-uk-pipeline/pipeline/"
# Sqlite ML-metadata db path.
_metadata_path = "/usr/local/airflow/dags/police-uk-pipeline/metadata/metadata.db"

# Pipeline arguments for Beam powered Components.
_beam_pipeline_args = [
    '--direct_running_mode=multi_processing',
    # 0 means auto-detect based on on the number of CPUs available
    # during execution time.
    '--direct_num_workers=0',
]

# Airflow-specific configs; these will be passed directly to airflow
_airflow_config = {
    'schedule_interval': None,
    'start_date': datetime.datetime(2019, 1, 1),
}


def _create_pipeline(
    pipeline_name: str, 
    pipeline_root: str, 
    data_root: str,
    module_file: str, 
    serving_model_dir: str,
    metadata_path: str,
    beam_pipeline_args: List[str]
    ) -> pipeline.Pipeline:
  """Implements the chicago taxi pipeline with TFX."""
  # Parametrize data root so it can be replaced on runtime. See the
  # "Passing Parameters when triggering dags" section of
  # https://airflow.apache.org/docs/apache-airflow/stable/dag-run.html
  # for more details.
  data_root_runtime = data_types.RuntimeParameter(
      'data_root', ptype=str, default=data_root)

  # Brings data into the pipeline or otherwise joins/converts training data.
  # example_gen = CsvExampleGen(input_base=data_root_runtime)

  executor_spec = ExecutorClassSpec(parquet_executor.Executor)
  example_gen = FileBasedExampleGen(input_base=data_root_runtime, custom_executor_spec=executor_spec)

  # Computes statistics over data for visualization and example validation.
  statistics_gen = StatisticsGen(examples=example_gen.outputs['examples'])

  # Generates schema based on statistics files.
  schema_gen = SchemaGen(
      statistics=statistics_gen.outputs['statistics'],
      infer_feature_shape=False)

  # Performs anomaly detection based on statistics and data schema.
  example_validator = ExampleValidator(
      statistics=statistics_gen.outputs['statistics'],
      schema=schema_gen.outputs['schema'])


  # Uses user-provided Python function that implements a model.
  trainer = Trainer(
      module_file=module_file,
      examples=example_gen.outputs['examples'],
      schema=schema_gen.outputs['schema'],
      train_args=trainer_pb2.TrainArgs(num_steps=1000),
      eval_args=trainer_pb2.EvalArgs(num_steps=20))


# Get the latest blessed model for model validation.
  model_resolver = resolver.Resolver(
      strategy_class=latest_blessed_model_resolver.LatestBlessedModelResolver,
      model=Channel(type=Model),
      model_blessing=Channel(
          type=ModelBlessing)).with_id('latest_blessed_model_resolver')


# Uses TFMA to compute a evaluation statistics over features of a model and
  # perform quality validation of a candidate model (compared to a baseline).
  eval_config = tfma.EvalConfig(
      model_specs=[
          tfma.ModelSpec(label_key='age_range')
          ],
      metrics_specs=[
          tfma.MetricsSpec(
              thresholds={
                  'accuracy':
                      tfma.MetricThreshold(
                          value_threshold=tfma.GenericValueThreshold(
                              lower_bound={'value': 0.6}),
                          # Change threshold will be ignored if there is no
                          # baseline model resolved from MLMD (first run).
                          change_threshold=tfma.GenericChangeThreshold(
                              direction=tfma.MetricDirection.HIGHER_IS_BETTER,
                              absolute={'value': -1e-10}))
              })
      ])

  evaluator = Evaluator(
      examples=example_gen.outputs['examples'],
      model=trainer.outputs['model'],
      baseline_model=model_resolver.outputs['model'],
      eval_config=eval_config)

  # Checks whether the model passed the validation steps and pushes the model
  # to a file destination if check passed.
  pusher = Pusher(
      model=trainer.outputs['model'],
      model_blessing=evaluator.outputs['blessing'],
      push_destination=pusher_pb2.PushDestination(
          filesystem=pusher_pb2.PushDestination.Filesystem(
              base_directory=serving_model_dir)))

  return pipeline.Pipeline(
      pipeline_name=pipeline_name,
      pipeline_root=pipeline_root,
      components=[
          example_gen,
          statistics_gen,
          schema_gen,
          example_validator,
          trainer,
          model_resolver,
          evaluator,
          pusher
      ],
      enable_cache=True,
      metadata_connection_config=metadata.sqlite_metadata_connection_config(
          metadata_path),
      beam_pipeline_args=beam_pipeline_args)


# 'DAG' below need to be kept for Airflow to detect dag.
DAG = AirflowDagRunner(AirflowPipelineConfig(_airflow_config)).run(
    _create_pipeline(
        pipeline_name=_pipeline_name,
        pipeline_root=_pipeline_root,
        data_root=_data_root,
        module_file=_module_file,
        serving_model_dir=_serving_model_dir,
        metadata_path=_metadata_path,
        beam_pipeline_args=_beam_pipeline_args))

