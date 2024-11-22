from fastapi import FastAPI, HTTPException
from pandas import read_csv
import os
os.getcwd()

df=read_csv("./biblio.csv", sep=";")
app = FastAPI()

@app.get("/do")
async def filia(filia:str, telefon:bool, adres:bool,  email:bool):
    if filia not in df["Nr filii"]:
        raise HTTPException(status_code=404, detail="Nie znaleziono filii")
    id_fill = df["Nr filii"]==filia
    res={}
    if telefon:
        res["Telefon"]=df["Telefon"][1]
    if adres:
        res["Adres"]=df["Adres"][1]
    if email:
        res["E-mail"]=df["E-mail"][1]
    return {"messange" : res}




