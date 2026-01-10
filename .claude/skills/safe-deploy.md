---
name: safe-deploy
description: Deploy with safety checks and verification
context: fork
agent: bash
model: haiku
user-invocable: true
hooks:
  PreToolUse:
    - matcher: Bash
      command: echo "[DEPLOY] Pre-check starting..."
  PostToolUse:
    - matcher: Bash
      command: echo "[DEPLOY] Step completed"
  Stop:
    - command: echo "[DEPLOY] Deployment workflow finished"
triggers:
  - "deploy"
  - "safe deploy"
  - "production deploy"
---

# Safe Deploy Skill

Deploy with built-in safety checks. Hooks are scoped to this skill only.

## Pre-Deploy Checklist

Before deploying, verify:
1. All tests pass
2. No uncommitted changes
3. On correct branch
4. Build succeeds

## Deployment Steps

1. **Verify environment**
   ```bash
   git status
   git branch --show-current
   ```

2. **Run tests**
   ```bash
   npm test  # or pytest
   ```

3. **Build**
   ```bash
   npm run build  # or equivalent
   ```

4. **Deploy**
   ```bash
   # Your deploy command here
   ```

## Post-Deploy Verification

After deployment:
1. Check service health
2. Verify key endpoints
3. Monitor logs for errors

## Rollback

If issues detected:
```bash
# Your rollback command
```
