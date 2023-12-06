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
