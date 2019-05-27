# Overview

Jupyter Charm for Kubernetes


## Build Docker Image

    $ docker build ./dockerfiles -t jamesbeedy/jupyter-k8s:v1.0.0

## Build Charm

    $ make build
    $ charm push ./build/builds/jupyter-k8s jupyter-k8s --resource jupyter_image=jamesbeedy/jupyter-k8s:v1.0.0

## Deplyment Example: NodePort

    $ juju deploy cs:~jamesbeedy/jupyter-k8s \
      --config kubernetes-service-type=LoadBalancer \
      --config juju-external-hostname="jenkins-k8s.myexamnple.com"


## Deplyment Example: LoadBalancer

    $ juju deploy cs:~jamesbeedy/jupyter-k8s \
      --config kubernetes-service-type=LoadBalancer \
      --config juju-external-hostname="jupyter-k8s.myexample.com"

