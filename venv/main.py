import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ui import tomarDatos

def dirigir():
    
    while(True):     
        tomarDatos()
        print("¿Quiere volver a hacer otra consulta? (si/no): ")
        respuesta = input().strip().lower() 
        
        if respuesta == 'si':
            continue  
        elif respuesta == 'no':
            break  
        else:
            print("Error: Respuesta no válida. Por favor, introduzca 'si' o 'no'.")  
            
            
if __name__ == '__main__':
    dirigir()
