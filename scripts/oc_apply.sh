#!/bin/bash
TARGET_PROJECT=$1
WORKSPACE_PATH=~/Projekte/MachineLearning/sentiment_analysis

echo "looking for manifest files in ${WORKSPACE_PATH}/${TARGET_PROJECT}"
find "${WORKSPACE_PATH}/${TARGET_PROJECT}/manifests" -type d | while read manifest_folder;do
	oc apply -f "${manifest_folder}"
done



