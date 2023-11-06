from .shell_commands import run
from sys import argv

command = argv[1]  # argv[0] is current path
arguments = argv[2:]

if command == 'run':
    run(*arguments)
else:
    print(f'Unknown command {command !r}')