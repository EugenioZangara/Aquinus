especialidades = {
    'IN': 1,
    'EL': 2,
    'AE': 3,
    'MW': 4,
    'AN': 5,
    'IM': 6,
    'MA': 7,
    'AG': 8,
    'MQ': 9,
    'EN': 10,
    'FU': 11,
    'OP': 12,
    'CO': 13,
    'SH': 14,
    'MU': 15
}



orientaciones={
    "AA": 2,
    "AC": 3,
    "AE": 4,
    "AG": 5,
    "Armas": 6,
    "AN": 7,
    "AS": 8,
    "AU": 9,
    "AV": 10,
    "BA": 11,
    "Buceo Táctico": 12,
    "Buceo": 13,
    "CA": 14,
    "CC": 15,
    "CD": 16,
    "CM": 17,
    "CO": 18,
    "CP": 19,
    "Control Tiro": 20,
    "EE": 21,
    "EL": 22,
    "EM": 23,
    "FU": 25,
    "GN": 26,
    "HI": 27,
    "IF": 28,
    "IM": 29,
    "IN": 30,
    "MA": 31,
    "MC": 32,
    "ME": 33,
    "MN": 34,
    "Motores": 35,
    "MQ": 36,
    "MW": 37,
    "MO": 38,
    "MU": 39,
    "OC": 40,
    "OP": 41,
    "PE": 42,
    "RC": 43,
    "Radar": 44,
    "SC": 45,
    "SH": 46,
    "Salvamento": 47,
    "SO": 48,
    "SU": 49,
    "TB": 50
}
# Diccionario invertido
especialidades_invertidas = {v: k for k, v in especialidades.items()}

# Función para convertir entre string y número
def convertirEspecialidad(valor):
   
        return especialidades.get(valor)
   

def convertirOrientaciones(orientacion):
    print("ORIENTACION", orientacion)
    return orientaciones.get(orientacion)  

grados={1:"ANPA",2:"ANSA", 3:"ANTA", 4:"POSTULANTE", 5:"CSCOM"}
def convertirGrado(grado):
    
    return grados[int(grado)]