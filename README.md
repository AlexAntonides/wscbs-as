## Getting Started
These instructions will get you a copy up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites
##### 1. Install the following software:
- [ ] [Python](https://www.python.org/)


### Installing
A step by step series of examples that tell you how to get a development environment running.

##### 1. Installing the modules
After cloning the repository, navigate to the project folder and run the following command: 
```console   
python -m pip install flask
python -m pip install validators
python -m pip install pytest
```

or 

```console   
python -m pip install -r requirements.txt
```

### Deployment
Once the modules have been installed, the project will be ready for deployment. 

##### 1. Start the Application
Run the following command to start URL Shorterner Service
```console   
python url_shorterner_service.py
```

### Testing
The application is also suitable for testing.

##### 1. Test the Application
Run the following command to test the application.
```console   
pytest
```