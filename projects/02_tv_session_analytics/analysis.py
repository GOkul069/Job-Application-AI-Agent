import numpy as np,pandas as pd
from pathlib import Path
OUT=Path(__file__).parent/"outputs"; OUT.mkdir(exist_ok=True)
rng=np.random.default_rng(7); n=300000
start=pd.Timestamp("2025-01-01")+pd.to_timedelta(rng.integers(0,90*24*60,n),unit="m")
df=pd.DataFrame({"session_id":np.arange(n),"user_id":rng.integers(1,50000,n),"channel":rng.integers(1,121,n),"start":start})
df["duration_min"]=np.clip(rng.gamma(2.5,24,n),2,360)
df["end"]=df.start+pd.to_timedelta(df.duration_min,unit="m")
df["hour"]=df.start.dt.hour; df["is_peak"]=df.hour.between(18,21)
summary=df.groupby(["channel","is_peak"]).agg(sessions=("session_id","count"),avg_duration=("duration_min","mean"),unique_users=("user_id","nunique")).reset_index()
summary.to_csv(OUT/"channel_summary.csv",index=False)
kpi=pd.DataFrame({"metric":["sessions","unique_users","avg_duration_min","peak_share"],"value":[len(df),df.user_id.nunique(),df.duration_min.mean(),df.is_peak.mean()]})
kpi.to_csv(OUT/"kpis.csv",index=False)
print(kpi.to_string(index=False))