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
    analyzer['dateIndex'] = om.newMap(omaptype='BST',
                                      comparefunction=compareDates)
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
    return analyzer



def updateDateIndex(map, EachAccident):
    """
    Se toma la fecha del accidente y se busca si ya existe en el arbol
    dicha fecha.  Si es asi, se adiciona a su lista de accidentes
    y se actualiza el indice de tipos de accidentes.

    Si no se encuentra creado un nodo para esa fecha en el arbol
    se crea y se actualiza el indice de tipos de accidentes
    """
    occurreddate = EachAccident['Start_Time'] 
    AccidentDate = datetime.datetime.strptime(occurreddate, '%Y-%m-%d %H:%M:%S')
    entry = om.get(map, AccidentDate.date())
    if entry is None:
        datentry = newDataEntry(EachAccident)
        om.put(map, AccidentDate.date(), datentry)
    else:
        datentry = me.getValue(entry)
    #addDateIndex(datentry, crime)
    return map



def newDataEntry(accident):
    """
    Crea una entrada en el indice por fechas, es decir en el arbol
    binario.
    Se crea el indice por estado, puede ser util para el requerimiento 5,
    pero no necesaria, REVISAR
    """
    entry = {'StateIndex': None, 'lstAccidents': None}
    entry['StateIndex'] = m.newMap(numelements=30,
                                     maptype='PROBING',
                                     comparefunction=CompareAccidentsState)
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

