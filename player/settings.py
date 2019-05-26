import os
import sys

# Translate asset paths to useable format for PyInstaller
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath('.'), relative_path)



PLAYER_ROOT = resource_path(os.path.dirname(__file__))


RAISE = '__defraise__'

# Base settings to override
SETTINGS = dict(
    # set the main window OS frame - set True to remove the OS frame
    frameless=True,
    json_file='config.json',
    init_size=[500, 400],
    player_title='My Fancy Player',
    bezel=2,
    assets='assets',
    images='{assets}/images',
    cache='{assets}/cache',
    # Filename loaded initially
    file="M:/Movies/Startrek TNG/Star.Trek.TNG.S03.COMPLETE.FS.DL.DVDRiP.Xvid-BEX.par2/Star.Trek.TNG.S03E14.Riker.unter.Verdacht.FS.DL.DVDRiP.Xvid-BEX.avi",
    # If a file is given, should the app autoplay on init load
    autoplay=True,
    root=PLAYER_ROOT,
    background_color='#3f4d82',
)


def resolve_in(conf, name, default=RAISE):
    '''Return a key `name` from the given conf `dict`. Resolved strings are
    formatted through the same conf dict, returning a templated string.
    '''
    if (name in conf) is False and default == RAISE:
        # Raise a default error early.
        return conf.get(name)

    val = conf.get(name, default)
    return val.format(**conf)


def load_settings(settings=None):
    config = SETTINGS.copy()

    fp = os.path.join(PLAYER_ROOT, config['json_file'])
    file_conf = {}
    if os.path.isfile(fp):
        with open(fp, 'r') as stream:
            file_conf = json.load(stream)
        config.update(file_conf)

    if settings is not None:
        config.update(settings)

    return config
