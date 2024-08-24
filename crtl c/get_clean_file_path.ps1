# Function to get the file path from clipboard
function Get-CleanFilePath {
    $clipData = Get-Clipboard -Format FileDropList -ErrorAction SilentlyContinue
    if ($null -ne $clipData -and $clipData.Count -gt 0) {
        $filePath = $clipData[0]
        return $filePath
    }
    return "No file path found"
}

# Get and print the clean file path
$filePath = Get-CleanFilePath
Write-Output $filePath
