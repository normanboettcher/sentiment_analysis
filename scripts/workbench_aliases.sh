alias forward_prometheus='kubectl port-forward -n monitoring svc/prometheus-k8s 9090'
alias forward_grafana='kubectl port-forward -n monitoring deploy/grafana 3000'
export WORKSPACE_PATH="~/Projekte/MachineLearning/sentiment_analysis/"
alias rest_api="cd ${WORKSPACE_PATH}/rest-api/"
alias model_frontend="cd ${WORKSPACE_PATH}/frontend"
alias model_project="cd ${WORKSPACE_PATH}/sentiment-model"
alias model_metrics="cd ${WORKSPACE_PATH}/metrics"