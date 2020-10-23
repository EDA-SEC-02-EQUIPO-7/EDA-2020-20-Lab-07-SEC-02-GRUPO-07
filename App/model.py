"""
 * Copyright 2020, Departamento de sistemas y Computación
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 """
from math import radians, cos, sin, asin, sqrt ,degrees,atan2

import config
from DISClib.ADT import list as lt
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.DataStructures import listiterator as it
from DISClib.ADT import map as m
import datetime
assert config

"""
En este archivo definimos los TADs que vamos a usar,
es decir contiene los modelos con los datos en memoria

"""

# -----------------------------------------------------
# API del TAD Catalogo de accidentes
# -----------------------------------------------------

def newAnalyzer():
    """ Inicializa el analizador

    Crea una lista vacia para guardar todos los accidentes
    Se crean indices (Maps) por los siguientes criterios:
    -Fechas

    Retorna el analizador inicializado.
    """
    analyzer = {'accidents': None,
                'dateIndex': None
                }

    analyzer['accidents'] = lt.newList('SINGLE_LINKED', compareIds) #Creo que sería mejor array, pero si trabajamos con todos los datos son > 1 millon, entonces perdimos
    analyzer['dateIndex'] = om.newMap(omaptype='',
                                      comparefunction=compareDates)
    analyzer["timeIndex"]= om.newMap(omaptype='',
                                      comparefunction=compareHour)
    analyzer["coordIndex"]= om.newMap(omaptype='',
                                      comparefunction=comparebycoord)
    return analyzer



#===============================================
# Funciones para agregar informacion al catalogo
# Funciones para agregar informacion al catalogo
# Funciones para agregar informacion al catalogo
#===============================================



def AddAnAccident(analyzer, EachAccident):
    """
    """
    lt.addLast(analyzer['accidents'], EachAccident)
    updateDateIndex(analyzer['dateIndex'], EachAccident)
    updateTimeIndex(analyzer["timeIndex"], EachAccident)
    updateCoordIndex(analyzer["coordIndex"],EachAccident)
    return analyzer


def updateDateIndex(map, EachAccident):
    """
    Se toma la fecha del accidente y se busca si ya existe en el arbol
    dicha fecha.  Si es asi, se adiciona a su lista de accidentes
    y se actualiza el indice de tipos de accidentes.

    Si no se encuentra creado un nodo para esa fecha en el arbol
    se crea y se actualiza el indice de tipos de accidentes
    """
    occurreddate =EachAccident['Start_Time'] 
    AccidentDate = datetime.datetime.strptime(occurreddate, '%Y-%m-%d %H:%M:%S')
    entry = om.get(map, AccidentDate.date())
    if entry is None:
        datentry = newDataEntry(EachAccident)
        om.put(map, AccidentDate.date(), datentry)
    else:
        datentry = me.getValue(entry)
    addDate(datentry,EachAccident)
    return map


def updateCoordIndex(map,EachAccident):
    occurredCoord ={"lat":float(EachAccident["Start_Lat"]),"lon":float(EachAccident["Start_Lng"])}
    entry=om.get(map,occurredCoord)
    if entry is None:
        coordentry =newDataEntryBono(EachAccident)
        om.put(map,occurredCoord,coordentry)
    else:
        coordentry=me.getValue(entry)
    addCoord(coordentry,EachAccident)
    return map
def addCoord(coordentry,accident):
    lst=coordentry["lst"]
    lt.addLast(lst,accident)



def updateTimeIndex(map,EachAccident):
    """Si no se encuentra creado un nodo para esa Tiempos Hora Minuto en el arbol
    se crea y se actualiza el indice de tipos de accidentes
    """
    occurreddate = EachAccident['Start_Time'] 
    AccidentTime= datetime.datetime.strptime(occurreddate,  '%Y-%m-%d %H:%M:%S')
    AccidentTime=AccidentTime.replace(second=0)
    AccidentTime=compareTime(AccidentTime)
    entry = om.get(map, AccidentTime.time())
    if entry is None:
        datentry = newDataEntrySevetiry(EachAccident,AccidentTime)
        om.put(map, AccidentTime.time(), datentry)
    else:
        datentry = me.getValue(entry)
    addTime(datentry,EachAccident)
    return map


