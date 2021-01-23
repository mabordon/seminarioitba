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