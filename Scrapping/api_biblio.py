from fastapi import FastAPI, HTTPException
from pandas import read_csv
from pandas import isna
import os
os.getcwd()

df=read_csv("./biblio.csv", sep=";")
app = FastAPI()

@app.get("/")
async def fil():
    return {"filie":df["Nr filii"].tolist()}


@app.get("/do")
async def filia(filia:str, telefon:bool, adres:bool,  email:bool):
    #return {"message": df["Nr filii"]}
    id=df["Nr filii"][df["Nr filii"]==filia]
    if len(id)!=1:
       raise HTTPException(status_code=404, detail="Nie znaleziono filii")
    wyn = df[df["Nr filii"]==filia]
    #return {"messange":wyn}
    res={}
    if telefon:
        if not(isna(wyn["Telefon"]).iloc[0]):
            res["Telefon"]=wyn["Telefon"].iloc[0]
        else:
            res["Telefon"]=""
    if adres:
        if not(isna(wyn["Adres"]).iloc[0]):
            res["Adres"]=wyn["Adres"].iloc[0]
        else:
            res["Adres"]=""
    if email:
        if not(isna(wyn["E-mail"]).iloc[0]):
            res["E-mail"]=wyn["E-mail"].iloc[0]
        else:
            res["E-mail"]=""
            
    return {"messange" : res}




