## Getting Started
These instructions will get you a copy up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites
##### 1. Install the following software:
- [ ] [Docker](https://www.docker.com/)
- [ ] [Kubernetes](https://kubernetes.io/)

### Installing
A step by step series of examples that tell you how to get a development environment running.

#### A. Docker
##### 1. Installing the modules
After cloning the repository, navigate to the project folder and run the following command: 
```console
docker-compose build
```

### Deployment
Once the modules have been installed, the project will be ready for deployment. 

##### 1. Start the Application
Run the following command to start URL Shorterner Service
```console   
docker-compose up
```

#### B. Kubernetes
##### 1. (Optional) Push to Docker Hub
You could use the standard image provided in the docker-compose, but if you would like to use your own images, change the image in the docker-composess to point towards your docker hub and use the following command to push the images:
```console
docker-compose push
```
##### 2. Kubernetes and Docker Hub  Image
Open the ./kubernetes/*.yaml files and validate the image path under spec/containers, so that it points towards the docker-hub image. See the example  below.
```yaml
spec:
    [...]
    template:
        [...]
        spec:
            containers:
                [...]
                image: docker-hub-id/image
```
##### 3. Kubernetes Pods
Finally, use the kubectl commands to build the Kubernetes pods.
```console
kubectl apply -f ./kubernetes/proxy.yaml
kubectl apply -f ./kubernetes/url-shortener-service.yaml
kubectl apply -f ./kubernetes/user-service.yaml
```
