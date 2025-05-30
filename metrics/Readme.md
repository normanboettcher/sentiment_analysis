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

