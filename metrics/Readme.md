## Starting with metrics

Integrating custom metrics and standard kubernetes metrics using prometheus and grafana.

- add prometheus_client library to `rest-api` project in `requirements.txt`
    - https://prometheus.github.io/client_python/

---

## Which metrics should be applied

to define the custom metrics, we should use some questions we would like to answer

- How many requests did a pod received?
- How many requests ended in failure and how many in success?
- How long did it take the whole request to response
- How long did it take the process of preprocessing the review?
- How many resources (CPU, Memory) was consumed by each pod?
- What is the average response time?
- What is the average review length ?

Some metrics are delivered as a standard, but some other must be implemented by ourselfs.

### Work with the prometheus_client

TBC

----

## Integrate the metrics in kubernetes cluster

#### Important

A ServiceMonitor can only attach a Service port that it can identify by name (or explicit targetPort number in the
endpoints block!)
So if your ServiceMonitor get config like this `endpoints.port=http` this expects a NAMED port "http".
You need to add `spec.ports.name=http` to your service manifest.

1. Set up a `ServiceMonitor` for our kubernetes `model-api-service`. It will be responsible for observing the metrics
   endpoints of our pods which are load balanced by the service.
2. The ServiceMonitor is created using `model-api-service-monitor.yml`
    3. Important note: since the definition in `model-api-service.yml` has the `metadata.name=model-api-service` you
       need to set the `spec.selector.matchLabels.name=model-api-service` in your `model-api-service-monitor.yml`
4. start up the cluster with the api- and frontend deployments.
5. send a review from frontend to your api and lets make it a prediction
6. use `kubectl get nodes -o wide` to get your nodes IP-Address
    7. now you can use a `curl` command or a tool like `insomnia` to make call to `http://<Node-IP>:<NodePort>/metrics`
    8. you should see an output now with some lines like this: `request_predict_seconds_sum 2.6654183739999553`
9. now use `kubectl apply -f metrics/manifests/model-api-service-monitor.yml`
10. with `kubectl get servicemonitor -n monitoring` you get all your service monitors in your cluster in namespace
    monitoring
    11. you should see a `model-api-service-monitor` running
12. Use Port Forwarding command `kubectl port-forward -n monitoring svc/prometheus-k8s 9090` to access
    prometheus from localhost
13. 
