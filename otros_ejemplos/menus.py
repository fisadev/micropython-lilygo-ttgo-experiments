from time import sleep_ms
from random import randint, random, choice

from machine import Pin, SPI
import st7789
import vga1_8x16 as font

spi = SPI(1, baudrate=30000000, polarity=1, phase=1, sck=Pin(18), mosi=Pin(19))
display = st7789.ST7789(
    spi,
    135,
    240,
    reset=Pin(23, Pin.OUT),
    cs=Pin(5, Pin.OUT),
    dc=Pin(16, Pin.OUT),
    backlight=Pin(4, Pin.OUT),
    rotation=0,
)
display.init()

display.rotation(1)
screen_size = 240, 135
font_size = 8, 16
fps = 10

button1 = Pin(0, Pin.IN)
button2 = Pin(35, Pin.IN)
ON = 0
OFF = 1



class Screen:
    """
    A screen to be shown in the app.
    By default, it's able to draw something, to handle button presses, and to do something on each tick.
    """
    current = None

    default_background_color = st7789.BLACK
    default_text_color = st7789.GREEN

    def draw(self):
        display.fill(Screen.default_background_color)

    def do_button1(self):
        pass

    def do_button2(self):
        pass

    def step(self):
        self.handle_buttons()

    def handle_buttons(self):
        if button1.value() == ON:
            self.do_button1()

        if button2.value() == ON:
            self.do_button2()


class MenuOption:
    """
    An option inside a menu.
    """
    def __init__(self, text, action=None, color=None, menu=None, is_back=False, extra_data=None):
        self.text = text
        self.action = action
        self.color = color
        self.menu = menu
        self.is_back = is_back
        self.extra_data = extra_data


class Menu(Screen):
    """
    A menu that you can navigate and click options from.
    """
    def __init__(self, *options, selected_option_idx=0, parent=None, title=None):
        self.options = options
        self.selected_option_idx = selected_option_idx
        self.parent = parent
        self.title = title

        # update parents of sub menus
        for option in self.options:
            if option.menu is not None:
                option.menu.parent = self

    def draw(self):
        display.fill(Screen.default_background_color)

        if self.title is not None:
            display.text(font, self.title, 0, 0, Screen.default_text_color, Screen.default_background_color)
            options_start = font_size[1]
        else:
            options_start = 0

        for idx, option in enumerate(self.options):
            if idx == self.selected_option_idx:
                prefix = ">"
            else:
                prefix = " "

            display.text(font, prefix + option.text, 0, options_start + font_size[1] * idx, option.color or Screen.default_text_color, Screen.default_background_color)

    def do_button1(self):
        # next as default
        self.selected_option_idx += 1
        if self.selected_option_idx > len(self.options) - 1:
            self.selected_option_idx = 0
        self.draw()

    def do_button2(self):
        # click by default
        option = self.options[self.selected_option_idx]
        if option.menu:
            Screen.current = option.menu
            Screen.current.draw()
        elif option.is_back:
            self.go_back()
        elif option.action:
            option.action(self, option)

    def go_back(self):
        Screen.current = self.parent
        Screen.current.draw()


def on_text_color_click(menu, option):
    if Screen.default_text_color == option.extra_data:
        menu.go_back()
    else:
        Screen.default_text_color = option.extra_data
        Screen.current.draw()


def on_background_color_click(menu, option):
    if Screen.default_background_color == option.extra_data:
        menu.go_back()
    else:
        Screen.default_background_color = option.extra_data
        Screen.current.draw()


def on_defaults_click(menu, option):
    Screen.default_text_color = st7789.GREEN
    Screen.default_background_color = st7789.BLACK
    Screen.current.draw()


menu = Menu(
    MenuOption("Text color", menu=Menu(
        MenuOption("Green", on_text_color_click, extra_data=st7789.GREEN),
        MenuOption("Red", on_text_color_click, extra_data=st7789.RED),
        MenuOption("Blue", on_text_color_click, extra_data=st7789.BLUE),
        MenuOption("Black", on_text_color_click, extra_data=st7789.BLACK),
        MenuOption("White", on_text_color_click, extra_data=st7789.WHITE),
        MenuOption("Back", is_back=True),
        title="[ Text color ]",
    )),
    MenuOption("Background color", menu=Menu(
        MenuOption("Green", on_background_color_click, extra_data=st7789.GREEN),
        MenuOption("Red", on_background_color_click, extra_data=st7789.RED),
        MenuOption("Blue", on_background_color_click, extra_data=st7789.BLUE),
        MenuOption("Black", on_background_color_click, extra_data=st7789.BLACK),
        MenuOption("White", on_background_color_click, extra_data=st7789.WHITE),
        MenuOption("Back", is_back=True),
        title="[ Background color ]",
    )),
    MenuOption("Defaults", on_defaults_click),
)


Screen.current = menu
Screen.current.draw()

while True:
    Screen.current.step()
    sleep_ms(int(1000 / fps))


