# sentiment_analysis

## switching to kubernetes

### install cert-manager

#### add encryption and HTTPS/TLS

1. `kubectl apply -f https://github.com/cert-manager/cert-manager/releases/latest/download/cert-manager.yaml`
2. verify if it's running: `kubectl get pods --namespace cert-manager`
3. create a cluster-issuer-prod.yml
4. apply it via `kubectl apply -f cluster-issuer-prod.yml`
5. update ingress
   6. 
