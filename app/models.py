from django.db import models
from django.contrib.auth.models import AbstractUser
#formato para guardar imagenes
class CustomUser(AbstractUser):
    TIPO_USUARIO = (
        ("1", 'ADMIN'), 
        ("2", 'DOCENTE'), 
        ("3", 'ESTUDIANTE')
    )
    user_type = models.CharField(default=1, choices = TIPO_USUARIO, max_length=20)
    first_name = models.CharField("Nombres", max_length = 30)
    last_name = models.CharField("Ap. Paterno", max_length = 30)
    sur_name = models.CharField("Ap. Materno", max_length = 30, blank=True)
    email = models.EmailField("Email", max_length=255, unique=True)

    def __str__(self):
        return self.email
    
    def get_full_name(self):
        return self.first_name + " " + self.last_name + " " + self.sur_name

    def get_short_name(self):
        return self.first_name.split(' ')[0] +" "+ self.last_name

class Base(models.Model):
    """Modelo abstract base del que heredan todos los modelos para manejar la auditoria"""
    fecha_registro = models.DateTimeField('Fecha de registro', auto_now_add=True)
    fecha_actualizacion = models.DateTimeField('Fecha de modificación', auto_now=True)
    #estado = models.BooleanField('Estado', default=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        super(Base, self).save(*args, **kwargs)

# ············ REGION EXTERNO ··············· {{{
class ubigeo(Base):
    codigo_ubigeo = models.CharField("Codigo Ubigeo", max_length=6, unique=True, primary_key=True)
    nombre = models.CharField("Nombre", max_length=150)
    tipo_ubigeo = models.CharField("Tipo Ubigeo",max_length=1)

        
    def __str__(self):
        return self.codigo_ubigeo

class colegio(Base):
    TIPO_COLEGIO = (
        ("PU","PUBLICO"),
        ("PR","PRIVADO"),
    )
    nombre_colegio = models.CharField("Nombre", max_length=180)
    codigo_modular = models.CharField("Codigo modular", max_length=10, unique=True, null=True)
    direccion_colegio = models.CharField("Direccion", max_length=200, null=True)
    id_ubigeo = models.ForeignKey(ubigeo, null=True, on_delete=models.SET_NULL)
    ubigeo_nombre = models.CharField("Nombre ubigeo", max_length=200, null=True)
    tipo_colegio = models.CharField("Tipo Colegio", max_length=2, choices=TIPO_COLEGIO)

    class Meta:
        ordering = ('id',)
    def __str__(self):
        return self.nombre_colegio
# ············ ENDREGION EXTERNO ··············· }}}

# ············ REGION ACTORES ··············· {{{
class persona(Base):
    dni = models.CharField("DNI",max_length=8, unique=True)
    nombres = models.CharField("Nombres",max_length=50)
    apellido_paterno = models.CharField("Ap. Paterno",max_length=50)
    apellido_materno = models.CharField("Ap. Materno",max_length=50)
    sexo = models.CharField("Sexo", max_length=5, choices=(("M","Masculino"),("F","Femenino")))
    fecha_nacimiento = models.DateField("Fecha de Nacimiento", null=True)
    lugar_nacimiento = models.ForeignKey(ubigeo, on_delete=models.RESTRICT, blank=True, null=True, verbose_name = "Lugar de nacimiento")

    class Meta:
        ordering = ['id']
        verbose_name = 'Persona'
        verbose_name_plural = 'Personas'

    def __str__(self):
        nombre_completo = self.apellido_paterno + " " + self.apellido_materno + " " + self.nombres
        return nombre_completo

class administrador(Base):
    email_institucional = models.EmailField("Correo Institucional")
    codigo_administrador = models.CharField("Codigo Administrador",max_length=15)
    user_type = models.OneToOneField(CustomUser, on_delete=models.RESTRICT,verbose_name='Tipo usuario')

    def __str__(self):
        cadena = str(self.user_type)
        return cadena
    
    class Meta:
        ordering = ['id']
        verbose_name = 'Administrador'
        verbose_name_plural = 'Administradores'

