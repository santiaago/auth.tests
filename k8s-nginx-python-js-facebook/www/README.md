# www subdomain

```bash
➜ minikube start
➜ pwd
    ~/auth.tests/k8s-nginx-python-js-facebook/www
➜ cd app
➜ yarn
➜ yarn build
➜ cd ..
➜ eval $(docker-machine env -u)
➜ docker build -f ./nginx/Dockerfile -t amblr/www:test .
➜ docker build -f ./web-api/Dockerfile -t app/web-api ./web-api/src/
```
