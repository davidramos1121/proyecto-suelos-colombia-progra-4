import pandas as pd
from sodapy import Socrata

def buscar(numeroRegistros, departamentos, municipios, cultivos):
    cliente = Socrata("www.datos.gov.co", None)
    
    try:
        consulta = {}
        if departamentos:
            consulta['departamento'] = departamentos
        if municipios:
            consulta['municipio'] = municipios
        if cultivos:
            consulta['cultivo'] = cultivos
            
        resultados = cliente.get("ch4u-f3i5", **consulta, limit=numeroRegistros)
        
        
        if not resultados:
            print("No se encontraron resultados a la búsqueda solicitada\n*Pruebe llenando los campos nuevamente\n*Recuerde llenar los campos correctamente\n*Recuerde que para el campo de los cultivos debe usar las respectivas mayúsculas y guiones(-) de ser necesario")
            return None
        
        
        resultadosDataFrame = pd.DataFrame.from_records(resultados)
        
    except Exception as e:
        print(f"Error al consultar la API: {e}")
        return None
    
    
    columnasInteres = {
        'ph_agua_suelo_2_5_1_0': 'pH_agua:suelo 2,5:1,0',
        'materia_org_nica_mo': 'Materia_organica (MO) %',
        'f_sforo_p_bray_ii_mg_kg': 'Fosforo (P) Bray II mg/kg',
        'azufre_s_fosfato_monocalcico_mg_kg': 'Azufre (S) Fosfato monocalcico mg/kg',
        'acidez_al_h_kcl_cmol_kg' : 'Acidez (Al+H) KCL cmol(+)/kg',
        'aluminio_al_intercambiable_cmol_kg' : 'Aluminio (Al) intercambiable cmol(+)/kg',
        'calcio_ca_intercambiable_cmol_kg':'calcio_ca_intercambiable_cmol_kg',
        'potasio_k_intercambiable_cmol_kg' : 'Potasio (K) intercambiable cmol(+)/kg',
        'sodio_na_intercambiable_cmol_kg' : 'Sodio (Na) intercambiable cmol(+)/kg',
        'capacidad_de_intercambio_cationico_cice_suma_de_bases_cmol_kg' : 'capacidad de intercambio cationico (CICE) suma de bases cmol(+)/kg',
        'conductividad_el_ctrica_ce_relacion_2_5_1_0_ds_m' : 'Conductividad electrica (CE) relacion 2,5:1,0 dS/m',
        'hierro_fe_disponible_olsen_mg_kg' : 'Hierro (Fe) disponible olsen mg/kg',
        'cobre_cu_disponible_mg_kg' : 'Cobre (Cu) disponible mg/kg',
        'manganeso_mn_disponible_olsen_mg_kg' : 'Manganeso (Mn) disponible Olsen mg/kg',
        'zinc_zn_disponible_olsen_mg_kg' : 'Zinc (Zn) disponible Olsen mg/kg',
        'boro_b_disponible_mg_kg' : 'Boro (B) disponible mg/kg',
        'hierro_fe_disponible_doble_cido_mg_kg' : 'Hierro (Fe) disponible doble acido mg/kg',
        'cobre_cu_disponible_doble_acido_mg_kg' :  'Cobre (Cu) disponible doble acido mg/kg',
        'manganeso_mn_disponible_doble_acido_mg_kg' : 'Manganeso (Mn) disponible doble acido mg/kg',
        'zinc_zn_disponible_doble_cido_mg_kg' : 'Zinc (Zn) disponible doble  cido mg/kg'
    }
    
    
    medianas = {}
    
    
    for columna, nombre in columnasInteres.items():
        if columna in resultadosDataFrame.columns:
            resultadosDataFrame[columna] = pd.to_numeric(resultadosDataFrame[columna], errors='coerce') 
            medianas[nombre] = resultadosDataFrame[columna].median()
        else:
            print(f"La columna '{nombre}' no está presente en los resultados.")
            medianas[nombre] = None
    
    
    columnasMostrar = ['municipio', 'departamento', 'cultivo', 'topografia']
    resultadosDataFrame = resultadosDataFrame[columnasMostrar]
    
    convertirCVS(medianas, resultadosDataFrame)
    mostrar(resultadosDataFrame, medianas)
    

def convertirCVS(medianas, resultadosDataFrame):
    medianasDataFrame = pd.DataFrame(list(medianas.items()), columns=['Variable', 'Mediana'])
    
    with open("resultados_y_medianas.csv", "w", encoding='utf-8') as f:
        resultadosDataFrame.to_csv(f, index=False)
        f.write("\n") 
        medianasDataFrame.to_csv(f, index=False)
        

def mostrar(resultadosDF, medianas):
    print(resultadosDF)
    for nombre, mediana in medianas.items():
        if mediana is not None:
            print(f"La mediana de {nombre} es: {mediana}")
