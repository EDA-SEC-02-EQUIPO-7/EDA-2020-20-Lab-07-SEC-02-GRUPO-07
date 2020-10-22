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

import config as cf
from App import model
import datetime
import csv

"""
El controlador se encarga de mediar entre la vista y el modelo.
Existen algunas operaciones en las que se necesita invocar
el modelo varias veces o integrar varias de las respuestas
del modelo en una sola respuesta.  Esta responsabilidad
recae sobre el controlador.
"""

# ___________________________________________________
#  Inicializacion del catalogo
# ___________________________________________________

def init():
    """
    Llama la funcion de inicializacion del modelo.
    """
    analyzer = model.newAnalyzer()
    return analyzer


# ___________________________________________________
#  Funciones para la carga de datos y almacenamiento
#  de datos en los modelos
# ___________________________________________________



def loadData(analyzer, accidentsfile):
    """
    Carga los datos de los archivos CSV en el modelo
    """

    accidentsfile = cf.data_dir + accidentsfile
    input_file = csv.DictReader(open(accidentsfile, encoding="utf-8"),
                                delimiter=",")
    for EachAccident in input_file:
        model.AddAnAccident(analyzer, EachAccident)
    return analyzer
    
# =========================
#Funciones Requerimientos 
#Funciones Requerimientos 
#Funciones Requerimientos 
# =========================


def getAccidentsByDate (analizer,date):
    date =  datetime.datetime.strptime(date, '%Y-%m-%d')
    return  model.getAccidentsByDate(analizer,date.date())

def getAccidentsByState (analizer,inicialDate, finalDate):
    inicialDate = datetime.datetime.strptime (inicialDate, '%Y-%m-%d')
    finalDate = datetime.datetime.strptime (finalDate, '%Y-%m-%d' )
    return model.getAccidentsByState (analizer,inicialDate.date(),finalDate.date())

#↓↓↓ Requerimiento 2 ↓↓↓
def bono(analyzer,lat,lon ,distancia):
    coord={"lat":None,
            "lon":None}
    print("----------------------")
    print(lat)
    print(lon)
    print("----------------------")
    coord["lat"]=(lat)
    coord["lon"]=(lon)
    return model.bono(analyzer,coord,float(distancia))

def getAccidentsBefore(analyzer, initialDate, finalDate):
    initialDate = datetime.datetime.strptime(initialDate, '%Y-%m-%d')
    finalDate = datetime.datetime.strptime(finalDate, '%Y-%m-%d')
    return model.getAccidentsBefore(analyzer, initialDate.date(), finalDate.date())

def getAccidentsRange(analyzer, initialDate, finalDate):
    initialDate = datetime.datetime.strptime(initialDate, '%Y-%m-%d')
    finalDate = datetime.datetime.strptime(finalDate, '%Y-%m-%d')
    return model.getAccidentsRange(analyzer, initialDate.date(), finalDate.date())
# =================================
#  Funciones para consultas RAPIDAS
#  Funciones para consultas RAPIDAS
#  Funciones para consultas RAPIDAS
# =================================

def crimesSize(analyzer):
    """
    Numero de Accidentes leidos
    """
    return model.crimesSize(analyzer)

def indexHeight(analyzer):
    """
    Altura del indice (arbol)
    """
    return model.indexHeight(analyzer)

def indexSize(analyzer):
    """
    Numero de nodos en el arbol
    """
    return model.indexSize(analyzer)

def minKey(analyzer):
    """
    La menor llave del arbol
    """
    return model.minKey(analyzer)

def maxKey(analyzer):
    """
    La mayor llave del arbol
    """
    return model.maxKey(analyzer)

