# app-001

A kubernetes cluster with an nginx ingress, a react application and a python web api.
The react app calls a the web server at `/api/version`.

## run in minikube

```bash
➜ pwd
~/auth.tests/app-001/
➜ minikube start
```

make sure you have ingress enabled

```bash
➜ minikube addons list | grep ingress
- ingress: enabled
```

if you don't, enable it ingress

```bash
➜ minikube addons enable ingress
```

build images

```bash
➜ cd www
➜ eval $(minikube docker-env)
➜ docker build -f ./nginx/Dockerfile -t app/www:test .
➜ docker build -f ./web-api/Dockerfile -t app/web-api:test .
```

install helm ingress

```bash
➜ pwd
~/fleet/app-001
➜ helm install stable/nginx-ingress -n nginxingress --values ./nginx-ingress/nginx-ingress-values-dev.yaml
➜ kubectl get pods
NAME                                                         READY     STATUS    RESTARTS   AGE
nginxingress-nginx-ingress-controller-f8947f46c-pbvkx        1/1       Running   0          36s
nginxingress-nginx-ingress-default-backend-5459bb66d-b4gb9   1/1       Running   0          36s
```

install helm chart

```bash
➜ pwd
~/fleet/app-001/www
➜ helm install ./www.app.com/ -n www.app.com
➜ kubectl get pods
NAME                                                         READY     STATUS    RESTARTS   AGE
api-app-764b687f7d-nz22x                                     1/1       Running   0          5s
nginxingress-nginx-ingress-controller-f8947f46c-pbvkx        1/1       Running   0          1m
nginxingress-nginx-ingress-default-backend-5459bb66d-b4gb9   1/1       Running   0          1m
www-app-5dfb7ccc58-j9kmv                                     1/1       Running   0          5s
```

Create www.minikube-app.com endpoint and navigate to it.

```bash
➜ echo "$(minikube ip) www.minikube-app.com" | sudo tee -a /etc/hosts
➜ kubectl get services | grep ingress-controller
nginxingress-nginx-ingress-controller        NodePort    10.100.196.161   <none>        80:32626/TCP,443:31235/TCP   2m
➜ curl -I www.minikube-app.com:32626
```

to delete

```bash
helm delete www.app.com --purge
helm delete nginxingress --purge
```

## run in dev

frontend:

frontend runs with a proxy to `8081` in development. see [package.json](.www/app/package.json)

```bash
pwd
~/auth.tests/app-001/www/app
yarn
yarn start
```

web api

```bash
pwd
fleet/app-001/www/web-api/src
gunicorn -b 0.0.0.0:8081 \
    --forwarded-allow-ips=* \
    --log-file - \
    --log-level debug \
    server:app
```