import logging

import shikigotchi.ui.fonts as fonts
from shikigotchi.ui.hw.base import DisplayImpl


class Waveshare29bV3(DisplayImpl):
    def __init__(self, config):
        super(Waveshare29bV3, self).__init__(config, 'waveshare2in9b_v3')

    def layout(self):
        fonts.setup(10, 9, 10, 35, 25, 9)
        self._layout['width'] = 296
        self._layout['height'] = 128
        self._layout['face'] = (0, 40)
        self._layout['name'] = (5, 25)
        self._layout['channel'] = (0, 0)
        self._layout['aps'] = (28, 0)
        self._layout['uptime'] = (230, 0)
        self._layout['line1'] = [0, 14, 296, 14]
        self._layout['line2'] = [0, 112, 296, 112]
        self._layout['friend_face'] = (0, 96)
        self._layout['friend_name'] = (40, 96)
        self._layout['shakes'] = (0, 114)
        self._layout['mode'] = (268, 114)
        self._layout['status'] = {
            'pos': (130, 25),
            'font': fonts.status_font(fonts.Medium),
            'max': 28
        }
        return self._layout

    def initialize(self):
        logging.info("initializing waveshare V3 2.9 inch display")
        from shikigotchi.ui.hw.libs.waveshare.epaper.v2in9b_v3.epd2in9b_V3 import EPD
        self._display = EPD()
        self._display.init()
        self._display.Clear()
        self._display.init()

    def render(self, canvas):
        buf = self._display.getbuffer(canvas)
        self._display.display(buf, None)

    def clear(self):
        self._display.Clear()
