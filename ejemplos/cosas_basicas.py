from time import sleep_ms
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


# Cosas que se pueden hacer con la pantalla:

# Pintar pantalla de color completo:
# display.fill(st7789.RED)

# Imprimir texto:
# display.text(fuente, texto, x, y, color_texto, color_fondo)
# Ej:
# import vga1_16x32 as font_grande
# display.text(font_grande, "Hola!", 10, 120, st7789.GREEN, st7789.RED)
# Más fuentes y colores listadas abajo

# Rotar la pantalla
# display.rotation(1)  # de 1 a 4 son las cuatro orientaciones posibles de la pantalla

# Pintar un pixel suelto:
# display.pixel(x, y, color)

# Dibujar líneas:
# display.line(x0, y0, x1, y1, color)  # en cualquier dirección
# display.hline(x, y, largo, color)  # horizontal
# display.vline(x, y, largo, color)  # vertical

# Dibujar rectángulos y círculos:
# display.rect(x, y, ancho, alto, color)  # solo bordes
# display.fill_rect(x, y, ancho, alto, color)  # relleno
# display.circle(x, y, radio, color)  # solo bordes
# display.fill_circle(x, y, radio, color)  # relleno

# Y usar imágenes! Pero es medio bardo:
# https://www.profetolocka.com.ar/2021/08/09/micropython-usando-la-placa-ttgo-t-display-de-lilygo-parte-3/

# Colores que se que existen:
# st7789.BLACK
# st7789.WHITE
# st7789.GREEN
# st7789.RED
# st7789.YELLOW
# st7789.BLUE
# (seguro hay más predeterminados)
# Y se puede crear cualquier color con RGB:
# st7789.color565(cantidad_rojo, cantidad_verde, cantidad_azul)  # las cantidades son números entre 0 y 255

# Fuentes que se pueden importar con "import nombre_de_la_fuente as bla"
# lista completa:
# vga1_16x16
# vga1_16x32
# vga1_8x16
# vga1_8x8
# vga1_bold_16x16
# vga1_bold_16x32
# vga2_16x16
# vga2_16x32
# vga2_8x16
# vga2_8x8
# vga2_bold_16x16
# vga2_bold_16x32
# vga_8x16
# vga_8x8

# Cosas que se pueden hacer con los botones:

# button1 = Pin(0, Pin.IN)
# button2 = Pin(35, Pin.IN)
# button1.value()  # devuelve 0 si está apretado, 1 si no está apretado (sí, al revés de lo esperable)
# button2.value()  # devuelve 0 si está apretado, 1 si no está apretado (sí, al revés de lo esperable)

# Otras cosas útiles:

# Esta función te devuelve qué tan largo es un texto, medido en pixeles. Útil para cosas dinámicas:
# display.write_len(fuente, texto)

# Y acá hay info sobre cosas como wifi, bus de serie, etc:
# https://docs.micropython.org/en/latest/esp32/quickref.html
