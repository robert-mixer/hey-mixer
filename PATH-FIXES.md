# Path Fixes for run.sh

## ✅ Fixed Issues

### 1. **Path Calculation**
**Before**: Script was calculating its own paths using `BASH_SOURCE`
**After**: Now uses environment variables exported by mixer.sh:
- `MIXER_ROOT` - The project root
- `AGENT_DIR` - The agent's directory
- `AGENT_NAME` - The agent name

### 2. **Removed Typo**
**Before**: `--dangerously-skip-permisssions` (three s's)
**After**: Removed this flag entirely (not needed for normal operation)

### 3. **Removed Duplicate Tool**
**Before**: Had both `"Bash"` and specific Bash commands
**After**: Only specific Bash commands (more restrictive, safer)

### 4. **Simplified add-dir Paths**
**Before**: `--add-dir \"$PROJECT_ROOT/.claude\"`
**After**: `--add-dir \".claude\"` (relative paths work since we're in project root)

### 5. **Changed Model**
**Before**: `--model opus`
**After**: `--model sonnet` (as originally intended)

## 📝 How It Works Now

1. **mixer.sh** does:
   ```bash
   export MIXER_ROOT=/path/to/project
   export AGENT_DIR=/path/to/project/agents/goal-builder
   export AGENT_NAME=goal-builder
   cd "$MIXER_ROOT"
   exec "${AGENT_DIR}/run.sh"
   ```

2. **run.sh** uses these variables:
   ```bash
   PROJECT_ROOT="${MIXER_ROOT}"
   SYSTEM_PROMPT_FILE="${AGENT_DIR}/system-prompt.md"
   ```

3. **Claude runs** with:
   - System prompt from the agent directory
   - Access to .claude and agents directories
   - Restricted tool permissions
   - Sonnet model

## ✨ Result

The script now correctly:
- Uses paths relative to where it's executed (project root)
- Leverages environment variables from mixer.sh
- Has no typos or redundant flags
- Maintains security with restricted tools