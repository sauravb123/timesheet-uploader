Usage Instructions
------------------

* First, ensure that you have the timekeeping template copied over to your drive.  
https://docs.google.com/spreadsheets/d/1CBEuZwoZMayjRGm6KruX2JHGSPx-KeJAfEiIdIcAK-s/edit?usp=sharing

* Ensure that your system has python3 installed. This will come into use later.  
a) On a mac, use `brew` to install python3.  
b) On windows use `choco` to install python3

* Install virtualenv
virtualenv provides you a sandboxed environment using the Python interpreter of your choice.  
Install it first  
`pip install virtualenv`

* Create a sandboxed python3 env to start working on.
From the root of the toptracker updater directory, do
`virtualenv -p python3 toptracker-env`

* Activate the python3 virtualenv
`source toptracker-env/bin/activate`
This should start a sandboxed python3 env with pip3 installed 
Do a `python --version` and `pip --version` to check that you are using Python 3.

* Install `requests` library
Invoke the following command to install the library
`pip install requests`

* Make sure that your timesheet for the month you are trying to upload is filled, and downloaded `as csv` to your local machine, on disk.

* From the root of the cloned directory,
    run the `update-activity` script.

    The usage of the script is as follows
    >> 
    ```
    python3 update_activity.py -h
    
    usage: update_activity.py [-h] -e EMAIL -f FILE [-p PASSWORD]

    required arguments:
      -e EMAIL, --email EMAIL
                            Your toptracker email [endswith @bitquilltech.com].
      -f FILE, --file FILE  Your timekeeping template file (csv).

    optional arguments:
      -h, --help            show this help message and exit
      -p PASSWORD, --password PASSWORD
                            Your toptracker password.
    ```

    Here, `email` and `password` are the credentials you use to sign into toptracker, where `password` is optional.  
    `password` can either be provided via the password flag or entered when prompted upon during the script execution.

* From the root of the toptracker updater repo do `source deactivate` to deactivate the virtual python env.

