PROMETHEUS_PATH="${HOME}/Projekte/kube-prometheus"
echo "running setup in ${PROMETHEUS_PATH}/manifests/setup"
oc create -f  "${PROMETHEUS_PATH}/manifests/setup"
echo "install the manifests"
oc create -f "${PROMETHEUS_PATH}/manifests"

