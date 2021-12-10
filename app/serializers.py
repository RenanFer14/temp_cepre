from rest_framework import serializers
from rest_framework import serializers
from app.models import *

class serializer_user(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = CustomUser
        fields = '__all__'

    def create(self, validated_data):
        user = super(serializer_user, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

class serializer_docente(serializers.ModelSerializer):
    class Meta:
        model = docente
        fields = '__all__'

class serializer_ubigeo(serializers.ModelSerializer):
    class Meta:
        model = ubigeo
        fields = '__all__'

class serializer_colegio(serializers.ModelSerializer):
    # ubigeo_id = serializers.PrimaryKeyRelatedField(queryset = ubigeo.objects.all(), write_only=True)
    # codigo_ubigeo =  serializers.ReadOnlyField(source="ubigeo.codigo_ubigeo", read_only=True)
    # nombre_ubigeo =  serializers.ReadOnlyField(source="ubigeo.nombre", read_only=True)
    
    class Meta:
        model = colegio
        fields = '__all__'
        #fields = ('id', 'ubigeo_id', 'codigo_ubigeo', 'nombre_ubigeo', 'nombre_colegio', 'tipo_colegio')

# ············ REGION INFRAESTRUCTURA ··············· {{{
class serializer_grupo_academico(serializers.ModelSerializer):
    class Meta:
        model = grupo_academico
        fields = '__all__'

class serializer_sede(serializers.ModelSerializer):
    class Meta:
        model = sede
        fields = '__all__'

class serializer_pabellon(serializers.ModelSerializer):
    class Meta:
        model = pabellon
        fields = '__all__'

class serializer_aula(serializers.ModelSerializer):
    class Meta:
        model = aula
        fields = '__all__'

# ············ END REGION INFRAESTRUCTURA ··············· }}}

# ············ REGION CICLO ··············· {{{
class serializer_ciclo(serializers.ModelSerializer):
    class Meta:
        model = ciclo
        fields = '__all__'

class serializer_documento_publicacion(serializers.ModelSerializer):
    class Meta:
        model = documento_publicacion
        fields = '__all__'

class serializer_pago(serializers.ModelSerializer):
    class Meta:
        model = pago
        fields = '__all__'

class serializer_detalle_pago(serializers.ModelSerializer):
    id_pago = serializer_pago()
    class Meta:
        model = detalle_pago
        fields = '__all__'
class serializer_detalle_pago_det(serializers.ModelSerializer):
    class Meta:
        model = detalle_pago
        fields = '__all__'

class serializer_preinscripcion(serializers.ModelSerializer):
    class Meta:
        model = preinscripcion
        fields = '__all__'

class serializer_compromiso_pago_oficial(serializers.ModelSerializer):
    class Meta:
        model = compromiso_pago
        fields = '__all__'

class serializer_detalle_compromiso_de_pago(serializers.ModelSerializer):
    class Meta:
        model = detalle_compromiso_de_pago
        fields = '__all__'

class serializer_inscripcion(serializers.ModelSerializer):
    class Meta:
        model = inscripcion
        fields = '__all__'

class serializer_padron_curso(serializers.ModelSerializer):
    class Meta:
        model = padron_curso
        fields = '__all__'
# ············ END REGION CICLO ··············· }}}

class serializer_persona(serializers.ModelSerializer):
    class Meta:
        model = persona
        fields = '__all__'

class serializer_administrador(serializers.ModelSerializer):
    class Meta:
        model = administrador
        fields = '__all__'

class serializer_user_int(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

class serializer_pagos(serializers.ModelSerializer):
    class Meta:
        model = pago
        fields = '__all__'

class serializer_detalle_pagos(serializers.ModelSerializer):
    class Meta:
        model = detalle_pago
        fields = '__all__'

class serializer_grupo_academico(serializers.ModelSerializer):
    class Meta:
        model = grupo_academico
        fields = '__all__'

class serializer_escuela_prof(serializers.ModelSerializer):
    class Meta:
        model = escuela_profesional
        fields = '__all__'

class serializer_detalle_compromiso_pago(serializers.ModelSerializer):
    class Meta:
        model = detalle_compromiso_de_pago
        fields = '__all__'


class serializer_escuela_profesional(serializers.ModelSerializer):
    class Meta:
        model = escuela_profesional
        fields = '__all__'



# ············· REGION CURSOS ······················ {{{
class serializer_padron_curso(serializers.ModelSerializer):
    class Meta:
        model = padron_curso
        fields = '__all__'


class serializer_padron_curso_grupo(serializers.ModelSerializer):
    class Meta:
        model = padron_cursos_grupo
        fields = '__all__'

class serializer_horario(serializers.ModelSerializer):
    class Meta:
        model = horario
        fields = '__all__'

class serializer_horario_curso(serializers.ModelSerializer):
    class Meta:
        model = horario_curso
        fields = '__all__'
# ············· ENDREGION CURSOS ······················ }}}

# ············· REGION ESTUDIANTE ······················ {{{
class serializer_estudiante_xd(serializers.ModelSerializer):
    class Meta:
        model = estudiante
        fields = '__all__'
class serializer_estudiante(serializers.ModelSerializer):
    user_type = serializer_user_int()
    class Meta:
        model = estudiante
        fields = '__all__'

class serializer_estudiante_horario(serializers.ModelSerializer):
    class Meta:
        model = estudiante_horario
        fields = '__all__'

class serializer_asistencia_estudiante(serializers.ModelSerializer):
    class Meta:
        model = asistencia_estudiante
        fields = '__all__'

class serializer_asistencia_docente(serializers.ModelSerializer):
    class Meta:
        model = asistencia_docente
        fields = '__all__'

class serializer_examen(serializers.ModelSerializer):
    #hora_inicio = serializers.TimeField(format='%I:%M %p', input_formats='%I:%M %p')
    #hora_fin = serializers.TimeField(format='%I:%M %p', input_formats='%I:%M %p')
    class Meta:
        model = examen
        fields = '__all__'

class serializer_examen_estudiante(serializers.ModelSerializer):
    class Meta:
        model = examen_estudiante
        fields = '__all__'

class serializer_estudiante_notas_por_curso(serializers.ModelSerializer):
    class Meta:
        model = estudiante_notas_por_curso
        fields = '__all__'

class serializer_registro_tesoreria(serializers.ModelSerializer):
    class Meta:
        model = registro_tesoreria
        fields = '__all__'

class serializer_configuraciones(serializers.ModelSerializer):
    class Meta:
        model = tabla_configuraciones
        fields = '__all__'

class serializer_documentos_inscripcion(serializers.ModelSerializer):
    class Meta:
        model = documentos_inscripcion
        fields = '__all__'
#··········· SOLO VISTA
class serializer_padron_documento_requisito(serializers.ModelSerializer):
    class Meta:
        model = padron_documento_requisito
        fields = '__all__'

class serializer_documentos_requisito_inscripcion(serializers.ModelSerializer):
    class Meta:
        model = documento_solicitado_ciclo
        fields = '__all__'

class serializer_material_curso(serializers.ModelSerializer):
    class Meta:
        model = material_curso
        fields = '__all__'

class serializer_comentarios_clase(serializers.ModelSerializer):
    class Meta:
        model = comentarios_clase
        fields = '__all__'

class serializer_balota_preguntas_curso(serializers.ModelSerializer):
    class Meta:
        model = balota_preguntas_curso
        fields = '__all__'

class serializer_alternativas_balotario(serializers.ModelSerializer):
    class Meta:
        model = alternativas_balotario
        fields = '__all__'

class serializer_documentos_inscripcion_revision(serializers.ModelSerializer):
    class Meta:
        model = documentos_inscripcion_revision
        fields = '__all__'
# ······································································        
class serializer_documentos_requisito_inscripcionver(serializers.ModelSerializer):
    id_padron_documento_requisito = serializer_padron_documento_requisito()
    class Meta:
        model = documento_solicitado_ciclo
        fields = '__all__'

class serializer_examen_grupo(serializers.ModelSerializer):
    class Meta:
        model = examen_grupo
        fields = '__all__'

class serializer_preguntas_examen_grupo(serializers.ModelSerializer):
    class Meta:
        model = preguntas_examen_grupo
        fields = '__all__'


# SERIALIZER JUST FOR SHOW INFORMATION
class serializer_preinscripcion_mostrar(serializers.ModelSerializer):
    dni_persona = serializer_persona()
    id_ciclo =serializer_ciclo()
    id_escuela_profesional = serializer_escuela_profesional()
    id_ubigeo = serializer_ubigeo()
    id_colegio = serializer_colegio()
    id_pago = serializer_pago()
    class Meta:
        model = preinscripcion
        fields = '__all__'        

class serializer_padron_curso_grupo_mostrar(serializers.ModelSerializer):
    id_padron_curso = serializer_padron_curso()
    id_grupo_academico = serializer_grupo_academico()
    class Meta:
        model = padron_cursos_grupo
        fields = '__all__'


class serializer_compromiso_pago(serializers.ModelSerializer):
    id_preinscripcion = serializer_preinscripcion_mostrar()
    class Meta:
        model = compromiso_pago
        fields = '__all__'

class serializer_preinscripcion_most(serializers.ModelSerializer):
    dni_persona = serializer_persona()
    id_ciclo = serializer_ciclo()
    id_escuela_profesional = serializer_escuela_profesional()
    class Meta:
        model = preinscripcion
        fields = '__all__'

class serializer_compromiso_pago_most(serializers.ModelSerializer):
    id_preinscripcion = serializer_preinscripcion_most()
    class Meta:
        model = compromiso_pago
        fields = '__all__'

class serializer_inscripcion_most(serializers.ModelSerializer):
    id_compromiso_pago = serializer_compromiso_pago_most()
    class Meta:
        model = inscripcion
        fields = '__all__'

class serializer_estudiante_most(serializers.ModelSerializer):
    id_inscripcion = serializer_inscripcion_most()
    class Meta:
        model = estudiante
        fields = '__all__'
        
class serializer_docente_mostrar(serializers.ModelSerializer):
    class Meta:
        model = docente
        fields = '__all__'
        
class serializer_horario_mostrar(serializers.ModelSerializer):
    id_padron_cursos_grupo = serializer_padron_curso_grupo_mostrar()    
    id_docente = serializer_docente_mostrar()
    id_ciclo = serializer_ciclo()
    id_aula = serializer_aula()
    class Meta:
        model = horario
        #fields = '__all__'
        exclude = ['fecha_registro', 'fecha_actualizacion']
class serializer_horario_curso_mostrar(serializers.ModelSerializer):
    id_horario = serializer_horario_mostrar()
    class Meta:
        model = horario_curso
        fields = '__all__'
        
class serializer_examen_estudiante_mostrar(serializers.ModelSerializer):
    id_examen = serializer_examen()
    class Meta:
        model = examen_estudiante
        fields = '__all__'

class serializer_material_curso_mostrar(serializers.ModelSerializer):
    id_horario = serializer_horario_mostrar()
    class Meta:
        model = material_curso
        #fields = '__all__'
        exclude = ['fecha_registro', 'fecha_actualizacion']

class serializer_comentario_clase_mostrar(serializers.ModelSerializer):
    id_horario = serializer_horario_mostrar()
    class Meta:
        model = comentarios_clase
        #fields = '__all__'
        exclude = ['fecha_registro', 'fecha_actualizacion']

class serializer_balota_preguntas_curso_mostrar(serializers.ModelSerializer):
    id_padron_curso_grupo =  serializer_padron_curso_grupo_mostrar()
    id_docente = serializer_docente()
    class Meta:
        model = balota_preguntas_curso
        #fields = '__all__'
        exclude = ['fecha_registro', 'fecha_actualizacion']

class serializer_alternativas_balota_mostrar(serializers.ModelSerializer):
    id_balota =  serializer_balota_preguntas_curso()
    class Meta:
        model = alternativas_balotario
        #fields = '__all__'
        exclude = ['fecha_registro', 'fecha_actualizacion']

class serializer_estudiante_horario_most(serializers.ModelSerializer):
    id_estudiante = serializer_estudiante()
    class Meta:
        model = estudiante_horario
        fields = '__all__'

class serializer_asistencia_estudiante_mostrar(serializers.ModelSerializer):
    id_estudiante_horario = serializer_estudiante_horario_most()
    class Meta:
        model = asistencia_estudiante
        fields = '__all__'
    
class serializer_documentos_inscripcion_mostrar(serializers.ModelSerializer):
    id_inscripcion = serializer_inscripcion_most()
    class Meta:
        model = documentos_inscripcion
        fields = '__all__'