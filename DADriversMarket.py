import json 
from collections import defaultdict
import sys 
import copy
def generador_preferencias(lista):
    i=0
    while i<len(lista):
        yield lista[i]
        i+=1

def get_index_of (driver,preferencias):
    result=sys.maxsize
    i=0
    while i<len(preferencias):
        if preferencias[i]==driver:
            result=i
            break
        i+=1
    return result


def get_index_driver (preferences,team,priority):
    result=sys.maxsize
    i=0
    while i<len(preferences):
        if preferences[i]["team"]==team and preferences[i]["driver_priority"]==priority :
            result=i
            break
        i+=1
    return result

def deferred_acceptance_drivers(drivers,teams):
    pending=list(drivers.keys())
    current_matchings={x:defaultdict(lambda:sys.maxsize) for x in teams.keys()}
    matchings={}
    unmatched=[]
    while len(pending)>0:
        desired_position=next(drivers[pending[0]],None)
        if (desired_position is not None):
            team=desired_position["team"]
            priority=desired_position["driver_priority"]
            index=get_index_of(pending[0],teams[team][priority])
            if current_matchings[team][priority]>index:
                if (current_matchings[team][priority]!=sys.maxsize):
                    pending.insert(1,teams[team][priority][current_matchings[team][priority]])
                current_matchings[team][priority]=index
                pending.pop(0)
        else:
             unmatched.append(pending.pop())
    for team,position in teams.items():
        dict_aux={}
        for x in position.keys():
            result="UNMATCHED"
            if (current_matchings[team][x]!=sys.maxsize):
                result=position[x][current_matchings[team][x]]
            dict_aux[x]=result
        matchings[team]=dict_aux
        ##matchings[team]={x:(position[x][current_matchings[team][x]] if current_matchings[team][x] >=0 else x:"UNMATCHED") for (x) in position.keys()}
    return matchings,unmatched

def deferred_acceptance_teams(teams,drivers):
    pending=[]
    aux={x:y.keys() for x,y in teams.items()}
    for x in aux.keys():
        for y in aux[x]:
            pending.append((x,y))
    for x,y in pending:
        teams[x][y]=generador_preferencias(teams[x][y])
    current_matchings=defaultdict(lambda:None)
    unmatched=[]
    while len(pending)>0:
        actual=pending[0]
        desired_position=next(teams[actual[0]][actual[1]],None)
        if (desired_position is not None):
            driver=desired_position
            index=get_index_driver(drivers[driver],actual[0],actual[1])
            if  not current_matchings[driver] or (current_matchings[driver] is not None and get_index_driver(drivers[driver],current_matchings[driver][0],current_matchings[driver][1])>index):
                if (current_matchings[driver]!=None):
                    pending.insert(1,current_matchings[driver])
                current_matchings[driver]=actual
                pending.pop(0)
        else:
            unmatched.append(pending.pop())
        ##matchings[team]={x:(position[x][current_matchings[team][x]] if current_matchings[team][x] >=0 else x:"UNMATCHED") for (x) in position.keys()}

    return current_matchings,unmatched

if __name__=="__main__":
    f=open("parameters.json")
    data=json.load(f)
    f.close()
    positions=data["sides"]["teams"]["roles"]
    matchings={x:[] for x in positions}
    teams_preferences= copy.deepcopy(data["preferences"]["teams"])
    drivers_preferences_drivers_side={x:generador_preferencias(y) for x,y in data["preferences"]["drivers"].items()}
    match_teams=deferred_acceptance_teams(teams_preferences,data["preferences"]["drivers"])
    teams_preferences= data["preferences"]["teams"]
    match_drivers=deferred_acceptance_drivers(drivers_preferences_drivers_side,teams_preferences)
    print(match_teams)
    print(match_drivers)