def addDate(datentry,accident):
    """
    Agrega un la fecha de un accidente y su ID al igual que un accidente 
    a la lista por estados
    """
    lst = datentry['lstAccidents']
    lt.addLast(lst,accident)
    existe = m.get(datentry['StateIndex'],accident["State"])
    if existe is not None:
        lst = me.getValue(existe)
        lt.addLast(lst,accident)
    else:
        accidents = lt.newList('SINGLE_LINKED', compareDates)
        m.put(datentry['StateIndex'],accident["State"],accidents)
        lt.addLast(accidents,accident)

def addTime(datentry,accident):
    """
    Agrega un la Hora  de un accidente y su ID al igual que un accidente 
    a la lista por Severidad
    """
    lst = datentry['lstAccidents']
    lt.addLast(lst,accident["ID"])
    existe = m.get(datentry['SeverityIndex'],accident["Severity"])
    if existe is not None:
        lst = me.getValue(existe)
        lt.addLast(lst,accident["ID"])
    else:
        accidents = lt.newList('SINGLE_LINKED', compareHour)
        m.put(datentry['SeverityIndex'],accident["Severity"],accidents)
        lt.addLast(accidents,accident["ID"])

def newDataEntry(accident):
    """
    Crea una entrada en el indice por fechas, es decir en el arbol
    binario.
    Se crea el indice por estado, por cada estado hay una lista 'SINGLE_LINKED'
    que guarda el "ID" de cada accidente en ese estado 
    """
    entry = {'StateIndex': None, 'lstAccidents': None, "occurreddate": accident['Start_Time']}
    entry['StateIndex'] = m.newMap(numelements=60,
                                     maptype='PROBING',
                                     comparefunction=CompareAccidentsState)
    accidents = lt.newList('SINGLE_LINKED', compareDates)
    m.put(entry['StateIndex'],accident["State"],accidents)
    entry['lstAccidents'] = lt.newList('SINGLE_LINKED', compareDates)
    return entry

def newDataEntrySevetiry(accident,occurredtime):
    """
    Crea una entrada en el indice por fechas, es decir en el arbol
    binario.
    Se crea el indice por estado, por cada estado hay una lista 'SINGLE_LINKED'
    que guarda el "ID" de cada accidente en ese estado 
    """
    entry = { "SeverityIndex": None, 'lstAccidents': None, "occurredtime": occurredtime}
    entry['SeverityIndex'] = m.newMap(numelements=12,
                                     maptype='PROBING',
                                     comparefunction=CompareAccidentsState)
    accidents = lt.newList('SINGLE_LINKED', compareHour)
    m.put(entry['SeverityIndex'],accident["Severity"],accidents)
    entry['lstAccidents'] = lt.newList('SINGLE_LINKED', compareHour)
    return entry

def newDataEntryBono(accident):
    entry={"lst":None}
    entry["lst"]=lt.newList("SINGLE_LINKED",comparebycoord)
    return entry



# ==============================
# Funciones de consulta RAPIDA
# Funciones de consulta RAPIDA
# Funciones de consulta RAPIDA
# ==============================


def crimesSize(analyzer):
    """
    Número de aacidentes en el catago
    """
    return lt.size(analyzer['accidents'])

def indexHeight(analyzer):
    """
    """
    return om.height(analyzer["dateIndex"])

def indexSize(analyzer):
    """
    """
    return om.size(analyzer["dateIndex"])

def minKey(analyzer):
    """
    """
    return om.minKey(analyzer["dateIndex"])

def maxKey(analyzer):
    """
    """
    return om.maxKey(analyzer["dateIndex" ])

# ==============================
# Funciones de Requerimientos
# ==============================

