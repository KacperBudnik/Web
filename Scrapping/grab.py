import requests
import json
import csv

respones=requests.get("http://127.0.0.1:8000/") # musi być uruchomione api_biblio.py (fastapi dev api_biblio.py)
filie = json.loads(respones.content)

#tmp=requests.get("http://127.0.0.1:8000/do?filia=47&telefon=true&adres=true&email=true")


with open('copy_biblio.csv', 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=["Nr filii", "Email", "telefon", "adress"])
    writer.writeheader()

    for fill in filie["filie"]:
        print(fill)
        tmp=json.loads(requests.get("http://127.0.0.1:8000/do?filia=" + fill + "&telefon=true&adres=true&email=true").content)
        print("Done")
        res={"Nr filii": fill, "Email": tmp["messange"]["E-mail"], "telefon":tmp["messange"]["Telefon"], "adress":tmp["messange"]["Adres"]}
        writer.writerow(res)

