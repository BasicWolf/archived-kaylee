#!/usr/bin/env python
from kaylee.manager import AdminCommandsManager

import logging

def setup_logging():
    logging.basicConfig(level=logging.DEBUG)

if __name__ == '__main__':
    setup_logging()
    AdminCommandsManager.execute_from_command_line()
