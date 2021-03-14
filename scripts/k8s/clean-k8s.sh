# !/bin/sh

kubectl delete all --all --force
kubectl delete clusterrole --all --force
kubectl delete clusterrolebinding --all --force
kubectl delete service --all --force
kubectl delete podsecuritypolicy --all --force
kubectl delete MutatingWebhookConfiguration --all --force
kubectl delete ValidatingWebhookConfiguration --all --force
kubectl delete thirdpartyresource --all --force
minikube stop
minikube delete