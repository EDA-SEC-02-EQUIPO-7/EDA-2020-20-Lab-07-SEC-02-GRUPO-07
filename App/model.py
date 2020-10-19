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
    analyzer["hourIndex"]= om.newMap(omaptype='',
                                      comparefunction=compareHour)
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
    updateTimeIndex(analyzer["hourIndex"], EachAccident)
    return analyzer


def updateDateIndex(map, EachAccident):
    """
    Se toma la fecha del accidente y se busca si ya existe en el arbol
    dicha fecha.  Si es asi, se adiciona a su lista de accidentes
    y se actualiza el indice de tipos de accidentes.

    Si no se encuentra creado un nodo para esa fecha en el arbol
    se crea y se actualiza el indice de tipos de accidentes
    """
    occurreddate = str(EachAccident['Start_Time'] )
    AccidentDate = datetime.datetime.strptime(occurreddate, '%Y-%m-%d %H:%M:%S')
    entry = om.get(map, AccidentDate.time())
    if entry is None:
        datentry = newDataEntry(EachAccident)
        om.put(map, AccidentDate.date(), datentry)
    else:
        datentry = me.getValue(entry)
    addDate(datentry,EachAccident)
    # Por cada accidente que agrega se acualiza el estado
    # Para hacer mas facil la busqueda del Req 4 
    lstAccidents = m.get(datentry['StateIndex'],EachAccident["State"])
    lstAccidents = me.getValue(lstAccidents)
    mayor = lt.size(lstAccidents)
    comparador = 0
    if mayor > comparador:
        datentry["Mayor"] = EachAccident["State"]
        comparador = mayor
    return map
def updateTimeIndex(map,EachAccident):
    """Si no se encuentra creado un nodo para esa Tiempos Hora Minuto en el arbol
    se crea y se actualiza el indice de tipos de accidentes
    """
    occurreddate = EachAccident['Start_Time'] 
    AccidentDate = datetime.datetime.strptime(occurreddate,  '%Y-%m-%d %H:%M:%S')
    print(AccidentDate.time())
    entry = om.get(map, AccidentDate.date())
    if entry is None:
        datentry = newDataEntry(EachAccident)
        om.put(map, AccidentDate.date(), datentry)
    else:
        datentry = me.getValue(entry)
    addDate(datentry,EachAccident)
    return map


def addDate(datentry,accident):
    """
    Agrega un la fecha de un accidente y su ID al igual que un accidente 
    a la lista por estados
    """
    lst = datentry['lstAccidents']
    lt.addLast(lst,accident)#["ID"])
    existe = m.get(datentry['StateIndex'],accident["State"])
    if existe is not None:
        lst = me.getValue(existe)
        lt.addLast(lst,accident)#['ID'])
    else:
        accidents = lt.newList('SINGLE_LINKED', compareDates)
        m.put(datentry['StateIndex'],accident["State"],accidents)
        lt.addLast(accidents,accident)#["ID"])

def newDataEntry(accident):
    """
    Crea una entrada en el indice por fechas, es decir en el arbol
    binario.
    Se crea el indice por estado, por cada estado hay una lista 'SINGLE_LINKED'
    que guarda el "ID" de cada accidente en ese estado 
    """
    entry = {'StateIndex': None, 'lstAccidents': None, "Mayor": None}
    entry['StateIndex'] = m.newMap(numelements=60,
                                     maptype='PROBING',
                                     comparefunction=CompareAccidentsState)
    accidents = lt.newList('SINGLE_LINKED', compareDates)
    m.put(entry['StateIndex'],accident["State"],accidents)
    entry['lstAccidents'] = lt.newList('SINGLE_LINKED', compareDates)
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
    return om.height(analyzer['dateIndex'])

def indexSize(analyzer):
    """
    """
    return om.size(analyzer['dateIndex'])

def minKey(analyzer):
    """
    """
    return om.minKey(analyzer['dateIndex'])

def maxKey(analyzer):
    """
    """
    return om.maxKey(analyzer['dateIndex'])

# ==============================
# Funciones de Requerimientos
# ==============================

def getAccidentsByDate(analyzer,date):
    accident = om.get(analyzer["dateIndex"],date)
    lst =  me.getValue(accident)
    lst = lst['lstAccidents']
    accidents = lt.size(lst)
    return accidents
    
def getAccidentsByState(analyzer,initialDate,finalDate):
    accidents = om.values(analyzer['dateIndex'],initialDate,finalDate)
    lstiterator = it.newIterator(accidents)
    state = None
    comparador = 0
    while (it.hasNext(lstiterator)):
        eachdate = it.next(lstiterator)
        statename = eachdate["Mayor"]
        lststate = m.get(eachdate["StateIndex"],statename)
        lststate = me.getValue(lststate)
        mayor = lt.size(lststate)
        comparador = 0
        if mayor > comparador:
            state = statename
            comparador = mayor
    return state


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
            Results["FechaAccidentada"] = lstdate['lstAccidents']['first']['info']['Start_Time'][:10]

        totalAccidents += lt.size(lstdate['lstAccidents'])

    Results["totalAccidents"] = totalAccidents

    return Results
#requerimiento grupal
def getAccidentsbytime(analyzer,initial,final):
    return  None

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
def compareminutes(min, hour):
    if min >= 0 and min<15:
        min=0
    if min>=15 and min<30:
        min=30
    if min>=30 and min<45:
        min=30
    if min>=45 and min<=60:
        min=0
        #hour +=1
    



def CompareAccidentsState(accident1, accident2):
    """
    Compara dos ids de libros, id es un identificador
    y entry una pareja llave-valor
    """
    offense = me.getKey(accident2)
    if (accident1 == offense):
        return 0
    elif (accident1 > offense):
        return 1
    else:
        return -1

    