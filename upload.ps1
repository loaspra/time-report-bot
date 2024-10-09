# Script to move the last file created in a directory to another directory

# First make sure that today is a working day
$today = (Get-Date).DayOfWeek

if ($today -eq "Saturday" -or $today -eq "Sunday") {
    Write-Output "You can't run this script on weekends"
    exit
}

# Define source and destination directories
$sourceDir = "C:\Users\santiago.madariaga\OneDrive - NEORIS\General - Test File Sync\pics"
$destDir = "C:\Users\santiago.madariaga\OneDrive - NEORIS\[NO BORRAR] Evidencias Activity Report - DATIO"
$backlogDir = "C:\Users\santiago.madariaga\OneDrive - NEORIS\General - Test File Sync\pics\backlog"

# Get the last file created in the directory
$files = Get-ChildItem -Path $sourceDir -Filter "*.png"

# Check if there are any files to process
if ($files.Count -eq 0) {
    Write-Output "No files found in the source directory"
    exit
}

# Copy each file to the destination directory and then move it to the backlog directory
foreach ($file in $files) {
    $filePath = $file.FullName
    $fileName = $file.Name
    $destFilePath = Join-Path -Path $destDir -ChildPath $fileName
    $backlogFilePath = Join-Path -Path $backlogDir -ChildPath $fileName

    # Copy the file to the destination directory
    Copy-Item -Path $filePath -Destination $destFilePath

    Write-Output $backlogFilePath

    # Move the file to the backlog directory
    Move-Item -Path $filePath -Destination $backlogFilePath

    Write-Output "Processed file: $fileName"
}

Write-Output "All files have been processed"