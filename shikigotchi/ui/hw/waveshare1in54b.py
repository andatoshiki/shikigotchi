import logging

import shikigotchi.ui.fonts as fonts
from shikigotchi.ui.hw.base import DisplayImpl


class Waveshare154inchb(DisplayImpl):
    def __init__(self, config):
        super(Waveshare154inchb, self).__init__(config, 'waveshare1in54b')

    def layout(self):
        fonts.setup(10, 9, 10, 35, 25, 9)
        self._layout['width'] = 200
        self._layout['height'] = 200
        self._layout['face'] = (0, 40)
        self._layout['name'] = (5, 20)
        self._layout['channel'] = (0, 0)
        self._layout['aps'] = (28, 0)
        self._layout['uptime'] = (135, 0)
        self._layout['line1'] = [0, 14, 200, 14]
        self._layout['line2'] = [0, 186, 200, 186]
        self._layout['friend_face'] = (0, 92)
        self._layout['friend_name'] = (40, 94)
        self._layout['shakes'] = (0, 187)
        self._layout['mode'] = (170, 187)
        self._layout['status'] = {
            'pos': (5, 90),
            'font': fonts.status_font(fonts.Medium),
            'max': 20
        }
        return self._layout

    def initialize(self):
        logging.info("initializing waveshare v154 display")
        from shikigotchi.ui.hw.libs.waveshare.epaper.v1in54b.epd1in54b import EPD
        self._display = EPD()
        self._display.init()
        self._display.Clear()

    def render(self, canvas):
        buf = self._display.getbuffer(canvas)
        self._display.display(buf, None)

    def clear(self):
        self._display.Clear()
