from time import sleep_ms
from random import randint, random, choice
from machine import Pin, SPI
import st7789
import vga1_8x8 as font

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
screen = 240, 135
background = st7789.WHITE
movement = 0, 0
speed = 5
speed_decay = 0.9
size = 40
position = randint(0, screen[0] - int(size / 2)), randint(0, screen[1] - int(size / 2))
fps = 10

display.fill(background)

button1 = Pin(0, Pin.IN)
button2 = Pin(35, Pin.IN)
ON = 0
OFF = 1

while True:
    if button1.value() == ON:
        background = st7789.color565(randint(0, 255), randint(0, 255), randint(0, 255))
    elif button2.value() == ON:
        background = st7789.WHITE
        display.fill(background)

    display.fill_circle(position[0] + int(size / 2), position[1] + int(size / 2), size, background)

    new_movement = random() * choice((1, -1)), random() * choice((1, -1))
    movement = tuple(
        int((old * speed_decay + new * speed))
        for old, new in zip(movement, new_movement)
    )

    position = tuple(
        min(limit - size, max(0, pos + move))
        for pos, move, limit in zip(position, movement, screen)
    )

    display.text(font, "Feliz", position[0], position[1], st7789.RED, background)
    display.text(font, "Navidad", position[0], position[1] + 10, st7789.GREEN, background)
    display.text(font, "Feli!", position[0], position[1] + 20, st7789.BLACK, background)

    sleep_ms(int(1000 / fps))



