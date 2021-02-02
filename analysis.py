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
       def do_arima():
             p = d = q = range(0, 2)
             pdq = list(itertools.product(p, d, q))
             seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]
             logger.info('Examples of parameter combinations for Seasonal ARIMA...')
             logger.info('SARIMAX: {} x {}'.format(pdq[1], seasonal_pdq[1]))
             logger.info('SARIMAX: {} x {}'.format(pdq[1], seasonal_pdq[2]))
             logger.info('SARIMAX: {} x {}'.format(pdq[2], seasonal_pdq[3]))
             logger.info('SARIMAX: {} x {}'.format(pdq[2], seasonal_pdq[4]))
             for param in pdq:
                 for param_seasonal in seasonal_pdq:
                   try:
                       mod = sm.tsa.statespace.SARIMAX(y,
                                            order=param,
                                            seasonal_order=param_seasonal,
                                            enforce_stationarity=False,
                                            enforce_invertibility=False)

                       results = mod.fit()

                       logger.info('ARIMA{}x{}12 - AIC:{}'.format(param, param_seasonal, 
                       results.aic))
                   except:
                        continue
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
       def validate_forecast(results):
            pred = results.get_prediction(start=pd.to_datetime('2021-01-22 04:25:52'), 
            dynamic=False)
            pred_ci = pred.conf_int()
            ax = y['2021-01-19 07:43:09':].plot(label='Observado')
            pred.predicted_mean.plot(ax=ax, label='One-step ahead Forecast',
            alpha=.4, figsize=(7, 4))
            ax.fill_between(pred_ci.index,
                            pred_ci.iloc[:, 0],
                            pred_ci.iloc[:, 1], color='k', alpha=.2)
            ax.set_xlabel('Tiempo')
            ax.set_ylabel('Temperatura')
            plt.plot()
            #plt.savefig(os.path.join(info_dir.static_folder,info_dir.images["validacion_forecast"]))           
            y_forecasted = pred.predicted_mean
            y_truth = y['2021-01-22 04:25:52':]
            mse = ((y_forecasted - y_truth) ** 2).mean()
            logger.info('The Mean Squared Error of our forecasts is {}'.format(round(mse, 2)))
            logger.info('The Root Mean Squared Error of our forecasts is {}'.format(round(np.sqrt(mse), 2)))


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
       do_arima()
       results=fit_arima_model()  
       validate_forecast(results)

if __name__=='__main__':
        do_analysis()
