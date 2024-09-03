import logging

import shikigotchi.ui.fonts as fonts
from shikigotchi.ui.hw.base import DisplayImpl


class Waveshare4in37g(DisplayImpl):
    def __init__(self, config):
        super(Waveshare4in37g, self).__init__(config, 'waveshare4in37g')

    def layout(self):
        fonts.setup(10, 8, 10, 18, 25, 9)
        self._layout['width'] = 512
        self._layout['height'] = 368
        self._layout['face'] = (0, 43)
        self._layout['name'] = (0, 14)
        self._layout['channel'] = (0, 0)
        self._layout['aps'] = (0, 71)
        self._layout['uptime'] = (0, 25)
        self._layout['line1'] = [0, 12, 512, 12]
        self._layout['line2'] = [0, 116, 512, 116]
        self._layout['friend_face'] = (12, 88)
        self._layout['friend_name'] = (1, 103)
        self._layout['shakes'] = (26, 117)
        self._layout['mode'] = (0, 117)
        self._layout['status'] = {
            'pos': (65, 26),
            'font': fonts.status_font(fonts.Small),
            'max': 12
        }
        return self._layout

    def initialize(self):
        logging.info("initializing waveshare 4.37g inch lcd display")
        from shikigotchi.ui.hw.libs.waveshare.epaper.v4in37g.epd4in37g import EPD
        self._display = EPD()
        self._display.init()
        self._display.Clear()

    def render(self, canvas):
        buf = self._display.getbuffer(canvas)
        self._display.display(buf)

    def clear(self):
        self._display.Clear()
