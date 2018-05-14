# app-002

A kubernetes cluster with an **nginx ingress**, a **react** application and a web api in **python**.
The react application logs in using Facebook authentication through the web api.

## run in minikube

you will need to update file at `app-002/www/www.app.com/templates/api-deployment.yaml` with your client id and secret

```bash
➜ pwd
~/auth.tests/app-002/
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
➜ cd app
➜ yarn
➜ yarn build
➜ cd ..
➜ docker build -f ./nginx/Dockerfile -t app/www:test .
➜ docker build -f ./web-api/Dockerfile -t app/web-api:test .
```

install helm ingress

```bash
➜ pwd
~/fleet/app-002
➜ helm install stable/nginx-ingress -n nginxingress --values ./nginx-ingress/nginx-ingress-values-dev.yaml
➜ kubectl get pods
NAME                                                         READY     STATUS    RESTARTS   AGE
nginxingress-nginx-ingress-controller-f8947f46c-pbvkx        1/1       Running   0          36s
nginxingress-nginx-ingress-default-backend-5459bb66d-b4gb9   1/1       Running   0          36s
```

install helm chart

```bash
➜ pwd
~/fleet/app-002/www
➜ helm install ./www.app.com/ -n www.app.com
➜ kubectl get pods
NAME                                                         READY     STATUS    RESTARTS   AGE
api-app-7dcdff7565-xp2pt                                     1/1       Running   0          4s
nginxingress-nginx-ingress-controller-f8947f46c-hvwc6        1/1       Running   0          1m
nginxingress-nginx-ingress-default-backend-5459bb66d-prvml   1/1       Running   0          1m
www-app-5dfb7ccc58-2r7t5                                     1/1       Running   0          4s
```

Create www.minikube-app.com endpoint and navigate to it.

```bash
➜ echo "$(minikube ip) www.minikube-app.com" | sudo tee -a /etc/hosts
➜ kubectl get services | grep ingress-controller
nginxingress-nginx-ingress-controller        NodePort    10.106.59.130   <none>        80:32163/TCP,443:31495/TCP   2m
➜ curl -I www.minikube-app.com:32163
```

to delete

```bash
➜ helm delete www.app.com --purge
➜ helm delete nginxingress --purge
```

## run in dev

frontend:

frontend runs with a proxy to `8081` in development. see [](.www/app/package.json)

```bash
➜ pwd
~/fleet/app-002/www/app
➜ yarn
➜ yarn start
```

web api

```bash
➜ pwd
fleet/app-002/www/web-api/src
➜ export FACEBOOK_OAUTH_CLIENT_ID=yourclientid
➜ export FACEBOOK_OAUTH_CLIENT_SECRET=yourclientsecret
➜ export OAUTHLIB_INSECURE_TRANSPORT=1
➜ gunicorn -b 0.0.0.0:8081 \
    --forwarded-allow-ips=* \
    --log-file - \
    --log-level debug \
    server:app
```