class docente(Base):
    CATEGORIAS = (
        ('P', 'Principal'),
        ('L', 'Locador'),
        ('A','Auxiliar'),
        ('C','Contratado')
    )
    user_type = models.OneToOneField(CustomUser, on_delete=models.RESTRICT,verbose_name='Tipo de usuario')
    codigo_docente = models.CharField("Codigo Docente", max_length=20)
    email_institucional = models.EmailField("Correo Institucional", null=True, blank=True)
    regimen_docente = models.CharField("Categoria Docente", max_length=3, choices=CATEGORIAS, null=True, blank=True)

    def __str__(self):
        return str(self.user_type)

    class Meta:
        ordering = ['id']
        verbose_name = 'Docente'
        verbose_name_plural = 'Docentes'
# ············ END REGION ACTORES ··············· }}}

# ············ REGION INFRAESTRUCTURA ··············· {{{
class grupo_academico(Base):
    denominacion = models.CharField("Denominacion", max_length=40)
    abreviacion = models.CharField("Abreviacion", max_length=10)
    descripcion = models.TextField("Descripcion", max_length=200, blank=True)

    def __str__(self):
        return self.denominacion

    class Meta:
        ordering = ['id']
        verbose_name = "Grupo Academico"
        verbose_name_plural = "Grupos Academicos"

class escuela_profesional(Base):
    codigo_escuela = models.CharField("Codigo", max_length=10, null=True, blank=True, unique=True)
    nombre_escuela_profesional = models.CharField("Nombre", max_length=40)
    abreviacion = models.CharField("Abreviacion", max_length=10, null=True, blank=True)
    descripcion = models.TextField("Descripcion", max_length=200, blank=True, null=True)
    id_grupo_academico = models.ForeignKey(grupo_academico, on_delete=models.RESTRICT, null=True, blank=True)

    def __str__(self):
        return self.nombre_escuela_profesional

    class Meta:
        ordering = ['id']
        verbose_name = "Escuela Profesional"
        verbose_name_plural = "Escuelas Profesionales"
    
class sede(Base):
    id_ubigeo = models.ForeignKey(ubigeo, on_delete=models.RESTRICT)
    denominacion_sede = models.CharField("Denominacion", max_length=50)
    telefono = models.CharField("Telefono", max_length=50, blank=True)
    direccion = models.CharField("Direccion", max_length=200, blank=True, null=True)

    def __str__(self):
        return self.denominacion_sede
    
    class Meta:
        ordering = ['id']
        verbose_name = "Sede"
        verbose_name_plural = "Sedes"

class pabellon(Base):
    id_sede = models.ForeignKey(sede, on_delete=models.RESTRICT, null=True, blank=True)
    codigo_pabellon = models.CharField("Codigo pabellon", max_length=10, null=True, blank=True)
    nombre_pabellon = models.CharField("Denominacion", max_length=50)
    numero_pisos = models.PositiveIntegerField("Nro. de Pisos", null=True, blank=True)

    def __str__(self):
        return self.nombre_pabellon
    
    class Meta:
        ordering = ['id']
        verbose_name = "Pabellon"
        verbose_name_plural = "Pabellones"
    
class aula(Base):
    TIPO_AULA = (
        ("TALLER", "Taller"),
        ("LABO", "Laboratorio"),
        ("TEORIA", "Teoria"),
    )
    id_pabellon = models.ForeignKey(pabellon, on_delete=models.RESTRICT)
    codigo_aula = models.CharField("Codigo de aula", max_length=10, null=True, blank=True)
    sillas_fijas = models.PositiveIntegerField("Nro. de sillas fijas", default=0)
    sillas_moviles = models.PositiveIntegerField("Nro. de sillas moviles", default=0)
    nro_salon = models.CharField("Nro. de Salon", max_length=10, null=True, blank=True)
    tipo_aula = models.CharField("Tipo de Aula", max_length=20, choices=TIPO_AULA, null=True, blank=True)
    capacidad = models.PositiveIntegerField("Capacidad", null=True, blank=True)
    piso = models.PositiveIntegerField("Piso", null=True, blank=True)

    def __str__(self):
        detalle_salon = self.codigo_aula +" "+ str(self.id_pabellon.nombre_pabellon)
        return detalle_salon
    
    class Meta:
        ordering = ['id']
        verbose_name = "Aula"
        verbose_name_plural = "Aulas"

