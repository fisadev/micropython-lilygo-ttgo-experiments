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
screen = screen_width, screen_height
size = 10
color = st7789.GREEN
background = st7789.BLACK
movement = 0, 0
speed = 10
speed_decay = 0.3
position = randint(0, screen_width - size), randint(0, screen_height - size)
fps = 10

display.fill(background)

while True:
    display.fill_circle(position[0], position[1], size, background)

    new_movement = random() * choice((1, -1)), random() * choice((1, -1))
    movement = tuple(
        int((old * speed_decay + new * speed))
        for old, new in zip(movement, new_movement)
    )

    position = tuple(
        min(limit - size, max(0, pos + move))
        for pos, move, limit in zip(position, movement, screen)
    )

    display.fill_circle(position[0], position[1], size, color)

    sleep_ms(int(1000 / fps))



