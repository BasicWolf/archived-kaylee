from .start_env import StartEnvCommand
from .run import RunCommand
from .start_project import StartProjectCommand


commands_classes = [
    StartEnvCommand,
    StartProjectCommand,
    RunCommand,
]
