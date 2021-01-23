import pandas as pd
from db import engine

df = pd.read_sql_query("select * from weather", engine)
print(df)