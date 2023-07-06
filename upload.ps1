# Script to move the last file created in a directory to another directory

# First make sure that today is a working day
$today = (Get-Date).DayOfWeek

if ($today -eq "Saturday" -or $today -eq "Sunday") {
    Write-Output "You can't run this script on weekends"
    exit
}


# Get the last file created in the directory
$lastFile = Get-ChildItem -Path "C:\Users\Server Gata\OneDrive - NEORIS\General - Test File Sync\pics" -Filter "*.png" -Recurse | Sort-Object -Property CreationTime -Descending | Select-Object -First 1

# Check if the file name contains the current date (YYYYMMdd)
$fileName = $lastFile.Name
$today = (Get-Date).ToString("yyyyMMdd")
if ($fileName -notlike "*$today*") {
    Write-Output "The file name doesn't contain the current date"
    # re run python script "main.py"
    python "C:\Users\Server Gata\Documents\Python-Scripts\main.py"
    
    # wait 5 minutes for the file to be created
    Start-Sleep -s 300
}

# Check again if the file name contains the current date (YYYYMMdd)
# Get the last file created in the directory
$lastFile = Get-ChildItem -Path "C:\Users\Server Gata\OneDrive - NEORIS\General - Test File Sync\pics" -Filter "*.png" -Recurse | Sort-Object -Property CreationTime -Descending | Select-Object -First 1
$fileName = "C:\Users\Server Gata\OneDrive - NEORIS\General - Test File Sync\pics\" + $lastFile.Name


Write-Host "File to copy: " + $lastFile
Write-Host $lastFile

if ($fileName -notlike "*$today*") {
    Write-Output "The file name doesn't contain the current date (2nd attempt)"
    exit
}

# Copy the file to the destination directory
Copy-Item -Path $fileName -Destination "C:\Users\Server Gata\OneDrive - NEORIS\[NO BORRAR] Evidencias Activity Report - DATIO"

# End of script