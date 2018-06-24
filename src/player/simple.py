import api

import logging

FORMAT = "- %(message)s"
logging.basicConfig(level=logging.DEBUG, format=FORMAT)

def log(*a):
    logging.info(' '.join(map(str, a)))

instance = None
player = None

def play(uri):
    global instance
    global player

    if instance is None:
        instance = api.Instance()

    player = instance.media_player_new(uri)
    player.play()
    return player

def stop(_player=None):
    p = _player or player
    return p.stop()


class Service(object):
    '''Expose the complex methods of the VLC api
    to a python caller fit for a URI And service implementation
    '''
    def __init__(self):
        self.screens = {}
        self.last_uri = None

    def load(self, uri=None):
        """Load a file into an instance. If the instance
        does not ecist a new one is created and loaded"""
        self.get_player(uri)
        self.last_uri = uri
        return True

    def play(self, uri=None):
        u = uri or self.last_uri
        player = self.get_player(u)
        log('playing', u)
        player.play()
        return True

    def info(self, uri=None):
        u = uri or self.last_uri
        player = self.get_player(u)
        log('playing', u)
        r = {}

        methods = [
            # 'add_slave',
            # 'audio_get_channel',
            # 'audio_get_delay',
            # 'audio_get_mute',
            # 'audio_get_track',
            # 'audio_get_track_count',
            # 'audio_get_track_description',
            'audio_get_volume',
            # 'audio_output_device_enum',
            # 'audio_output_device_get',
            # 'audio_output_device_set',
            # 'audio_output_set',
            # 'audio_set_callbacks',
            # 'audio_set_channel',
            # 'audio_set_delay',
            # 'audio_set_format',
            # 'audio_set_format_callbacks',
            # 'audio_set_mute',
            # 'audio_set_track',
            # 'audio_set_volume',
            # 'audio_set_volume_callback',
            # 'audio_toggle_mute',
            'can_pause',
            # 'event_manager',
            # 'from_param',
            # 'get_agl',
            # 'get_chapter',
            # 'get_chapter_count',
            # 'get_chapter_count_for_title',
            'get_fps',
            #'get_full_chapter_descriptions',
            #'get_full_title_descriptions',
            'get_fullscreen',
            # 'get_hwnd',
            # 'get_instance',
            'get_length',
            'get_media',
            #'get_nsobject',
            'get_position',
            'get_rate',
            # 'get_role',
            'get_state',
            'get_time',
            'get_title',
            'get_title_count',
            # 'get_xwindow',
            # 'has_vout',
            'is_playing',
            'is_seekable',
            # 'navigate',
            # 'next_chapter',
            # 'next_frame',
            # 'pause',
            # 'play',
            # 'previous_chapter',
            # 'program_scrambled',
            # 'release',
            # 'retain',
            # 'set_agl',
            # 'set_android_context',
            # 'set_chapter',
            # 'set_equalizer',
            # 'set_evas_object',
            # 'set_fullscreen',
            # 'set_hwnd',
            # 'set_media',
            # 'set_mrl',
            # 'set_nsobject',
            # 'set_pause',
            # 'set_position',
            # 'set_rate',
            # 'set_renderer',
            # 'set_role',
            # 'set_time',
            # 'set_title',
            # 'set_video_title_display',
            # 'set_xwindow',
            # 'stop',
            # 'toggle_fullscreen',
            # 'toggle_teletext',
            # 'video_get_adjust_float',
            # 'video_get_adjust_int',
            # 'video_get_aspect_ratio',
            # 'video_get_chapter_description',
            'video_get_crop_geometry',
            'video_get_cursor',
            'video_get_height',
            # 'video_get_logo_int',
            # 'video_get_marquee_int',
            # 'video_get_marquee_string',
            'video_get_scale',
            'video_get_size',
            'video_get_spu',
            'video_get_spu_count',
            'video_get_spu_delay',
            'video_get_spu_description',
            'video_get_teletext',
            'video_get_title_description',
            'video_get_track',
            'video_get_track_count',
            'video_get_track_description',
            'video_get_width',
            # 'video_set_adjust_float',
            # 'video_set_adjust_int',
            # 'video_set_aspect_ratio',
            # 'video_set_callbacks',
            # 'video_set_crop_geometry',
            # 'video_set_deinterlace',
            # 'video_set_format',
            # 'video_set_format_callbacks',
            # 'video_set_key_input',
            # 'video_set_logo_int',
            # 'video_set_logo_string',
            # 'video_set_marquee_int',
            # 'video_set_marquee_string',
            # 'video_set_mouse_input',
            # 'video_set_scale',
            # 'video_set_spu',
            # 'video_set_spu_delay',
            # 'video_set_subtitle_file',
            # 'video_set_teletext',
            # 'video_set_track',
            # 'video_take_snapshot',
            # 'video_update_viewpoint',
            'will_play'
        ]

        for name in methods:
            r[name] = getattr(player, name)()

        return r

    def stop(self, uri=None):
        u = uri or self.last_uri
        player = self.get_player(u, create=False)
        log('Stop playing', u)

        player.stop()

        return True

    def get_player(self, uri, create=True):
        screen = self.get_screen(uri)
        log('player:', uri)

        player = screen.get('player', None)
        if player is None:
            if create is True:
                log('Creating Player')
                player = screen['instance'].media_player_new(uri)
                screen['player'] = player
                self.screens[uri] = screen
        return player

    def get_screen(self, uri):
        screen = self.screens.get(uri, None)
        if screen is None:
            screen = self.create_instance(uri)
            self.screens[uri] = screen
        return screen


    def create_instance(self, uri):
        '''Build a default instance, stored against the given
        'uri' or unique word
        '''
        log('Creating new screen instance', uri)
        instance = api.Instance()
        self.screens[uri] = {"instance": instance, "id": len(self.screens)}

        return self.screens[uri]
