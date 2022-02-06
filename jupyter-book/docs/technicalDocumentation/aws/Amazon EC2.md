# Development Environment based on AWS EC2

We our team started out, we had very diverse individual computing stacks. We had a few Windows User, one Linux user and one on Mac OSX. While running virtualized worklaods one woud suspect this would not make much of a difference but in reality it dit.

After getting access to credits, we decided to deploy a EC2 instance to be used by Pascal to develop there. We picked a Linux Image provied by Amazon a so called Amazon AMI Linux image. This utilizes the EC2 resources the best and comes preinstalled with the aws-cli and a bunch of other useful software.

We installed a GUI for Pascal and he was able to use the Virtual Desktop Environment via SSH / VNC. 

The Instructions to install a GUI on AWS Linux can be found [here](https://aws.amazon.com/premiumsupport/knowledge-center/ec2-linux-2-install-gui/)

This ingenious solution proved great over the entire project length and after adding more CPU Cores and Nvidia GPU to the instance we were able to train our model much faster.

When training TensorFlow Models on the GPU loads of driver installations are required and some configuration steps need to be taken to make it work inside a Docker Container aswell.

Some relevant guides for this are:

- [Tensorflow](https://www.tensorflow.org/install/gpu)

- [Install NVIDIA Drivers in AWS EC2]((https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/install-nvidia-driver.html)

This can be quite a time extensive task, while this seems like a pretty standard approach in the machine learning world, managing dependencies between drivers / hardware can proof to be very frustrating

Overall we rate this decision as one of the big success factors of our project, and for large scale enterprises having access to public or private cloud instances seems like a must nowadays.

Our provsioned specification (very oversized):

|                 | Specs             |
| --------------- | ----------------- |
| Instance Type   | G3.4Xlarge        |
| CPU             | 16vCores          |
| GPU             | Nvidia M40 8GB    |
| RAM             | 122GB             |
| SSD             | 150GB             |
| Price/hr(Linux) | 1.14$ for US East |
