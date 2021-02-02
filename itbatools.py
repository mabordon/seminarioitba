import json
import sys
import logging
import os.path


services={"weather_api":"apiconfig.json","weather_db":"dbconfig.json","ws_config":"wservconfig.json"}

class Service(type):
               __cls__={}
               def __call__(cls,*args,**kwargs):                     
                          service_type="{0}_{1}".format(cls.__name__,args[0])                         
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
         return PropertyHook.get_instance("weather_api")                    

def get_db_property_hook():
         return PropertyHook.get_instance("weather_db")

def get_dir_property_hook():
         return PropertyHook.get_instance("ws_config")   

def get_itba_logger(logname,screen=False):    
          
          def find_handler(handlername,isfile=False): 
              if isfile:
                 items=list(filter(lambda x:os.path.basename(x.stream.name)==handlername,l.handlers))                 
              else:
                 items=list(filter(lambda x:x.stream.name==handlername,l.handlers))
              
              return len(items)>0                
             
          logging.basicConfig(level=logging.DEBUG,handlers=[])
          l= logging.getLogger(logname)    
          formatter=logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')         
          
          if not find_handler("{0}.log".format(logname),isfile=True): 
              
              file_handler = logging.FileHandler(filename="logs/{0}.log".format(logname))
              file_handler.setFormatter(formatter)            
              l.handlers.append(file_handler)  
              
          if screen and not find_handler("<stdout>"):

               stdout_handler = logging.StreamHandler(sys.stdout)
               stdout_handler.setFormatter(formatter)  
               l.handlers.append(stdout_handler)                  
   
          return logging.getLogger(logname)