def bono(analyzer,coord,distance):
    rbt=analyzer['coordIndex']
    values = {"list":None,
                "map":None,
                "lunes":None,
                "martes":None,
                "miercoles":None,
                "jueves":None,
                "viernes":None,
                "sabado":None,
                "domingo":None}
    values["list"]=lt.newList('SINGLELINKED', rbt['cmpfunction'])
    values["map"]=m.newMap(numelements=14,
                                     maptype='PROBING',
                                     comparefunction=CompareAccidentsWeek)
    m.put(values["map"],0,0)
    m.put(values["map"],1,0)
    m.put(values["map"],2,0)
    m.put(values["map"],3,0)
    m.put(values["map"],4,0)
    m.put(values["map"],5,0)
    m.put(values["map"],6,0)
    print(lat(-distance,float(coord["lat"])))
    print(lat(distance,float(coord["lat"])))
    print("------------------------")
    values = valuesRangebono(rbt['root'], lat(-distance,float(coord["lat"])), lat(distance,float(coord["lat"])), values,coord,distance)
    values["lunes"]=me.getValue(m.get(values["map"],0))
    values["martes"]=me.getValue(m.get(values["map"],1))
    values["miercoles"]=me.getValue(m.get(values["map"],2))
    values["jueves"]=me.getValue(m.get(values["map"],3))
    values["viernes"]=me.getValue(m.get(values["map"],4))
    values["sabado"]=me.getValue(m.get(values["map"],5))
    values["domingo"]=me.getValue(m.get(values["map"],6))
    
    return values


def valuesRangebono(root, keylo, keyhi, values,coord,distance):
    if (root is not None):
        y=float((root["key"]["lat"]))
        z=float(root["key"]["lon"])
        x=float(coord["lat"])
        w=float(coord["lon"])
        if (root["key"]["lat"] > keylo):
            valuesRangebono(root['left'], keylo, keyhi, values,coord,distance)
        if (haversine(z,y,w,x)<=distance and root["key"]["lat"] > keylo and root["key"]["lat"] < keyhi):
            print(haversine(z,y,w,x))
            lstiterator=it.newIterator(root["value"]["lst"])
            while it.hasNext(lstiterator):
                eachaccident=it.next(lstiterator)
                lt.addLast(values["list"],eachaccident) 
                date= datetime.datetime.strptime(eachaccident["Start_Time"],  '%Y-%m-%d %H:%M:%S') 
                date.date()
                x=date.weekday()
                entry=m.get(values["map"],x)
                val=me.getValue(entry)
                m.put(values["map"],x ,val+1)
        if (root["key"]["lat"] < keyhi):
            valuesRangebono(root['right'], keylo, keyhi, values,coord,distance)
    return values


def getAccidentsByDate(analyzer,date):
    accident = om.get(analyzer["dateIndex"],date)
    lst =  me.getValue(accident)
    lst = lst['lstAccidents']
    accidents = lt.size(lst)
    return accidents
    
