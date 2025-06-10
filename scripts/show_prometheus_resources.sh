#!/bin/bash
DIVIDER="============================="
echo "${DIVIDER} DEPLOYMENTS ${DIVIDER}"
kubectl get deployments -n monitoring
echo "${DIVIDER} STATEFUL_SETS ${DIVIDER}"
kubectl get statefulsets -n monitoring
echo "${DIVIDER} DAEMON_SETS ${DIVIDER}"
kubectl get daemonsets -n monitoring
echo "${DIVIDER} SERVICES ${DIVIDER}"
kubectl get services -n monitoring