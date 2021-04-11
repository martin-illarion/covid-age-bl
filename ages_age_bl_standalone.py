import glob
import re
import csv
import requests
from datetime import date

today = date.today()

dat = today.strftime("%Y/%m/%d")

def mk_int(s):
    s = s.strip()
    return int(s) if s else 0

file="//home/ubuntu/ages_age/covid-age-bl/CovidFaelle_Altersgruppe.csv"

path="/home/ubuntu/ages_age/covid-age-bl/"

url = 'https://covid19-dashboard.ages.at/data/CovidFaelle_Altersgruppe.csv'
req = requests.get(url, allow_redirects=True)

url_content = req.content
csv_file = open(file, 'wb')

csv_file.write(url_content)
csv_file.close()

infected = {}
population = {}
dead = {}

bl=["Burgenland","Kärnten","Niederösterreich","Oberösterreich","Salzburg","Steiermark","Tirol","Vorarlberg","Wien","Österreich"]
for b in bl:
    infected[b]={}
    population[b]={}
    dead[b]={}

for b in bl:
    infected[b] = {}
    infected[b]["M"] = {}
    infected[b]["W"] = {}
    population[b] = {}
    population[b]["M"] = {}
    population[b]["W"] = {}
    dead[b] = {}
    dead[b]["M"] = {} 
    dead[b]["W"] = {}  
with open(file, newline='',encoding="utf-8") as csvfile:
    cov_reader = csv.DictReader(csvfile, delimiter=';')
    for row in cov_reader:
        #print(row["Anzahl"])
        bundesland = row["Bundesland"] 
        alter = row["Altersgruppe"]
        geschlecht = row["Geschlecht"]
        if geschlecht != "U":
            infected[bundesland][geschlecht][alter] = mk_int(row["Anzahl"])
            population[bundesland][geschlecht][alter] = mk_int(row["AnzEinwohner"])
            dead[bundesland][geschlecht][alter] = mk_int(row["AnzahlTot"])
        else:
            print("Geschlecht U gefunden. " + bundesland + " " + row["Anzahl"])

for b in bl:
    #print(b)
    hdr=True
    
    out_fl = path + b + ".csv"
    
    
    


    
    f = open(out_fl, "r")
    contents = f.readlines()
    f.close()
    
    with open(out_fl,"r+", encoding='utf-8') as csv_out:
        res_line = dat
        for age in population[b]["M"]:
            pop = population[b]["M"][age] + population[b]["W"][age]
            res_line += "," + str(pop)
        for age in infected[b]["M"]:
            inf = infected[b]["M"][age] + infected[b]["W"][age]
            res_line += "," + str(inf)
        for age in dead[b]["M"]:
            dea = dead[b]["M"][age] + dead[b]["W"][age]
            res_line += "," + str(dea)
        res_line += "\n"
        
        contents = csv_out.readlines()
        contents.insert(1, res_line)  # new_string should end in a newline
        csv_out.seek(0)  # readlines consumes the iterator, so we need to start over
        csv_out.writelines(contents)  # No need to truncate as we are increasing filesize

        
        #print(b + ": " + res_line)
        #csv_out.write(res_line)
        #hdr = False

