from .start_env import StartEnvCommand
from .run import RunCommand
from .start_project import StartProjectCommand
from .build import BuildCommand

commands_classes = [
    StartEnvCommand,
    StartProjectCommand,
    RunCommand,
    BuildCommand,
]
