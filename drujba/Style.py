from colorama import init

init()
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"
YELLOW = '\033[93m'
BLUE = '\u001b[34m'
BLACK = '\u001b[30m'
LIGTHBLUE = '\033[38;5;6m'
WHITEBLUE = '\033[38;5;81m'


def command_message(str) -> str:
    return f'{WHITEBLUE}{str}{RESET}'


def positive_action(str) -> str:
    return (f'{GREEN}{str}{RESET}')


def error_message(str) -> str:
    return (f'{RED}{str}{RESET}')


def help_message(str):
    return (f'{BLUE}{str}{RESET}')


def book_style(str):
    return (f'{LIGTHBLUE}{str}{RESET}')


def help1_message(str):
    return (f'{RED}{str}{RESET}')

# def show_all_collor():
#     for i in range(16):
#         for j in range(16):
#             code = str(i * 16 + j)
#             print(f"\033[48;5;{code}m {code.ljust(4)} \033[0m", end="")
#         print()
