# Player

Play video using python and and VLC Codec.

Designed to be developer friendly, pluggable and (hopefully) extendable given the
architecture. So I used VLC as a base, spinkled some python and QT for a directshow
media view, with a python primary base.

Using QT I've overcome my main focus _"anti-alias/transparent overlays upon a standard hWnd or DirectShow panel"_. - For a custom flux. But with that I can extend another idea of 'pretty vlc'.

Due the the internet of docs and the accessible API, the QT inclusion was extremely easy. As VLC is my go-to player and the tutorial examples work without trouble.
Some features I've applied - and want:

+ Standard right click, mouse, keyboard shortcuts
+ transparent overlays and X11 drawing (for styling)
+ asyncio backend and websocket API.
+ Indendent state management for network control.
+ Multiplex multiple movies with auto positioning (fluid grid)
+ Custom styling to look like the best.



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



## Current

Its base features note POC for all good things:

+ VLC Directshow integration - with good memory management
+ remote handling of player - asyncio
+ chromless window, X11, DirectDraw layers - for better skinning
+ Anti-alias/transparent overlays, pngs - for controls
+ EXE generation - pyinstaller
+ data handling: args, config, dragdrop
+ Good Mouse handling, Keybaord state management, ADA addons - full window dragging, custom keyboard combos, leapmotion/gesture appliances.


## Incoming

Incoming features are pain-points for me with standard players.

+ Network dispatch or 'follow play'
+ Desktop pinning (PIP)
+ preference management
+ Media integration
+ event Bus, and (more) pluggability.

These tools combine a greater project; but are still useful.

### Follow Play

I have monitors and TVs throughout the house but when whating a program (and moving around) I need to stay fixed to one screen or carry a small device. This is fine but for a integrated approach, it would be nice if my media _followed_ me through the house.

Scenaio: Cleaning the house, moving from room to room. Each room has a netowkr ready machine with the player installed and waiting.

A user starts their media on Machine A and proceeds to room B with machine B. Though additional plugins, the machine B will be alerted to wake up and continue the media stream. this will be done through a combination of:

+ Visual recognition
+ room motion
+ pre-determined activity through neural net (sadie context)
+ Human switch.

There is a lead time for 'booting' the network machines.


### Desktop PIP

Pin the players position on the desktiop. A lot like 'always on top', but ensuring size, position and other factors throughout intermittent sessions.

### Preference Management

Keep settings per media file - such as subtitle settings and aspect ratio. This should _smart_ filter up to sibiling folders and media files. E.g a 'series' maintains the subtitle preferences through media location and name alone.

This should be done with the preliminary 'graphdb' implementation (other project).
Settings applied to a media object (graph leaf) will bubble up to sibling trees with similar attributes. As such a folder of _spanish_ may maintain a subtitle preference without setting each media file.

### Media Integration

Work with local media with sharing and self-media service in mind. Allow automated extration from a media tool (CEF) and utitlise the media management for better file walking.

+ Auto step series media
+ Manage names, favorites

#### Global media

A _private and secure_ content media sharing to populate meta data from global sources. They may be automatic such as media cover images, but also may be user driven; such as machete bookmarks assigned witin the media interface.


### Youtube - online autopeek.

Assistance with browser addons for steam peeking, and network control of online media. Not illegal stuff - just leveraging my youtube in a personal control; so I can

+ move rooms with persistence
+ personal bookmarks and screenshots (local library)
+ Better self-hosted meta data for vimeo/youtube etc locations..

### Plugins

I full-metal-jacket plugin system. To allow JS/Py/rest/RPC calls to the player from any service. Allowing more developer integration. This the personal projects

+ AI training: Personal AI gym - (watch my videos)
+ Video developer fun: face detection, screenshot havok.
+ Easy remote tools; desktop tooling; widget development.
+ Extendability with plugin scope for sharing.

#### Future

The extra elements I intend to add - for my own gainz.

##### Leap Scrubber.

Using hand gesture control, build a UI button/scrubber for motion control of media:

+ Presents as a single button on the ui
+ active upon detection of an 'init' motion
+ Pause play by hand stop/pat geature
+ skip using air stoke; speed for length of step.
+ rewind/fast-forward for scrubbing using hand knob turn motion
+ thumbnail scubber to 'pick', scroll, swipe navigation of the video player.
+ up/down motion for audio.
+ grab for stop/play.



##### Fast index.

A super fast file index for iterating with a CTRL+SHIFT+P

+ local media
+ HTML indexes
+ remote network store

##### Other

+ Privacy mode?
+ Media 'bookmark', rename, like/dislike, watch track - on the fly.
+ hoe stop for fast shutdown, but safe persistence.
+


---

I'm essentially looking for a mini netflix for my own legit home movies (all 33 of them :/) and a relic set of mp3s.

---

## Issues

If you see a lot of:

    [0000000000125f70] main libvlc error: stale plugins cache: modified

In the command line:

1. Attempt to refresh your VLC Plugins

    ```
    # C:\Program Files\VideoLAN\VLC\
    > vlc-cache-gen.exe C:\Program Files\VideoLAN\VLC\plugins\
    ```

2. If that fails, delete `plugins.dat` (I renamed it but nothing broke...)

    ```
    C:\Program Files\VideoLAN\VLC\plugins\plugin.dat
    ```

---

Cannot build pyinstaller because of `TypeError`:

    https://stackoverflow.com/questions/54138898/an-error-for-generating-an-exe-file-using-pyinstaller-typeerror-expected-str
