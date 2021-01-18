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


     
                     
    
                    


