from time import sleep_ms
from random import randint, random, choice
from machine import Pin, SPI
import st7789

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

display.rotation(2)
screen_height = 240
screen_width = 135
colors = (
    st7789.color565(0, 255, 0),
    st7789.color565(0, 200, 0),
    st7789.color565(0, 150, 0),
    st7789.color565(0, 100, 0),
    st7789.color565(0, 50, 0),
)
max_age = len(colors) - 1
background = st7789.BLACK
fps = 10
chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%&()[]+=?{}"
density = 2
import vga1_8x8 as font
font_height = 8
font_width = 8
rows_count = int(screen_height / font_height) - 2  # weird to need that -2
cols_count = int(screen_width / font_width)

display.fill(background)

def new_row():
    for _ in range(density):
        yield randint(0, cols_count - 1), 0, choice(chars), 0

actors = []

while True:
    #display.fill(background)

    actors.extend(
        (randint(0, cols_count - 1), 0, [choice(chars)])
        for _ in range(density)
    )

    new_actors = []

    for col, row, char_history in actors:
        age = len(char_history) - 1

        for char_age, char in enumerate(char_history):
            aged_row = row + 1 - char_age
            if row >= char_age and aged_row < rows_count:
                display.text(font, char, font_width * col, font_height * aged_row, colors[char_age], background)
        if age == max_age:
            display.fill_rect(font_width * col, font_height * (row - max_age), font_width, font_height, background)

        if row < rows_count + max_age:
            char_history.insert(0, choice(chars))
            if age == max_age:
                char_history.pop()
            new_actors.append((col, row + 1, char_history))

    actors = new_actors

    sleep_ms(int(1000 / fps))
