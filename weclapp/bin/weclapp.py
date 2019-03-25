from ..app import WeclappApp
from .. import WeclappBaseException

def main():
    try:
        return WeclappApp().run()
    except WeclappBaseException as e:
        print("Something went wrong: %s" % e)
        return 1
