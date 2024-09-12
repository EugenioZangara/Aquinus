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
    'MU': 15,
}

orientaciones={
2:"AM",
3:"AC",
# 4:"AE",
# 5:"AG",
6:"AA",
# 7:"AR"
# 8:"AS",
# 9:"AU",
10:"AV",
11:"BA",
# 12:"BT",
# 13:"BU",
# 14:"CA",
# 15:"CC",
# 16:"CD",
# 17:"CM",
18:"CO",
# 19:"ComputaciÃ³n
# 20:"CT"
21:"EE",
# 22:"EL"
# 23:"EE",
# 24:"EN"
# 25:"FU"
# 26:"GE"
27:"HI",
# 28:"IN"
# 29:"IM"
# 30:"IN"
# 31:'MA'
32:"MC",
 33:"ME",
# 34:"MN"
# 35:'MO'
# 36:'MA'
# 37:"MW"
# 38:'MO'
# 39:MÃºsicos
40:"OC",
# 41:Operaciones
# 42:Peluqueros
# 43:Radiocomunicaciones
# 44:Radar
# 45:"Sistemas de Control"
46:"SH",
# 47:Salvamento
# 48:Sonaristas
# 49:'su'
# 50:Turbinas
}
def convertirEspecialidad(especialidad):
    return especialidades[especialidad]

def convertirOrientaciones(orientacion):
    return orientaciones[orientacion]   

grados={1:"ANPA",2:"ANSA", 3:"ANTA", 4:"POSTULANTE", 5:"CSCOM"}
def convertirGrado(grado):
    return grados[grado]