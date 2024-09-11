from django.db import models
from datetime import datetime
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.contrib.auth.models import User  # Importa el modelo User

from apps.alumnos.models import persona
# Create your models here.

TIPO_DE_MATERIA = [('ANUAL', 'ANUAL'),
                   ('SEMESTRAL', 'SEMESTRAL'),
                   ('CUATRIMESTRAL', 'CUATRIMESTRAL'),
                   ('TRIMESTRAL', 'TRIMESTRAL')]
ESPECIALIDADES = [
    ('AE', 'AE'),
    ('AG', 'AG'),
    ('AN', 'AN'),
    ('CO', 'CO'),
    ('EL', 'EL'),
    ('EN', 'EN'),
    ('FU', 'FU'),
    ('IM', 'IM'),
    ('IN', 'IN'),
    ('IPDSV', 'IPDSV'),
    ('MA', 'MA'),
    ('MQ', 'MQ'),
    ('MU', 'MU'),
    ('MW', 'MW'),
    ('OP', 'OP'),
    ('SH', 'SH')
]

ORIENTACIONES=[
    ('ME', 'ME'),
        ('MS', 'MS'),
        ('HI', 'HI'),
        ('AM', 'AM'),
        ('AV', 'AV'),
        ('MC', 'MC'),
        ('OPCR/AC', 'OPCR/AC'),
        ('OPDT', 'OPDT'),
        ('SU', 'SU'),
        ('EMMH', 'EMMH'),
        ('AE', 'AE'),
        ('AEAM', 'AEAM'),
        ('AEAV', 'AEAV'),
        ('AEMC', 'AEMC'),
        ('AESU', 'AESU'),
        ('CO', 'CO'),
        ('EL', 'EL'),
        ('OC', 'OC'),
        ('FU', 'FU'),
        ('IN', 'IN'),
        ('CA', 'CA'),
        ('MO', 'MO'),
        ('SC', 'SC'),
        ('TB', 'TB'),
        ('MU', 'MU'),
        ('AA', 'AA'),
        ('GN', 'GN'),
        ('EN', 'EN'),
        ('BA', 'BA'),
        ('AC', 'AC'),
        ('EE', 'EE'),
        ('II', 'II'),
        ('MT', 'MT'),
        ('AU', 'AU'),
        ('EM', 'EM'),
        ('CC', 'CC'),
        ('CD', 'CD'),
        ('CM', 'CM'),
        ('PE', 'PE'),
        ('IM', 'IM'),
        ('(ITD)', '(ITD)'),
        ('MA', 'MA'),
        ('MQ', 'MQ'),
        ('AS', 'AS'),
        ('CP', 'CP'),
        ('CT', 'CT'),
        ('MN', 'MN'),
        ('SO', 'SO'),
        ('RC', 'RC'),
        ('EESI', 'EESI'),
        ('EECT', 'EECT'),
        ('EMAM', 'EMAM'),
        ('EMEL', 'EMEL'),
        ('RD', 'RD'),
        ('SR', 'SR'),
        ('EMPR', 'EMPR'),
    ]
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


def validate_four_digits(value):
        if not (1000 <= value <= 9999):
            raise ValidationError('El valor debe ser un número de cuatro dígitos.')

def validate_orientacion(especialidad, orientacion):
    if especialidad not in combinaciones_permitidas:
        raise ValidationError(f"Especialidad '{especialidad}' no es válida.")
    
    if orientacion not in combinaciones_permitidas[especialidad]:
        raise ValidationError(f"Orientación '{orientacion}' no es válida para la especialidad '{especialidad}'.")


class Materia(models.Model):
    nombre=models.CharField(max_length=100)
    abreviatura=models.CharField(max_length=20)
    tipo=models.CharField(max_length=50, choices=TIPO_DE_MATERIA)
    area=models.CharField(max_length=50)
    regimen=models.CharField(max_length=50, choices=[('PROMOCIONABLE','PROMOCIONABLE'),('NO PROMOCIONABLE','NO PROMOCIONABLE'),('ESPECIAL','ESPECIAL')])
    observaciones=models.TextField(max_length=500, null=True, blank=True)
    def __str__(self):
        return self.nombre
    
    '''
    Se asegura que el nombre y abreviatura de la materia esté todo en mayúsculas
    '''
    def save(self,*args, **kwargs):
        self.nombre=self.nombre.upper()
        self.abreviatura=self.abreviatura.upper()
        super().save(*args, **kwargs)

        
    
