import pandas as pd
import warnings
import itertools
import numpy as np
import matplotlib.pyplot as plt
import os 
import pandas as pd
import statsmodels.api as sm
import matplotlib
from statsmodels.tsa.seasonal import seasonal_decompose
from pylab import rcParams
from pylab import rcParams
from db import engine
from itbatools import get_itba_logger, get_dir_property_hook

info_dir=get_dir_property_hook()
logger=get_itba_logger("analyzer",screen=True)
warnings.filterwarnings("ignore")
plt.style.use('fivethirtyeight')
matplotlib.rcParams['axes.labelsize'] = 5
matplotlib.rcParams['xtick.labelsize'] = 5
matplotlib.rcParams['ytick.labelsize'] = 5
matplotlib.rcParams['lines.linewidth'] = 1
matplotlib.rcParams['text.color'] = 'k'
matplotlib.rcParams['axes.titlesize'] = 12


def do_analysis():
       def descomponer():
            rcParams['figure.figsize'] = 10, 10
            decomposition = sm.tsa.seasonal_decompose(y, model='additive', period=43)
            fig = decomposition.plot()
            fig.savefig(os.path.join(info_dir.static_folder,info_dir.images["descomposicion"]))
       
       def fit_arima_model():
            mod = sm.tsa.statespace.SARIMAX(y,
                                order=(1, 1, 1),
                                seasonal_order=(1, 1, 0, 12),
                                enforce_stationarity=False,
                                enforce_invertibility=False)
            results = mod.fit()
            logger.info(results.summary().tables[1])
            results.plot_diagnostics(figsize=(16, 8))
            plt.savefig(os.path.join(info_dir.static_folder,info_dir.images["ajuste"]))
            plt.clf()
            return results
      
       df = pd.read_sql_query("select dt, temperature from weather", engine)
       logger.info(df)  
       df = df.set_index('dt')
       logger.info(df.index)
       y=df['temperature']
       x=df.index
       plt.plot(x,y)       
       plt.savefig(os.path.join(info_dir.static_folder,info_dir.images["serie_temperaturas"]))
       plt.clf()
       descomponer()    
       results=fit_arima_model()  
       

if __name__=='__main__':
        do_analysis()
