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

### 2. Environment Management
- Added automatic virtual environment handling
- New standardized naming convention: `agentstackvenv_[project_name]`
- Interactive prompt to handle environment switching
- Clear command preview before execution
- Automatic dependency installation with UV

### 3. Project Initialization
- Improved project initialization process
- Removed automatic dependency installations from existing environments
- Added clear success messages and next steps
- TODO: Add support for migrating from regular CrewAI projects

### 4. Dependency Management
- Enhanced environment detection (Conda/venv)
- Integrated UV for dependency handling
- Clear instructions for manual setup when needed

### 5. Flag Compatibility
Updated flag validation to ensure proper usage:
- `--template`: Cannot be used with `--wizard`
- `--wizard`: Cannot be used with `--template`

## Usage Examples

### Standard Project Creation
```bash
agentstack init my_project
```

### Using the Wizard
```bash
agentstack init --wizard
```

### With Template
```bash
agentstack init my_project --template hello_alex
```

## Environment Setup

The CLI now offers two ways to handle virtual environments:

### 1. Automatic Setup
When in an existing virtual environment, the CLI will:
1. Ask for permission to handle environment switching
2. Show preview of commands to be executed
3. Create new environment with standardized name
4. Install all dependencies automatically

### 2. Manual Setup
If automatic setup is declined or fails, clear instructions are provided:
```bash
deactivate  # Leave current environment
cd [project_name]
uv venv --name agentstackvenv_[project_name]
source agentstackvenv_[project_name]/bin/activate
uv lock
uv sync
```

## Next Steps

### Planned Improvements
- Add CrewAI project migration support
- Enhance template management
- Add more configuration options
- Improve error handling and recovery

### Testing
To ensure these changes work as expected:
1. Test environment detection
2. Verify automatic environment setup
3. Confirm dependency installation
4. Check error handling scenarios
