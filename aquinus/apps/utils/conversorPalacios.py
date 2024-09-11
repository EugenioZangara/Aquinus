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

# orientaciones={2:"AR"
# 3:"Auxiliar Comando"
# 4:"AE"
# 5:"AG""
# 6:"Armas
# 7:"Arsenales
# 8:""Armas Submarinas"
# 9:"Auxiliares
# 10:"AviÃ³nicos
# 11:"Balizamiento
# 12:""Buceo TÃ¡ctico"
# 13:"Buceo
# 14:""Control AverÃ­as"
# 15:"Cocineros
# 16:"Conductores
# 17:"Camareros
# 18:"Comunicaciones
# 19:"ComputaciÃ³n
# 20:""Control Tiro"
# 21:"ElectrÃ³nicos
# 22:"EL"
# 23:"ElectromecÃ¡nicos
# 24:"EN"
# 25:"FU"
# 26:"GE"
# 27:"HidrografÃ­a
# 28:"IN"
# 29:"IM"
# 30:"InformÃ¡ticos
# 31:'MA'
# 32:MecÃ¡nicos
# 33:MeteorologÃ­a
# 34:MuniciÃ³n
# 35:'MO'
# 36:'MA'
# 37:"MW"
# 38:'MO'
# 39:MÃºsicos
# 40:OceanografÃ­a
# 41:Operaciones
# 42:Peluqueros
# 43:Radiocomunicaciones
# 44:Radar
# 45:"Sistemas de Control"
# 46:"Servicios HidrogrÃ¡ficos"
# 47:Salvamento
# 48:Sonaristas
# 49:'su'
# 50:Turbinas
# }
def convertirEspecialidad(especialidad):
    return especialidades[especialidad]

grados={1:"ANPA",2:"ANSA", 3:"ANTA"}
def convertirGrado(grado):
    return grados[grado]