Usage Instructions
------------------

1. First, ensure that you have the timekeeping template copied over to your drive.
[INSERT LINK HERE]

2. Ensure that your system has python3 installed. This will come into use later.
a) On a mac, use `brew` to install it.
b) On windows use `choco` to install python3

3. Install virtualenv
virtualenv provides you a sandboxed environment using the Python interpreter of your choice.
Install it first
`brew install virtualenv`

4. Create a sandboxed python3 env to start working on.
From the root of the toptracker updater directory, do
`virtualenv -p python3 toptracker-env`

5. Activate the python3 virtualenv
`source toptracker-env/bin/activate`
This should start a sandboxed python3 env with pip3 installed 
Do a `python --version` and `pip --version` to check that you are using Python 3.

6. Install `requests` library
Invoke the following command to install the library
`pip install requests`

7. Make sure that your timesheet is filled, and downloaded `as csv` to your local machine, on disk.

a) From the root of the cloned directory,
run the `update-activity` script.

The usage of the script is as follows

```
python update_activity.py -h
usage: update_activity.py [-h] [-e EMAIL] [-p PASSWORD] [-f FILE]

optional arguments:
  -h, --help            show this help message and exit
  -e EMAIL, --email EMAIL
                        Your toptracker email [endswith @bitquilltech.com]
  -p PASSWORD, --password PASSWORD
                        Your password for toptracker
  -f FILE, --file FILE  Your timekeeping template file (csv)
```

Here, `email` and `password` are the credentials you use to sign into toptracker.

8. From the root of the toptracker updater repo do `deactivate` to deactivate the virtual python env.

