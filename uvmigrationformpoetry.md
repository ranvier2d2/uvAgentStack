# Migration from Poetry to UV

This document outlines the successful migration of AgentStack from Poetry to UV package manager.

## Files Changed

### Modified Files
1. `.gitignore`:
   - Added UV-specific patterns
   - Removed Poetry-specific patterns

2. `agentstack/cli/cli.py`:
   - Updated project initialization to use UV
   - Added UV lock and sync commands
   - Removed Poetry-specific initialization
   - Updated success messages with correct UV workflow

3. `agentstack/generation/files.py`:
   - Modified ProjectFile class for UV support
   - Removed Poetry metadata handling
   - Updated error messages for UV

4. `agentstack/templates/crewai/{{cookiecutter.project_metadata.project_slug}}/pyproject.toml`:
   - Converted from Poetry to UV format
   - Updated dependency specifications
   - Maintained project scripts section
   - Simplified author metadata to use only author_name

5. `tests/test_generation_files.py`:
   - Added UV configuration tests
   - Removed Poetry-specific tests
   - Updated test fixtures

6. `tox.ini`:
   - Simplified configuration for UV
   - Updated test environment setup
   - Modified dependency handling
   - Added proper development mode installation

### Deleted Files
- `poetry.lock`: Removed as UV uses its own lock file format

## Migration Steps

### 1. Initial Setup
```bash
# Clone the repository
git clone https://github.com/AgentOps-AI/AgentStack.git
cd agentstack

# Generate lock file with UV
uv lock

# Create virtual environment and install dependencies
uv sync
```

### 2. Test Environment Configuration

The key to successful test execution was using `tox-uv` with the correct configuration:

```ini
# tox.ini
[tox]
envlist = py310,py311,py312
isolated_build = True
requires = tox-uv

[testenv]
runner = uv-venv-lock-runner
uv_seed = True
uv_resolution = highest
deps =
    pytest>=7.0
    parameterized
    mypy
    -e .

commands =
    uv pip install -e .
    pytest -vv {posargs}
```

### 3. Changes Made

#### Project Templates and Initialization
The `agentstack init` command now creates projects using UV instead of Poetry. Key changes:

##### Template Changes (pyproject.toml)
```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "{{cookiecutter.project_metadata.project_name}}"
version = "{{cookiecutter.project_metadata.version}}"
description = "{{cookiecutter.project_metadata.description}}"
authors = [{name = "{{cookiecutter.project_metadata.author_name}}"}]
license = {text = "{{cookiecutter.project_metadata.license}}"}
requires-python = ">=3.10,<=3.13"
dependencies = [
    "agentstack",
    "crewai==0.83.0",
    "crewai-tools==0.14.0"
]
```

##### CLI Changes (cli.py)
- Updated initialization messages to show the correct UV workflow:
  ```python
  print(
      "\n"
      " \033[92mAgentStack project generated successfully!\033[0m\n\n"
      "  Next steps:\n"
      f"    cd {project_details['name']}\n\n"
      "  Make sure you have UV installed:\n"
      "    pip install uv\n\n"
      "  Create and activate virtual environment:\n"
      "    uv venv\n"
      "    source .venv/bin/activate\n\n"
      "  Initialize UV and install dependencies:\n"
      "    uv lock\n"
      "    uv sync\n"
      "    uv pip install -e .\n\n"
      "  Finally, try running your agent with:\n"
      "    agentstack run\n\n"
      "  Run `agentstack quickstart` or `agentstack docs` for next steps.\n"
  )
  ```

##### Project File Handling (files.py)
- Modified ProjectFile class to handle UV configuration:
  ```python
  class ProjectFile:
      @property
      def project_metadata(self) -> dict:
          try:
              return self._data['tool']['uv']
          except KeyError:
              raise KeyError("No UV metadata found in pyproject.toml.")
  ```

#### Impact on AgentStack Commands
When users run AgentStack commands:

1. `agentstack init crew_name`:
   - Creates new project with UV configuration
   - Automatically runs `uv lock` and `uv sync`
   - No longer creates poetry.lock file

2. `agentstack run`:
   - Now expects UV-managed dependencies
   - Works with UV-installed packages

3. Other commands (train, replay, test):
   - All work with UV-managed environment
   - No changes to command behavior, only dependency management

