## Virtual Evironment (venv) Setup

### Create venv

Navigate to the directory of the project and run the following

```
python3 -m venv venv
```

### Activate venv

You should see a file venv file called venv. Cd into this directory and activate.

```
source env/bin/activate
```

### Install required packages

Install the the required packages using the preset requirements.txt file. This will ensure that your env
has the same versions of the required packages as everyone else and ensure that the project will run as expected.

```
python3 -m pip3 install -r requirements.txt
```

### Deactivate venv

To switch to another venv or to leave virtual environment, deactivate the venv.

```
deactivate
```

## Run App

First run the application using the following command

```
steamlit run main.py
```

If you want this application to be reachable by other devices on your network then you need to proxy an SSL
in order for the real-time video streaming to work on other devices. For demonstration purposes, this app 
uses [ssl-proxy repo](https://github.com/suyashkumar/ssl-proxy). Download the binary file for your OS add
and run the following command. This command assumes the application started running on port 8501 and is port
forwarding to port 8000.

```
./ssl-proxy-darwin-amd64 -from 0.0.0.0:8000 -to 127.0.0.1:8501
```
