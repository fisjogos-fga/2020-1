import re

import pyxel
from pyxel.ui import Widget
from pyxel.ui.constants import INPUT_FIELD_COLOR, INPUT_TEXT_COLOR

RE_KEY = re.compile('KEY_(KP_)?.')


class Input(Widget):
    """
    Events:
        __on_press(): called when user press enter.
        __on_change(): called when input change. 
    """
    
    @property
    def callback(self):
        return self._callback

    @callback.setter
    def callback(self, value):
        if self._wrapped_callback:
            self.remove_event_handler("press", self._wrapped_callback)
        
        if value:
            self._wrapped_callback = lambda: value(self.data)
            self.add_event_handler("press", self._wrapped_callback)
        else:
            self._wrapped_callback = None
        self._callback = value

    def __init__(self, parent, x, y, size, data="", *, is_visible=True, is_enabled=True, callback=None, focus=True, text_transform=lambda st: st):
        width = pyxel.FONT_WIDTH * size + 4
        height = pyxel.FONT_HEIGHT + 2
        super().__init__(parent, x, y, width, height, is_visible=is_visible, is_enabled=is_enabled)
        
        self._callback = None
        self._wrapped_callback = None
        self.data = data
        self.size = size
        self.focus = focus
        self.text_transform = text_transform
        self.callback = callback
        self._btnp = lambda k: pyxel.btnp(k, 10, 5)
        self.keymap = {
            **{getattr(pyxel, k): k[-1] for k in dir(pyxel) if RE_KEY.fullmatch(k)},
            pyxel.KEY_SPACE: ' ',
            pyxel.KEY_QUOTE: '"',
            pyxel.KEY_COMMA: ",",
            pyxel.KEY_MINUS: "-",
            pyxel.KEY_PERIOD: ".",
            pyxel.KEY_SLASH: "/",
            pyxel.KEY_SEMICOLON: ";",
            pyxel.KEY_EQUAL: "=",
            pyxel.KEY_LEFT_BRACKET: "[",
            pyxel.KEY_BACKSLASH: "\\",
            pyxel.KEY_RIGHT_BRACKET: "]",
            pyxel.KEY_BACKQUOTE: "`",
            pyxel.KEY_KP_DECIMAL: ".",
            pyxel.KEY_KP_DIVIDE: "/",
            pyxel.KEY_KP_MULTIPLY: "*",
            pyxel.KEY_KP_SUBTRACT: "-",
            pyxel.KEY_KP_ADD: "+",
            pyxel.KEY_KP_EQUAL: "=",
        }
        self.shift_keymap = {
            **self.keymap,
            pyxel.KEY_0: ')',
            pyxel.KEY_1: '!',
            pyxel.KEY_2: '@',
            pyxel.KEY_3: '#',
            pyxel.KEY_4: '$',
            pyxel.KEY_5: '%',
            pyxel.KEY_6: '"',
            pyxel.KEY_7: '&',
            pyxel.KEY_8: '*',
            pyxel.KEY_9: '(',
            pyxel.KEY_QUOTE: '"',
            pyxel.KEY_COMMA: "<",
            pyxel.KEY_MINUS: "_",
            pyxel.KEY_PERIOD: ">",
            pyxel.KEY_SLASH: "?",
            pyxel.KEY_SEMICOLON: ":",
            pyxel.KEY_EQUAL: "+",
            pyxel.KEY_LEFT_BRACKET: "{",
            pyxel.KEY_BACKSLASH: "|",
            pyxel.KEY_RIGHT_BRACKET: "}",
            pyxel.KEY_BACKQUOTE: "´",
        }
        
        self.add_event_handler("draw", self.__on_draw)
        self.add_event_handler("update", self.__on_update)

    def __on_draw(self):
        pyxel.rect(self.x, self.y, self.width, self.height, INPUT_FIELD_COLOR)
        if self.focus or (pyxel.frame_count // 5) % 2:
            pyxel.text(self.x + 2, self.y + 1, self.data[-self.size:], INPUT_TEXT_COLOR)

    def __on_update(self):
        if self.focus:
            self._update_keys()

    def _update_keys(self):
        btnp = self._btnp

        if btnp(pyxel.KEY_ENTER) or pyxel.btnp(pyxel.KEY_KP_ENTER):
            self.call_event_handler('press')
        
        if btnp(pyxel.KEY_ESCAPE):
            self.focus = False
            return
        
        if btnp(pyxel.KEY_BACKSPACE):
            self.data = self.data[:-1]
        
        shift = pyxel.btn(pyxel.KEY_SHIFT)
        keymap = self.shift_keymap if shift else self.keymap

        for key, ch in keymap.items():
            if btnp(key):
                self.data = self.text_transform(self.data + ch)
                self.call_event_handler("change")
