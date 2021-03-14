# !/bin/sh

minikube config set memory 12288
minikube config set cpus 4
minikube delete
minikube start
eval $(minikube -p minikube docker-env)