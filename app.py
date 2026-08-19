import streamlit as st
import numpy as np
from tensorflow.keras.models import load_model
from PIL import Image
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase
import av
import cv2

st.set_page_config(page_title="Clasificador de Imágenes IA", page_icon="")

st.title("🧠 Clasificador de Imágenes con IA")
st.markdown("Josue Elias Duron Miguel 202410010782")

@st.cache_resource
def cargar_modelo():
    return load_model('modelo_clasificador.h5')

modelo = cargar_modelo()

nombres_clases = ['Avión', 'Auto', 'Pájaro', 'Gato', 'Ciervo',
                   'Perro', 'Rana', 'Caballo', 'Barco', 'Camión']

def predecir(img_array):
    """Recibe un array RGB de cualquier tamaño y devuelve clase + confianza"""
    img_resized = cv2.resize(img_array, (32, 32))
    img_norm = img_resized.astype('float32') / 255.0
    img_norm = np.expand_dims(img_norm, axis=0)
    pred = modelo.predict(img_norm, verbose=0)
    clase = nombres_clases[np.argmax(pred)]
    confianza = np.max(pred)
    return clase, confianza

opcion = st.radio("Selecciona una opción:", ["📷 Cámara en vivo", "📁 Subir imagen"])

# ---------- OPCIÓN 1: CÁMARA EN VIVO (predicción en caliente) ----------
if opcion == "📷 Cámara en vivo":
    st.write("Apunta la cámara hacia un objeto y la predicción se mostrará sobre el video.")

    class Procesador(VideoProcessorBase):
        def recv(self, frame):
            img = frame.to_ndarray(format="bgr24")

            # Convertir a RGB para el modelo
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            clase, confianza = predecir(img_rgb)

            # Dibujar el texto de la predicción sobre el frame
            texto = f"{clase} ({confianza*100:.1f}%)"
            cv2.putText(img, texto, (20, 40), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 255, 0), 2, cv2.LINE_AA)

            return av.VideoFrame.from_ndarray(img, format="bgr24")

    webrtc_streamer(
        key="camara-live",
        video_processor_factory=Procesador,
        media_stream_constraints={"video": True, "audio": False},
    )

# ---------- OPCIÓN 2: SUBIR IMAGEN ----------
else:
    archivo = st.file_uploader("Sube una imagen", type=["jpg", "jpeg", "png"])
    if archivo:
        imagen = Image.open(archivo).convert('RGB')
        st.image(imagen, caption="Imagen cargada", use_column_width=True)

        clase, confianza = predecir(np.array(imagen))
        st.success(f"### Predicción: {clase}")
        st.info(f"Confianza: {confianza*100:.2f}%")