def getAccidentsByState(analyzer,initialDate,finalDate):
    """ 
    Crea un nuevo mapa para odenar los accidentes por estado aptovechando el ordenamiendo de Eachdate
    Se usa un mapa para que al momento de necesita una estado especifico la operacion de busqueda sea de O(1)
    a diferencia de otras estuccturas
    Cada que revisa una fecha especifica revisa si esta es la que tiene mas accidentes
    States es una lista que contiene todos los estados del archivo """
    comparador = 0
    comparadorDates = 0
    mayorState = None
    mayor = None
    accidents = om.values(analyzer['dateIndex'],initialDate,finalDate)
    lstiterator = it.newIterator(accidents)
    stateMap =  m.newMap(numelements=60,
                                     maptype='PROBING',
                                     comparefunction=CompareAccidentsState)
    states = ["AL", "AR", "AZ", "CA", "CO", "CT", "DC", "DE", "FL", "GA", "IA", "ID", "IL", "IN", "KS", "KY", "LA", "MA", "MD", "ME","MI", "MN", "MO", "MS", "MT", "NC", "ND", "NE", "NH", "NJ", "NM", "NV", "NY", "OH", "OK", "OR", "PA", "RI", "SC", "SD","TN", "TX", "UT", "VA", "VT", "WA", "WI", "WV", "WY"]
    for i in states:
        m.put(stateMap,i,0)
    while (it.hasNext(lstiterator)):
        eachdate = it.next(lstiterator)
        stateMapDate = eachdate["StateIndex"]
        accidents = eachdate['lstAccidents']
        accidents = lt.size(accidents)
        if accidents > comparadorDates:
            comparadorDates = accidents
            mayor = eachdate["occurreddate"]
        stateList = m.keySet(stateMapDate)
        stateIterator = it.newIterator(stateList)
        while (it.hasNext(stateIterator)):
            statename = it.next(stateIterator)
            numberAccidents = lt.size(me.getValue(m.get(stateMapDate,statename)))
            updateAccidets = me.getValue(m.get(stateMap,statename)) + numberAccidents
            m.put(stateMap,statename, updateAccidets)
            if updateAccidets > comparador:
                mayorState = statename
                comparador = updateAccidets
    return [mayor, mayorState]

def getAccidentsByTime(analyzer,initialTime,finalTime):
    accidents = om.values(analyzer['timeIndex'],initialTime,finalTime)
    lstiterator = it.newIterator(accidents)
    SeverityMap =  m.newMap(numelements=8,
                                     maptype='PROBING',
                                     comparefunction=CompareAccidentsState)
    for i in range(1,5):
        m.put(SeverityMap,str(i),0)
    while (it.hasNext(lstiterator)):
        eachtime = it.next(lstiterator)
        SeverityMapEachTime = eachtime["SeverityIndex"]
        accidents = eachtime['lstAccidents']
        accidents = lt.size(accidents)
        SeverityList = m.keySet(SeverityMapEachTime)
        SeverityIterator = it.newIterator(SeverityList)
        while (it.hasNext(SeverityIterator)):
            severityRange = it.next(SeverityIterator)
            ValueEachtime = lt.size(me.getValue(m.get(SeverityMapEachTime,severityRange)))
            ValueSeverity = (me.getValue(m.get(SeverityMap,severityRange)))
            numberAccidents = ValueEachtime + ValueSeverity
            m.put(SeverityMap,severityRange,numberAccidents)
    return SeverityMap

def getAccidentsBySeverity(Map,SeverityIndex):
    if m.get(Map,SeverityIndex) is not None:
        numberAccidents = me.getValue(m.get(Map,SeverityIndex))
    else:
        numberAccidents = 0
    return numberAccidents


#↓↓↓ Requerimiento 2 ↓↓↓
def getAccidentsBefore(analyzer, initialDate, finalDate):

    lst = om.values(analyzer['dateIndex'], initialDate, finalDate)
    lstiterator = it.newIterator(lst)
    Results = {}
    totalAccidents = 0
    Results["CantidadPorFecha"] = 0

    while (it.hasNext(lstiterator)):
        lstdate = it.next(lstiterator)      
        if lt.size(lstdate['lstAccidents']) > Results["CantidadPorFecha"]:
            Results["CantidadPorFecha"] = lt.size(lstdate['lstAccidents'])
            Results["FechaAccidentada"] = lstdate['occurreddate'][:10]

        totalAccidents += lt.size(lstdate['lstAccidents'])

    Results["totalAccidents"] = totalAccidents

    return Results



#requerimiento grupal
def getAccidentsbytime(analyzer,initial,final):
    return  None
 
def getAccidentsRange(analyzer, keylo, keyhi):
    rbt =analyzer['dateIndex']
    values = {"list":None,
                "map":None,
                "mayor":0,
                "category":""}
    
    values["list"]=lt.newList('SINGLELINKED', rbt['cmpfunction'])
    values["map"]=m.newMap(numelements=10,
                                     maptype='PROBING',
                                     comparefunction=CompareAccidentsState)
    values = valuesRangeA(rbt['root'], keylo, keyhi, values,
                                rbt['cmpfunction'])
    return values