class PlanEstudio(models.Model):
    
    especialidad=models.CharField(max_length=10, choices=ESPECIALIDADES)
    orientacion=models.CharField(max_length=10, blank=True, null=True, choices=ORIENTACIONES)
    materias=models.ManyToManyField(Materia, related_name='materias_plan_de_estudio',help_text="Materias asociadas al plan de estudio")
    anio=models.IntegerField(validators=[validate_four_digits],  # Aplica la validación personalizada
        )
    vigente=models.BooleanField(default=True)
    
    class Meta:
        constraints = [
            # Garantiza que la combinación de especialidad y año sea única
            models.UniqueConstraint(fields=['especialidad', 'anio'], name='unique_especialidad_anio'),
        ]

    def clean(self):
        super().clean()
        # Validar que solo haya un plan vigente por especialidad
        if self.especialidad and self.orientacion:
            validate_orientacion(self.especialidad, self.orientacion)
        if self.vigente:
            # Busca otros planes de estudio de la misma especialidad que estén vigentes
            planes_vigentes = PlanEstudio.objects.filter(especialidad=self.especialidad, vigente=True)
            if self.pk:  # Si estamos actualizando un objeto existente, excluimos este objeto de la búsqueda
                planes_vigentes = planes_vigentes.exclude(pk=self.pk)
            if planes_vigentes.exists():
                raise ValidationError(f'Ya existe un plan de estudio vigente para la especialidad {self.especialidad}.')


        def save(self, *args, **kwargs):
            self.clean()  # Asegúrate de llamar a clean antes de guardar
            super().save(*args, **kwargs)





    def __str__(self):
        if self.orientacion:
            return f'{self.especialidad}{self.orientacion}'
        else:
            return self.especialidad
    

class Curso(models.Model):
    nombre=models.CharField(max_length=100, unique=True)
    plan_de_estudio=models.ForeignKey(PlanEstudio, on_delete=models.DO_NOTHING, related_name='plan_estudio_curso')
    activo=models.BooleanField(default=False)
    puede_calificar=models.BooleanField(default=False)
    division=models.IntegerField(default=1)
    def save(self, *args, **kwargs):
        if not self.nombre:  # Solo lo genera si el nombre no ha sido definido aún
            año_actual = datetime.now().year
            self.nombre = f'{self.especialidad}-{año_actual}-{self.division}'
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.nombre
    
    
class Cursante(models.Model):
    alumno=models.OneToOneField(persona, on_delete=models.CASCADE,related_name='persona_alumno')
    curso=models.ForeignKey(Curso, on_delete=models.DO_NOTHING, related_name='alumno_curso')
    
    def __str__(self):
        return self.alumno.dni
    


class Calificaciones(models.Model):
    
    CALIFICACIONES_CHOICES=[
    ('BIMESTRAL','Bimestral'), #Calificación promedio de las calificaciones ordinarias del bimestre
    ('TRIMESTRAL','Trimestral'), # Calificación promedio de las calificaciones ordinarias del trimestre
    ('PROMEDIO CURSADA','Promedio Cursada'), #n Calificación promedio de las notas de los periodos intermedios (trimestre/bimestre)
    ('EXAMEN FINAL','Examen Final'), # Nota de examen final de la materia, las materias promocionables pueden no tenerlo
    ('FINAL','Final'), # Nota final de la materia (promedio de examen fina y promedio de cursada o promedio de cursada en caso de promocionables)
    ('COMPLEMENTARIO', 'Complementario'), # Calificación correspondiente a un examen complementario, debe acompañar el campo numero_complementario
    ('ORDINARIA','Ordinaria') #Calificación volcada por el profesor durante la cursada en función de las evaluaciones que haga
]
    
    materia=models.ForeignKey(Materia,on_delete=models.DO_NOTHING,  related_name='calificacion_materia')
    cursante=models.ForeignKey(Cursante, on_delete=models.DO_NOTHING, related_name='nota_cursante')
    valor=models.DecimalField(decimal_places=2, max_digits=3)
    tipo=models.CharField(max_length=50, choices=CALIFICACIONES_CHOICES)
    numero_complementario=models.IntegerField(blank=True, null=True)
    fecha_examen=models.DateField()
    fecha=models.DateTimeField( auto_now_add=True)
    calificador = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)


    