# Worktree Manager

**Description:** Manage git worktrees for parallel Claude Code development
**Allowed Tools:** bash, read, write

---

## Usage

```bash
/worktree create <feature-name>   # Create new worktree
/worktree list                    # List all worktrees
/worktree merge <feature-name>    # Merge worktree to main
/worktree cleanup                 # Remove completed worktrees
/worktree status                  # Show status of all worktrees
```

---

## Prompt

When user runs `/worktree`:

### **Action: CREATE**
```bash
# Parse feature name from arguments
FEATURE_NAME="$1"
BRANCH_NAME="feature/${FEATURE_NAME}"

# Create worktree directory if doesn't exist
mkdir -p .worktrees

# Create worktree
git worktree add .worktrees/${FEATURE_NAME} -b ${BRANCH_NAME}

# Provide instructions
echo "✅ Worktree created!"
echo ""
echo "📂 Location: .worktrees/${FEATURE_NAME}"
echo "🌿 Branch: ${BRANCH_NAME}"
echo ""
echo "🚀 Next steps:"
echo "  1. Open new terminal"
echo "  2. cd .worktrees/${FEATURE_NAME}"
echo "  3. claude"
echo "  4. Start working on ${FEATURE_NAME}!"
```

### **Action: LIST**
```bash
echo "📋 Active Worktrees:"
echo ""
git worktree list
echo ""
echo "💡 Tip: Each worktree can run Claude Code independently"
```

### **Action: MERGE**
```bash
FEATURE_NAME="$1"
BRANCH_NAME="feature/${FEATURE_NAME}"

# Switch to main
git checkout main

# Pull latest
git pull origin main

# Merge feature branch
git merge ${BRANCH_NAME}

# Push
git push origin main

echo "✅ Merged ${FEATURE_NAME} to main!"
echo "Run '/worktree cleanup' to remove the worktree"
```

### **Action: CLEANUP**
```bash
echo "🧹 Cleaning up merged worktrees..."

# List worktrees
git worktree list | grep ".worktrees" | while read worktree; do
  path=$(echo $worktree | awk '{print $1}')
  branch=$(echo $worktree | awk '{print $3}' | tr -d '[]')

  # Check if branch is merged
  if git branch --merged main | grep -q "$branch"; then
    echo "Removing: $path (merged)"
    git worktree remove $path
  fi
done

echo "✅ Cleanup complete!"
```

### **Action: STATUS**
```bash
echo "📊 Worktree Status:"
echo ""

git worktree list | grep ".worktrees" | while read worktree; do
  path=$(echo $worktree | awk '{print $1}')
  branch=$(echo $worktree | awk '{print $3}' | tr -d '[]')

  echo "📁 $path"
  echo "🌿 Branch: $branch"

  # Check if merged
  if git branch --merged main | grep -q "$branch"; then
    echo "✅ Status: Merged (ready to cleanup)"
  else
    echo "🚧 Status: Active development"
  fi
  echo ""
done
```

---

## Examples

### **Create Worktree**
```bash
/worktree create dark-mode

# Output:
# ✅ Worktree created!
# 📂 Location: .worktrees/dark-mode
# 🌿 Branch: feature/dark-mode
# 🚀 Next steps: cd .worktrees/dark-mode && claude
```

### **Parallel Development**
```bash
# Terminal 1
/worktree create feature-1
cd .worktrees/feature-1
claude
> "Implement feature 1"

# Terminal 2
/worktree create feature-2
cd .worktrees/feature-2
claude
> "Implement feature 2"

# Both work simultaneously!
```

### **List All**
```bash
/worktree list

# Output:
# 📋 Active Worktrees:
# /path/to/main        abc123 [main]
# /path/.worktrees/ui  def456 [feature/ui]
# /path/.worktrees/api ghi789 [feature/api]
```

### **Merge & Cleanup**
```bash
/worktree merge dark-mode
/worktree cleanup
```

---

## Best Practices

1. **Independent Features** - Each worktree should work on separate files
2. **Frequent Merges** - Merge to main often to avoid conflicts
3. **Clean Up** - Remove merged worktrees regularly
4. **Test Before Merge** - Run tests in each worktree before merging
5. **Document** - Keep notes on what each worktree is working on

---

## Tips

- **Avoid Overlap** - Don't edit same files in multiple worktrees
- **Sync Often** - Pull from main in each worktree regularly
- **Use .gitignore** - Add `.worktrees/` to .gitignore
- **Name Clearly** - Use descriptive feature names
- **Limit Count** - Don't create too many worktrees (3-5 max)
