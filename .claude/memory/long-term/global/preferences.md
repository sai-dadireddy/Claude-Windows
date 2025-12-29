
## [2025-12-10 01:06:32]
User prefers concise responses without emojis unless requested

## [2025-12-15 17:36:00]
User accesses Linux server from Windows machine. For AWS SSO login, ALWAYS use --use-device-code flag since browser callbacks to 127.0.0.1 don't work. Command: aws sso login --profile PROFILE --use-device-code

## [2025-12-23 20:00:39]
User connects via SSM from PowerShell 7, then sudo su - claude. Tmux prefix changed to Ctrl+a and backtick for SSM compatibility. Hooks log to ~/.claude/logs/hooks.log (watch-hooks alias)
