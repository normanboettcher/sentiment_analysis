alias forward_prometheus='kubectl port-forward -n monitoring svc/prometheus-k8s 9090'
alias forward_grafana='kubectl port-forward -n monitoring deploy/grafana 3000'