# ············ END REGION INFRAESTRUCTURA ··············· }}}

# ············ REGION CICLO ··············· {{{
class ciclo(Base):
    activo = models.BooleanField("Estado Activo", default=True)
    denominacion = models.CharField("Denominacion Ciclo",max_length=100)
    anio = models.PositiveIntegerField("Año")
    nro_ciclo_de_año = models.PositiveSmallIntegerField("Nro. Ciclo")
    requisitos = models.TextField("Requisitos", null=True, blank=True)
    caja_mensaje = models.TextField("Mensaje", null=True, blank=True)
    fecha_inicio_ciclo = models.DateField("Fecha inicio",null=True)
    fecha_fin_ciclo = models.DateField("Fecha Culminacion", null=True)
    fecha_inicio_preinscripcion = models.DateField("Fecha inicio preinscripcion", null=True)
    fecha_fin_preinscripcion = models.DateField("Fecha final preinscripcion", null=True)
    fecha_inicio_inscripcion = models.DateField("Fecha inicio inscripcion", null=True)
    fecha_fin_inscripcion = models.DateField("Fecha final inscripcion", null=True)
    id_administrador = models.ForeignKey(administrador, on_delete=models.RESTRICT, null=True)
    #numero_examenes = models.IntegerField("Nro. de examenes")
    #numero_maximo_cuotas = models.IntegerField("Nro. de cuotas maximo")
    #turno_mañana = models.BooleanField("Turno Mañana", default=False, null=True)
    #turno_tarde = models.BooleanField("Turno Tarde", default=False, null=True)
    #turno_noche = models.BooleanField("Turno Noche", default=False, null=True)
    #monto_colegio_privado = models.DecimalField("Monto Colegio Privado", max_digits=10, decimal_places=2)
    #monto_colegio_publico = models.DecimalField("Monto Colegio Publico", max_digits=10, decimal_places=2)

    def __str__(self):
        return self.denominacion

    class Meta:
        ordering = ['id']
        verbose_name = 'Ciclo'
        verbose_name_plural = 'Ciclos'
        

class documento_publicacion(Base):
    descripcion = models.TextField("Descripcion", max_length=100, blank=True)
    id_ciclo = models.ForeignKey(ciclo, on_delete=models.RESTRICT)
    nombre_documento = models.CharField("Nombre del archivo", max_length=100, null=True)
    archivo = models.FileField("Archivo", null=True)
    estado = models.BooleanField("Estado", default=True)

    def __str__(self):
        return self.nombre_documento

    class Meta:
        ordering = ['id']
        verbose_name = 'Documento de Publicacion'
        verbose_name_plural = 'Documentos de Publicacion'

class padron_documento_requisito(Base):
    estado = models.BooleanField("Estado activo", default=True)
    nombre_documento = models.CharField("Nombre del documento", max_length=150, null=True)
    descripcion = models.TextField("Descripcion de requisito", max_length=100, blank=True, null=True)
    documento = models.FileField("Subir documento", upload_to="docrequisitos", null = True, blank=True)

    def __str__(self):
        return self.nombre_documento
    
    class Meta:
        ordering = ['id']
        verbose_name = 'Padron de Requisito Inscripcion'
        verbose_name_plural = 'Padron de Requisitos Inscripcion'

class documento_solicitado_ciclo(Base):
    id_padron_documento_requisito = models.ForeignKey(padron_documento_requisito, on_delete=models.RESTRICT)
    id_ciclo = models.ForeignKey(ciclo, on_delete=models.RESTRICT)

    def __str__(self):
        return str(self.id_padron_documento_requisito)
    
    class Meta:
        ordering = ['id']
        verbose_name = "Documento Solicitado Inscripcion"
        verbose_name_plural = "Documentos Solicitado Inscripcion"
        
