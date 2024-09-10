import pandas as pd
from api import buscar
import sys
sys.stdout.reconfigure(encoding='UTF-8')

def tomarDatos():
    
    while True:

        try:
            limite = int(input("Ingrese el límite de registros (Debe ser menor a 500): "))
            
            if limite < 500:              
                departamento = input("Ingrese el nombre del departamento a buscar: ")
                municipio = input("Ingrese el nombre del municipio: ")
                cultivo = input("Ingrese el cultivo que desea consultar: ")      
                break
            
            print("Error, el número supera el límite (500). Intente nuevamente.")
       
        except ValueError:
            print("El número tiene que ser un entero. Intente nuevamente.")
    
    dataFrame = buscar(limite, departamento.upper(), municipio.upper(), cultivo)
