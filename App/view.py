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

import sys
import config
from DISClib.ADT import list as lt
from App import controller
assert config

"""
La vista se encarga de la interacción con el usuario.
Presenta el menu de opciones  y  por cada seleccion
hace la solicitud al controlador para ejecutar la
operación seleccionada.
"""

# ___________________________________________________
#  Ruta a los archivos
# ___________________________________________________


AccidentsFile = "us_accidents_small.csv"

# ___________________________________________________
#  Menu principal
# ___________________________________________________


def printMenu():
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("1- Inicializar Analizador")
    print("2- Cargar información de accidentes")
    print("3- Conocer accidentes en una fecha especicifica")
    print("4- Requerimento 2")
    print("5- Requerimento 3")
    print("6- Conocer el estado con más accidentes en un rango de fechas")
    print("0- Salir")
    print("*******************************************")


"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n>')

    if int(inputs[0]) == 1:
        print("\nInicializando....")
        # cont es el controlador que se usará de acá en adelante
        cont = controller.init()
        print ("Analizador de accidentes cargado correctamente")

    elif int(inputs[0]) == 2:
        print("\nCargando información de accidentes ....")
        controller.loadData(cont, AccidentsFile)
        #print (cont['accidents']['first']["info"]) 
        print('Acidentes cargados: ' + str(controller.crimesSize(cont)))
        print('Altura del arbol: ' + str(controller.indexHeight(cont)))
        print('Elementos en el arbol: ' + str(controller.indexSize(cont)))
        print('Menor Llave: ' + str(controller.minKey(cont)))
        menor=(str(controller.minKey(cont)))
        print('Mayor Llave: ' + str(controller.maxKey(cont)))
        

    elif int(inputs[0]) == 3:
        print("\nBuscando accidentes en una fecha especifica: ")
        date = input("Escriba la fecha en formato (AAAA-MM-DD): ")
        accidents = controller.getAccidentsByDate(cont,date)
        print (("El numero de accidentes ocurridos en {} son {}".format(date,accidents)))
        
    elif int(inputs[0]) == 3:
        print("\nBuscando crimenes en una fecha especifica: ")
        date = input("Escriba la fecha en formato (AAAA-MM-DD): ")
        accidents = controller.getAccidentsByDate(cont,date)
        print (("El numero de accidentes ocurridos en {} son {}".format(date,accidents)))
        
    # ↓↓↓ Requerimiento 2 - Cristhian Perdomo ↓↓↓    
    elif int(inputs[0]) == 4:
        print("\nPara esta búsqueda se conocerá el total de accidentes ocurridos antes de una fecha, así como la fecha que más accidentes ha reportado:")
        PreviousTo = input("Ingrese una fecha para consultar (YYYY-MM-DD): ")
        total = controller.getAccidentsBefore(cont, menor, PreviousTo)
        print ("\nEl total de accidentes registrados antes de {} es: {}.\n*Durante este pediodo, la fecha que más registro accidentes fue {}, con {} en total." .format(PreviousTo, str(total["totalAccidents"]), str(total["FechaAccidentada"]), str(total["CantidadPorFecha"])))
        

    elif int(inputs[0]) == 6:
        print("\nBuscando el estado con mas accidentes en un rango de fechas: ")
        initialDate = input("Escriba la fecha inicial en formato (AAAA-MM-DD): ")
        finalDate = input("Escriba la fecha final en formato (AAAA-MM-DD): ")
        accidents = controller.getAccidentsByState(cont,initialDate,finalDate)
        print (("El estado con el mayor numero de accidentes ocurridos entre {} y {} son {}".format(initialDate,finalDate,accidents)))


    else:
        sys.exit(0)
sys.exit(0)