# ············ END REGION CICLO ··············· }}}

# ············ REGION INSCRIPCION ··············· {{{
class pago(Base):

    TURNOS = (
        ("MA", "MAÑANA"),
        ("TA", "TARDE"),
        ("NO", "NOCHE"),
    )
    nro_cuotas = models.PositiveIntegerField("Nro. de cuota(s)")
    tipo_colegio = models.CharField("Tipo de Colegio", max_length=10, choices=(("PR","Privado"),("PU", "Publico")))
    monto_total = models.DecimalField("Monto Total", max_digits=10, decimal_places=2, null=True)
    id_ciclo = models.ForeignKey(ciclo, on_delete=models.RESTRICT)
    #turno_pago = models.CharField("Turno", max_length=10, choices= TURNOS, null=True)
    def __str__(self):
        return str(self.nro_cuotas) + " Cuota(s) " + self.tipo_colegio

    class Meta:
        ordering = ['id']
        unique_together = ['id','id_ciclo']
        verbose_name = 'Pago'
        verbose_name_plural = 'Pagos'


class detalle_pago(Base):
    id_pago = models.ForeignKey(pago, on_delete=models.RESTRICT)
    nro_cuota = models.PositiveIntegerField("Nro. de cuota")
    monto_parcial = models.DecimalField("Monto Parcial", max_digits=10, decimal_places=2)
    especie_mora = models.CharField("Tipo de mora", max_length=50, choices=(("PORC","Porcentaje (%)"),("FIJO","Monto fijo")), null=True)
    monto_mora = models.DecimalField("Valor", max_digits=10, decimal_places=2, null=True)
    fecha_inicio = models.DateField("Fecha Inicio")
    fecha_fin = models.DateField("Fecha Final")

    def __str__(self):
        return str(self.id_pago) + " Cuota " + str(self.nro_cuota)

    class Meta:
        ordering = ['id']
        verbose_name = 'Detalle Pago'
        verbose_name_plural = 'Detalle Pagos'
        ordering = ['nro_cuota']


class preinscripcion(Base):

    IDIOMAS = (
        ("ES","ESPAÑOL"),
        ("BO","BORA"),
        ("MA","MATSIGENKA"),
        ("SK","SHIPIBO-KONIBO"),
        ("IN", "INGLES")
    )
    estado = models.BooleanField("Estado Activo", default=True)
    dni_persona = models.OneToOneField(persona, on_delete=models.RESTRICT)
    id_ciclo = models.ForeignKey(ciclo, on_delete=models.RESTRICT)
    id_escuela_profesional = models.ForeignKey(escuela_profesional, on_delete=models.RESTRICT, null=True)
    id_ubigeo = models.ForeignKey(ubigeo, on_delete=models.RESTRICT, verbose_name = "Lugar actual de residencia", blank=True, null=True)
    id_colegio = models.ForeignKey(colegio, on_delete=models.RESTRICT, null=True)
    idioma = models.CharField("Idioma", max_length=30, choices=IDIOMAS, null=True)
    progreso_preinscripcion = models.SmallIntegerField("Progreso Preinscripcion", default=1, null=True)
    direccion = models.CharField("Direccion", max_length=120, null=True)
    esta_enviado = models.BooleanField("Enviado", default=False, null=True)
    telefono_personal = models.CharField("Telefono", max_length=15, null=True)    
    email_respaldo = models.EmailField("Correo de contacto", blank=True, null=True)
    id_pago = models.ForeignKey(pago, on_delete=models.RESTRICT, null=True)
    nombres_apoderado = models.CharField("Nombre del apoderado", max_length=200, null=True, blank=True)
    telefono_apoderado = models.CharField("Telefono del apoderado", max_length=12,null=True, blank=True)
    condicion_discapacidad = models.BooleanField("Discapacidad", default=False)
    detalle_discapacidad = models.CharField("Especifique su discapacidad", max_length=100, null=True, blank=True)

    def __str__(self):
        return str(self.dni_persona)

    class Meta:
        ordering = ['id']
        verbose_name = 'Preinscripcion'
        verbose_name_plural = 'Preinscripciones'

