# Seminario Itba

## Trabajo Práctico de la materia Seminario de Tópicos Avanzados de la Especialización en Ciencia de Datos.


### Funcionalidad:


Se descompone en **cuatro bloques**, los cuales se mencionan a continuación:

#### Extracción/Carga: 
                
Consiste en  recuperar información asociada a la temperatura de la ciudad de **Hurlingham**, utilizando para ello la [**api OpenWeather**](
https://rapidapi.com/community/api/open-weather-map). Cabe destacar que por medio de este método los datos son sensados a intervalos regulares de tiempo (cada 30 minutos).

Por cada registro recuperado durante la extracción se lleva a cabo la inserción de los datos en la tabla **weather** de la base de datos **homónima** para su posterior análisis. 
**Los archivos empleados son los siguientes (se marca en negrita el ejecutable):**

| Archivo                   | Descripción                                                                  |          
| --------------------------|----------------------------------------------------------------------------- |
| weatherapi.py             | Clase utilizada para recuperar la información de la api.                     |       
| apiconfig.json            | Archivo Json de configuración de la api OpenWeather.                         |       
| dbconfig.json             | Archivo Json que cuenta con la cadena de conexión para la base de datos.     |     
| models.py y db.py         | Capa de persistencia contra la base de datos.                                |
| **feeder.py**             | Utilizado para invocar a la api e insertar los registros en la base de datos.|         
| itbatools.py              | Librería auxiliar.                                                           | 
| logs/feeder.log           | Log utilizado en las etapas de extracción y carga.                           |

#### Análisis:

Tomando como referencia a **ARIMA**, se realiza una descomposición de la serie de tiempo en: **tendencia**, **estacionalidad** y **residuos** , con sus 
correspondientes gráficos. **Los archivos empleados son los siguientes (se marca en negrita el ejecutable):**

| Archivo                   | Descripción                                                                             |          
| --------------------------|-----------------------------------------------------------------------------------------|
| **analysis.py**           | Realiza la descomposición ARIMA: tendencia, estacionalidad y ruido. Genera los gráficos.|       
| itbatools.py              | Librería auxiliar.                                                                      |
| logs/analyzer.log         | Log utilizado en la etapa de análisis.                                                  |

#### Visualización:

Los gráficos generados en la instancia de análisis se disponibilizan por medio de un webserver cuyo 
puerto es susceptible de configuración. **Los archivos empleados son los siguientes (se marca en negrita el ejecutable):**

| Archivo                  | Descripción                                                                                                 |          
|--------------------------|------------------------------------------------------------------------------------------------------------ |
| **webserver.py**         | Es el webserver encargado de disponibilizar las imágenes generadas en la etapa de análisis.                 |       
| wservconfig.json         | Se trata del archivo de configuración del webserver.                                                        |       
| static                   | Es el directorio donde se almacenan los gráficos generados en la fase de análisis.                          |     
| template                 | Es el directorio donde se encuentra el index.html que es la página sobre la cual se insertarán los gráficos.|
| itbatools.py             | Librería auxiliar.                                                                                          |




#### Planificador o Scheduler:

Todos los items anteriores se encuentran gobernados por un **planificador** o **scheduler** sobre el cual se configuran los intervalos de ejecución de las etapas consideradas. 

| Fase                      | Planificación  |          
| --------------------------|:--------------:|
| Extracción y Carga        | Cada 30 minutos|       
| Análisis                  | L a V 00:00 hs |       
| Web Server (Visualización)| L a V 00:30 hs |      

**Los archivos empleados son los siguientes (se marca en negrita el ejecutable):**

| Archivo                   | Descripción                                                                                  |          
| --------------------------|--------------------------------------------------------------------------------------------- |
| **starter.py**            | Planifica las etapas del pipeline. Punto de entrada principal de ejecución para el operador. |  


Con respecto a la visualización, una de las tareas planificadas, a ejecutarse de forma autónoma, consiste en disponibilizar el web server para que el operador pueda acceder a los gráficos. Sin embargo esta acción que implica levantar el servicio puede ser realizada manualmente por el usuario, a través de la ejecución del archivo **webserver.py**.

### Plataforma de ejecución:

* S.0: Windows 10 Home.
* Python: 3.6. 
* Anaconda Navigator: 1.10.
* Base de datos: PostgreSQL.





