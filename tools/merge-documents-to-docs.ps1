# Merge documents/ folder into docs/ folder
# Created: 2025-10-14

$source = "documents"
$dest = "docs"

if (-not (Test-Path $source)) {
    Write-Output "Source folder 'documents' does not exist. Nothing to merge."
    exit 0
}

if (-not (Test-Path $dest)) {
    Write-Output "Destination folder 'docs' does not exist. Creating it..."
    New-Item -ItemType Directory -Path $dest -Force | Out-Null
}

Write-Output "Merging $source into $dest..."

# Get all items in source
$items = Get-ChildItem -Path $source -Force -Recurse

$fileCount = 0
$folderCount = 0

# Copy each item
foreach ($item in Get-ChildItem -Path $source -Force) {
    $relativePath = $item.Name
    $targetPath = Join-Path $dest $relativePath

    if (Test-Path $targetPath) {
        Write-Output "  Merging: $relativePath (exists, copying contents)..."
        Copy-Item -Path $item.FullName -Destination $dest -Recurse -Force
        if ($item.PSIsContainer) { $folderCount++ } else { $fileCount++ }
    } else {
        Write-Output "  Moving: $relativePath..."
        Move-Item -Path $item.FullName -Destination $dest -Force
        if ($item.PSIsContainer) { $folderCount++ } else { $fileCount++ }
    }
}

Write-Output ""
Write-Output "Merge complete!"
Write-Output "  Folders processed: $folderCount"
Write-Output "  Files processed: $fileCount"

# Remove empty source folder
if ((Get-ChildItem -Path $source -Force).Count -eq 0) {
    Write-Output ""
    Write-Output "Removing empty 'documents' folder..."
    Remove-Item -Path $source -Force -Recurse
    Write-Output "Done! All contents from 'documents/' are now in 'docs/'"
} else {
    Write-Output ""
    Write-Output "Warning: 'documents' folder still has contents. Manual review needed."
}
