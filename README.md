# Seminario Itba

## Trabajo Práctico de la materio Seminario de Tópicos Avanzados de la Especialización en Ciencia de Datos.


### Funcionalidad:


Se descompone en **cuatro bloques**, los cuales se mencionan a continuación:

#### Extracción/Carga: 
                
Consiste en  recuperar información asociada a la temperatura de la ciudad de **Hurlingham**, utilizando para ello la [**api OpenWeather**](
https://rapidapi.com/community/api/open-weather-map). Cabe destacar que por medio de este método los datos son sensados a intervalos regulares de tiempo (cada 30 minutos).

Por cada registro recuperado durante la extracción se lleva a cabo la inserción de los datos en la tabla **weather** de la base de datos **homónima** para su posterior análisis. 

| Archivo                   | Descripción                                                                  |          
| --------------------------|----------------------------------------------------------------------------- |
| weatherapi.py             | Clase utilizada para recuperar la información de la api.                     |       
| apiconfig.json            | Archivo Json de configuración de la api OpenWeather.                         |       
| dbconfig.json             | Archivo Json que cuenta con la cadena de conexión para la base de datos.     |     
| models.py y db.py         | Capa de persistencia contra la base de datos.                                |
| feeder.py                 | Utilizado para invocar a la api e insertar los registros en la base de datos.|         


#### Análisis:

Tomando como referencia a **ARIMA**, se realiza una descomposición de la serie de tiempo en: **tendencia**, **estacionalidad** y **residuos** , con sus 
correspondientes gráficos. 

| Archivo                   | Descripción                                                                                       |          
| --------------------------|---------------------------------------------------------------------------------------------------|
| analysis.py               | Realiza parte de la descomposición ARIMA: tendencia, estacionalidad y ruido. Genera los gráficos  |       


#### Visualización:

Los gráficos generados en la instancia de análisis se disponibilizan por medio de un webserver cuyo 
puerto es susceptible de configuración.

| Archivo                  | Descripción                                                                                                 |          
|--------------------------|------------------------------------------------------------------------------------------------------------ |
| webserver.py             | Es el webserver encargado de disponibilizar las imagenes generadas en la etapa de análisis.                 |       
| wservconfig.json         | Se trata del archivo de configuración del webserver.                                                        |       
| static                   | Es el directorio donde se almacenan los graficos generados en la fase de análisis.                          |     
| template                 | Es el directorio donde se encuentra el index.html que es la página sobre la cual se insertarán los gráficos.|




#### Planificador o Scheduler:

Todos los items anteriores se encuentran gobernados por un **planificador** o **scheduler** sobre el cual se configuran los intervalos de ejecución de las etapas consideradas. 

| Fase                      | Planificación  |          
| --------------------------|:--------------:|
| Extracción y Carga        | Cada 30 minutos|       
| Análisis                  | L a V 00:00 hs |       
| Web Server (Visualización)| L a V 00:30 hs |       

Con respecto a la visualización, una de las tareas planificadas, a ejecutarse de forma autónoma, consiste en disponibilizar el web server para que el operador pueda acceder a los gráficos. Sin embargo esta acción que implica levantar el servicio puede ser realizada manualmente por el usuario. 

| Archivo                   | Descripción                                                                                  |          
| --------------------------|--------------------------------------------------------------------------------------------- |
| starter.py                | Planifica las etapas del pipeline. Punto de entrada principal de ejecución para el operador. |  




