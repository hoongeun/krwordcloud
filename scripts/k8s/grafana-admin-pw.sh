#!/usr/bin/env bash
set -euo pipefail

kubectl get secret --namespace default krwordcloud-grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo
