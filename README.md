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

## Dev run

    env3\Scripts\activate
    python src


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


## Issues

If you see a lot of:

    [0000000000125f70] main libvlc error: stale plugins cache: modified

In the command line:

1. Attempt to refresh your VLC Plugins

    # C:\Program Files\VideoLAN\VLC\
    > vlc-cache-gen.exe C:\Program Files\VideoLAN\VLC\plugins\

2. If that fails, delete `plugins.dat` (I renamed it but nothing broke...)

    C:\Program Files\VideoLAN\VLC\plugins\plugin.dat

---

Cannot build pyinstaller because of `TypeError`:

    https://stackoverflow.com/questions/54138898/an-error-for-generating-an-exe-file-using-pyinstaller-typeerror-expected-str
