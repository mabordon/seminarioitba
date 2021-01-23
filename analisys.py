import pandas as pd
from db import engine
#hola


df = pd.read_sql_query("select * from weather", engine)
print(df)
