import os
import unittest
from pathlib import Path
import shutil
from agentstack import conf
from agentstack.conf import ConfigFile
from agentstack.generation.files import EnvFile, ProjectFile
from agentstack.utils import (
    verify_agentstack_project,
    get_framework,
    get_telemetry_opt_out,
    get_version,
)

BASE_PATH = Path(__file__).parent


# TODO copy files to working directory
class GenerationFilesTest(unittest.TestCase):
    def setUp(self):
        self.project_dir = BASE_PATH / "tmp" / "generation_files"
        os.makedirs(self.project_dir)

        shutil.copy(BASE_PATH / "fixtures/agentstack.json", self.project_dir / "agentstack.json")
        conf.set_path(self.project_dir)

    def tearDown(self):
        shutil.rmtree(self.project_dir)

    def test_read_config(self):
        config = ConfigFile()  # + agentstack.json
        assert config.framework == "crewai"
        assert config.tools == []
        assert config.telemetry_opt_out is None
        assert config.default_model is None
        assert config.agentstack_version == get_version()
        assert config.template is None
        assert config.template_version is None

    def test_write_config(self):
        with ConfigFile() as config:
            config.framework = "crewai"
            config.tools = ["tool1", "tool2"]
            config.telemetry_opt_out = True
            config.default_model = "openai/gpt-4o"
            config.agentstack_version = "0.2.1"
            config.template = "default"
            config.template_version = "1"

        tmp_data = open(self.project_dir / "agentstack.json").read()
        assert (
            tmp_data
            == """{
    "framework": "crewai",
    "tools": [
        "tool1",
        "tool2"
    ],
    "telemetry_opt_out": true,
    "default_model": "openai/gpt-4o",
    "agentstack_version": "0.2.1",
    "template": "default",
    "template_version": "1"
}"""
        )

    def test_read_missing_config(self):
        conf.set_path(BASE_PATH / "missing")
        with self.assertRaises(FileNotFoundError) as _:
            _ = ConfigFile()

    def test_verify_agentstack_project_valid(self):
        verify_agentstack_project()

    def test_verify_agentstack_project_invalid(self):
        conf.set_path(BASE_PATH / "missing")
        with self.assertRaises(SystemExit) as _:
            verify_agentstack_project()

    def test_get_framework(self):
        assert get_framework() == "crewai"

    def test_get_framework_missing(self):
        conf.set_path(BASE_PATH / "missing")
        with self.assertRaises(SystemExit) as _:
            get_framework()

    def test_read_env(self):
        shutil.copy(BASE_PATH / "fixtures/.env", self.project_dir / ".env")

        env = EnvFile()
        assert env.variables == {"ENV_VAR1": "value1", "ENV_VAR2": "value2"}
        assert env["ENV_VAR1"] == "value1"
        assert env["ENV_VAR2"] == "value2"
        with self.assertRaises(KeyError) as _:
            env["ENV_VAR100"]

    def test_write_env(self):
        shutil.copy(BASE_PATH / "fixtures/.env", self.project_dir / ".env")

        with EnvFile() as env:
            env.append_if_new("ENV_VAR1", "value100")  # Should not be updated
            env.append_if_new("ENV_VAR100", "value2")  # Should be added

        tmp_data = open(self.project_dir / ".env").read()
        assert (
            tmp_data
            == """\nENV_VAR1=value1\nENV_VAR2=value_ignored\nENV_VAR2=value2\n#ENV_VAR3=""\nENV_VAR100=value2"""
        )

    def test_read_env_numeric_that_can_be_boolean(self):
        shutil.copy(BASE_PATH / "fixtures/.env", self.project_dir / ".env")

        with EnvFile() as env:
            env.append_if_new("ENV_VAR100", 0)
            env.append_if_new("ENV_VAR101", 1)
        
        env = EnvFile()  # re-read the file
        assert env.variables == {"ENV_VAR1": "value1", "ENV_VAR2": "value2", "ENV_VAR100": "0", "ENV_VAR101": "1"}

    def test_write_env_commented(self):
        """We should be able to write a commented-out value."""
        shutil.copy(BASE_PATH / "fixtures/.env", self.project_dir / ".env")

        with EnvFile() as env:
            env.append_if_new("ENV_VAR3", "value3")

        env = EnvFile()  # re-read the file
        assert env.variables == {"ENV_VAR1": "value1", "ENV_VAR2": "value2", "ENV_VAR3": "value3"}

        tmp_file = open(self.project_dir / ".env").read()
        assert (
            tmp_file
            == """\nENV_VAR1=value1\nENV_VAR2=value_ignored\nENV_VAR2=value2\n#ENV_VAR3=""\nENV_VAR3=value3"""
        )

    def test_read_project_file(self):
        # Create a test pyproject.toml with UV configuration
        pyproject_content = """
[tool.uv]
name = "test-project"
version = "0.1.0"
description = "Test project description"
authors = ["Test Author"]
license = "MIT"

[tool.uv.dependencies]
python = ">=3.10,<=3.13"
agentstack = {version = "0.1.0", extras = ["crewai"]}
"""
        with open(self.project_dir / "pyproject.toml", "w") as f:
            f.write(pyproject_content)

        project = ProjectFile()
        assert project.project_name == "test-project"
        assert project.project_version == "0.1.0"
        assert project.project_description == "Test project description"

    def test_read_project_file_missing_uv(self):
        # Create a test pyproject.toml without UV configuration
        pyproject_content = """
[project]
name = "test-project"
version = "0.1.0"
"""
        with open(self.project_dir / "pyproject.toml", "w") as f:
            f.write(pyproject_content)

        project = ProjectFile()
        with self.assertRaises(KeyError) as cm:
            _ = project.project_metadata
        assert str(cm.exception) == "'No UV metadata found in pyproject.toml.'"

    def test_read_project_file_missing_file(self):
        with self.assertRaises(FileNotFoundError) as _:
            _ = ProjectFile()
