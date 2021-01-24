import db
from weatherapi import WeatherApi
from models import Weather
from apscheduler.schedulers.background import BlockingScheduler
import json
from itbatools import get_itba_logger

logger=get_itba_logger("feeder",screen=False)

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

 
if __name__ == '__main__':        
          sched = BlockingScheduler()
          sched.add_job(load_table, 'interval', seconds =60)
          sched.start()

