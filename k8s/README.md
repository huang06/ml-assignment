# Deploying Translation Service on Kubernetes

This guide will walk you through the steps to deploy a Translation Service application on a Kubernetes cluster. The Translation Service is packaged as a Docker container and deployed to Kubernetes, where it can be scaled and managed.

## Steps

### Launch a Kubernetes Cluster

First, you need to have a Kubernetes cluster running. For simplicity, this guide uses k3s, a lightweight Kubernetes distribution.

For detailed instructions on setting up k3s, visit the k3s Quick Start Guide: <https://docs.k3s.io/quick-start>

### Preparing the Container Image

To deploy the translation service, you must prepare the container image containing your service application. Use the following commands to build your Docker image, save it as a tarball, and import it into your k3s cluster.

```bash
# build the container image
docker build -f ./app/Dockerfile -t my-repo/library/ml-assignment:latest .
# save the image as a tarball and import the image into k3s
docker save --output ml-assignment.tar my-repo/library/ml-assignment:latest
sudo k3s ctr images import ml-assignment.tar
```

### Deploying the Service

```bash
kubectl apply -f ./volumes.yaml
kubectl apply -f ./deployment.yaml
kubectl apply -f ./service.yaml
```
