# ml-assignment

## Prerequisites

- Docker
- Kubernetes cluster
- model artifacts (./artifacts/)

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

## Input/Output

```bash
curl --location --request POST 'http://127.0.0.1:9527/translation' \
--header 'Content-Type: application/json' \
--data-raw '{
    "payload": {
        "fromLang": "en",
        "records": [
            {
                "id": "123",
                "text": "Life is like a box of chocolates."
            }
        ],
        "toLang": "ja"
    }
}' | jq
```

```json
{
   "result":[
      {
         "id":"123",
         "text":"人生はチョコレートの箱のようなものだ。"
      }
   ]
}
```
