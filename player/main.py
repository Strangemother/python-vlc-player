"""
Main application start tool
"""

import app as _app
import sys


def main():
    app = _app.App(sys.argv)
    app.run()

if __name__ == '__main__':
    main()
