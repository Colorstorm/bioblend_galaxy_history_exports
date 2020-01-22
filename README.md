# bioblend_galaxy_history_exports
```
General
    Uses Python3 and Bioblend
    A Python script for exporting galaxy histories
    Could export every history from every user or
    every history from a specific user or
    a specific histories
    A directory with the username will be generated in these are the exported history as tar.gz

Requirements
    Python3
    bioblend
    
Arguments
  positional arguments
    ip: IP of the galaxy machine(see servers, vm3: 172.24.148.206, vm10: 172.24.148.203)
    API Key: The Galaxy API Key of an admin (List of all API Keys: galaxy>admin>users)
  optional arguments
    -u Usernames: List of the usernames you want to export(List of all usernames: galaxy>admin>user) spelling is important
    -i history IDs: List of history IDs you want to export(the ID is the first part of the exported/error file)
    -e errorCorrection: is default False/not activated. If it is True/activated and if a history is allready succesfully         exported it will be skipped, if the history is not exported it will be exported and if the history export failed before, it will be exported and the error message will be refreshed(in case of an error) or removed. If it is False/not activated every history will be exported and it will overwrite histories who are already exported.
    -w warnings: default false/not. If activated everytime a history will be skipped a warning will be printed. Only for debugging useful

Guide
  Export all
    Copy the python script in an empty backup directory
    Start the python script
    Go on with the error correction 
      python3 galaxyHistoryExport.py <IP> <API Key>
    A normal history takes about a minute.(the complete Backup for vm3 2019_12 took some days)
    Less errors occur if it runs over night/when servers are not in use
    Error rate could probalby be up to 40-50%
    This mode does override any existing hsitory backup in the direcetory
  
  Error correction
    Make sure the python script is still there
    Start the python script, use the command below
    Repeat it until no errors occur
      #command to start the python script
      python3 galaxyHistoryExport.py -e True<IP> <API Key>
    A normal history takes about a minute.
    Less errors occur if it runs over night/when servers are not in use
    Error rate could still be up to 40-50%
    After 4 to 5 tries without succes there is probably something wrong with the history
    This mode does not override any existing history backup
  
  Export histories of specific users
    Make sure the python script is still there
    Start the python script, use the command below to correct errors or to overwrite the histories
      #command to overwrite the history
      python3 galaxyHistoryExport.py -u <username1> <username...> -e False <IP> <API Key>
      #command to correct the error of the history
      python3 galaxyHistoryExport.py -u <username1> <username...> -e True <IP> <API Key>
    A normal history takes about a minute.
    Error rate could be up to 40-50%
  
  Export histories with specific IDs
    Make sure the python script is still there
    Start the python script, use the command below to correct an error or to overwrite the history
      #command to overwrite the history
      python3 galaxyHistoryExport.py -i <ID1> <ID...> -e False <IP> <API Key>
      #command to correct the error of the history
      python3 galaxyHistoryExport.py -i <ID1> <ID...> -e True <IP> <API Key>
    A normal history takes about a minute.
    Less errors occur if it runs over night/when servers are not in use
    Error rate could still be up to 40-50%
    The runtime is slower than the runtime of usernames and IDs
  
  Export histories with specific IDs from specific users
    Make sure the python script is still there
    Start the python script, use the command below to correct errors or to overwrite the histories
      #command to overwrite the history
      python3 galaxyHistoryExport.py -u <username1> <username...> -i <ID1> <ID...> -e False <IP> <API Key>
      #command to correct the error of the history
      python3 galaxyHistoryExport.py -u <username1> <username...> -i <ID1> <ID...> -e True <IP> <API Key>
    A normal history takes about a minute.
    Error rate could be up to 40-50%
    more efficient than using only the history ID
    
usage: galaxyHistoryExport.py [-h] [-u USERNAMES [USERNAMES ...]]
                              [-i IDS [IDS ...]] [-e ERRORCORRECTION]
                              [-w WARNING]
                              ip key

positional arguments:
  ip                    ip/hostname of your galaxy machine
  key                   The API key of an admin on the galaxy machine

optional arguments:
  -h, --help            show this help message and exit
  -u USERNAMES [USERNAMES ...], --usernames USERNAMES [USERNAMES ...]
                        To export only histories of special users
  -i IDS [IDS ...], --ids IDS [IDS ...]
                        To export only histories with the id
  -e ERRORCORRECTION, --errorCorrection ERRORCORRECTION
                        Mode for error correction, if there is a tar.gz file
                        for the history it will skip these
  -w WARNING, --warning WARNING
                        Print warnings

Exports histories from galaxy using bioblend.
```
