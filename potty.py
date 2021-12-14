import datetime
import matplotlib.pyplot as plt
import pandas as pd


# Parameters
n_days = 5

# Load data
df = pd.read_excel("data/potty.xlsx")

# Data Wrangling: Stack columns
df_stack = df.stack().reset_index()
df_stack.columns = ["index", "date", "time"]
df_stack["time_bin"] = pd.to_datetime(df_stack["time"], format="%H:%M:%S").dt.floor("30T").dt.strftime("%H:%M")
df_stack = df_stack[["date", "time_bin"]].copy()
if n_days:
    df_stack = df_stack[df_stack["date"] > datetime.datetime.today() - datetime.timedelta(days=5)]

# Get all time axis and join DataFrame
time_all = [x.strftime("%H:%M") for x in pd.date_range("2021-01-01", periods=48, freq="30T")]
df_time_all = pd.DataFrame(time_all, columns=["time_bin"])
df_all = pd.merge(df_stack, df_time_all, on="time_bin", how="outer")

df_group = df_all.groupby(["time_bin"])["date"].count().to_frame("potty_count").reset_index()
plt.Figure()
plt.bar(df_group["time_bin"], df_group["potty_count"])
plt.xticks(rotation="90")
plt.title(f"Bella Potty Schedule over {df_stack.date.nunique()} days")
plt.show()
