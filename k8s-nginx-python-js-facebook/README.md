# k8s nginx python js facebook

```bash
pwd
~/auth.tests/k8s-nginx-python-js-facebook/www
minikube start
minikube addons enable ingress
eval $(minikube docker-env)
docker build -f ./nginx/Dockerfile -t app/www:test --build-arg NGINX_CONFIG=nginx/test.conf .
docker build -f ./web-api/Dockerfile -t app/web-api:test .
cd ..
helm install stable/nginx-ingress -n nginxingress --values ./nginx-ingress/nginx-ingress-values-dev.yaml
cd www
helm install ./www.app.com/ -n www.app.com
echo "$(minikube ip) www.minikube-app.com" | sudo tee -a /etc/hosts
kubectl get services | grep ingress-controller
curl -I www.minikube-app.com:30859
```

to delete

```bash
helm delete www.app.com --purge
helm delete nginxingress --purge
```