class compromiso_pago(Base):
    id_preinscripcion = models.OneToOneField(preinscripcion, on_delete=models.RESTRICT)
    fecha_vencimiento = models.DateField("Fecha vencimiento", null=True)
    id_pago = models.ForeignKey(pago, on_delete=models.RESTRICT)
    def __str__(self):
        return str(self.id_preinscripcion)

    class Meta:
        ordering = ['id']
        verbose_name = "Compromiso de Pago"
        verbose_name_plural = "Compromisos de Pagos"
class detalle_compromiso_de_pago(Base):
    id_compromiso_pago = models.ForeignKey(compromiso_pago, on_delete=models.RESTRICT)
    codigo_compromiso_pago = models.CharField("Codigo de pago", max_length=50)
    numero_cuota = models.PositiveIntegerField("Nro. Cuota")
    monto = models.DecimalField("Monto a pagar", max_digits=10, decimal_places=2)
    fecha_inicio = models.DateField("Fecha inicio")
    fecha_fin = models.DateField("Fecha limite")
    esta_pagado = models.BooleanField("Pagado")
    monto_mora = models.DecimalField("Mora", max_digits=10, decimal_places=2, blank=True, null=True )
    fecha_pagado = models.DateField("Fecha de pago", blank = True, null=True)
    modalidad_pago = models.CharField("Medio de pago", max_length=40, blank=True, null=True)

    def __str__(self):
        return str(self.id_compromiso_pago) + " " + str(self.numero_cuota)

    class Meta:
        unique_together = ['id_compromiso_pago','numero_cuota',]
        verbose_name = "Detalle Compromiso Pago"
        verbose_name_plural = "Detalles Compromisos de Pago"
        ordering = ['id']
class inscripcion(Base):
    id_compromiso_pago = models.OneToOneField(compromiso_pago, on_delete=models.RESTRICT)
    estado_finalizado = models.BooleanField("Finalizado", default=False)
    def __str__(self):
        return str(self.id_compromiso_pago.id_preinscripcion)

    class Meta:
        ordering = ['id']
        verbose_name = "Inscripcion"
        verbose_name_plural = "Inscripciones"
# ············ END REGION INSCRIPCION ··············· }}}

class documentos_inscripcion(Base):
    id_inscripcion = models.ForeignKey(inscripcion, on_delete=models.RESTRICT, null=True)
    nombre_documento = models.CharField("Nombre", max_length=100, null=True, blank=True)
    documento = models.FileField("Documentos",upload_to='inscrito_files_path')
    esta_aprobado = models.BooleanField("Estado de aprovado", default=False)
    def __str__(self):
        return self.nombre_documento
    class Meta:
        ordering = ['id']
        verbose_name_plural = "Documentos de Inscripcion"
class documentos_inscripcion_revision(Base):
    id_documento_inscripcion = models.ForeignKey(documentos_inscripcion, on_delete=models.RESTRICT)
    esta_aprobado = models.BooleanField("Estado de aprovado", default=False)
    id_administrador = models.ForeignKey(administrador, on_delete=models.RESTRICT, null=True)

    def __str__(self):
        return self.id_documento_inscripcion.nombre_documento + " " + str(self.esta_aprobado)
    
    class Meta:
        ordering = ['id']
        verbose_name = "Documento de Inscripcion - Revision"
        verbose_name_plural = "Documentos de Inscripcion - Revision"
# ············· REGION CURSOS ······················ {{{
class padron_curso(Base):
    nombre_curso = models.CharField("Nombre del Curso", max_length=50)
    abreviacion = models.CharField("Abreviacion", max_length=10)
    descripcion = models.TextField("Descripcion", max_length=100, blank=True)
    estado = models.BooleanField("Estado", default=True)

    def __str__(self):
        return self.nombre_curso

    class Meta:
        ordering = ['id']
        verbose_name = "Padron de Cursos"
        verbose_name_plural = "Padron de Cursos"
    
