# Seminario Itba

## Trabajo Práctico de la materio Seminario de Tópicos Avanzados de la Especialización en Ciencia de Datos.


### Funcionalidad:


Se descompone en **5 grandes bloques**, los cuales se mencionan a continuación:

#### Extracción: 
                
Consiste en  recuperar información asociada a la temperatura de la ciudad de **Hurlingham**, utilizando para ello la [**api OpenWeather**](
https://rapidapi.com/community/api/open-weather-map). Cabe destacar que por medio de este método los datos son sensados a intervalos regulares de tiempo (cada 30 minutos).

#### Carga:

Por cada registro recuperado durante la fase de extracción se lleva a cabo la inserción de los datos en la tabla **weather** de la base de datos **homónima** para su posterior análisis. 

#### Análisis:

Tomando como referencia a **ARIMA**, se realiza una descomposición de la serie de tiempo en: **tendencia**, **estacionalidad** y **residuos** , con sus 
correspondientes gráficos. 

#### Visualización:

Los gráficos generados en la instancia de análisis se disponibilizan por medio de un webserver cuyo 
puerto es susceptible de configuración.

#### Planificador o Scheduler:

Todos los items anteriores se encuentran gobernados por un **planificador** o **scheduler** sobre el cual se configuran los intervalos de ejecución de las etapas consideradas. 

| Fase                      | Planificación  |          
| --------------------------|:--------------:|
| Extracción y Carga        | Cada 30 minutos|       
| Análisis                  | L a V 00:00 hs |       
| Web Server (Visualización)| L a V 00:30 hs |       

Con respecto a la visualización, una de las tareas planificadas, a ejecutarse de forma autónoma, consiste en disponibilizar el web server para que el operador pueda acceder a los gráficos. Sin embargo esta acción que implica levantar el servicio puede ser realizada manualmente por el usuario. 

### Descripción de los componentes por fase:




