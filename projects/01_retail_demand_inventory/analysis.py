import numpy as np, pandas as pd
from pathlib import Path
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split

OUT=Path(__file__).parent/"outputs"; OUT.mkdir(exist_ok=True)
rng=np.random.default_rng(42)
dates=pd.date_range("2025-01-05",periods=52,freq="W")
rows=[]
for store in range(12):
    for sku in range(20):
        base=rng.integers(20,90); price=rng.uniform(8,45)
        for i,d in enumerate(dates):
            promo=rng.binomial(1,.22); ad=rng.uniform(0,1); social=rng.uniform(0,1)
            trend=1+0.004*i
            demand=max(0,base*trend*(1+.35*promo+.18*ad+.12*social)+rng.normal(0,6))
            rows.append([d,store,sku,price,promo,ad,social,demand])
df=pd.DataFrame(rows,columns=["date","store","sku","price","promo","ad_score","social_score","demand"])
df["week"]=df["date"].dt.isocalendar().week.astype(int)
df["lag_1"]=df.groupby(["store","sku"]).demand.shift(1)
df["lag_4"]=df.groupby(["store","sku"]).demand.shift(4)
df=df.dropna()
features=["store","sku","price","promo","ad_score","social_score","week","lag_1","lag_4"]
train=df[df.date<"2025-11-01"]; test=df[df.date>="2025-11-01"]
model=RandomForestRegressor(n_estimators=150,max_depth=12,random_state=42,n_jobs=-1)
model.fit(train[features],train.demand); pred=model.predict(test[features])
mae=mean_absolute_error(test.demand,pred)
test["forecast"]=pred
test["safety_stock"]=1.65*test.groupby(["store","sku"]).demand.transform("std").fillna(5)
test["reorder_qty"]=(test.forecast*2+test.safety_stock).round().clip(lower=0)
test[["date","store","sku","demand","forecast","reorder_qty"]].to_csv(OUT/"forecast_recommendations.csv",index=False)
pd.DataFrame({"metric":["MAE","forecast_rows"],"value":[mae,len(test)]}).to_csv(OUT/"metrics.csv",index=False)
print(f"MAE={mae:.2f}; recommendations={len(test)}")