from fastapi import FastAPI, HTTPException

app = FastAPI()

lista: list[str]=[] 

@app.get("/todo")
async def lista_doto():
    return {"tood": lista}

@app.put("/todo")
async def dodaj_todo(co :str):
    lista.append(co)
    return {"messange": "ok"}

@app.delete("/todo")
async def usun_todo(co :str):
    if co in lista:
        lista.remove(co)
        return {"messange": "ok"}
    else:
        raise HTTPException(status_code=404, detail="item not found")


@app.get("/hello")
async def welcome(name: str):
    return {"messange": f"Welcome {name}"}