class padron_cursos_grupo(Base):
    id_padron_curso = models.ForeignKey(padron_curso, on_delete=models.RESTRICT)
    hora_semana = models.PositiveIntegerField("Horas a la semana")
    id_grupo_academico = models.ForeignKey(grupo_academico, on_delete=models.RESTRICT)
    estado = models.BooleanField("Estado activo", default=True)
    nro_preguntas_examen = models.PositiveIntegerField("Preguntas para examen")

    def __str__(self):
        return str(self.id_padron_curso) + " Grupo " + str(self.id_grupo_academico.abreviacion)

    class Meta:
        ordering = ['id']
        verbose_name = "Padron cursos por grupo"
        verbose_name_plural = "Padron cursos por grupo"
    
class horario(Base):    
    id_ciclo = models.ForeignKey(ciclo, on_delete=models.RESTRICT)
    id_aula = models.ForeignKey(aula, on_delete=models.RESTRICT)
    id_docente = models.ForeignKey(docente, on_delete=models.RESTRICT)
    id_padron_cursos_grupo = models.ForeignKey(padron_cursos_grupo, on_delete=models.RESTRICT)
    enlace_meet = models.URLField("Enlace de sala virtual", blank=True, null=True)
    def __str__(self):
        return str(self.id_padron_cursos_grupo) + " " + str(self.id_aula)

    class Meta:
        ordering = ['id']
        verbose_name = "Horario"
        verbose_name_plural = "Horarios"

class horario_curso(Base):

    DIAS_DICTADO = (
        ('LUN','Lunes'),
        ('MAR','Martes'),
        ('MIE','Miercoles'),
        ('JUE','Jueves'),
        ('VIE','Viernes'),
        ('SAB','Sabado'),
        ('DOM','Domingo')
    )
    id_horario = models.ForeignKey(horario, on_delete=models.RESTRICT)
    dia_dictado = models.CharField(max_length=15, choices=DIAS_DICTADO)
    hora_inicio = models.TimeField("Hora Inicio")
    hora_fin = models.TimeField("Hora Fin")
    
    def __str__(self):
        return "Detalle "+ str(self.id_horario) 

    class Meta:
        ordering = ['id']
        verbose_name = "Detalle Horario Curso"
        verbose_name_plural = "Detalle Horario Cursos"
    
class material_curso(Base):
    descripcion_material = models.TextField("Descripcion")
    enlace_recurso = models.URLField("Link", null=True, blank=True)
    archivo_adjunto = models.FileField("Archivo", upload_to="materiales", null=True, blank=True)
    tipo_recurso = models.CharField("Tipo", max_length=10, choices=(("AVISO","AVISO"),("RECURSO","RECURSO")))
    id_horario = models.ForeignKey(horario, on_delete=models.RESTRICT)
    
    def __str__(self):
        return self.tipo_recurso + " - " + self.descripcion_material

    class Meta:
        verbose_name = "Material de clase"
        verbose_name_plural = "Materiales de clase"
        ordering = ('-fecha_registro',)

class balota_preguntas_curso(Base):
    texto_pregunta = models.TextField("Pregunta")
    img_pregunta = models.ImageField("Imagen", blank=True, null=True)
    id_padron_curso_grupo = models.ForeignKey(padron_cursos_grupo, on_delete=models.RESTRICT)
    id_docente = models.ForeignKey(docente, on_delete=models.RESTRICT)
    
    def __str__(self):
        return self.texto_pregunta
    
    class Meta:
        verbose_name = "Preguntas de balotario"
        verbose_name_plural = "Balotario"
        ordering = ("id",)

class alternativas_balotario(Base):
    texto_alternativa = models.TextField("Alternativa")
    es_respuesta = models.BooleanField("Respuesta")
    id_balota = models.ForeignKey(balota_preguntas_curso, on_delete=models.RESTRICT)

    def __str__(self):
        return self.texto_alternativa

    class Meta:
        verbose_name = "Alternativa"
        verbose_name = "Alternativas"
        ordering = ("id",)

