# It is all about the cloud

Developing, training and deploying Machine Learning Models is a very computing extensive task. Most non-gaming computers are not up to this task and training models and tuning for different hyperparameters will take forever. Also most MLOps Framworks are built with the cloud in mind. Most deployment guides are written for the big 3 cloud vendoers: Amazon Web Services, Microsoft Azure & Google Plattform

Google even developed an entire Software Plattform around the MLOps process, Kubeflow is basically the entire process in software form.

When we started out with this project, we wanted to build everything local because we did not have access to cloud credits to run the workloads there. In hindsight this was probably a bad decision, most of the software is just not made for an average laptop. We ran into many issues when it came to Memory Issues but also just compatibility in general was quite bad.

We were not able to run Tensorflow Extended on a Windows Host and also using the much famed Windows Subsystem for Linux didnt result in the desired effects.

This led us to running a developing instance at aws to have a native linux system.

We ran all of our workload in AWS, because we had access to cloud credits there. This needs to kept in mind when running any of our code. While AWS has many AI offerings aswell, most of the guide for TFX are written with Google in mind. This definetly made the implementation of our use-case a challenge at times.
