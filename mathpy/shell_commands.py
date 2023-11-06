from . import run_file


def run(path: str, *args: list):
    print(path[-3:])

    try:
        file = open(path, 'rt', encoding='utf-8')
    except FileNotFoundError:
        print(f'File {path !r} not found.')
    else:
        run_file(file)