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

<img title="" src="file:///C:/Users/Pasca/OneDrive/Desktop/MLOPS/kirenz-mlops-semester/jupyter-book/assets/img/2021-12-15-17-54-05-image.png" alt="" data-align="inline">

This error occurs because Windows does not have Home. After some research we found a post on stackoverflow where we recommended to adjust the path in base_handler.py

**Folder: ** C:\Users\anaconda3\envs\tf\Lib\site-packages\tfx\tools\cli\handler\base_handler.py

In this file we changes the os.environ['HOME'] to os.path.expanduser('~')

After that we run the above command again. 

2. **SyntaxError: (unicode error) 'unicodescape codec can't decode bytes in position 2-3: truncated \UXXXXXXXX escape **

![](C:\Users\Pasca\OneDrive\Desktop\MLOPS\kirenz-mlops-semester\jupyter-book\assets\img\2021-12-15-18-02-53-image.png)

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

![](C:\Users\Pasca\OneDrive\Desktop\MLOPS\kirenz-mlops-semester\jupyter-book\assets\img\2021-12-15-18-07-00-image.png)

![](C:\Users\Pasca\OneDrive\Desktop\MLOPS\kirenz-mlops-semester\jupyter-book\assets\img\2021-12-15-18-07-13-image.png)

It was not possible to run the tfx pipeline on windows. 



After that we have decided to work in the wsl. Enclosed the docu for the [wsl]([Install WSL | Microsoft Docs](https://docs.microsoft.com/en-us/windows/wsl/install)). 



After some timenhowever it has also become apparent that wsl is reaching its limits in this project. Again and again various errors occurred or certain modules could not be installed. Because of this we decided to work in a VM. In retrospect this was one of the best decisions in this project. We just should have made it earlier ;-)
