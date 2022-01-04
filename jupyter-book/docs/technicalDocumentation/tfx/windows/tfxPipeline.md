# TensorFlow extended on windows

## Installation

Installation of TensorFlow and TensorFlow Extended worked fine 

## Building TFX pipeline

### Step 6 - create a pipeline

All the steps before worked without any problems.

After the following command was executed an error message appeared

```python
tfx pipeline create --pipeline_path=your-path-to-txf-taxi/local_runner.py
```

1. **KeyError: 'Home' occured**

<img title="" src="\\wsl$\Ubuntu-20.04\home\pascal\dev\kirenz-mlops-semester\jupyter-book\assets\img\2021-12-15-17-54-05-image.png" alt="" data-align="inline">

This error occurs because Windows does not have Home. After some research we found a post on stackoverflow where we recommended to adjust the path in base_handler.py

**Folder: ** C:\Users\anaconda3\envs\tf\Lib\site-packages\tfx\tools\cli\handler\base_handler.py

In this file we changes the os.environ['HOME'] to os.path.expanduser('~')

After that we run the above command again. 

2. **SyntaxError: (unicode error) 'unicodescape codec can't decode bytes in position 2-3: truncated \UXXXXXXXX escape **

![](\\wsl$\Ubuntu-20.04\home\pascal\dev\kirenz-mlops-semester\jupyter-book\assets\img\2021-12-15-18-02-53-image.png)

The paths musst be written with double backslash

```
Example: 

OUTPUT_DIR = 'C:\\Users\\Name\\MLOPS\\\kirenz-mlops-semester\\minikube\\tensorflow\\
dataPreProcessing\\tfxPipeline\\tfx-taxi\\output'
```

After we fixed the above problems, it was possible to create the pipeline

___

In the next step we tried to run the pipeline 

```python
tfx run create --pipeline_name=pipeline-taxi
```

The following error occured:

![](\\wsl$\Ubuntu-20.04\home\pascal\dev\kirenz-mlops-semester\jupyter-book\assets\img\2021-12-15-18-07-00-image.png)

![](\\wsl$\Ubuntu-20.04\home\pascal\dev\kirenz-mlops-semester\jupyter-book\assets\img\2021-12-15-18-07-13-image.png)
