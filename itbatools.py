import json

services={"apiweather":"apiconfig.json","dbweather":"dbconfig.json"}

class Service(type):
               __cls__={}
               def __call__(cls,*args,**kwargs):                     
                          service_type="{0}_{1}".format(cls.__name__,args[0])
                          print(service_type)
                          if service_type not in Service.__cls__:
                                       Service.__cls__[service_type]=type.__call__(cls,*args,**kwargs)
                          return Service.__cls__[service_type]

class PropertyHook(metaclass=Service):        
             def __init__(self,type): 
                         self.type=type                         
             def __load_properties(self,inifile):                
                  with open(inifile,'r') as file:                                     
                       self.__dict__=dict((json.load(file)).items())       
             @classmethod                
             def get_instance(cls,servicetype):
                       _instance=None         
                       if servicetype in services:            
                              _instance=PropertyHook(servicetype)
                              _instance.__load_properties(services[servicetype])
                       return _instance
             
def get_api_property_hook():
         return PropertyHook.get_instance("apiweather")                    

def get_db_property_hook():
         return PropertyHook.get_instance("dbweather")