def valuesRangeA(root, keylo, keyhi, values, cmpfunction):
    if (root is not None):
        complo = cmpfunction(keylo, root['key'])
        comphi = cmpfunction(keyhi, root['key'])
        if (complo < 0):
            valuesRangeA(root['left'], keylo, keyhi, values,
                        cmpfunction)
        if ((complo <= 0) and (comphi >= 0)):
            lstiterator=it.newIterator(root["value"]["lstAccidents"])
            while it.hasNext(lstiterator):
                eachaccident=it.next(lstiterator)
                lt.addLast(values["list"],eachaccident) 
                exist=m.contains(values["map"],eachaccident["Severity"] )
                if exist:
                    entry=m.get(values["map"],eachaccident["Severity"])
                    val=me.getValue(entry)
                    m.put(values["map"],eachaccident["Severity"] ,val+1)
                else:
                    m.put(values["map"],eachaccident["Severity"] ,1)
                entry=m.get(values["map"],eachaccident["Severity"])
                par=me.getValue(entry)
                if par>values["mayor"]:
                    values["mayor"]=par
                    values["category"]=me.getKey(entry)
        if (comphi > 0):
            valuesRangeA(root['right'], keylo, keyhi, values,
                        cmpfunction)
    return values
    
# ==============================
# Funciones de Comparacion
# ==============================

def compareIds(id1, id2):
    """
    Compara dos accidentes por su id
    """
    if (id1 == id2):
        return 0
    elif id1 > id2:
        return 1
    else:
        return -1


def compareDates(date1, date2):
    """
    Compara dos ids de accidentes, id es un identificador
    y entry una pareja llave-valor
    """
    if (date1 == date2):
        return 0
    elif (date1 > date2):
        return 1
    else:
        return -1
def compareHour(hour1, hour2):
    """
    Compara dos ids de accidentes, id es un identificador
    y entry una pareja llave-valor
    """
    if (hour1 == hour2):
        return 0
    elif (hour1 > hour2):
        return 1
    else:
        return -1
def compareTime(hora):
    if hora.minute>=0 and hora.minute<15:
        hora=hora.replace(minute=0)
    if hora.minute>=15 and hora.minute<30:
        hora=hora.replace(minute=30)
    if hora.minute>=30 and hora.minute<45:
        hora=hora.replace(minute=30)
    if hora.minute>=45 and hora.minute<=60:
        hora=hora.replace(minute=0)
        x=hora.hour+1
        x%=24
        hora=hora.replace(hour=x)
    return hora

    


def CompareAccidentsState(accident1, accident2):
    offense = me.getKey(accident2)
    if (accident1 == offense):
        return 0
    elif (accident1 > offense):
        return 1
    else:
        return -1
def CompareAccidentsWeek(accident1, accident2):
    offense = me.getKey(accident2)
    if (accident1 == offense):
        return 0
    elif (accident1 > offense):
        return 1
    else:
        return -1

def comparebycoord(coord1,coord2):
    if coord1["lat"]==coord2["lat"]:
        return 0
    if coord1["lat"]>coord2["lat"]:
        return 1
    else:
        return -1
        

def haversine(lon1, lat1, lon2, lat2):
    lon1=radians(lon1)
    lat1=radians(lat1)
    lon2=radians(lon2)   
    lat2=radians(lat2)
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 
    return c * r

def lat(d,lat1):
    R = 6371 #Radius of the Earth
    brng =0 #Bearing is 90 degrees converted to radians.
    lat1 =radians(lat1) #Current lat point converted to radians
    lat2 = asin( sin(lat1)*cos(d/R) +
         cos(lat1)*sin(d/R)*cos(brng))
    
    lat2 =degrees(lat2)
    return lat2

