# Dealership Review

This project implements a full-stack review system with the function of user authentication, review management, sentiment analysis using Django.

The application is deployed on IBM Cloud and avaiable at
https://dealershipreview.us-south.cf.appdomain.cloud/djangoapp


The application is portable. It can be containerized with
```
docker build -t <APP_NAME> .
```
and deployed with
```
kubectl apply -f deployment.yaml
```
