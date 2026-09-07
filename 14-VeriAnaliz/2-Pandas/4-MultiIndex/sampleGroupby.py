import numpy as np
import pandas as pd

dataset = {
        "Departman":["IT","İK","Muhasebe","Muhasebe","IT","İK"],
        "Çalışan": ["Ali","Elif","Selen","Zeynep","Şamil","Ahmet"],
        "Maaş":[6000,3500,4500,4500,8000,2000]
        }
 
print(dataset)
df = pd.DataFrame(dataset)
print(df)
bolGrup  = df.groupby("Departman")
print(bolGrup.sum())
bolumToplam = bolGrup.sum().loc["IT"]
print(bolumToplam)
print(bolGrup.count())
print(df.groupby("Departman").max())
print(df.groupby("Departman").min())
bolumOrt  = df.groupby("Departman").mean().loc["IT"]["Maaş"]
print(bolumOrt)