from django.shortcuts import render

combinaciones_permitidas = {
    'SH': ['ME', 'HI', 'OC', 'BA'],
    'IM': ['MS', 'AA', 'AC', 'CO', 'EE', 'II', 'MT'],
    'AE': ['AM', 'AV', 'MC', 'OPCR/AC', 'OPDT', 'SU'],
    'AN': ['EMMH', 'AE', 'AEAM', 'AEAV', 'AEMC', 'AESU', 'AU', 'EE', 'EM'],
    'CO': ['CO'],
    'EL': ['EL'],
    'FU': ['FU'],
    'IN': ['IN'],
    'MQ': ['CA', 'MO', 'SC', 'TB', 'MQ'],
    'MU': ['MU'],
    'MW': ['AA', 'AS', 'CP', 'MN', 'RC'],
    'OP': ['GN', 'SO'],
    'AG': ['CC', 'CD', 'CM', 'PE'],
    'IPDSV': ['CD', 'CM'],
    'MA': ['(ITD)', 'MA']
}
def get_orientaciones(request):
    especialidad= request.GET.get('especialidad')
    orientaciones=combinaciones_permitidas[especialidad]
    print(orientaciones)
    return render(request, 'parciales/cursos/orientaciones_choices.html', {'orientaciones':orientaciones})