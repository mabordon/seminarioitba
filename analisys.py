import pandas as pd
from db import engine

#df = pd.read_sql_query("select * from weather", engine)
#print(df)

### read dt and temperature colums from weather data base
### save querry to data frame "df_2"
df_2 = pd.read_sql_query("select weather.dt, weather.temperature from weather", engine)
#df_2 = pd.read_sql_query("select weather.temperature from weather", engine)
print(df_2)

### save querry to csv file
df_2.to_csv (r'C:\Users\juanm\OneDrive\Documents\Personal\1.Projects\4. Data Science - ITBA\9. Seminario\TP\seminarioitba2\export_dataframe.csv', index = False, header=True)

import warnings
import itertools
import numpy as np
import matplotlib.pyplot as plt
warnings.filterwarnings("ignore")
plt.style.use('fivethirtyeight')
import pandas as pd
import statsmodels.api as sm
import matplotlib
from statsmodels.tsa.seasonal import seasonal_decompose
from pylab import rcParams

matplotlib.rcParams['axes.labelsize'] = 5
matplotlib.rcParams['xtick.labelsize'] = 5
matplotlib.rcParams['ytick.labelsize'] = 5
matplotlib.rcParams['lines.linewidth'] = 1
matplotlib.rcParams['text.color'] = 'k'
matplotlib.rcParams['axes.titlesize'] = 12

df_2 = df_2.set_index('dt')
df_2.index

#print(df_2.index)

#juan = df_2['2021-01-21 21:06:30':]
#print(juan)

y = df_2['temperature']
y.plot(figsize=(15, 6))
plt.show()


from pylab import rcParams
rcParams['figure.figsize'] = 10, 10
decomposition = sm.tsa.seasonal_decompose(y, model='additive', period=43)
fig = decomposition.plot()
plt.show()

###########################
#Time series forecasting with ARIMA
##########################


p = d = q = range(0, 2)
pdq = list(itertools.product(p, d, q))
seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]

print('Examples of parameter combinations for Seasonal ARIMA...')
print('SARIMAX: {} x {}'.format(pdq[1], seasonal_pdq[1]))
print('SARIMAX: {} x {}'.format(pdq[1], seasonal_pdq[2]))
print('SARIMAX: {} x {}'.format(pdq[2], seasonal_pdq[3]))
print('SARIMAX: {} x {}'.format(pdq[2], seasonal_pdq[4]))


for param in pdq:
    for param_seasonal in seasonal_pdq:
        try:
            mod = sm.tsa.statespace.SARIMAX(y,
                                            order=param,
                                            seasonal_order=param_seasonal,
                                            enforce_stationarity=False,
                                            enforce_invertibility=False)

            results = mod.fit()

            print('ARIMA{}x{}12 - AIC:{}'.format(param, param_seasonal, 
            results.aic))
        except:
            continue

#AIC=201.67423123487916

###########
#Fitting the ARIMA model
###########

mod = sm.tsa.statespace.SARIMAX(y,
                                order=(1, 1, 1),
                                seasonal_order=(1, 1, 0, 12),
                                enforce_stationarity=False,
                                enforce_invertibility=False)
results = mod.fit()
print(results.summary().tables[1])


results.plot_diagnostics(figsize=(16, 8))
plt.show()

##################
# Validating forecasts
#################

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
plt.legend()

plt.show()

y_forecasted = pred.predicted_mean
y_truth = y['2021-01-22 04:25:52':]
mse = ((y_forecasted - y_truth) ** 2).mean()
print('The Mean Squared Error of our forecasts is {}'.format(round(mse, 2)))

print('The Root Mean Squared Error of our forecasts is {}'.format(round(np.sqrt(mse), 2)))


#########################
#Producing and visualizing forecasts
#########################

pred_uc = results.get_forecast(steps=220)
pred_ci = pred_uc.conf_int()

ax = y.plot(label='Observado', figsize=(7, 4))
pred_uc.predicted_mean.plot(ax=ax, label='Forecast')
ax.fill_between(pred_ci.index,
                pred_ci.iloc[:, 0],
                pred_ci.iloc[:, 1], color='k', alpha=.25)
ax.set_xlabel('Tiempo')
ax.set_ylabel('Temperatura')

plt.legend()
plt.show()