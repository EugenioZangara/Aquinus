from .models import Perfil



from django.shortcuts import render


def get_usuarios_x_dni(request):
    dni= request.POST.get('dni')
    context={}
    try:
        
        perfil=Perfil.objects.get(dni=dni)
       
        context['perfil']=perfil
    except Perfil.DoesNotExist:
        context['perfil']=None
    except Perfil.MultipleObjectsReturned:
        context['perfil']="multiples resultados"
 
    return render(request, 'parciales/usuarios/usuarios_x_dni.html', context)