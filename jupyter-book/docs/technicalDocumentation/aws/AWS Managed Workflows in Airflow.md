When embarking on our journey in the MLOps world, we first started out by deploying kubeflow on a private university cloud. The space and resources on the instance were very limited and thus we had to take a different direction, because we could not make kubeflow run stable.

Our professor introduced the orchestrating tool Airflow to us. Which we ran locally with some success. We decided that for running our workloads in a realisitic setting we needed to deploy them to the cloud. Because the configuration of Airflow seemed daunting, we picked the SaaS offering by AWS, the so called: [Managed Workflow for Apache Airflow](https://aws.amazon.com/managed-workflows-for-apache-airflow/)

The setup of this service is fairly straight forward. You just need to decide which version of Airflow to run, we picked 2.0.2 and then you will need a S3 Bucket to store your DAGS / requirements.txt and decide how many workers you will need.

A typical workflow in MWAA:

![How it works - Amazon Managed Workflows for Apache Airflow](https://d1.awsstatic.com/product-marketing/Pinwheel/Product-Page-Diagram_Amazon-MWAA_Diagram_2x.718f4566de4f2c4225aea18a70f73e42544e703a.png)

This service is very convenient but at the same time limits you in your approach a little bit. There is only very few configuration options.

What is great about this service though, is that AWS provides a Docker image which can be used locally to test your DAGs prior to deployment and we used this image extensively.

We customised it to fit our own needs and even implemented GPU support to speed up the training process. While our solution is certainly customized for the amazon cloud, is could easily be adapted to be run inside any other Docker engine. 