# ············· ENDREGION CURSOS ······················ }}}

# ············· REGION ESTUDIANTE ······················ {{{
class estudiante(Base):
    id_inscripcion = models.OneToOneField(inscripcion, on_delete=models.RESTRICT)
    user_type = models.OneToOneField(CustomUser, on_delete=models.RESTRICT)
    tema_personalizado = models.PositiveIntegerField("Tema personalizado", default=1)
    foto_perfil = models.ImageField("Foto de perfil", upload_to="perfiles", null=True)

    def __str__(self):
        return str(self.id_inscripcion)

    class Meta:
        ordering = ['id']
        verbose_name = "Estudiante"
        verbose_name_plural = "Estudiantes"

class estudiante_horario(Base):
    id_estudiante = models.ForeignKey(estudiante, on_delete=models.RESTRICT)
    id_horario = models.ForeignKey(horario, on_delete=models.RESTRICT)

    def __str__(self):
        return str(self.id_estudiante)

    class Meta:
        ordering = ['id']
        verbose_name = "Horario de estudiante"
        verbose_name_plural = "Horarios de estudiante"
        
class asistencia_estudiante(Base):
    fecha_sesion = models.DateTimeField("Fecha sesion", auto_now_add = True)
    id_estudiante_horario = models.ForeignKey(estudiante_horario, on_delete=models.RESTRICT)
    estado_asistencia = models.BooleanField(default=False)
    def __str__(self):
        return str(self.id_estudiante_horario)

    class Meta:
        ordering = ['id']
        verbose_name = "Asistencia Estudiante"
        verbose_name_plural = "Asistencias Estudiante"
# ············· ENDREGION ESTUDIANTE ······················ }}}

# ············· REGION ASISTENCIA DOCENTE ······················ {{{

class asistencia_docente(Base):
    fecha_sesion = models.DateTimeField("Fecha registro", auto_now_add = True)
    id_horario = models.ForeignKey(horario, on_delete=models.RESTRICT)

    def __str__(self):
        return str(self.id_horario.id_docente)

    class Meta:
        ordering = ['id']
        verbose_name = "Asistencia Docente"
        verbose_name_plural = "Asistencias Docente"
# ············· ENDREGION ASISTENCIA DOCENTE ······················ }}}
class comentarios_clase(Base):
    texto_comentario =models.TextField("Comentario")
    archivo_adjunto = models.FileField("Archivo adjunto", upload_to="archivos_clase", null=True, blank=True)
    id_docente = models.ForeignKey(docente, max_length=100, on_delete=models.RESTRICT, null=True, blank=True)
    id_estudiante = models.ForeignKey(estudiante, max_length=100, on_delete=models.RESTRICT, null=True, blank=True)
    id_horario = models.ForeignKey(horario, on_delete=models.RESTRICT)

    def __str__(self):
        return self.texto_comentario
    
    class Meta:
        verbose_name = "Comentario de clase"
        verbose_name_plural = "Comentarios de clase"
        ordering = ("-fecha_registro",)

# ············· REGION EXAMENES ······················ {{{
class examen(Base):

    TIPO_EXAMEN = (
        ("PARCIAL","Parcial"),
        ("SIMULACRO","Simulacro"),
        #("CURSO","Curso especifico"),
    )

    fecha_examen = models.DateField("Fecha")
    denominacion_examen = models.CharField("Denominacion", max_length=50)
    tipo_examen = models.CharField("Tipo de examen", max_length=20, choices=TIPO_EXAMEN)
    nro_examen = models.PositiveIntegerField("Nro. de examen")
    hora_inicio = models.TimeField("Hora Inicio")
    hora_fin = models.TimeField("Hora Final")
    id_ciclo = models.ForeignKey(ciclo, on_delete=models.RESTRICT)

    def __str__(self):
        return self.denominacion_examen

    class Meta:
        ordering = ['id']
        verbose_name = "Examen"
        verbose_name_plural = "Examenes"

