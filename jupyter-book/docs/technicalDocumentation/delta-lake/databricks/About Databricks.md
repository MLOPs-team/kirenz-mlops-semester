# Databricks - A Lakehouse unicorn

Databricks advertises with this slogan:

`All your data, analytics and AI on one lakehouse platform`

Its a SaaS service that provied a collaborative soltuion to the entire machine learning lifecycle. It is build with data pipelines in mind and on top of the lakehouse architecture.

The pricing model of databricks is based on databricks processing units which are billed ontop of the cloud costs you have with your cloud provider. When first setting up databricks, you need to connect it to your cloud account so the workers get provisoned there. The costs are not very transparent at first though, one needs to keep in mind that you are both billed by your cloud provider and by databricks.

This business model has turned the company into one of the fastest growing AI companies according to Gardner.

## The collaborative approach

Many data scientists and AI researchers like to work in Jupyter Notebooks. The iterative approach needed for building advanced machine learning solutions is very time consuming, so the interactivity the notebooks allow speed up the process immensly.

The presentation of code and result is also liked by many.

Databricks has used this same approach for the ETL processes in Spark, as can be seen with this GUI screenshot, where we load our police dataset and transform it and then write it into the delta-lake:

![](/Users/niklasdenneler/Development/kirenz-mlops-semester/jupyter-book/assets/img/2022-02-06-23-21-25-image.png)

On the left hand side one can browse through his Git Repo, pick which file to work on or change the configuration of the Spark Cluster. 

## Advantages:

- intuitive UI, which can be used for collaborating in a team

- good Integration of Source Code Providers like GitHub / BitBucket

- cluster can be shared by many Editors

- very good integration of third parties like delta-lake, aws & azure, hadoop etc.

## Disadvantages:

- pricing model 

- dependency between Databricks & Apache Spark

- spark can be very slow when running commands -> configuration of cluster?

## What needs to be explored further?

- machine Learning pipelines inside the databricks runtime

- scalability of the platform

- IAM Integration into corporate environments
