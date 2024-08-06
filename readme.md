Things I ran into

1. Can't activate virtual environment due to scripts being disabled. 

> venv\Scripts\Activate.ps1
    C:\Users\schne\Documents\GitHub\spinning-logs\venv\Scripts\Activate.ps1 cannot be loaded because  
    running scripts is disabled on this system. For more information, see about_Execution_Policies    
    at https:/go.microsoft.com/fwlink/?LinkID=135170.
    https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_execution_policies?view=powershell-7.4

To change the Execution Policy, 
- run PowerShell as Admin. 
- Get-ExecutionPolicy -List
- Set-ExecutionPolicy RemoteSigned
- Get-ExecutionPolicy -List

Restricted: No scripts are allowed to run. This is the default setting.
AllSigned: Only scripts signed by a trusted publisher can run.
RemoteSigned: Scripts created on the local machine can run, but scripts downloaded from the internet must be signed by a trusted publisher.
Unrestricted: All scripts can run, but you'll be warned before running scripts downloaded from the internet.
Bypass: No restrictions; all scripts can run.
Undefined: No policy is set; it will inherit from the local Group Policy or the system's default policy.