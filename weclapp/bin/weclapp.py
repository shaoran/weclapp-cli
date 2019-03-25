from colorama import init as colorama_init, Fore, Style

from ..app import WeclappApp
from .. import WeclappBaseException

def main():
    try:
        colorama_init()
        return WeclappApp().run()
    except WeclappBaseException as e:
        print(Fore.RED + ('Something went wrong: %s' % e) + Style.RESET_ALL)
        return 1
