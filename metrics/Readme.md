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

### Important Prerequisites

A ServiceMonitor can only attach a Service port that it can identify by name (or explicit targetPort number in the
endpoints block!)
So if your ServiceMonitor get config like this `endpoints.port=http` this expects a NAMED port "http".
You need to add `spec.ports.name=http` to your service manifest.
You need to add a `Role` and a `RoleBinding` if your pods are running in a namespace where prometheus has no
permissions.
Exmaple: Prometheus is running in the `monitoring` namespace with the ServiceAccount `prometheus-k8s`. But our
`ServiceMonitor`
is configured to scrape services/endpoint in our custom namespace like `sentiment-app-dev`. The ServiceAccount is used
to list/watch services and endpoints to know what to scrape. But by default, the `prometheus-k8s` ServiceAccount does
not have permissions to read resources in other namespaces.
With a `Role` and corresponding `RoleBinding` we grant permissions to `prometheus-k8s` to read services, endpoints and
pods in our custom namespace.
After applying these manifests, Prometheus can discover the `model-api-service` endpoints and scrape the metrics
successfully.

#### Role

A `Role` defines permissions within a specific namespace e.g. `sentiment-app-dev`.
With `metadata.namespace` we define in which namespace the Role is applied.
The `rules` section specify what resources and actions this Role grants permission to. Here we have the following:

- `apiGroups: [""]`: Empty string is the core API group where resources like services, endpoints and pods live.
- `resources`: The Kubernetes resource types this Role grants access to:
    - `services`: to discover services
    - `endpoints`: to discover the IP/Ports behind services
    - `pods`: Sometimes needed for pod metadata or additional discovery
- `verbs`: The allowed actions on those resources
    - `get`: Read a single resource
    - `list`: List all resources of this type
    - `watch`: Watch for changes to resources, so Prometheus get updated info

You find an example for a `Role` in `prometheus-service-discovery-role.yml`. This Role is defined to allow Prometheus to
scrape the metrics on our custom namespace.

#### RoleBinding

In the next step, we need a `RoleBinding`. This resource binds the created Role to a user, group, service account,
effectively granting the permissions in that Role to the subject. In our case the RoleBinding must be applied to the
`ServiceAccount` with name `prometheus-k8s`. The `metadata.namespace` must match your Roles namepsace.
Then we have `subjects`:

- `kind: ServiceAccount`: To tell Kubernetes that the identity is a Kubernetes ServiceAccount
- `name: prometheus-k8s`: The ServiceAccount we are looking for.
- `namespace: monitoring`: The ServiceAccount lives in the `monitoring` namespace (or whereever your Prometheus runs)
  And the `roleRef`. It defines which Role is being granted. The roleRef has the following settings in our case:
- `kind: Role`: Refers to a Role (not a ClusterRole or sth.)
- `name: prometheus-service-discovery`: The Role we created above
- `apiGroup: rbac.authorization.k8s.io`: Standard RBAC API group

### How to get the metrics work

1. Set up a `ServiceMonitor` for our kubernetes `model-api-service`. It will be responsible for observing the metrics
   endpoints of our pods which are load balanced by the service.
2. The ServiceMonitor is created using `model-api-service-monitor.yml`
    3. Important note: since the definition in `model-api-service.yml` has the `metadata.name=model-api-service` you
       need to set the `spec.selector.matchLabels.name=model-api-service` in your `model-api-service-monitor.yml`
4. Create a `Role` and `RoleBinding` (see [Role](#role) and [RoleBinding](#rolebinding))
5. start up the cluster with the api- and frontend deployments.
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
13. go to `http://localhost:9090/targets` and look at your ServiceMonitor. You should see all pods which are observed.
14. If you would like to use Grafana to visualize your metrics, execute
    `kubectl port-forward -n monitoring deploy/grafana 3000` and go to `http://localhost:3000`
