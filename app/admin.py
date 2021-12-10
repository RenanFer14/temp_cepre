from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Permission
# Register your models here.
admin.site.register(material_curso)
admin.site.register(balota_preguntas_curso)
admin.site.register(alternativas_balotario)
admin.site.register(comentarios_clase)
#admin.site.register(CustomUser)
admin.site.register(documentos_inscripcion_revision)
admin.site.register(CustomUser , UserAdmin)
admin.site.register(ubigeo)
admin.site.register(grupo_academico)
admin.site.register(sede)
admin.site.register(pabellon)
admin.site.register(aula)
admin.site.register(asistencia_docente)
admin.site.register(asistencia_estudiante)
admin.site.register(examen)
admin.site.register(examen_estudiante)
admin.site.register(estudiante_notas_por_curso)
admin.site.register(persona)
admin.site.register(colegio)
admin.site.register(padron_documento_requisito)
admin.site.register(documento_solicitado_ciclo)
admin.site.register(horario_curso)
admin.site.register(horario)
admin.site.register(registro_tesoreria)
admin.site.register(preguntas_examen_grupo)
admin.site.register(examen_grupo)

#admin.site.register(detalle_pago)
admin.site.site_header = "Administracion del sitio CEPRE - UNIQ"
admin.site.site_title = "CEPRE - UNIQ"
admin.site.index_title = "Panel Administrativo"
class itemCiclo(admin.ModelAdmin):
    list_display = ('id', 'denominacion', 'fecha_inicio_ciclo', 'fecha_fin_ciclo',)
    list_display_links = ('id', 'denominacion')
    list_per_page = 10
    search_fields = ('denominacion',)

class itemEscuelaProfesional(admin.ModelAdmin):
    list_display = ('id', 'nombre_escuela_profesional', 'abreviacion')
    list_display_links = ('id', 'nombre_escuela_profesional')
    list_per_page = 10
    search_fields = ('nombre_escuela_profesional',)

class itemPagos(admin.ModelAdmin):
    list_display = ('id', 'tipo_colegio', 'monto_total')
    list_display_links = ('id',)
    list_per_page = 15
    search_fields = ('id',)

class itemPadronCurso(admin.ModelAdmin):
    list_display = ('id', 'nombre_curso', 'abreviacion', 'estado')
    list_display_links = ('id',)
    list_per_page = 15
    search_fields = ('id','nombre_curso')
    ordering = ['id']

admin.site.register(ciclo, itemCiclo)
admin.site.register(escuela_profesional, itemEscuelaProfesional)
admin.site.register(administrador)
admin.site.register(docente)
admin.site.register(documento_publicacion)
admin.site.register(pago, itemPagos)
admin.site.register(detalle_pago)
admin.site.register(preinscripcion)
admin.site.register(compromiso_pago)
admin.site.register(detalle_compromiso_de_pago)
admin.site.register(inscripcion)
admin.site.register(estudiante)
admin.site.register(padron_curso,itemPadronCurso)
admin.site.register(padron_cursos_grupo)
admin.site.register(estudiante_horario)
#admin.site.register(horario)
admin.site.register(tabla_configuraciones)
admin.site.register(documentos_inscripcion)
admin.site.register(Permission)