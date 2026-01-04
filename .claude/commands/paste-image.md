# Paste Clipboard Image

Save clipboard image to temp file and analyze it.

## Get Image from Clipboard

```bash
pwsh -File ~/.claude/scripts/clipboard-image.ps1
```

## Workflow

1. Run the PowerShell script above to save clipboard to temp file
2. Read the returned file path
3. Analyze the image using the Read tool

## Usage

When user says "paste image" or "analyze clipboard":
1. Execute the PowerShell script
2. Use the returned path to read the image
3. Describe or analyze the image content
