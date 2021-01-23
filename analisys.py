import pandas as pd
from db import engine
#hola
#hola 2


df = pd.read_sql_query("select * from weather", engine)
print(df)
