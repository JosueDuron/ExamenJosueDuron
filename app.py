import streamlit as st
import numpy as np
from PIL import Image
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase
import av
import cv2
import tflite_runtime.interpreter as tflite

st.set_page_config(page_title="Clasificador de Imagenes IA")
st.title("Clasificador de Imagenes con IA")
st.markdown("Josue Elias Duron Miguel 202410010782")
st.write("Sube una imagen o activa la camara para identificar el objeto.")


@st.cache_resource
def cargar_modelo():
    interpreter = tflite.Interpreter(model_path="modelo_clasificador.tflite")
    interpreter.allocate_tensors()
    return interpreter


interpreter = cargar_modelo()
entrada_info = interpreter.get_input_details()
salida_info = interpreter.get_output_details()

nombres_clases = ['Avion', 'Auto', 'Pajaro', 'Gato', 'Ciervo',
                   'Perro', 'Rana', 'Caballo', 'Barco', 'Camion']


def predecir(img_array):
    img_resized = cv2.resize(img_array, (32, 32))
    img_norm = img_resized.astype('float32') / 255.0
    img_norm = np.expand_dims(img_norm, axis=0)

    interpreter.set_tensor(entrada_info[0]['index'], img_norm)
    interpreter.invoke()
    pred = interpreter.get_tensor(salida_info[0]['index'])

    clase = nombres_clases[np.argmax(pred)]
    confianza = np.max(pred)
    return clase, confianza


opcion = st.radio("Selecciona una opcion:", ["Camara en vivo", "Subir imagen"])

if opcion == "Camara en vivo":
    st.write("Apunta la camara hacia un objeto y la prediccion se mostrara sobre el video.")

    class Procesador(VideoProcessorBase):
        def recv(self, frame):
            img = frame.to_ndarray(format="bgr24")
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            clase, confianza = predecir(img_rgb)
            texto = f"{clase} ({confianza*100:.1f}%)"
            cv2.putText(img, texto, (20, 40), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 255, 0), 2, cv2.LINE_AA)
            return av.VideoFrame.from_ndarray(img, format="bgr24")

    webrtc_streamer(
        key="camara-live",
        video_processor_factory=Procesador,
        media_stream_constraints={"video": True, "audio": False},
    )

else:
    archivo = st.file_uploader("Sube una imagen", type=["jpg", "jpeg", "png"])
    if archivo:
        imagen = Image.open(archivo).convert('RGB')
        st.image(imagen, caption="Imagen cargada", use_container_width=True)

        clase, confianza = predecir(np.array(imagen))
        st.success(f"Prediccion: {clase}")
        st.info(f"Confianza: {confianza*100:.2f}%")
