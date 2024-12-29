# CLI Modifications Documentation

## Recent Changes

### 1. Environment-Aware Dependency Management
The initialization process now intelligently handles dependencies based on the user's environment:

#### Virtual Environment Detection
- Detects if user is in:
  - Conda environment (via `CONDA_PREFIX`)
  - Python virtual environment (via `VIRTUAL_ENV`)
  - No environment

#### UV Integration
- Checks for UV installation
- For venv + UV environments:
  ```bash
  # Automatically runs:
  uv lock
  uv sync
  ```
- Shows environment-specific guidance:
  - Conda users: Instructions for UV in conda
  - Venv users without UV: UV installation steps
  - No environment: Full setup instructions

### 2. CrewAI Migration Wizard
Added a new `--migratecrew` flag to facilitate migration from CrewAI projects:

```bash
agentstack init <project_name> --migratecrew
```

#### Features
- Streamlined migration process
- Only asks for essential information:
  - Agent names (snake_case)
  - Task names (snake_case)
  - Task-to-agent assignments
- Provides placeholder comments for:
  - Agent roles
  - Agent goals
  - Agent backstories
  - Task descriptions
  - Expected outputs

#### Example Placeholders
```python
# Agent
agent['role'] = "# Replace with your CrewAI agent's role:
# Example: agent.role = 'Senior Data Analyst'"

# Task
task['description'] = "# Replace with your CrewAI task's description:
# Example: task.description = 'Analyze monthly sales data'"
```

### 3. Flag Compatibility
Updated flag validation to ensure proper usage:
- `--template`: Cannot be used with `--wizard` or `--migratecrew`
- `--wizard`: Cannot be used with `--template` or `--migratecrew`
- `--migratecrew`: Cannot be used with `--template` or `--wizard`

## Usage Examples

### Standard Project Creation
```bash
agentstack init myproject
```

### Using the Wizard
```bash
agentstack init myproject --wizard
# or
agentstack init myproject -w
```

### Migrating from CrewAI
```bash
agentstack init myproject --migratecrew
# or
agentstack init myproject -m
```

### Using a Template
```bash
agentstack init myproject --template hello_alex
# or
agentstack init myproject -t hello_alex
```

## Next Steps
1. Test the CrewAI migration workflow with real projects
2. Consider adding automatic detection of CrewAI project structure
3. Add more detailed examples in placeholder comments
4. Consider adding validation for CrewAI-specific patterns
