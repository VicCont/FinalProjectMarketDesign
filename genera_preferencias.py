import random 
import json
import copy

f=open('parameters.json')
parametros=json.load(f)
f.close()
drivers=parametros["sides"]["drivers"]["names"]
aux=parametros["sides"]["teams"]["names"]
roles=['reserve', 'first', 'second']
res={}
for x in drivers:
     random.shuffle(aux)
     lista_aux=[]
     for y in aux:
             lista_aux.append({'driver_proirity':roles[random.randint(0,2)],'team':y})
     res[x]=lista_aux
json_cont=json.dumps(res)
parametros["preferences"]["drivers"]=res
f=open('prefs_equipos_drivers.json','w+')
f.write(json_cont)
f.close()
res={}
for x in aux:
     dict_aux={}
     for y in roles:
             random.shuffle(drivers)
             dict_aux[y]=drivers
     res[x]=dict_aux
jsoni=json.dumps(res)
parametros["preferences"]["teams"]=res
f=open('prefesteams.json','w+')
f.write(jsoni)
f.close()
f=open('parameters.json',"w+")
f.write(json.dumps(parametros,indent=4))
f.close()