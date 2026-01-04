# Save clipboard image to temp file
# Usage: pwsh -File clipboard-image.ps1
# Returns path to saved image

Add-Type -AssemblyName System.Windows.Forms

$clipboard = [System.Windows.Forms.Clipboard]::GetImage()

if ($clipboard) {
    $tempPath = [System.IO.Path]::Combine($env:TEMP, "clipboard_$(Get-Date -Format 'yyyyMMdd_HHmmss').png")
    $clipboard.Save($tempPath, [System.Drawing.Imaging.ImageFormat]::Png)
    Write-Output $tempPath
} else {
    Write-Error "No image in clipboard"
    exit 1
}
