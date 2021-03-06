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


AccidentsFile1 = "us_accidents_dis_2016.csv"
AccidentsFile2 = "us_accidents_dis_2017.csv"
AccidentsFile3 = "us_accidents_dis_2018.csv"
AccidentsFile4 = "us_accidents_dis_2019.csv"

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
    print("4- Conocer los accidentes anteriores a una fecha especifica")
    print("5- Conocer accidnetes en un rango de fechas")
    print("6- Conocer el estado con mas accidentes y la fecha con mas accidentes en un rango")
    print("7- Conocer accidentes en un rango de horas")
    print("8- Conocer accidentes en un rango")
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
        controller.loadData(cont, AccidentsFile1)
        print("cargado 2016")
        controller.loadData(cont, AccidentsFile2)
        print("cargado 2017")
        controller.loadData(cont, AccidentsFile3)
        print("cargado 2018")
        controller.loadData(cont, AccidentsFile4)
        print("cargado 2019")
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
                
    # ↓↓↓ Requerimiento 2 - Cristhian Perdomo ↓↓↓    
    elif int(inputs[0]) == 4:
        print("\nPara esta búsqueda se conocerá el total de accidentes ocurridos antes de una fecha, así como la fecha que más accidentes ha reportado:")
        PreviousTo = input("Ingrese una fecha para consultar (YYYY-MM-DD): ")
        total = controller.getAccidentsBefore(cont, menor, PreviousTo)
        print ("\nEl total de accidentes registrados antes de {} es: {}.\n*Durante este pediodo, la fecha que más registro accidentes fue {}, con {} en total." .format(PreviousTo, str(total["totalAccidents"]), str(total["FechaAccidentada"]), str(total["CantidadPorFecha"])))
    #santiago
    elif int(inputs[0]) == 5:
        print("\nBuscando accidentes en un rango de fechas: ")
        menor = input("Ingrese una fecha inferior para consultar (YYYY-MM-DD): ")
        PreviousTo = input("Ingrese una fecha superior para consultar (YYYY-MM-DD): ")
        total = controller.getAccidentsRange(cont, menor, PreviousTo)
        print("Entre "+menor+" y "+PreviousTo+" ocurrieron "+str(lt.size(total["list"]))+" accidentes")
        print("El tipo de severidad más comun fue "+total["category"])

    #alelejandra
    elif int(inputs[0]) == 6:
        print("\nBuscando el estado con mas accidentes en un rango de fechas: ")
        initialDate = input("Escriba la fecha inicial en formato (AAAA-MM-DD): ")
        finalDate = input("Escriba la fecha final en formato (AAAA-MM-DD): ")
        accidents = controller.getAccidentsByState(cont,initialDate,finalDate)
        print ("Es estado con mayor numero de accidentes entre {} y {} es {}".format(initialDate,finalDate,accidents[1]))
        print ("La fecha con mayor numero de accidentes entre {} y {} es {}".format(initialDate,finalDate,accidents[0]))
        
    elif int(inputs[0]) == 7:
        print("\nBuscando accidentes en un rango de Horas: ")
        initialDate = input("Escriba la fecha inicial en formato (HH:MM): ")
        finalDate = input("Escriba la fecha final en formato (HH:MM): ")
        accidents = controller.getAccidentsByTime(cont,initialDate,finalDate)
        grado1 = controller.getAccidentsBySeverity(accidents,"1")
        grado2 = controller.getAccidentsBySeverity(accidents,"2")
        grado3 = controller.getAccidentsBySeverity(accidents,"3")
        grado4 = controller.getAccidentsBySeverity(accidents,"4")
        print ("\nAccidentes de Primer Grado")
        print (grado1)
        print ("Accidentes de Segundo Grado")
        print (grado2)
        print ("Accidentes de Tercer Grado")
        print (grado3)
        print ("Accidentes de Cuarto Grado")
        print (grado4)
        print ("El promedio de accidentes ocurridos entre las {} y las {} es de {}{}".format(initialDate,finalDate,round(((grado1 + grado2 + grado3 + grado4)/controller.crimesSize(cont))*100,2),"%"))

    elif int(inputs[0]) == 8:
        print("\nBuscando accidentes dentro del radio: ")
        lat = input("Escriba latitud: ")
        lon = input("Escriba longitud): ")
        distancia=input("Escriba radio): ")
        accidents = controller.bono(cont,lat,lon,distancia)
        print("La cantidad de accidendes presentados en el radio inscrito fue de "+str(lt.size(accidents["list"])))
        print("En el lunes se presentaron "+str(accidents["lunes"]))
        print("En el Martes se presentaron "+str(accidents["martes"]))
        print("En el Miercoles se presentaron "+str(accidents["miercoles"]))
        print("En el Jueves se presentaron "+str(accidents["jueves"]))
        print("En el Viernes se presentaron "+str(accidents["viernes"]))
        print("En el Sabado se presentaron "+str(accidents["sabado"]))
        print("En el Domingo se presentaron "+str(accidents["domingo"]))
        

    else:
        sys.exit(0)
sys.exit(0)
