# TensorFlow extended on windows

## Installation

Installation of TensorFlow and TensorFlow Extended worked fine 



## Building TFX pipeline

### Step 6 - create a pipeline

All the steps before worked without any problems.



1. **OUTPUT_DIR and DATA_PATH **
   
   In this step, there were small deviations from the documentation that have to be taken into account in Windows so that this step works 
   
   
   
   The paths musst be written with double backslash

```
Example: 

OUTPUT_DIR = 'C:\\Users\\Name\\MLOPS\\\kirenz-mlops-semester\\minikube\\tensorflow\\
dataPreProcessing\\tfxPipeline\\tfx-taxi\\output'

```



2. 

```bash
tfx pipeline create --pipeline_path=your-path-to-txf-taxi/local_runner.py
```

I performed the following steps so that the pipeline could be created: 

- 
