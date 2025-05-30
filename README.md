# sentiment_analysis

## build and run the project

TBC

## switching to kubernetes

### adding monitoring

#### monitoring with metrics-server

install metrics-server with the following commands:

`helm repo add metrics-server https://kubernetes-sigs.github.io/metrics-server/`

`helm repo update`

`helm upgrade --install metrics-server metrics-server/metrics-server \
--namespace sentiment-app-dev --create-namespace`

if necessary, remove old installation of metrics-server:

`kubectl delete deployment metrics-server -n kube-system`

`kubectl delete clusterrole system:metrics-server`

`kubectl delete clusterrolebinding system:metrics-server`

`kubectl delete rolebinding metrics-server-auth-reader -n kube-system`

`kubectl delete serviceaccount metrics-server -n kube-system`

`kubectl delete apiservice v1beta1.metrics.k8s.io`

You can now have a look at your nodes and pods via:

`kubectl top nodes`

`kubectl top pods -A`

These command should now include CPU and Memory Usage

##### enhance metrics using prometheus

1. Install Prometheus via:
   `git clone http://github.com/prometheus-operator/kube-prometheus.git`
2. run setups in your prometheus installation
   `kubectl create -f manifests/setup`
3. install the manifests
   `kubectl create -f manifests`
4. to view all created resources in namespace monitoring, execute `show_prometheus_resources.sh`
5. Port-Forwarding to localhost, to interact with Prometheus
   `kubectl port-forward -n monitoring statefulset/prometheus-k8s 9090`

### install cert-manager

#### add encryption and HTTPS/TLS

1. `kubectl apply -f https://github.com/cert-manager/cert-manager/releases/latest/download/cert-manager.yaml`
2. verify if it's running: `kubectl get pods --namespace cert-manager`
3. create a cluster-issuer-prod.yml
4. apply it via `kubectl apply -f cluster-issuer-prod.yml`
5. update ingress
