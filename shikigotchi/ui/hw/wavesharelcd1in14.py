import logging

import shikigotchi.ui.fonts as fonts
from shikigotchi.ui.hw.base import DisplayImpl


class Wavesharelcd1in14(DisplayImpl):
    def __init__(self, config):
        super(Wavesharelcd1in14, self).__init__(config, 'wavesharelcd1in14')

    def layout(self):
        fonts.setup(10, 8, 10, 18, 25, 9)
        self._layout['width'] = 240
        self._layout['height'] = 135
        self._layout['face'] = (0, 43)
        self._layout['name'] = (0, 14)
        self._layout['channel'] = (0, 0)
        self._layout['aps'] = (0, 71)
        self._layout['uptime'] = (0, 25)
        self._layout['line1'] = [0, 12, 168, 12]
        self._layout['line2'] = [0, 116, 168, 116]
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
        logging.info("initializing waveshare 1.14 inch lcd display")
        from shikigotchi.ui.hw.libs.waveshare.lcd.lcdhat1in14.LCD_1inch14 import LCD_1inch14
        self._display = LCD_1inch14()
        self._display.Init()
        self._display.clear()
        self._display.bl_DutyCycle(50)

    def render(self, canvas):
        self._display.ShowImage(canvas)

    def clear(self):
        self._display.clear()
