import streamlit as st
import numpy as np
from PIL import Image
import cv2
import tflite_runtime.interpreter as tflite
from camera_input_live import camera_input_live

st.set_page_config(page_title="Clasificador de Imagenes IA")
st.title("Clasificador de Imagenes con IA")
st.markdown("Josue Duron - 202410010782")
st.write("Sube una imagen o activa la camara en vivo para identificar el objeto.")


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

imagen = None

if opcion == "Camara en vivo":
    st.write("Apunta la camara hacia el objeto. La imagen y la prediccion se actualizan automaticamente.")
    foto = camera_input_live()
    if foto:
        imagen = Image.open(foto).convert('RGB')
else:
    archivo = st.file_uploader("Sube una imagen", type=["jpg", "jpeg", "png"])
    if archivo:
        imagen = Image.open(archivo).convert('RGB')

if imagen:
    clase, confianza = predecir(np.array(imagen))

    st.image(imagen, caption=f"Prediccion: {clase} ({confianza*100:.1f}%)", use_container_width=True)
    st.success(f"Prediccion: {clase}")
    st.info(f"Confianza: {confianza*100:.2f}%")