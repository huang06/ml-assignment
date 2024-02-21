# ML Assignment

## Prerequisites

- Docker
- Kubernetes cluster
- model artifacts (./artifacts/)

We will use mounting to allow each container to share the LLM model.

```bash
sudo apt-get install git-lfs
git lfs install
git clone https://huggingface.co/facebook/m2m100_418M artifacts/m2m100_418M
```

## Deploy ml-assignment with Docker Compose

```bash
docker compose build
docker compose up -d
```

## Deploy ml-assignment with Kubernetes

### Launch a Kubernetes Cluster

For simplicity uses k3s, a lightweight Kubernetes distribution.

For detailed instructions on setting up k3s, visit the k3s Quick Start Guide: <https://docs.k3s.io/quick-start>

### Prepare the Container Image

```bash
docker compose build

docker save ml-assignment:latest | sudo k3s ctr images import -
```

### Apply Configurations

```bash
# update **hostPath** before applying volumes.yaml
kubectl apply -f ./k8s/volumes.yaml
kubectl apply -f ./k8s/deployment.yaml
```

### Expose the Service

Open a new session and execute the following command:

```bash
kubectl port-forward deployment/ml-assignment --address 0.0.0.0 '9527:9527'
```

## Development

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 -m pip install -r requirements-dev.txt
```

```bash
pre-commit install
pre-commit install -t commit-msg
```

```bash
export LLM_DIR=${PWD}/artifacts/m2m100_418M
uvicorn app.main:app --host 0.0.0.0 --port 9527 --reload
```

### Tests

```bash
pytest tests -vvs
```
