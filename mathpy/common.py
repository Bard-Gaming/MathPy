from time import time

module_folder = "/".join(__file__.split('\\')[:-1])

program_start_time = time()


def current_time() -> float:
    return round(time() - program_start_time, 3)


def call_logger(fnc):
    def wrapper(*args, **kwargs):
        print(f'[{current_time()}] - Calling function {fnc.__name__ !r}...')
        return_value = fnc(*args, **kwargs)
        print(f'[{current_time()}] - Finished calling function {fnc.__name__ !r} ({return_value = !r}).')
        return return_value

    return wrapper
