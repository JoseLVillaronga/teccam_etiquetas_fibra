from PIL import Image, ImageDraw
from pathlib import Path

def create_label_icon(size: int) -> Image.Image:
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    scale = size / 64.0

    # 1. Sombra exterior difusa
    draw.rounded_rectangle(
        [7 * scale, 9 * scale, 57 * scale, 57 * scale],
        radius=max(1, int(6 * scale)),
        fill=(0, 0, 0, 35)
    )

    # 2. Cuerpo blanco de la etiqueta
    draw.rounded_rectangle(
        [6 * scale, 8 * scale, 56 * scale, 56 * scale],
        radius=max(1, int(6 * scale)),
        fill=(255, 255, 255, 255),
        outline=(27, 40, 93, 255),
        width=max(1, int(2.5 * scale))
    )

    # 3. Banda superior corporativa azul Teccam (#1b285d)
    header = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    hdraw = ImageDraw.Draw(header)
    hdraw.rounded_rectangle(
        [6 * scale, 8 * scale, 56 * scale, 56 * scale],
        radius=max(1, int(6 * scale)),
        fill=(27, 40, 93, 255)
    )
    # Máscara recortada a la parte superior
    mask = Image.new('L', (size, size), 0)
    ImageDraw.Draw(mask).rectangle([0, 0, size, int(20 * scale)], fill=255)
    img.paste(header, (0, 0), mask)

    # 4. Detalle decorativo rojo (#dc2626) y azul claro
    draw.rounded_rectangle(
        [11 * scale, 12 * scale, 24 * scale, 15 * scale],
        radius=max(1, int(1.5 * scale)),
        fill=(220, 38, 38, 255)
    )
    draw.ellipse(
        [48 * scale, 11.5 * scale, 52 * scale, 15.5 * scale],
        fill=(96, 165, 250, 255)
    )

    # 5. Código de barras (Code 39 simbólico)
    bars = [
        (11, 3.5), (16.5, 2), (20.5, 4.5), (27, 2),
        (31, 4), (37, 2), (41, 5), (48, 3)
    ]
    for x, w in bars:
        draw.rectangle(
            [x * scale, 25 * scale, (x + w) * scale, 44 * scale],
            fill=(27, 40, 93, 255)
        )

    # 6. Metadatos inferiores de la etiqueta
    draw.rounded_rectangle(
        [11 * scale, 47.5 * scale, 51 * scale, 50.5 * scale],
        radius=max(1, int(scale)),
        fill=(100, 116, 139, 255)
    )

    return img

def main():
    root = Path(__file__).resolve().parent.parent
    static_dir = root / 'app' / 'static'
    img_dir = static_dir / 'img'

    sizes = [16, 32, 48, 64]
    icons = [create_label_icon(s) for s in sizes]

    # Guardar app/static/favicon.ico multi-resolución
    ico_path = static_dir / 'favicon.ico'
    icons[0].save(ico_path, format='ICO', sizes=[(s, s) for s in sizes], append_images=icons[1:])
    print(f'[OK] Generado favicon.ico en: {ico_path}')

    # Guardar app/static/img/favicon.png de alta resolución (64x64)
    png_path = img_dir / 'favicon.png'
    icons[-1].save(png_path, format='PNG')
    print(f'[OK] Generado favicon.png en: {png_path}')

if __name__ == '__main__':
    main()
