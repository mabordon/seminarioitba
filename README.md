# Especialización en Ciencia de Datos ITBA

## Trabajo Práctico de la materia Seminario de Tópicos Avanzados.

### Integrantes:

| Nombre y Apellido         | DNI          |          
| --------------------------|:------------:|
| Maximiliano Bordón        |29.053.775    |       
| Juan Manuel Domínguez     |25.021.357    |       

**Tabla de Contenidos**   
1. [Breve descripción del proyecto](#id1)
2. [Diagrama](#id2)
3. [Funcionalidad](#id3)
   1. [Extracción-Transformación-Carga](#id3.1)
   2. [Análisis](#id3.2)
   3. [Visualización](#id3.3)
   4. [Planificador o Scheduler](#id3.4)
4. [Itba Tools](#id4)
5. [Plataforma de ejecución utilizada](#id5)
6. [Dependencias python](#id6)
7. [Bootstrap y JQuery](#id7)
8. [Instalación y puesta en marcha](#id8)
9. [Capturas de pantalla](#id9)

### Breve descripción del proyecto:<a name="id1"></a>

El proyecto consiste en tomar la información ,por medio de una api, de las condiciones meteorológicas asociadas a un punto arbitrario de buenos aires, en este caso [Hurlingham](https://es.wikipedia.org/wiki/Hurlingham) **(ciudad donde vive uno de los integrantes del equipo)**  y almacenarla en una base de datos, para luego generar una serie de tiempo tomando la temperatura y el horario de  medición, decomponiéndola en **tendencia**, **estacionalidad** y **residuos** (aclaramos que no se trata de un análisis **ARIMA** completo). Finalmente se disponibiliza un webserver que permite ver al operador los gráficos generados durante la etapa mencionada con anterioridad. Las fases consideradas del proceso se encuentran regidas por un **cron o scheduler**.

### Diagrama:<a name="id2"></a>

![Arquitectura](/capturas/arquitectura.jpeg "Arquitectura")

### Funcionalidad:<a name="id3"></a>


Se descompone en **cuatro bloques**, los cuales se mencionan a continuación:

#### Extracción-Transformación-Carga:<a name="id3.1"></a> 
                
Consiste en  recuperar información meteorológica de la ciudad de **Hurlingham**, utilizando para ello la [api OpenWeather](
https://rapidapi.com/community/api/open-weather-map). Cabe destacar que por medio de este método los datos son sensados a intervalos regulares de tiempo (cada 30 minutos). La invocación de la api se encuentra a cargo de ***weatherapi.py*** que por medio de **itbatools.py** recupera la configuración para hacer la llamada, según se ilustra a continuación:

```python
import requests
import json
from itbatools import get_api_property_hook
                

class WeatherApi:
          def __init__(self):
                    self._propertyhook=get_api_property_hook()                     
          def get_weather_info(self): 
                response = requests.request("GET", self._propertyhook.url, 
                                                   headers=self._propertyhook.headers, 
                                                   params=self._propertyhook.querystring)
                
                return response
```



El json devuelto por el servicio presenta la siguiente forma:

```javascript
{
    "coord": {
        "lon": -58.6391,
        "lat": -34.5883
    },
    "weather": [{
        "id": 802,
        "main": "Clouds",
        "description": "scattered clouds",
        "icon": "03n"
    }],
    "base": "stations",
    "main": {
        "temp": 19.88,
        "feels_like": 20.42,
        "temp_min": 19.44,
        "temp_max": 20.56,
        "pressure": 1012,
        "humidity": 83
    },
    "visibility": 10000,
    "wind": {
        "speed": 2.57,
        "deg": 160
    },
    "clouds": {
        "all": 40
    },
    "dt": 1612238761,
    "sys": {
        "type": 1,
        "id": 8232,
        "country": "AR",
        "sunrise": 1612257371,
        "sunset": 1612306821
    },
    "timezone": -10800,
    "id": 3433522,
    "name": "Hurlingham",
    "cod": 200
```
Se adjunta link para consultar el significado de los [campos devueltos en la llamada](https://openweathermap.org/current#parameter).

Por cada registro recuperado durante la extracción se lleva a cabo la inserción de los datos en la tabla **weather** de la base de datos **homónima** para su posterior análisis. 
La **transformación** aqui consiste en aplanar los niveles de anidamiento de la respuesta JSON al momento de trasladarla al **modelo entidad relación** y descartar ciertas entradas del response consideradas irrelevantas para el análisis posterior.

En **models.py** podemos observar como la entidad Weather se mapea con la tabla del mismo nombre en la base de datos:

```python
import db
from sqlalchemy import Column, Integer, String, Float,DateTime
from datetime import datetime

class Weather(db.Base):
       __tablename__='weather'
       id = Column(Integer, primary_key=True)
       weather=Column(String(60))
       temperature = Column(Float)
       tempmin=Column(Float)
       tempmax=Column(Float)
       feelslike=Column(Float)
       pressure=Column(Float)
       humidity=Column(Float)
       visibility=Column(Float)
       windspeed=Column(Float)
       winddeg=Column(Float)   
       cloudiness=Column(Float)
       dt=Column(DateTime)    
       def __init__(self,
                    weather,temperature,tempmin,tempmax,feelslike, 
                    pressure, humidity,visibility,windspeed,winddeg,
                    cloudiness,dt):
            self.weather=weather
            self.temperature=temperature
            self.tempmin=tempmin
            self.tempmax=tempmax
            self.feelslike=feelslike
            self.pressure=pressure
            self.humidity=humidity
            self.visibility=visibility
            self.windspeed=windspeed
            self.winddeg=winddeg        
            self.cloudiness=cloudiness
            self.dt=datetime.fromtimestamp(dt)
       def save(self):
               db.session.add(self)
               db.session.commit() 
       def __str__(self):
                 return self.weather
       __repr__=__str__
                    
       
db.Base.metadata.create_all(db.engine) 
```
La instrucción **db.Base.metadata.create_all(db.engine)** permite crear la tabla weather de forma automática sólo en el caso que no exista. 

Despues de la primera ejecución, si verificamos del lado de la BD observaremos que la tabla **weather** posee la siguiente forma:
```sql
CREATE TABLE public.weather
(
    id integer NOT NULL DEFAULT nextval('weather_id_seq'::regclass),
    weather character varying(60) COLLATE pg_catalog."default",
    temperature double precision,
    tempmin double precision,
    tempmax double precision,
    feelslike double precision,
    pressure double precision,
    humidity double precision,
    visibility double precision,
    windspeed double precision,
    winddeg double precision,
    cloudiness double precision,
    dt timestamp without time zone,
    CONSTRAINT weather_pkey PRIMARY KEY (id)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.weather
    OWNER to postgres;
```
Como se mencionó con antelación, la llamada a la api y la inserción de registros en la base de datos se realiza por medio del archivo **feeder.py**

```python
import db
from weatherapi import WeatherApi
from models import Weather
import json
from itbatools import get_itba_logger

logger=get_itba_logger("feeder",screen=True)

def load_table():
  try:    
    feeder=WeatherApi()
    response=feeder.get_weather_info() 
    data=json.loads(response.text)    
    weather=data["weather"][0]["main"]
    temperature = data["main"]["temp"]
    tempmin=data["main"]["temp_min"]
    tempmax=data["main"]["temp_max"]
    feelslike=data["main"]["feels_like"]
    pressure=data["main"]["pressure"]
    humidity=data["main"]["humidity"]
    visibility=data["visibility"]
    windspeed=data["wind"]["speed"]
    winddeg=data["wind"]["deg"]  
    cloudiness=data["clouds"]["all"]
    dt=data["dt"]
    w=Weather(weather,temperature,tempmin,tempmax,feelslike, 
                    pressure, humidity,visibility,windspeed,winddeg,
                    cloudiness,dt)
    w.save() 
    logger.info(f"Ejecutando la inserción de {response.text}")

  
  except Exception as e:
                      logger.error(e)

if __name__=='__main__':
         load_table()
```
La instrucción **logger=get_itba_logger("feeder",screen=True)** genera el log llamado feeder.log en el directorio logs. El flag screen determina si la información que se guarda en el log deberá mostrarse adicionalmente por pantalla cuando se encuentra configurado a True. En caso de estar configurado a False se omite salida por pantalla.

**Los archivos empleados durante la fase de extracción y carga son los siguientes (se marca en negrita el ejecutable):**

| Archivo                   | Descripción                                                                  |          
| --------------------------|----------------------------------------------------------------------------- |
| weatherapi.py             | Clase utilizada para recuperar la información de la api.                     |       
| apiconfig.json            | Archivo Json de configuración de la api OpenWeather.                         |       
| dbconfig.json             | Archivo Json que cuenta con la cadena de conexión para la base de datos.     |     
| models.py y db.py         | Capa de persistencia contra la base de datos.                                |
| **feeder.py**             | Utilizado para invocar a la api e insertar los registros en la base de datos.|         
| itbatools.py              | Librería auxiliar.                                                           | 
| logs/feeder.log           | Log utilizado en las etapas de extracción y carga.                           |


#### Análisis:<a name="id3.2"></a>

Tomando como referencia a **ARIMA**, se realiza una descomposición de la serie de tiempo en: **tendencia**, **estacionalidad** y **residuos** , con sus 
correspondientes gráficos. **Los archivos empleados son los siguientes (se marca en negrita el ejecutable):**

| Archivo                   | Descripción                                                                             |          
| --------------------------|-----------------------------------------------------------------------------------------|
| **analysis.py**           | Realiza la descomposición ARIMA: tendencia, estacionalidad y ruido. Genera los gráficos.|       
| itbatools.py              | Librería auxiliar.                                                                      |
| logs/analyzer.log         | Log utilizado en la etapa de análisis.                                                  |

#### Visualización:<a name="id3.3"></a> 

Los gráficos generados en la instancia de análisis se disponibilizan por medio de un webserver cuyo 
puerto es susceptible de configuración. **Los archivos empleados son los siguientes (se marca en negrita el ejecutable):**

| Archivo                  | Descripción                                                                                                 |          
|--------------------------|------------------------------------------------------------------------------------------------------------ |
| **webserver.py**         | Es el webserver encargado de disponibilizar las imágenes generadas en la etapa de análisis.                 |       
| wservconfig.json         | Se trata del archivo de configuración del webserver.                                                        |       
| static                   | Es el directorio donde se almacenan los gráficos generados en la fase de análisis.                          |     
| template                 | Es el directorio donde se encuentra el index.html que es la página sobre la cual se insertarán los gráficos.|
| itbatools.py             | Librería auxiliar.                                                                                          |

**Para el webserver se utiliza Flask e itbatools.py para obtener información de los directorios para recuperar los recursos (página index.html e imágenes)**

```python
from flask import Flask, render_template
from itbatools import get_dir_property_hook

webserver_info = get_dir_property_hook()


app = Flask(
    __name__,
    template_folder=webserver_info.templates,
    static_folder=webserver_info.static_folder,
)


@app.route("/")
@app.route("/index")
def get_images():
    return render_template(
        "index.html",
        serie_temperaturas=f"{webserver_info.static_folder}/{webserver_info.images['serie_temperaturas']}",
        descomposicion=f"{webserver_info.static_folder}/{webserver_info.images['descomposicion']}",
        ajuste_normal=f"{webserver_info.static_folder}/{webserver_info.images['ajuste']}",
    )


# Metodo para arrancar el webserver en el puerto 8000 que es el que esta configurado en wservconfig.json
def start_server():
    app.run(host="localhost", port=webserver_info.webserver_port)


if __name__ == "__main__":
    start_server()

```

#### Planificador o Scheduler:<a name="id3.4"></a> 

Todos los items anteriores se encuentran gobernados por un **planificador** o **scheduler** sobre el cual se configuran los intervalos de ejecución de las etapas consideradas. 

| Fase                      | Planificación  |          
| --------------------------|:--------------:|
| Extracción y Carga        | Cada 30 minutos|       
| Análisis                  | l a v 00:00 hs |       
| Web Server (Visualización)| l a v 00:30 hs |      

**Los archivos empleados son los siguientes (se marca en negrita el ejecutable):**

| Archivo                   | Descripción                                                                                  |          
| --------------------------|--------------------------------------------------------------------------------------------- |
| **starter.py**            | Planifica las etapas del pipeline. Punto de entrada principal de ejecución para el operador. |  

**El código es el siguiente:**

```python
from feeder import load_table
from apscheduler.schedulers.background import BlockingScheduler
from analysis import do_analysis
from webserver import start_server

if __name__ == '__main__':      
          sched = BlockingScheduler()          
          sched.add_job(load_table, 'interval', seconds =1800)
          sched.add_job(do_analysis,'cron',day_of_week='mon-fri',hour=00,minute=00)
          sched.add_job(start_server,'cron',day_of_week='mon-fri',hour=00,minute=30)
          sched.start()
```

Con respecto a la visualización, una de las tareas planificadas, a ejecutarse de forma autónoma, consiste en disponibilizar el web server (**start_server**) para que el operador pueda acceder a los gráficos. Sin embargo esta acción que implica levantar el servicio puede ser realizada manualmente por el usuario, a través de la ejecución del archivo **webserver.py**.

### Itba Tools:<a name="id4"></a>

Para este proyecto se diseño la librería llamada **itbatools.py** la cual es utilizada en todas las etapas del proceso.
Provee los siguientes recursos: 

* Loggers. Los archivos se guardan en el directorio */logs*
* Configuración de la *api open weather* 
* Configuración de *base de datos*
* Configuración del web server para mostrar los gráficos

**Para cada servicio se devuelve una única instancia de configuración empleando el patrón Singleton**

El código fuente es el siguiente: 

```python
import json
import sys
import logging
import os.path


services = {
    "weather_api": "apiconfig.json",
    "weather_db": "dbconfig.json",
    "ws_config": "wservconfig.json",
}


class Service(type):
    __cls__ = {}

    def __call__(cls, *args, **kwargs):
        service_type = "{0}_{1}".format(cls.__name__, args[0])
        if service_type not in Service.__cls__:
            Service.__cls__[service_type] = type.__call__(cls, *args, **kwargs)
        return Service.__cls__[service_type]


class PropertyHook(metaclass=Service):
    def __init__(self, type):
        self.type = type

    def __load_properties(self, inifile):
        with open(inifile, "r") as file:
            self.__dict__ = dict((json.load(file)).items())

    @classmethod
    def get_instance(cls, servicetype):
        _instance = None
        if servicetype in services:
            _instance = PropertyHook(servicetype)
            _instance.__load_properties(services[servicetype])
        return _instance


def get_api_property_hook():
    return PropertyHook.get_instance("weather_api")


def get_db_property_hook():
    return PropertyHook.get_instance("weather_db")


def get_dir_property_hook():
    return PropertyHook.get_instance("ws_config")


def get_itba_logger(logname, screen=False):
    def find_handler(handlername, isfile=False):
        if isfile:
            items = list(
                filter(
                    lambda x: os.path.basename(x.stream.name) == handlername, l.handlers
                )
            )
        else:
            items = list(filter(lambda x: x.stream.name == handlername, l.handlers))

        return len(items) > 0

    logging.basicConfig(level=logging.DEBUG, handlers=[])
    l = logging.getLogger(logname)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    if not find_handler("{0}.log".format(logname), isfile=True):

        file_handler = logging.FileHandler(filename="logs/{0}.log".format(logname))
        file_handler.setFormatter(formatter)
        l.handlers.append(file_handler)

    if screen and not find_handler("<stdout>"):

        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setFormatter(formatter)
        l.handlers.append(stdout_handler)

    return logging.getLogger(logname)
```

### Plataforma de ejecución utilizada:<a name="id5"></a>

* S.O: Windows 10 Home.
* Python: 3.6. 
* Anaconda Navigator: 1.10.
* Base de datos: PostgreSQL.

### Dependencias python:<a name="id6"></a>

Ver [requerimientos](requirements.txt)

### Bootstrap  y JQuery:<a name="id7"></a>

[Bootstrap 3.4.1](https://getbootstrap.com/docs/3.4/) y [JQuery 3.5.1](https://jquery.com/download/) son utilizados por la página **templates/index.html** que sirve los gráficos generados en el proceso.
```html
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script>
</head>
```


### Instalación y puesta en marcha:<a name="id8"></a>

* Instalar Postgres https://www.postgresql.org/download/
* Instalar Git Bash https://git-scm.com/downloads
* Instalar Anaconda https://www.anaconda.com/distribution/
* Crear en postgres la base de datos llamada weather. 
* Para comenzar con datos, pegue el script que figura en el directorio **scripts db/weather.sql** y ejecutelo sobre la query tool de pgadmin, posicionándose en la db anteriormente creada. Este script crea la tabla weather y la puebla.
* Clonar el proyecto desde gitbash console:
```shell
   git clone https://github.com/mabordon/seminarioitba.git
```

* Ejecutar Anaconda prompt

* Crear el entorno en el directorio del repositorio, con la siguiente instrucción:

```cmd
conda create --name seminario_itba --file requirements.txt
```

* Activar el entorno creado con:

```cmd
conda activate seminario_itba
```

* Puesta en marcha:

  Ir a la carpeta donde se descargo el repositorio y en la consola de anaconda ejecutar

```cmd
python starter.py
```

* Para probar cada componente por separado:

**ETL:**

Ir a la carpeta donde se descargo el repositorio y en la consola de anaconda ejecutar (con el entorno **seminario_itba** activo):

```cmd
python feeder.py
```

**Análisis:**

Ir a la carpeta donde se descargo el repositorio y en la consola de anaconda ejecutar (con el entorno **seminario_itba** activo):

```cmd
python analysis.py
```

**Visualización:**

Ir a la carpeta donde se descargo el repositorio y en la consola de anaconda ejecutar (con el entorno **seminario_itba** activo):

```cmd
python webserver.py
```
Luego acceder al browser en http://localhost:8000


### Capturas de pantalla:<a name="id9"></a>

![Web server main screen](/capturas/webserver_panel.JPG "Web server main screen")
![Serie de tiempo](/capturas/serie_de_tiempo.JPG "Serie de tiempo")
![Descomposición](/capturas/descomposicion_serie.JPG "Descomposición")
![Ajuste normal](/capturas/ajuste_normal.JPG "Ajuste normal")

