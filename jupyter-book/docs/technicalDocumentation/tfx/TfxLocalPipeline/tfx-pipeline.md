# tfx-pipeline

Bei dem Bau der tfx-pipeline haben wir uns an den folgenden Beispielen orientiert: 

- Penguin example [[Simple TFX Pipeline Tutorial using Penguin dataset &nbsp;|&nbsp; TensorFlow](https://www.tensorflow.org/tfx/tutorials/tfx/penguin_simple)]

- taxi example [[tfx/tfx/examples/chicago_taxi_pipeline at master · tensorflow/tfx · GitHub](https://github.com/tensorflow/tfx/tree/master/tfx/examples/chicago_taxi_pipeline)]

Für die orchestrierung der Pipeline haben wir Apache Airflow verwendet. 

Als Basis haben wir die das taxi example verwendet. Wir haben das Projekt, wie in der beigefügten Readme [[tfx/tfx/examples/chicago_taxi_pipeline at master · tensorflow/tfx · GitHub](https://github.com/tensorflow/tfx/tree/master/tfx/examples/chicago_taxi_pipeline)] beschrieben aufgesetzt. 

## Local prerequisites

- [Apache Airflow](https://airflow.apache.org/) is used for pipeline orchestration.
- [Apache Beam](https://beam.apache.org/) is used for distributed processing.
- [TensorFlow](https://tensorflow.org/) is used for model training, evaluation and inference.(https://github.com/tensorflow/tfx/tree/master/tfx/examples/chicago_taxi_pipeline#install-dependencies)Install dependencies

Install tfx:

```python
pip install tfx==1.3.4
```

Create conda environment :

```python
conda create -n tfx python=3.6
```

Activate the conda environment: 

```python
conda activate tfx
```

Configure common paths:

```python
export AIRFLOW_HOME=~/airflow
export TAXI_DIR=~/taxi
export TFX_DIR=~/tfx
```

Next, install the dependencies required by the Chicago Taxi example:

```python
pip install apache-airflow==1.10.9
pip install -U tfx[examples]
```

Next, initialize Airflow:

```python
airflow initdb
```

The benefit of the local example is that you can edit any part of the pipeline and experiment very quickly with various components. First let's download the data for the example:

```python
mkdir -p $TAXI_DIR/data/simple
wget -O $TAXI_DIR/data/simple/data.csv https://github.com/tensorflow/tfx/blob/master/tfx/examples/chicago_taxi_pipeline/data/simple/data.csv?raw=true
```

Next, copy the TFX pipeline definition to Airflow's `DAGs directory` `($AIRFLOW_HOME/dags)` so it can run the pipeline. To find the location of your TFX installation, use this command:

```python
pip show tfx
```

Use the location shown when setting the TFX_EXAMPLES path below.

```python
export TFX_EXAMPLES=~/taxi_pipeline/lib/python3.6/site-packages/tfx/examples/chicago_taxi_pipeline
```

Copy the Chicago Taxi example pipeline into the Airflow DAG folder. Info: You have to execute this command again after each change before you start the pipeline.

```py
mkdir -p $AIRFLOW_HOME/dags/
cp $TFX_EXAMPLES/taxi_pipeline_simple.py $AIRFLOW_HOME/dags/
```

The module file `taxi_utils.py` used by the Trainer and Transform components will reside in $TAXI_DIR. Copy it there. Info: You have to execute this command again after each change before you start the pipeline.

```python
cp $TFX_EXAMPLES/taxi_utils.py $TAXI_DIR
```

## Run the local example pipeline

Start the airflow webserver

```python
airflow webserver -p 8082
```

Start the airflow scheduler in a new terminal: 

```python
conda activate tfx
airflow scheduler
```

Open your browser on localhost:8082

Now you can see the airflow interface and start the pipeline

![](C:\Users\Pasca\OneDrive\Desktop\MLOPS\kirenz-mlops-semester\jupyter-book\assets\img\2022-02-06-21-18-14-image.png)

## Customize pipeline

We customized the taxi example pipeline as follow:

- Example Gen -> no changes

- Statistic Gen -> no changes

- Schema Gen -> no changes

- example Validator - no changes 

- pusher - no changes

### Trainer

Since we want to perform a classification in our case, we have used the penguin example in the tfx documentation. We have customized this example in the current use case.

Since we did not use the Transform component in our pipeline, we had to make some adjustments. In our case, we did not need the Transform component because the data could already be loaded from Delta Lake in the required form.

```python
trainer = Trainer(
      module_file=module_file,
      examples=example_gen.outputs['examples'],
      schema=schema_gen.outputs['schema'],
      train_args=trainer_pb2.TrainArgs(num_steps=1000),
      eval_args=trainer_pb2.EvalArgs(num_steps=20))
```

The next step was to write the model training code. For this we used this example [[Simple TFX Pipeline Tutorial using Penguin dataset &nbsp;|&nbsp; TensorFlow](https://www.tensorflow.org/tfx/tutorials/tfx/penguin_simple)].

```python
from typing import List
from absl import logging
import tensorflow as tf
import datetime
from tensorflow import keras
from tensorflow_transform.tf_metadata import schema_utils

from tfx import v1 as tfx
from tfx_bsl.public import tfxio
from tensorflow_metadata.proto.v0 import schema_pb2

_FEATURE_KEYS = ['action', 'involved_person',
       'self_defined_ethnicity_white', 'self_defined_ethnicity_black',
       'self_defined_ethnicity_asian', 'self_defined_ethnicity_other',
       'self_defined_ethnicity_mixed', 'gender_Female', 'gender_Male',
       'gender_Other', 'legislation_Aviation_Security_Act_1982__section_27_1',
       'legislation_Conservation_of_Seals_Act_1970__section_4',
       'legislation_Criminal_Justice_Act_1988__section_139B',
       'legislation_Criminal_Justice_and_Public_Order_Act_1994__section_60',
       'legislation_Crossbows_Act_1987__section_4',
       'legislation_Customs_and_Excise_Management_Act_1979__section_163',
       'legislation_Deer_Act_1991__section_12',
       'legislation_Environmental_Protection_Act_1990__section_34B_',
       'legislation_Firearms_Act_1968__section_47',
       'legislation_Hunting_Act_2004__section_8',
       'legislation_Misuse_of_Drugs_Act_1971__section_23',
       'legislation_Poaching_Prevention_Act_1862__section_2',
       'legislation_Police_and_Criminal_Evidence_Act_1984__section_1',
       'legislation_Police_and_Criminal_Evidence_Act_1984__section_6',
       'legislation_Protection_of_Badgers_Act_1992__section_11',
       'legislation_Psychoactive_Substances_Act_2016__s36_2',
       'legislation_Psychoactive_Substances_Act_2016__s37_2',
       'legislation_Public_Stores_Act_1875__section_6',
       'legislation_Wildlife_and_Countryside_Act_1981__section_19',
       'officer_defined_ethnicity_Asian', 'officer_defined_ethnicity_Black',
       'officer_defined_ethnicity_Mixed', 'officer_defined_ethnicity_Other',
       'officer_defined_ethnicity_White', 'type_Person_and_Vehicle_search',
       'type_Person_search', 'type_Vehicle_search',
       'object_of_search_Anything_to_threaten_or_harm_anyone',
       'object_of_search_Article_for_use_in_theft',
       'object_of_search_Articles_for_use_in_criminal_damage',
       'object_of_search_Controlled_drugs', 'object_of_search_Crossbows',
       'object_of_search_Detailed_object_of_search_unavailable',
       'object_of_search_Evidence_of_offences_under_the_Act',
       'object_of_search_Evidence_of_wildlife_offences',
       'object_of_search_Firearms', 'object_of_search_Fireworks',
       'object_of_search_Game_or_poaching_equipment',
       'object_of_search_Goods_on_which_duty_has_not_been_paid_etc.',
       'object_of_search_Offensive_weapons',
       'object_of_search_Psychoactive_substances',
       'object_of_search_Seals_or_hunting_equipment',
       'object_of_search_Stolen_goods', 'object_of_search_dog',
       'force_avon-and-somerset', 'force_bedfordshire', 'force_btp',
       'force_cambridgeshire', 'force_cheshire', 'force_city-of-london',
       'force_cleveland', 'force_cumbria', 'force_derbyshire',
       'force_devon-and-cornwall', 'force_dorset', 'force_durham',
       'force_dyfed-powys', 'force_essex', 'force_gloucestershire',
       'force_hampshire', 'force_hertfordshire', 'force_humberside',
       'force_kent', 'force_lancashire', 'force_leicestershire',
       'force_lincolnshire', 'force_merseyside', 'force_metropolitan',
       'force_norfolk', 'force_north-wales', 'force_north-yorkshire',
       'force_northamptonshire', 'force_northumbria', 'force_staffordshire',
       'force_suffolk', 'force_sussex', 'force_thames-valley',
       'force_warwickshire', 'force_west-mercia', 'force_west-yorkshire',
       'force_wiltshire']



_LABEL_KEY = 'age_range'

_TRAIN_BATCH_SIZE = 20
_EVAL_BATCH_SIZE = 10


# Since we're not generating or creating a schema, we will instead create
# a feature spec.  Since there are a fairly small number of features this is
# manageable for this dataset.
_FEATURE_SPEC = {
    **{
        feature: tf.io.FixedLenFeature(shape=[1], dtype=tf.float32)
           for feature in _FEATURE_KEYS
       },
    _LABEL_KEY: tf.io.FixedLenFeature(shape=[1], dtype=tf.int64)
}


def _input_fn(file_pattern: List[str],
              data_accessor: tfx.components.DataAccessor,
              schema: schema_pb2.Schema,
              batch_size: int = 200) -> tf.data.Dataset:
  """Generates features and label for training.

  Args:
    file_pattern: List of paths or patterns of input tfrecord files.
    data_accessor: DataAccessor for converting input to RecordBatch.
    schema: schema of the input data.
    batch_size: representing the number of consecutive elements of returned
      dataset to combine in a single batch

  Returns:
    A dataset that contains (features, indices) tuple where features is a
      dictionary of Tensors, and indices is a single Tensor of label indices.
  """
  return data_accessor.tf_dataset_factory(
      file_pattern,
      tfxio.TensorFlowDatasetOptions(
          batch_size=batch_size, label_key=_LABEL_KEY),
      schema=schema).repeat()


def _build_keras_model() -> tf.keras.Model:
  """Creates a DNN Keras model for classifying penguin data.

  Returns:
    A Keras Model.
  """
  # The model below is built with Functional API, please refer to
  # https://www.tensorflow.org/guide/keras/overview for all API options.
  inputs = [keras.layers.Input(shape=(1,), name=f) for f in _FEATURE_KEYS]
  d = keras.layers.concatenate(inputs)
  for _ in range(2):
    d = keras.layers.Dense(8, activation='relu')(d)
  outputs = keras.layers.Dense(5)(d)

  model = keras.Model(inputs=inputs, outputs=outputs)
  model.compile(
      optimizer=keras.optimizers.Adam(1e-2),
      loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
      metrics=[keras.metrics.SparseCategoricalAccuracy()])

  model.summary(print_fn=logging.info)
  return model


# TFX Trainer will call this function.
def run_fn(fn_args: tfx.components.FnArgs):
  """Train the model based on given args.

  Args:
    fn_args: Holds args used to train the model as name/value pairs.
  """

  # This schema is usually either an output of SchemaGen or a manually-curated
  # version provided by pipeline author. A schema can also derived from TFT
  # graph if a Transform component is used. In the case when either is missing,
  # `schema_from_feature_spec` could be used to generate schema from very simple
  # feature_spec, but the schema returned would be very primitive.
  schema = schema_utils.schema_from_feature_spec(_FEATURE_SPEC)

  train_dataset = _input_fn(
      fn_args.train_files,
      fn_args.data_accessor,
      schema,
      batch_size=_TRAIN_BATCH_SIZE)
  eval_dataset = _input_fn(
      fn_args.eval_files,
      fn_args.data_accessor,
      schema,
      batch_size=_EVAL_BATCH_SIZE)

  model = _build_keras_model()
  log_dir = "/usr/local/airflow/dags/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
  tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)

  model.fit(
      train_dataset,
      steps_per_epoch=fn_args.train_steps,
      validation_data=eval_dataset,
      validation_steps=fn_args.eval_steps,
      callbacks=[tensorboard_callback])

  # The result of the training should be saved in `fn_args.serving_model_dir`
  # directory.
  model.save(fn_args.serving_model_dir, save_format='tf')
```

The results can be viewed in the tensorboard. Please have a look at the chapter Tensorboard.

### Evaluator

In the evaluator we used tfma to validate the model.

Useful links here are the following:

- [Module: tfma.metrics &nbsp;|&nbsp; TFX &nbsp;|&nbsp; TensorFlow](https://www.tensorflow.org/tfx/model_analysis/api_docs/python/tfma/metrics)

- [Getting Started with TensorFlow Model Analysis &nbsp;|&nbsp; TFX](https://www.tensorflow.org/tfx/model_analysis/get_started

```python
# Get the latest blessed model for model validation.
  model_resolver = resolver.Resolver(
      strategy_class=latest_blessed_model_resolver.LatestBlessedModelResolver,
      model=Channel(type=Model),
      model_blessing=Channel(
          type=ModelBlessing)).with_id('latest_blessed_model_resolver')


# Uses TFMA to compute a evaluation statistics over features of a model and
  # perform quality validation of a candidate model (compared to a baseline).
  metrics = [
            tfma.metrics.ConfusionMatrixPlot(name='confusion_matrix_plot'),
            tfma.metrics.BalancedAccuracy(name='bac'),
            tfma.metrics.MeanLabel(name='mean_label'),
            tfma.metrics.MeanPrediction(name='mean_prediction'),
            tfma.metrics.Calibration(name='calibration'),
            tfma.metrics.CalibrationPlot(name='calibration_plot'),
        ]
  eval_config = tfma.EvalConfig(
        model_specs=[
            tfma.ModelSpec(label_key='age_range')
        ],
        metrics_specs = tfma.metrics.specs_from_metrics(metrics),

        slicing_specs=[
        # An empty slice spec means the overall slice, i.e. the whole dataset.
            tfma.SlicingSpec()],
        options=tfma.Options(include_default_metrics=BoolValue(value=True)),
      )
```
