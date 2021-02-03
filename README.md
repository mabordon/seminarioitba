# Seminario Itba

## Trabajo Práctico de la materia Seminario de Tópicos Avanzados de la Especialización en Ciencia de Datos.


### Funcionalidad:


Se descompone en **cuatro bloques**, los cuales se mencionan a continuación:

#### Extracción/Carga: 
                
Consiste en  recuperar información meteorológica de la ciudad de **Hurlingham**, utilizando para ello la [**api OpenWeather**](
https://rapidapi.com/community/api/open-weather-map). Cabe destacar que por medio de este método los datos son sensados a intervalos regulares de tiempo (cada 30 minutos). El json devuelto por el servicio presenta la siguiente forma:

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

En **models.py** podemos observar la entidad Weather que se mapea con la tabla homónima de la base de datos:

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
    print(response.text)
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

**Para el webserver se utiliza Flask e itbatools.py para obtener información de los directorios para recuperar los recursos (página index.html e imágenes)**

```python
from flask import Flask,render_template
from itbatools import get_dir_property_hook

webserver_info=get_dir_property_hook()


app = Flask(__name__,template_folder=webserver_info.templates,
                      static_folder=webserver_info.static_folder)

@app.route('/')
@app.route('/index')
def get_images():    
    return render_template("index.html", serie_temperaturas=f"{webserver_info.static_folder}/{webserver_info.images['serie_temperaturas']}",
                                         descomposicion=f"{webserver_info.static_folder}/{webserver_info.images['descomposicion']}",
                                         ajuste_normal=f"{webserver_info.static_folder}/{webserver_info.images['ajuste']}")


#Metodo para arrancar el webserver en el puerto 8000 que es el que esta configurado en wservconfig.json
def start_server():
    app.run(host="localhost",port=webserver_info.webserver_port)


if __name__=='__main__':
    start_server()
```

#### Planificador o Scheduler:

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

### Plataforma de ejecución:

* S.0: Windows 10 Home.
* Python: 3.6. 
* Anaconda Navigator: 1.10.
* Base de datos: PostgreSQL.

### Librerías python:



