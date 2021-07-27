import glob
import re
import csv
import requests
from datetime import date
from datetime import datetime

today = date.today()

dat = today.strftime("%Y/%m/%d")

def mk_int(s):
    s = s.strip()
    return int(s) if s else 0

file="//home/ubuntu/ages_age/covid-age-bl/CovidFaelle_Altersgruppe.csv"
#WIN file="C:\\Users\\mpolak_cloudbees\\Dropbox\\python\\covid_github\\CovidFaelle_Altersgruppe.csv"

path="/home/ubuntu/ages_age/covid-age-bl/"
#WIN path="C:\\Users\\mpolak_cloudbees\\Dropbox\\python\\covid_github\\dest\\"

age_grps=["<5","5-14","15-24","25-34","35-44","45-54","55-64","65-74","75-84",">84"]

url = 'https://covid19-dashboard.ages.at/data/CovidFaelle_Altersgruppe.csv'
req = requests.get(url, allow_redirects=True)

url_content = req.content
csv_file = open(file, 'wb')

csv_file.write(url_content)
csv_file.close()

infected = {}
population = {}
dead = {}
# utf-8
with open(file, newline='',encoding="utf-8-sig") as csvfile:
    cov_reader = csv.DictReader(csvfile, delimiter=';')
    for row in cov_reader:
        #print(row["Anzahl"])
        bundesland = row["Bundesland"] 
        alter = row["Altersgruppe"]
        geschlecht = row["Geschlecht"]
        date_str = row["Time"]
        date_obj = datetime.strptime(date_str, "%d.%m.%Y %H:%M:%S")
        date = date_obj.strftime("%Y/%m/%d")
        if geschlecht != "U":
            if date not in infected:
                infected[date] = {}
                population[date] = {}
                dead[date] = {}
            if bundesland not in infected[date]:
                infected[date][bundesland] = {}
                population[date][bundesland] = {}
                dead[date][bundesland] = {}
            if geschlecht not in infected[date][bundesland]:
                infected[date][bundesland][geschlecht] = {}
                population[date][bundesland][geschlecht] = {}
                dead[date][bundesland][geschlecht] = {}
            infected[date][bundesland][geschlecht][alter] = mk_int(row["Anzahl"])
            population[date][bundesland][geschlecht][alter] = mk_int(row["AnzEinwohner"])
            dead[date][bundesland][geschlecht][alter] = mk_int(row["AnzahlTot"])
        else:
            print("Geschlecht U gefunden. " + bundesland + " " + row["Anzahl"])


set_hdr = True

for dat_i, inf_i in sorted(list(infected.items()), key=lambda x:x[0].lower(), reverse=True):
    for bl in infected[dat_i]:
        out_fl_full = path + bl + "_full.csv"
        out_fl = path + bl + ".csv"

        with open(out_fl,"a+", encoding='utf-8') as csv_out:
            if set_hdr:
                hdr = "date"
                hdr_full = "date"
                for ag in age_grps:
                    hdr += "," + "pop_" + ag
                    hdr_full += "," + "pop_m_" + ag + "," + "pop_w_" + ag
                for ag in age_grps:
                    hdr += "," + "inf_" + ag
                    hdr_full += "," + "inf_m_" + ag + "," + "inf_w_" + ag
                for ag in age_grps:
                    hdr += "," + "dea_" + ag
                    hdr_full += "," + "dea_m_" + ag + "," + "dea_w_" + ag
                hdr += "\n"
                hdr_full += "\n"
                csv_out.seek(0)
                csv_out.truncate()
                csv_out.write(hdr)
            line = dat_i
            line_full = dat_i
            for ag in age_grps:
                line += "," + str( population[dat_i][bl]["M"][ag]+population[dat_i][bl]["W"][ag] )
                line_full += "," + str( population[dat_i][bl]["M"][ag] ) + "," + str( population[dat_i][bl]["W"][ag] ) 
            for ag in age_grps:
                line += "," + str( infected[dat_i][bl]["M"][ag]+infected[dat_i][bl]["W"][ag] )
                line_full += "," + str( infected[dat_i][bl]["M"][ag] ) + "," + str( infected[dat_i][bl]["W"][ag] ) 
            for ag in age_grps:
                line += "," + str( dead[dat_i][bl]["M"][ag]+dead[dat_i][bl]["W"][ag] )
                line_full += "," + str( dead[dat_i][bl]["M"][ag] ) + "," + str( dead[dat_i][bl]["W"][ag] ) 
            line += "\n"
            line_full += "\n"
            csv_out.write(line)
        with open(out_fl_full,"a+", encoding='utf-8') as csv_out_full:
            if set_hdr:
                csv_out_full.seek(0)
                print("Set full to seek 0, set_hdr: " + str(set_hdr))
                csv_out_full.truncate()
                csv_out_full.write(hdr_full)
                set_hdr = False
            csv_out_full.write(line_full)