### 4. Testing and Results

#### Running Tests
Tests can be run in two ways, both producing the same results:

1. Using pytest directly:
```bash
uv pip install -e .
uv run pytest -vv
```

2. Using tox with UV:
```bash
uv run tox
```

Key points:
- Using `tox-uv` ensures proper integration between UV and tox
- Tests run in the correct working directory
- Environment variables are properly set
- Dependencies are correctly resolved

#### Test Updates
Added three new test cases in `test_generation_files.py`:

1. `test_read_project_file`:
   - Tests successful reading of UV configuration
   - Verifies metadata properties (name, version, description)
   - Uses proper UV configuration format

2. `test_read_project_file_missing_uv`:
   - Tests error handling when UV section is missing
   - Ensures old Poetry format is rejected

3. `test_read_project_file_missing_file`:
   - Tests error handling for missing pyproject.toml
   - Verifies FileNotFoundError is raised

#### Test Results
- All tests passing after fixing author metadata handling
- 77 tests passed
- 16 tests skipped (dependency resolution related)
- No test failures
- Significant improvement in test execution time

## Command Builders and Project Structure

### Project Initialization (`agentstack init`)
The command creates a new project with the following structure:
1. Project Structure:
   - `src/` directory contains main project files (crew.py, main.py)
   - `tools/` is a subdirectory under src for tool modules
   - No `__init__.py` required in src/ and tools/ (modern Python)

2. Configuration Files:
   - `pyproject.toml`: Uses Hatchling build system
   - `uv.lock`: Generated by UV for dependency locking
   - `.env`: For environment variables and configuration

3. UV Integration:
   - Uses `uv venv` for virtual environment creation
   - Dependencies managed with `uv lock` and `uv sync`
   - Development install with `uv pip install -e .`

4. Command Flow:
   ```bash
   # Initial setup
   agentstack init my_project
   cd my_project
   
   # UV environment setup
   pip install uv
   uv venv
   source .venv/bin/activate
   
   # Dependency installation
   uv lock
   uv sync
   uv pip install -e .
   
   # Run the project
   agentstack run
   ```

5. Key Changes from Poetry:
   - Replaced `poetry install` with `uv lock` and `uv sync`
   - Using `uv venv` instead of Poetry's virtual environment
   - Simplified dependency management in pyproject.toml
   - More explicit package installation steps

## Benefits of UV Migration
1. Faster dependency resolution
2. Better compatibility with modern Python tooling
3. Simplified package management
4. Improved test execution environment

## For Users

### New Projects
New projects created with `agentstack init` will automatically use UV:
```bash
agentstack init my_crew
cd my_crew
source .venv/bin/activate  # UV environment will be ready
```

### Existing Projects
To migrate an existing project:

1. Install UV:
```bash
pip install uv
```

2. Convert your pyproject.toml:
- Replace [tool.poetry] with [tool.uv]
- Update dependency format to UV style
- Keep your [project.scripts] section unchanged

3. Initialize UV:
```bash
uv lock
uv sync
```

4. Remove poetry.lock if present

### Git Changes
When committing changes:
1. Add modified files:
   ```bash
   git add .gitignore agentstack/cli/cli.py agentstack/generation/files.py \
          agentstack/templates/crewai/{{cookiecutter.project_metadata.project_slug}}/pyproject.toml \
          tests/test_generation_files.py tox.ini
   ```
2. Remove poetry.lock:
   ```bash
   git rm poetry.lock
   ```

## NOTES about how the command "agentstack init" and the folders it creates work:
- agentstack init will create the project in the current directory
	1.	Project Structure:
	•	The src folder directly contains the main project files (crew.py, main.py, etc.).
	•	tools is a subdirectory under src, containing modules like file_read_tool.py.
	2.	No __init__.py:
	•	It seems the src and tools directories didn’t require __init__.py files to work. This is likely because modern Python no longer requires __init__.py in directories for them to be considered packages if using standard tools like Hatchling.
	3.	Key Files:
	•	The presence of pyproject.toml, uv.lock, and .env indicates that this is a UV-based project with all the necessary configurations.
	4.	File Hierarchy:
	•	The main project files (main.py, crew.py) are directly in src, not within a package-specific directory like src/astack_crew.