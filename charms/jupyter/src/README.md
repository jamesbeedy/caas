# Overview

Jenkins for Kubernetes


## Build Docker Image

    $ docker build ./dockerfiles -t jamesbeedy/juju-jenkins-test:1.0

## Build Charm

    $ make build
    $ charm push ./build/builds/jenkins-k8s jenkins-k8s --resource jenkins_image=jamesbeedy/juju-jenkins-test:1.0

## Deplyment Example

    $ juju deploy cs:~jamesbeedy/jenkins-k8s \
      --storage jenkins-home=10G,k8s-ebs \
      --config kubernetes-service-type=LoadBalancer \
      --config juju-external-hostname="jenkins-k8s.myexamnple.com"

