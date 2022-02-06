Why Data Extraction is so important?

In any Machine Learning Project the data acquisition is the starting point to then polish the data and build and train a model. 

APIs are prone to change and the data volume which needs to be extracted depending on the use-case.

Our Use-Case

For our Use-Case we wanted to extract Data from the UK Police API, which is fairly well documented and provided lots of data. 

Challenges:

- Multiple Requests to API need to be made

- APIs are prone to change

- Lots of data included which is not needed for our Use-Case

## Stage 1: Basic Python Script

First we tried to get Data via a simple Python Script just to check the data format.

Then we realized we needed to loop through some requests to get all the data

## Stage 2: Apache Spark with basic Python Script

We then tried to see how Apache Spark might help us solve this problem. We realized we were not taking advantage of Sparks full potential.

## Stage 3: Apache Spark with User-Defined Function

To make full use of Sparks capabilities for distributed computing one needs to leverage the so called User Defined Functions. These make it possible to run large web requests on multiple worker nodes and speed up the progress off the data extraction.

This solution would in a real world scenario be the way to go. For our approach this was overly complex. 

For our current MLOps Process we therfore decided to take a dump off the data in a basic CSV File and and skip the entire data extraction process. This CSV File is then converted into a DataFrame and loaded into the Delta-Lake which uses a AWS S3 Bucket for storage.

Later on in this process we realized, that running a custom Spark Cluster was both tedious and also required loads of resources. 
We then made the decision to move from our own individual stack to the offerings of [Databricks](https://databricks.com/)
