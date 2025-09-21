# Generador de Cartas tipo Dobble 🎴

Aplicación web en **Streamlit** para generar mazos de cartas tipo *Dobble/Spot It!* a partir de imágenes.

## 🚀 Uso local

```bash
pip install -r requirements.txt
streamlit run app.py
```

Acceder en: http://localhost:8501

## 🐳 Uso con Docker

```bash
docker build -t dobble-generator .
docker run -d -p 8501:8501 dobble-generator
```

Acceder en: http://<ip-de-tu-servidor>:8501

## 📌 Funcionalidades
- Subida de imágenes desde el navegador.
- Generación de mazos válidos según matemáticas de Dobble.
- Selección del tamaño de las cartas (mm).
- Descarga en:
  - **ZIP** con todas las cartas en JPG.
  - **PDF A4** con las cartas acomodadas a tamaño real.
