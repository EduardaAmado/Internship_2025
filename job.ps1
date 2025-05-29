<#
.SYNOPSIS  
    Job synopsis
.DESCRIPTION  
    Job description
.AUTHOR
    unknown
.VERSION
    1.0
#>

# Set job environment based on the script definition
Set-JobEnv $MyInvocation.MyCommand.Definition

$script:SCRIPTPATH = (Get-ChildItem $MyInvocation.MyCommand.Path).DirectoryName
$dateRun = Get-Date -Format "yyyy-MM-dd HH:mm"

# Initialize variables
$_CODE = 0
$_EXE = ""
$_PARM = ""

$ODATE = $args[0]

@"
========================================================
Start of Job $env:T_JOB : $(Get-Date -Format u)
========================================================
"@

# Change to the directory where the scripts are located
Set-Location -Path "D:\_Apps\ARM\_Batchs\PARM_DGET_RUNNERS_DATA\bin"
$_CODE = 100
$_EXE = "python.exe"

# List of parameters for executing the two scripts
$_PARMS = @(
    "-u D:\_Apps\ARM\_Batchs\PARM_DGET_RUNNERS_DATA\bin\get_exp_data.py",
    "-u D:\_Apps\ARM\_Batchs\PARM_DGET_RUNNERS_DATA\bin\get_expa_data.py"  
)

# Display the command that will be executed
Write-Host "Start-Process $_EXE -ArgumentList $_PARMS -PassThru -Wait"

# Execute the first script
$process1 = Start-Process $_EXE -ArgumentList $($_PARMS[0]) -PassThru -Wait
$_CODE = $process1.ExitCode

# If the first script executed successfully, execute the second
if ($_CODE -eq 0) {
    $process2 = Start-Process $_EXE -ArgumentList $($_PARMS[1]) -PassThru -Wait
    $_CODE = $process2.ExitCode
}

Write-Host $_CODE

@"
========================================================
End of Job $env:T_JOB : $(Get-Date -Format u)
========================================================
"@
echo "Exit Code : $_CODE"
exit $_CODE
