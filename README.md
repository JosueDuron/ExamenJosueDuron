# Clasificador de Imagenes con IA

**Nombre:** Josue Duron
**Numero de cuenta:** 202410010782
**Link:** https://examen-josueduron.streamlit.app/ 
**Repositorio:** https://github.com/JosueDuron/ExamenJosueDuron 
**Curso:** Computacion en la Nube
**Docente:** Ing. Asalia Zavala
**Universidad Tecnologica de Honduras (UTH)**

## Objetivo

Aplicacion web que utiliza un modelo de Machine Learning (red neuronal convolucional) entrenado en Google Colab para identificar objetos en imagenes, ya sea subiendo una foto o usando la camara en tiempo real.

## Que hace la app

La aplicacion permite:

- Subir una imagen desde el dispositivo y obtener la prediccion del objeto junto con el porcentaje de confianza.
- Activar la camara y ver la prediccion actualizarse en tiempo real mientras se apunta hacia un objeto.

## Clases que identifica el modelo

El modelo fue entrenado con el dataset CIFAR-10 y reconoce unicamente las siguientes 10 categorias:

- Avion
- Auto
- Pajaro
- Gato
- Ciervo
- Perro
- Rana
- Caballo
- Barco
- Camion

Nota: si se sube o se apunta la camara hacia un objeto que no pertenece a estas categorias (por ejemplo una persona o un libro), el modelo igual entregara una prediccion, pero sera incorrecta ya que solo conoce estas 10 clases.

## Como usarla

1. Ingresar a la URL publica de la aplicacion.
2. Elegir una de las dos opciones disponibles:
   - **Subir imagen:** seleccionar un archivo .jpg, .jpeg o .png desde el dispositivo.
   - **Camara en vivo:** activar la camara y apuntar hacia el objeto a identificar.
3. La aplicacion mostrara la clase predicha junto con el porcentaje de confianza.

## Tecnologias utilizadas

- **Google Colab**: entrenamiento del modelo de clasificacion de imagenes (CNN).
- **Dataset**: CIFAR-10 (cargado directamente desde tensorflow.keras.datasets).
- **TensorFlow Lite**: formato liviano del modelo para optimizar el uso de memoria en el despliegue.
- **Streamlit**: desarrollo de la interfaz web de la aplicacion.
- **Streamlit-WebRTC**: procesamiento de video en tiempo real para la deteccion en vivo con camara.
- **Streamlit Cloud**: despliegue publico de la aplicacion.

## Estructura del repositorio

```
.
├── app.py
├── modelo_clasificador.tflite
├── requirements.txt
└── README.md
```

## Proceso de entrenamiento (resumen)

1. Carga y normalizacion del dataset CIFAR-10.
2. Definicion de un modelo CNN con capas convolucionales, normalizacion por lotes y dropout.
3. Entrenamiento del modelo con el conjunto de entrenamiento y validacion con el conjunto de prueba.
4. Evaluacion de precision y perdida del modelo.
5. Conversion del modelo entrenado a formato .tflite para reducir su tamano y consumo de memoria.
6. Integracion del modelo en la aplicacion de Streamlit.

## URL de la aplicacion desplegada

[Agregar aqui la URL publica de Streamlit Cloud]
