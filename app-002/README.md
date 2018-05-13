# app-002

kubernetes nginx python js facebook

## run in minikube

```bash
pwd
~/fleet/app-002/
minikube start
minikube addons enable ingress
eval $(minikube docker-env)
cd www
docker build -f ./nginx/Dockerfile -t app/www:test .
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

## run in dev

frontend:

frontend runs with a proxy to `8081` in development. see [](.www/app/package.json)

```bash
pwd
~/fleet/app-002/www/app
yarn
yarn start
```

web api

```bash
pwd
fleet/app-002/www/web-api/src
export FACEBOOK_OAUTH_CLIENT_SECRET=yoursecret
export FACEBOOK_OAUTH_CLIENT_ID=yourclientid
export OAUTHLIB_INSECURE_TRANSPORT=1
gunicorn -b 0.0.0.0:8081 \
    --forwarded-allow-ips=* \
    --log-file - \
    --log-level debug \
    server:app
```