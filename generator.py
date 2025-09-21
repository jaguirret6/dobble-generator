import os
import random
from PIL import Image, ImageDraw, ImageOps

def generar_cartas(n):
    """Genera la estructura matemática de las cartas (plano proyectivo finito)."""
    cartas = []
    cartas.append([0] + [i + 1 for i in range(n)])
    for j in range(n):
        cartas.append([0] + [n + 1 + n * j + i for i in range(n)])
    for i in range(n):
        for j in range(n):
            cartas.append([i + 1] + [n + 1 + n * k + ((i * k + j) % n) for k in range(n)])
    return cartas

def redondear_icono(imagen, size):
    img = imagen.copy().convert("RGBA")
    img = ImageOps.fit(img, (size, size), Image.ANTIALIAS)
    mask = Image.new("L", (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size, size), fill=255)
    img.putalpha(mask)
    return img

def crear_carta(imagenes, indices, ancho, alto, icon_min, icon_max):
    carta = Image.new("RGBA", (ancho, alto), (255, 255, 255, 255))
    for idx in indices:
        size = random.randint(icon_min, icon_max)
        img = redondear_icono(imagenes[idx], size)
        x = random.randint(size // 2 + 20, ancho - size // 2 - 20)
        y = random.randint(size // 2 + 20, alto - size // 2 - 20)
        carta.paste(img, (x - img.size[0] // 2, y - img.size[1] // 2), img)
    return carta
