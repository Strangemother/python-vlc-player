# Player

Play video using python and and VLC Codec.

## Requirements

+ python 3
+ Qt5
+ VLC
+ Flask
+ pynput


## Install

    py setup.py install


## Run

If installed as a package, import and run the main application

    from player.qt_app import App
    app = App()
    app.run()

Alternatively the entire folder is ran using a `__main__` method:

    $> ls
        - vlc_player/
            - __main__.py
        - other/
    $> py vlc_player
