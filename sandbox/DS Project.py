# %%
import pandas as pd

y1df = pd.read_csv("C:/Users/mpierre2/Downloads/McKenzy Pierre Freshman Year Soccer Game by Game Stats(Test).csv", skiprows=1)

y1df = y1df.drop(y1df.index[16:22])

y1df

# %%
y1df.info()

# %%
y1df.shape
y1df.columns
# %%
y1df["GS"] = (y1df["GP"] == "*").astype(int)
y1df["GS"].value_counts()

# %%
