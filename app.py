import streamlit as st
import zipfile
import io
from PIL import Image
from generator import generar_cartas, crear_carta
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader


VALORES_N = [2, 3, 5, 7, 11, 13]
DPI = 300
MM_TO_PX = DPI / 25.4

st.title("Generador de Cartas tipo Dobble 🎴")

imagenes_subidas = st.file_uploader(
    "Subí tus imágenes", accept_multiple_files=True, type=["png", "jpg", "jpeg"]
)

st.write("### Opciones disponibles")
st.table({
    "Imágenes por carta": [n+1 for n in VALORES_N],
    "Imágenes necesarias": [n**2 + n + 1 for n in VALORES_N],
    "Cartas totales": [n**2 + n + 1 for n in VALORES_N]
})

simbolos_por_carta = st.selectbox("Elegí imágenes por carta", [n+1 for n in VALORES_N])
N = simbolos_por_carta - 1
necesarias = N**2 + N + 1

st.write("### Tamaño de carta (en milímetros)")
ancho_mm = st.number_input("Ancho (mm)", value=61)
alto_mm = st.number_input("Alto (mm)", value=95)

ANCHO = int(ancho_mm * MM_TO_PX)
ALTO = int(alto_mm * MM_TO_PX)

if st.button("Generar mazo"):
    if not imagenes_subidas:
        st.error("Tenés que subir imágenes.")
    elif len(imagenes_subidas) < necesarias:
        st.error(f"Necesitás {necesarias} imágenes, pero subiste {len(imagenes_subidas)}.")
    else:
        # Cargar imágenes
        imagenes = [Image.open(img).convert("RGBA") for img in imagenes_subidas]
        cartas_idx = generar_cartas(N)
        cartas = [crear_carta(imagenes, indices, ANCHO, ALTO, 100, 180) for indices in cartas_idx]

        # 🔹 Generar ZIP con JPG
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as zf:
            for i, carta in enumerate(cartas):
                img_bytes = io.BytesIO()
                carta.convert("RGB").save(img_bytes, format="JPEG")
                zf.writestr(f"carta_{i+1}.jpg", img_bytes.getvalue())
        zip_buffer.seek(0)

        # 🔹 Generar PDF A4 respetando tamaño real
        pdf_buffer = io.BytesIO()
        c = canvas.Canvas(pdf_buffer, pagesize=A4)
        page_w, page_h = A4
        mm_to_pt = 72 / 25.4
        card_w = ancho_mm * mm_to_pt
        card_h = alto_mm * mm_to_pt
        cols = int(page_w // card_w)
        rows = int(page_h // card_h)
        margin_x = (page_w - cols * card_w) / 2
        margin_y = (page_h - rows * card_h) / 2

        for i, carta in enumerate(cartas):
            col = i % cols
            row = (i // cols) % rows
            x = margin_x + col * card_w
            y = page_h - margin_y - (row + 1) * card_h

            carta_rgb = carta.convert("RGB")
            img_reader = ImageReader(carta_rgb)
            c.drawImage(img_reader, x, y, width=card_w, height=card_h)

            if (i + 1) % (rows * cols) == 0:
                c.showPage()

        c.save()
        pdf_buffer.seek(0)

        st.success(f"✅ Se generaron {len(cartas)} cartas ({ancho_mm}×{alto_mm} mm).")
        st.download_button("📥 Descargar mazo en ZIP (JPG)", zip_buffer, "cartas.zip", "application/zip")
        st.download_button("📥 Descargar mazo en PDF (A4)", pdf_buffer, "cartas.pdf", "application/pdf")