class examen_estudiante(Base):
    id_examen = models.ForeignKey(examen, on_delete=models.RESTRICT)
    id_estudiante = models.ForeignKey(estudiante, on_delete=models.RESTRICT)
    nota_promedio = models.DecimalField("Nota Promedio", max_digits=5, decimal_places=3)

    def __str__(self):
        return str(self.id_estudiante)

    class Meta:
        ordering = ['id']
        verbose_name = "Notas Estudiante"
        verbose_name_plural = "Notas Estudiantes"
    
class estudiante_notas_por_curso(Base):
    id_examen_estudiante = models.ForeignKey(examen_estudiante, on_delete=models.RESTRICT)
    notas_curso = models.DecimalField("Nota", max_digits=5, decimal_places=3)
    id_padron_curso = models.ForeignKey(padron_cursos_grupo, on_delete=models.RESTRICT)
    
    def __str__(self):
        return str(self.id_estudiante)

    class Meta:
        ordering = ['id']
        verbose_name = "Notas Estudiante Por Curso"
        verbose_name_plural = "Notas Estudiantes Por Curso"


# ············· ENDREGION EXAMENES ······················ }}}

# ················ REGION TESORERIA ······················{{{
class registro_tesoreria(Base):
    admin = models.ForeignKey(administrador, on_delete=models.RESTRICT, null=True)
    esta_pagado =models.BooleanField("Esta pagado", default=False)
    modalidad_pago = models.CharField("Modalidad de pago", max_length=40, null=True, blank=True)
    fecha_pago = models.DateField("Fecha de pago", null=True)
    id_detalle_compromiso = models.ForeignKey(detalle_compromiso_de_pago, on_delete=models.RESTRICT)

    def __str__(self):
        return str(self.id_detalle_compromiso)

    class Meta:
        ordering = ['id']
        verbose_name_plural = "Compromisos de pago tesoreria"

# ············· ENDREGION TESORERIA ······················ }}}
#·················· REGION EXAMENES ·······················{{{
class examen_grupo(Base):
    id_examen = models.ForeignKey(examen, on_delete=models.RESTRICT)
    id_grupo_academico = models.ForeignKey(grupo_academico, on_delete=models.RESTRICT)
    finalizado = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id_examen)
    
    class Meta:
        verbose_name = "Examen por grupo"
        verbose_name_plural = "Examenes por grupo"
        ordering = ['id']
    
class preguntas_examen_grupo(Base):
    id_examen_grupo = models.ForeignKey(examen_grupo, on_delete=models.RESTRICT)
    id_balota_curso = models.ForeignKey(balota_preguntas_curso, on_delete=models.RESTRICT)

    def __str__(self):
        return str(self.id_examen_grupo)
    
    class Meta:
        verbose_name = "Pregunta examen"
        verbose_name_plural = "Preguntas examen"


#··················· ENDREGION EXMENES ····················}}}



# ················ REGION SETTINGS ······················{{{
class tabla_configuraciones(models.Model):

    validacion_telefono = models.BooleanField("Validar telefono")
    validacion_email = models.BooleanField("Validar email")
    fuente_datos_persona = models.CharField("Importar desde", max_length=10, choices=(("PIDE","Datos PIDE"),("BDD","Base de datos local")))
    mostrar_enlace_tesoreria = models.BooleanField("Monstrar enlace a tesoreria en Incripcion")
    URL_tesoreria = models.URLField("Enlace a Tesoreria")
    direccion_pago_fisico = models.CharField("Direccion de caja", max_length=200, null=True)
    mostrar_pago_fisico = models.BooleanField("Mostrar pago fisico", default=True, null=True)    
    mostrar_pago_virtual = models.BooleanField("Mostrar pago virtual", default=True, null=True)

    def __str__(self):
        return "Configuracion global"
    class Meta:
        ordering = ['id']
        verbose_name = "Configuracion"
        verbose_name_plural = "Configuraciones"
# ················· ENDREGION SETTINGS ···················}}}