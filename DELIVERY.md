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

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

```bash
optimum-cli export onnx \
  --task text2text-generation-with-past \
  --framework pt \
  --model ./artifacts/m2m100_418M \
  --optimize O1 ./artifacts/m2m100_418M_onnx
```

## Deploy ml-assignment with Docker Compose

```bash
docker compose build
docker compose up -d
```

## Deploy ml-assignment with Kubernetes

### Launch a Kubernetes Cluster

For simplicity uses k3s, a lightweight Kubernetes distribution.

```bash
curl -sfL https://get.k3s.io | INSTALL_K3S_VERSION=v1.28.6+k3s2 sh -
```

For detailed instructions on setting up k3s, see <https://docs.k3s.io/quick-start>

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
kubectl port-forward service/ml-assignment --address 0.0.0.0 '9527:9527'
```

## Development

```bash
python3 -m pip install -r requirements-dev.txt
```

```bash
pre-commit install
pre-commit install -t commit-msg
```

```bash
export LLM_DIR=${PWD}/artifacts/m2m100_418M
export ONNX_DIR=${PWD}/artifacts/m2m100_418M_onnx
uvicorn app.main:app --host 0.0.0.0 --port 9527 --reload
```

### Tests

```bash
pytest tests -vvs
```
