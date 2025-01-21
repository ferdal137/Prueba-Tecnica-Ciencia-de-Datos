# Predicción del Tipo de Alojamiento Preferido

Este repositorio contiene el desarrollo de la prueba técnica, enfocada en predecir el tipo de alojamiento preferido por los usuarios de un sistema de recomendaciones de viajes personalizadas. 

## Estructura del Repositorio

```
|-- Analisis_Principal.ipynb   # Notebook principal del análisis de datos               
|-- caso_prueba_ciencia_datos.pdf  # Descripción completa del caso de estudio
|
Chatbot/
    |-- Prompts de prueba.txt          # Archivo de pruebas para el chatbot
    |-- chatbot.py                     # Código principal del chatbot
    |-- config.py                      # Archivo con la API KEY de openai
    |-- graficas.py                    # Clase con los métodos para generar las gráficas
|
data/
    |-- TestDataAccomodation.csv  
    |-- train_data.csv             # Datos de entrenamiento en formato CSV
    |-- train_data.txt             # Datos de entrenamiento original en formato TXT
```

## Descripción de la Tarea

Se proporciona un conjunto de datos (`train_data.txt`) con los siguientes atributos:

- **id**: Identificador único del viaje.
- **durationOfStay**: Duración del viaje (en días).
- **gender**: Género de la persona que reservó.
- **age**: Edad de la persona que reservó (en años).
- **kids**: Indica si hay niños en el grupo de viaje (true/false).
- **destinationCode**: Código del país de destino.
- **acomType**: Tipo de alojamiento (departamento/hotel).

El objetivo principal es identificar patrones en las características del viajero y del viaje que permitan predecir el tipo de alojamiento preferido.

## Archivos Principales

- **Analisis_Principal.ipynb**: Notebook que contiene el análisis exploratorio de datos (EDA), el preprocesamiento y la implementación de modelos predictivos.
- **chatbot.py**: Script que implementa un chatbot para generar visualizaciones de forma automatica.
- **graficas.py**: Script que contiene la clase del Graficador con los métodos para generar los diferentes tipos de gráficas.
- **train_data.txt**: Datos originales de entrenamiento, que se procesan para el análisis.

