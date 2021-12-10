from rest_framework import viewsets
import datetime
from rest_framework import generics
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser, JSONParser
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import Http404, HttpResponse
from rest_framework.views import APIView
from app.models import *
from .serializers import *
from django.http import HttpResponse 
from django.db.models import Q
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveUpdateAPIView
import datetime
import json
import re
from .scrap import *
import bcrypt
import jwt
from django.shortcuts import get_object_or_404
from django.core.files.storage import FileSystemStorage #To upload Profile Picture
import random
# Email Field
from django.core.mail import send_mail
from django.conf import settings
from django.views.generic import View

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

# Create your views here.
class enviarEmailPreinscripcion(APIView):
    def post(self, request, pk):
        preinsc = preinscripcion.objects.get(id=pk)
        nombre_completo = preinsc.dni_persona
        dni = preinsc.dni_persona.dni
        escuela_prof = preinsc.id_escuela_profesional.nombre_escuela_profesional
        nombre_ciclo = preinsc.id_ciclo.denominacion
        cant_cuotas = preinsc.id_pago.nro_cuotas
        if cant_cuotas > 1: tipo_pago = 'En cuotas' 
        else: tipo_pago = 'Unico'
        compro = compromiso_pago.objects.get(id_preinscripcion=preinsc.id)
        detalle_cuotas = detalle_compromiso_de_pago.objects.filter(id_compromiso_pago=compro.id)

        email_to = request.data['email_destino']
        hmtl_content = render_to_string(
            "preinscripcion.html",{
                'nombre_completo': nombre_completo,
                'dni': dni,
                'escuela_profesional': escuela_prof,
                'denominacion_ciclo': nombre_ciclo,
                'tipo_pago': tipo_pago,
                'cantidad_cuotas' : cant_cuotas,
                'detalle_cuotas': detalle_cuotas
            },
        )
        text_content = strip_tags(hmtl_content)

        email = EmailMultiAlternatives(
            "BIENVENIDO AL CENTRO PREUNIVERSITARIO - UNIQ",
            text_content,
            settings.EMAIL_HOST_USER,
            [email_to]
        )

        email.attach_alternative(hmtl_content, "text/html")
        email.send()
        return Response({"message":"Enviado con exito"})

# Create your views here.
# ············ REGION EXTERNO ··············· {{{
class vista_ubigeo(viewsets.ModelViewSet):
    queryset = ubigeo.objects.all()
    serializer_class = serializer_ubigeo

    def get_queryset(self):
        tipo = self.request.GET.get('tipo', '')
        padre = self.request.GET.get('padre', '')

        q1 = Q(tipo_ubigeo = tipo)

        if tipo == 'P':
            q2 = Q(codigo_ubigeo__startswith = padre)
            return self.queryset.filter(q1, q2)


        return self.queryset.filter(q1)

class persona_list(ListCreateAPIView):
    queryset = persona.objects.all()
    serializer_class = serializer_persona

class persona_rud(RetrieveUpdateDestroyAPIView):
    queryset = persona.objects.all()
    serializer_class = serializer_persona

class colegio_list(ListCreateAPIView):
    queryset = colegio.objects.all()
    serializer_class = serializer_colegio

class colegio_rud(RetrieveUpdateDestroyAPIView):
    queryset = colegio.objects.all()
    serializer_class = serializer_colegio

@api_view(['POST'])
def login(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    user = CustomUser.objects.get(email=body['username'])
    if not bcrypt.hashpw(body['password'].encode('utf-8'), user.password.encode('utf-8')):
        return HttpResponse('No autorizado', status=401)
    token = jwt.encode({"sub": user.id}, "secret", algorithm="HS256")
    return Response(token)



# ············ ENDREGION EXTERNO ··············· }}}
@api_view(['GET'])
def consulta_persona(request):
    dni = ""
    dni = request.GET.get('dni')
    if dni == None or re.compile('[0-9]{8}').match(dni) == None:
        raise serializers.ValidationError('DNI no válido')
    try:
        opersona = persona.objects.get(dni=dni)
        return Response(serializer_persona(opersona).data)
    except persona.DoesNotExist:
        raise Http404


# ············ REGION PIDE ··············· {{{


# ············ ENDREGION PIDE ··············· }}}

# ············ REGION INFRAESTRUCTURA ··············· {{{
class grupo_academico_list(ListCreateAPIView):
    queryset = grupo_academico.objects.all()
    serializer_class = serializer_grupo_academico

class grupo_academico_rud(RetrieveUpdateDestroyAPIView):
    queryset = grupo_academico.objects.all()
    serializer_class = serializer_grupo_academico


class escuela_profesional_list(ListCreateAPIView):
    queryset = escuela_profesional.objects.all()
    serializer_class = serializer_escuela_profesional

    def get_queryset(self):
        grupo = self.request.GET.get('grupo', None)
        if grupo != None:
            q = Q(grupo = grupo)
            return self.queryset.filter(q)

        return self.queryset.all()

class escuela_profesional_rud(RetrieveUpdateDestroyAPIView):
    queryset = escuela_profesional.objects.all()
    serializer_class = serializer_escuela_profesional


class sede_list(ListCreateAPIView):
    queryset = sede.objects.all()
    serializer_class = serializer_sede

class sede_rud(RetrieveUpdateDestroyAPIView):
    queryset = sede.objects.all()
    serializer_class = serializer_sede


class pabellon_list(ListCreateAPIView):
    queryset = pabellon.objects.all()
    serializer_class = serializer_pabellon

class pabellon_rud(RetrieveUpdateDestroyAPIView):
    queryset = pabellon.objects.all()
    serializer_class = serializer_pabellon


class aula_list(ListCreateAPIView):
    queryset = aula.objects.all()
    serializer_class = serializer_aula

class aula_rud(RetrieveUpdateDestroyAPIView):
    queryset = aula.objects.all()
    serializer_class = serializer_aula
# ············ END REGION INFRAESTRUCTURA ··············· }}}

# ············ REGION CICLO ··············· {{{
class ciclo_list(ListCreateAPIView):
    queryset = ciclo.objects.all()
    serializer_class = serializer_ciclo

class ciclo_rud(RetrieveUpdateDestroyAPIView):
    queryset = ciclo.objects.all()
    serializer_class = serializer_ciclo


class documento_publicacion_list(ListCreateAPIView):
    queryset = documento_publicacion.objects.all()
    serializer_class = serializer_documento_publicacion

class documento_publicacion_rud(RetrieveUpdateDestroyAPIView):
    queryset = documento_publicacion.objects.all()
    serializer_class = serializer_documento_publicacion

# ············ END REGION CICLO ··············· }}}

# ············ REGION INSCRIPCION ··············· {{{
class pago_list(ListCreateAPIView):
    queryset = pago.objects.all()
    serializer_class = serializer_pago

class pago_rud(RetrieveUpdateDestroyAPIView):
    queryset = pago.objects.all()
    serializer_class = serializer_pago


class detalle_pago_list(ListCreateAPIView):
    queryset = detalle_pago.objects.all()
    serializer_class = serializer_detalle_pago

class detalle_pago_rud(RetrieveUpdateDestroyAPIView):
    queryset = detalle_pago.objects.all()
    serializer_class = serializer_detalle_pago


class preinscripcion_list(ListCreateAPIView):
    queryset = preinscripcion.objects.all()
    serializer_class = serializer_preinscripcion

class preinscripcion_rud(RetrieveUpdateDestroyAPIView):
    queryset = preinscripcion.objects.all()
    serializer_class = serializer_preinscripcion


class compromiso_pago_list(ListCreateAPIView):
    queryset = compromiso_pago.objects.all()
    serializer_class = serializer_compromiso_pago

class compromiso_pago_rud(RetrieveUpdateDestroyAPIView):
    queryset = compromiso_pago.objects.all()
    serializer_class = serializer_compromiso_pago


class detalle_compromiso_de_pago_list(ListCreateAPIView):
    queryset = detalle_compromiso_de_pago.objects.all()
    serializer_class = serializer_detalle_compromiso_de_pago

class detalle_compromiso_de_pago_rud(RetrieveUpdateDestroyAPIView):
    queryset = detalle_compromiso_de_pago.objects.all()
    serializer_class = serializer_detalle_compromiso_de_pago


class inscripcion_list(ListCreateAPIView):
    queryset = inscripcion.objects.all()
    serializer_class = serializer_inscripcion

class inscripcion_rud(RetrieveUpdateDestroyAPIView):
    queryset = inscripcion.objects.all()
    serializer_class = serializer_inscripcion


class docente_list(ListCreateAPIView):
    queryset = docente.objects.all()
    serializer_class = serializer_docente

class docente_rud(RetrieveUpdateDestroyAPIView):
    queryset = docente.objects.all()
    serializer_class = serializer_docente

class admin_list(ListCreateAPIView):
    queryset = administrador.objects.all()
    serializer_class = serializer_administrador

class admin_rud(RetrieveUpdateDestroyAPIView):
    queryset = administrador.objects.all()
    serializer_class = serializer_administrador

class user_list(ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = serializer_user

class user_rud(RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = serializer_user
    # ············ END REGION INSCRIPCION ··············· }}}


# ············· REGION CURSOS ······················ {{{
class padron_curso_list(ListCreateAPIView):
    queryset = padron_curso.objects.all()
    serializer_class = serializer_padron_curso

class padron_curso_rud(RetrieveUpdateDestroyAPIView):
    queryset = padron_curso.objects.all()
    serializer_class = serializer_padron_curso


class padron_cursos_grupo_list(ListCreateAPIView):
    queryset = padron_cursos_grupo.objects.all()
    serializer_class = serializer_padron_curso_grupo

class padron_cursos_grupo_rud(RetrieveUpdateDestroyAPIView):
    queryset = padron_cursos_grupo.objects.all()
    serializer_class = serializer_padron_curso_grupo


class horario_list(ListCreateAPIView):
    queryset = horario.objects.all()
    serializer_class = serializer_horario

class horario_rud(RetrieveUpdateDestroyAPIView):
    queryset = horario.objects.all()
    serializer_class = serializer_horario


class horario_curso_list(ListCreateAPIView):
    queryset = horario_curso.objects.all()
    serializer_class = serializer_horario_curso

class horario_curso_rud(RetrieveUpdateDestroyAPIView):
    queryset = horario_curso.objects.all()
    serializer_class = serializer_horario_curso
# ············· ENDREGION CURSOS ······················ }}}

# ············· REGION ESTUDIANTE ······················ {{{
class estudiante_list(ListCreateAPIView):
    queryset = estudiante.objects.all()
    serializer_class = serializer_estudiante

class estudiante_rud(RetrieveUpdateDestroyAPIView):
    queryset = estudiante.objects.all()
    serializer_class = serializer_estudiante


class estudiante_horario_list(ListCreateAPIView):
    queryset = estudiante_horario.objects.all()
    serializer_class = serializer_estudiante_horario

class estudiante_horario_rud(RetrieveUpdateDestroyAPIView):
    queryset = estudiante_horario.objects.all()
    serializer_class = serializer_estudiante_horario


class estudiante_horario_list(ListCreateAPIView):
    queryset = estudiante_horario.objects.all()
    serializer_class = serializer_estudiante_horario

class estudiante_horario_rud(RetrieveUpdateDestroyAPIView):
    queryset = estudiante_horario.objects.all()
    serializer_class = serializer_estudiante_horario

class asistencia_estudiante_list(ListCreateAPIView):
    queryset = asistencia_estudiante.objects.all()
    serializer_class = serializer_asistencia_estudiante

class asistencia_estudiante_rud(RetrieveUpdateDestroyAPIView):
    queryset = asistencia_estudiante.objects.all()
    serializer_class = serializer_asistencia_estudiante

# ············· ENDREGION ESTUDIANTE ······················ }}}

# ············· REGION ASISTENCIA DOCENTE ······················ {{{
class asistencia_docente_list(ListCreateAPIView):
    queryset = asistencia_docente.objects.all()
    serializer_class = serializer_asistencia_docente

class asistencia_docente_rud(RetrieveUpdateDestroyAPIView):
    queryset = asistencia_docente.objects.all()
    serializer_class = serializer_asistencia_docente
# ············· ENDREGION ASISTENCIA DOCENTE ······················ }}}

# ············· REGION EXAMENES ······················ {{{
class examen_list(ListCreateAPIView):
    queryset = examen.objects.all()
    serializer_class = serializer_examen

class examen_rud(RetrieveUpdateDestroyAPIView):
    queryset = examen.objects.all()
    serializer_class = serializer_examen

class examen_estudiante_list(ListCreateAPIView):
    queryset = examen_estudiante.objects.all()
    serializer_class = serializer_examen_estudiante

class examen_estudiante_rud(RetrieveUpdateDestroyAPIView):
    queryset = examen_estudiante.objects.all()
    serializer_class = serializer_examen_estudiante

class estudiante_notas_por_curso_list(ListCreateAPIView):
    queryset = estudiante_notas_por_curso.objects.all()
    serializer_class = serializer_estudiante_notas_por_curso

class estudiante_notas_por_curso_rud(RetrieveUpdateDestroyAPIView):
    queryset = estudiante_notas_por_curso.objects.all()
    serializer_class = serializer_estudiante_notas_por_curso
# ············· ENDREGION EXAMENES ······················ }}}

# ············· REGION TESORERIA ······················ {{{
class registro_tesoreria_list(ListCreateAPIView):
    queryset = registro_tesoreria.objects.all()
    serializer_class = serializer_registro_tesoreria

class registro_tesoreria_rud(RetrieveUpdateDestroyAPIView):
    queryset = registro_tesoreria.objects.all()
    serializer_class = serializer_registro_tesoreria
# ············· ENDREGION TESORERIA ······················ }}}
# ············· REGION ASISTENCIA DOCENTE ······················ {{{
class configuracion_list(ListCreateAPIView):
    queryset = tabla_configuraciones.objects.all()
    serializer_class = serializer_configuraciones

class configuracion_rud(RetrieveUpdateDestroyAPIView):
    queryset = tabla_configuraciones.objects.all()
    serializer_class = serializer_configuraciones
# ············· ENDREGION ASISTENCIA DOCENTE ······················ }}}


# ············· PROCESOS APIView·······························
 
# ·············· REGION PREINSCRIPCION ··················{{{
class preinscripcionListCreateAPIView(APIView):
    def get(self, request, format=None):
        snippets = preinscripcion.objects.all()
        serializer = serializer_preinscripcion(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        entrada_data = request.data
        dni_entrada = entrada_data['dni']
        try:
            persona_entr = persona.objects.get(dni=dni_entrada)
            data = json.dumps(entrada_data)
            data = json.loads(data)
            data['dni_persona'] = persona_entr.id
            preinscripcion_nuevo = serializer_preinscripcion(data=data)
            if preinscripcion_nuevo.is_valid(raise_exception=True):
                preinscripcion_save = preinscripcion_nuevo.save()
            return Response({
                "persona_data" : serializer_persona(persona_entr).data,
                "preinscripcion_data": preinscripcion_nuevo.data
            })
        except persona.DoesNotExist:
            serializer_person = serializer_persona(data = entrada_data)
            if serializer_person.is_valid(raise_exception=True):
                persona_save = serializer_person.save()

            ult_persona = persona.objects.get(dni=dni_entrada)
            data = json.dumps(entrada_data)
            data = json.loads(data)
            data['dni_persona'] = ult_persona.id
            serializer_preinscr = serializer_preinscripcion(data = data)
            if serializer_preinscr.is_valid(raise_exception=True):
                preinsc_save = serializer_preinscr.save()         

            return Response({
                "persona_data" : serializer_person.data,
                "preinscripcion_data": serializer_preinscr.data
            })
    def put(self, request, format=None, pk=None):
        if pk:
            try:
                preinsc = preinscripcion.objects.get(id=pk)
                print("preincripcion",preinsc)
                persona_ = persona.objects.get(id=preinsc.dni_persona.id)
                print("persona", persona_)
                preinscrito_update = serializer_preinscripcion(preinsc, data = request.data)
                if preinscrito_update.is_valid():
                    preinscripcion_update = preinscrito_update.save()

                persona_update = serializer_persona(persona_, data = request.data)
                if persona_update.is_valid():
                    preinscripcion_update = persona_update.save()

                return Response({
                    "persona_data" : persona_update.data,
                    "preinscripcion_data": preinscrito_update.data
                })                

            except preinscripcion.DoesNotExist:
                return Response({
                    "error": "No existe registros"
                })
@api_view(['GET', 'POST', 'PUT', 'PATCH'])
def preinscripcion_update(request, pk=None):
    entrada_data = request.data
    preinscrito = preinscripcion.objects.filter(id=pk).first()
    persona_ = persona.objects.get(id=preinscrito.dni_persona.id)
    if preinscrito:
        #RETRIEVE INFORMATION
        if request.method == 'GET':
            preinscrito_serializer = serializer_preinscripcion(preinscrito)
            return Response(preinscrito_serializer.data, status = status.HTTP_200_OK)
        #UPDATE INFORMATION
        elif request.method == 'PUT':
            preinscrito_serializer = serializer_preinscripcion(preinscrito, data = request.data)
            if preinscrito_serializer.is_valid(raise_exception=True):
                preinscripcion_update = preinscrito_serializer.save()
            persona_serializer = serializer_persona(persona_, data = request.data, partial=True)
            if persona_serializer.is_valid(raise_exception=True):
                persona_update = persona_serializer.save()
                return Response({
                    "preinscripcion_data": preinscrito_serializer.data,
                    "persona_data" : persona_serializer.data
                })
        elif request.method == 'PATCH':
            preinscrito_serializer = serializer_preinscripcion(preinscrito, data = request.data, partial=True)
            if preinscrito_serializer.is_valid(raise_exception=True):
                preinscripcion_update = preinscrito_serializer.save()
                
            persona_serializer = serializer_persona(persona_, data = request.data, partial=True)
            if persona_serializer.is_valid(raise_exception=True):
                persona_update = persona_serializer.save()
                return Response({
                    "preinscripcion_data": preinscrito_serializer.data,
                    "persona_data" : persona_serializer.data
                })

        elif request.method == 'POST' and preinscrito.esta_enviado == True:
            """················· COMPROMISO DE PAGO ··················"""
            ultimo_reg_preinsc = preinscrito
            print(preinscrito)
            #Se agrega el campo id_preinscripcion
            data = json.dumps(entrada_data)
            data = json.loads(data)
            data['id_preinscripcion'] = ultimo_reg_preinsc.id
            # ············ DATOS A GUARDAR ···············
            serializerCompromisoPago = serializer_compromiso_pago_oficial(data=data)
            if serializerCompromisoPago.is_valid(raise_exception=True):
                compromiso_pago_save = serializerCompromisoPago.save()
            """ ·········· DETALLE COMPROMISO DE PAGO & TESORERIA ··········· """
            #RECUPERANDO EL ULTIMO REGISTRO
            ultimo_reg_compromiso_pago = compromiso_pago.objects.filter(id_preinscripcion=preinscrito.id).first()
            pago_det = ultimo_reg_preinsc.id_pago
            nroCuotas = pago_det.nro_cuotas
            # EDITAR LA INFORMACION DENTRO DEL REQUEST
            datos_det_compromiso = json.dumps(entrada_data)
            datos_det_compromiso = json.loads(datos_det_compromiso)
                    
            #DATOS DE LA TABLA CICLO
            dni = ultimo_reg_preinsc.dni_persona.dni
            info_anio_ciclo = ultimo_reg_preinsc.id_ciclo.anio
            info_nro_ciclo = ultimo_reg_preinsc.id_ciclo.nro_ciclo_de_año
            tipo_colegio = ultimo_reg_preinsc.id_colegio.tipo_colegio
            #generarCod(dni, info_nro_ciclo, (i+1), tipo_colegio)
            for i in range(0,nroCuotas):
                detalle_pago_seleccionado = detalle_pago.objects.get(id_pago=pago_det.id, nro_cuota=(i+1))
                datos_det_compromiso['id_compromiso_pago'] = ultimo_reg_compromiso_pago.id
                datos_det_compromiso['codigo_compromiso_pago'] = generarCod(dni, info_nro_ciclo, (i+1), tipo_colegio)
                datos_det_compromiso['numero_cuota'] = (i+1)
                datos_det_compromiso['monto'] = detalle_pago_seleccionado.monto_parcial
                datos_det_compromiso['fecha_inicio'] = detalle_pago_seleccionado.fecha_inicio
                datos_det_compromiso['fecha_fin'] = detalle_pago_seleccionado.fecha_fin
                datos_det_compromiso['esta_pagado'] = False
                datos_det_compromiso['monto_mora'] = 0
                datos_det_compromiso['modalidad_pago'] = ""
                
                serializerDetCompromisoPago = serializer_detalle_compromiso_de_pago(data=datos_det_compromiso)
                if serializerDetCompromisoPago.is_valid(raise_exception=True):
                    det_compromiso_pago_save = serializerDetCompromisoPago.save()
                """ ················ TESORERIA ···················· """
                ultimo_detalle_compromiso = detalle_compromiso_de_pago.objects.filter(id_compromiso_pago=ultimo_reg_compromiso_pago.id, numero_cuota=(i+1)).first()
                datos_det_compromiso['id_detalle_compromiso'] = ultimo_detalle_compromiso.id
                print(datos_det_compromiso)
                serializerRegistroTesoreria = serializer_registro_tesoreria(data=datos_det_compromiso)
                if serializerRegistroTesoreria.is_valid(raise_exception=True):
                    compromiso_pago_save = serializerRegistroTesoreria.save()
            
        return Response({
            "success": "PREINSCRIPCION"           
        })
class eliminar_preinscripcion_incompleta(APIView):
    def delete(self, request,pk, format=None):
        try:
            preinsc = preinscripcion.objects.get(id=pk)
            preinsc.delete()
            return Response({
                "message":"eliminado correctamente"
            })
        except preinscripcion.DoesNotExist:
            return Response({
                "message":"No se encontraron registros"
            })
# ··············· ENDREGION PREINSCRIPCION ··············}}}

# ··············· REGION VALDACION DNI ··············}}}
class validacionConsultaDNI(APIView):
    def post(self, request, format=None):
        entrada_data = request.data
        dni = entrada_data['dni']
        settings = tabla_configuraciones.objects.all()[0]
        if settings.fuente_datos_persona == "BDD":
            try:
                #consulta si exite una persona con ese dni en la tabla persona
                persona_consulta = persona.objects.get(dni=dni)            
                if persona_consulta:
                    try:
                        #consulta si exite un registro de preinscricion activa
                        preinscripcion_consulta = preinscripcion.objects.get(dni_persona=persona_consulta)
                        if preinscripcion_consulta:
                            serializer_preins = serializer_preinscripcion(preinscripcion_consulta)
                            serializer_person = serializer_persona(persona_consulta)
                            return Response({
                                "exists_preinscripcion": True,
                                "preinscripcion_data": serializer_preins.data,
                                "persona_data": serializer_person.data
                            })
                    except preinscripcion.DoesNotExist:
                        pass
                    edad = datetime.date.today().year - int(persona_consulta.fecha_nacimiento.strftime('%Y'))
                    if edad >= 18:
                        serializer = serializer_persona(persona_consulta)
                        return Response({
                            "exists_preinscripcion": False,
                            "is_valid_person" : True,
                            "with_data": True,
                            "person_data": serializer.data
                        })
                    else:
                        return Response({
                            "exists_preinscripcion": False,
                            "is_valid_person" : True,
                            "with_data": False,
                            "dni":dni

                        })
            except persona.DoesNotExist:
                return Response({
                    "exists" : False,
                    "dni": dni
                })
        elif settings.fuente_datos_persona == "PIDE":
            status, datosWeb = consultaDNI(dni)
            if status == 200:
                data_person = json.loads(datosWeb)
                try:
                #consulta si exite una persona con ese dni en la tabla persona
                    persona_consulta = persona.objects.get(dni=dni)            
                    if persona_consulta:
                        try:
                            #consulta si exite un registro de preinscricion activa
                            preinscripcion_consulta = preinscripcion.objects.get(dni_persona=persona_consulta)
                            if preinscripcion_consulta:
                                serializer_preins = serializer_preinscripcion(preinscripcion_consulta)
                                serializer_person = serializer_persona(persona_consulta)
                                return Response({
                                    "exists_preinscripcion": True,
                                    "preinscripcion_data": serializer_preins.data,
                                    "persona_data": data_person
                                })
                        except preinscripcion.DoesNotExist:
                            pass
                        edad = datetime.date.today().year - int(persona_consulta.fecha_nacimiento.strftime('%Y'))
                        if edad >= 18:
                            serializer = serializer_persona(persona_consulta)
                            return Response({
                                "exists_preinscripcion": False,
                                "is_valid_person" : True,
                                "with_data": True,
                                "persona_data": data_person
                            })
                        else:
                            return Response({
                                "exists_preinscripcion": False,
                                "is_valid_person" : True,
                                "with_data": False,
                                "dni":dni
                            })
                except persona.DoesNotExist:
                    return Response({
                    "exists_preinscripcion": False,
                    "persona_data": data_person
                })
            else:
                return Response({
                    "exists": False,
                    "dni": dni
                })
# ··············· ENDREGION VALIDACION DNI ··············}}}
# ··············· REGION COMPROMISO PAGO ··············{{{
class compromisoPagoView(APIView):
    def get(self, request, format=None):
        snippets = compromiso_pago.objects.all()
        serializer = serializer_compromiso_pago(snippets, many=True)
        return Response(serializer.data)
# ··············· ENDREGION COMPROMISO PAGO ··············}}}
# ··············· REGION DETALLES COMPROMISO PAGO ··············{{{
class detalleCompromisoPagoView(APIView):
    def get(self, request, format=None,pk=None):
        if pk:
            try:
                preinsc = preinscripcion.objects.get(id=pk)
                print(preinsc.id)
                try:
                    compromiso_pago_id = compromiso_pago.objects.get(id_preinscripcion=preinsc.id)
                    print(compromiso_pago_id.id)
                    escuela_prof = preinsc.id_escuela_profesional.nombre_escuela_profesional
                    ciclo = preinsc.id_ciclo.denominacion
                    nrocuotas = preinsc.id_pago.nro_cuotas
                    snippets = detalle_compromiso_de_pago.objects.filter(id_compromiso_pago=compromiso_pago_id.id)
                    serializer = serializer_detalle_compromiso_de_pago(snippets, many=True)
                    return Response({
                        "data": serializer.data,
                        "escuela_profesional": escuela_prof,
                        "ciclo": ciclo,
                        "nroCuotas": nrocuotas
                    })
                except compromiso_pago.DoesNotExist:
                    return Response({
                        "error": "something goes wrong"
                    })

            except preinscripcion.DoesNotExist:
                return Response({
                    "error": "No existe registros"
                })
        else:
            snippets = detalle_compromiso_de_pago.objects.all()
            serializer = serializer_detalle_compromiso_de_pago(snippets, many=True)
            return Response(serializer.data)
# ··············· ENDREGION DETALLES COMPROMISO PAGO ··············}}}


# ·················· INSCRIPCION ·····························
# ··············· REGION VALIDACION DE PREINSCRIPCION ··············{{{
class validacion_preinscripcion(APIView):
    def post(self, request, format=None):
        entrada_data = request.data
        dni = entrada_data['dni']
        fecha_nac = entrada_data['fecha_nacimiento']
        ciclo = entrada_data['id_ciclo']
        fecha_dato = datetime.datetime.strptime(fecha_nac, "%Y-%m-%d").date()
        try:
            persona_dni = persona.objects.get(dni=dni, fecha_nacimiento= fecha_dato)
            try:
                preinscripcion_consulta = preinscripcion.objects.get(dni_persona=persona_dni, id_ciclo=ciclo)
                try:
                    compromiso_consulta = compromiso_pago.objects.get(id_preinscripcion=preinscripcion_consulta.id)
                    detalles = detalle_compromiso_de_pago.objects.get(id_compromiso_pago=compromiso_consulta, numero_cuota=1)
                    if detalles.esta_pagado == True:
                        serializer = serializer_preinscripcion_mostrar(preinscripcion_consulta)
                        insc = inscripcion.objects.get(id_compromiso_pago=compromiso_consulta.id)
                        serial = serializer_inscripcion(insc)
                        return Response({
                                "is_valid" : True,
                                "with_data": True,
                                "preinscripcion_data": serializer.data,
                                "inscripcion": serial.data
                            })
                    else:
                        return Response({
                            "is_valid": False,
                            "esta_pagado": False,
                            "message": "Realiza el pago de tu primera cuota para poder inscribirte"
                        })
                except compromiso_pago.DoesNotExist:
                    return Response({
                        "is_valid": False,
                        "esta_pagado": False,
                        "message": "Finaliza tu preinscripcion para poder realizar tu pago e inscrbirte"
                    })
            except preinscripcion.DoesNotExist:
                return Response({
                    "is_valid": False,
                    "esta_pagado": False,
                    "message": "Realiza tu preinscripcion para iniciar con los procesos de matricula"
                })                        
        except persona.DoesNotExist:
            return Response({
                "is_valid" : False
            })
# ··············· ENDREGION VALIDACION DE INSCRIPCION ··············}}}

# ···················· REGION UBIGEO ······················{{{
class ubigeoDepartamento(APIView):
    def get(self, request, format=None):        
        departamentos = ubigeo.objects.filter(tipo_ubigeo='D')
        serializer = serializer_ubigeo(departamentos, many=True)
        if len(serializer.data) != 0:
            return Response(serializer.data)
        else:
            departamentos = extraerDepartamentos()
            departamentos_ = json.dumps(departamentos)
            departamentos_ = json.loads(departamentos_)
            for i in departamentos_:
                i['codigo_ubigeo'] = i['codigo']
                i['tipo_ubigeo'] = i['tipo']
                del i['codigo']
                del i['tipo']
            for i in departamentos_:
                serializer_dep = serializer_ubigeo(data=i)
                if serializer_dep.is_valid(raise_exception=True):
                    serializer_dep.save()
            #serializer = serializer_ubigeo(departamentos_, many=True)
            return Response(departamentos_)
class ubigeoProv(APIView):
    def get(self, request, ubigeo_, format=None):
        #dep = request.data['departamento']
        prov_ubigeo = ubigeo.objects.filter(codigo_ubigeo__startswith=ubigeo_[0:2], tipo_ubigeo='P')
        serializer_prov = serializer_ubigeo(prov_ubigeo, many=True)
        if len(serializer_prov.data) != 0:
            return Response(serializer_prov.data)
        else:
            provincia = extraerProvincia(ubigeo_)
            provincia_ = json.dumps(provincia)
            provincia_ = json.loads(provincia_)
            for i in provincia_:
                i['codigo_ubigeo'] = i['codigo']
                i['tipo_ubigeo'] = i['tipo']
                del i['codigo']
                del i['tipo']
            for i in provincia_:
                serializer_pro = serializer_ubigeo(data=i)
                if serializer_pro.is_valid(raise_exception=True):
                    serializer_pro.save()
            prov_ubigeo = ubigeo.objects.filter(codigo_ubigeo__startswith=ubigeo_[0:2], tipo_ubigeo='P')
            serializer_prov = serializer_ubigeo(prov_ubigeo, many=True)
            return Response(serializer_prov.data)
        
        ''' try:
            departamento_ubigeo = ubigeo.objects.filter(codigo_ubigeo__startswith=dep[0:2], tipo_ubigeo='P')
            serializer_prov = serializer_ubigeo(departamento_ubigeo, many=True)
            return Response(serializer_prov.data)
        except ubigeo.DoesNotExist:
            return Response({
                "message": "no hay datos"
            }) '''
class ubigeoDist(APIView):
    def get(self, request, prov ,format=None):
        #prov = request.data['provincia']
        dist_ubigeo = ubigeo.objects.filter(codigo_ubigeo__startswith=prov[0:4], tipo_ubigeo='I')
        serializer_dis = serializer_ubigeo(dist_ubigeo, many=True)
        if len(serializer_dis.data) != 0:
            return Response(serializer_dis.data)
        else:
            distrito = extraerDistrito(prov)
            distrito_ = json.dumps(distrito)
            distrito_ = json.loads(distrito_)
            for i in distrito_:
                i['codigo_ubigeo'] = i['codigo']
                i['tipo_ubigeo'] = i['tipo']
                del i['codigo']
                del i['tipo']

            for i in distrito_:
                serializer_dis = serializer_ubigeo(data=i)
                if serializer_dis.is_valid(raise_exception=True):
                    serializer_dis.save()
            dist_ubigeo = ubigeo.objects.filter(codigo_ubigeo__startswith=prov[0:4], tipo_ubigeo='I')
            serializer_dis = serializer_ubigeo(dist_ubigeo, many=True)
            return Response(serializer_dis.data)
class UbigeoColegio(APIView):
    def get(self, request, distr, tipo, format=None):
        #distr = request.data['distrito']
        colegio_s = consultaColegios(distr)
        colegio_ = json.dumps(colegio_s)
        colegio_ = json.loads(colegio_)
        
        for i in colegio_:
            i['id_ubigeo'] = distr
            i['nombre_colegio'] = i['nombre']
            i['codigo_modular'] = i['codigo']
            i['direccion_colegio'] = i['direccion']
            i['ubigeo_nombre'] = i['distritoNombre']
            del i['codigo']
            del i['nombre']
            del i['direccion']
            del i['distritoNombre']
            del i['id']
            del i['distrito']
            del i['nivelEscuelaNombre']
            if i['tipoNombre']=="Privado":
                i['tipo_colegio'] = "PR"
                del i['tipoNombre']
            elif i['tipoNombre']=="Público":
                i['tipo_colegio'] = "PU"
                del i['tipoNombre']
        #print(colegio_)
        for k in colegio_:
            try:
                colegio_mod = colegio.objects.get(codigo_modular=str(k['codigo_modular']))
            except colegio.DoesNotExist:
                serializer = serializer_colegio(data=k)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
        #retornar la data grabada en la bd
        colegios_bd = colegio.objects.filter(id_ubigeo=distr, tipo_colegio=tipo)
        serializ = serializer_colegio(colegios_bd, many=True)
        return Response(serializ.data)
class recuperarUbicacion(APIView):
    def get(self, request, distrito,format=None):
        #distrito = request.data['distrito']
        try:
            ubigeoDistrito = ubigeo.objects.get(codigo_ubigeo=distrito, tipo_ubigeo='I')
            departamento = ubigeo.objects.get(codigo_ubigeo__startswith=distrito[0:2], tipo_ubigeo='D')
            provincia = ubigeo.objects.get(codigo_ubigeo__startswith=distrito[0:4], tipo_ubigeo='P')
            return Response({
                "departamento" : serializer_ubigeo(departamento).data,
                "provincia" : serializer_ubigeo(provincia).data,
                "distrito" : serializer_ubigeo(ubigeoDistrito).data
            })
        except ubigeo.DoesNotExist:
            return Response({
                "message": "No existen datos"
            })
# ···················· ENDREGION UBIGEO ······················}}}

# ···················· REGION ADMIN ························{{{
class verCompromisosPago(APIView):
    def get(self, request, format=None):
        snippets = compromiso_pago.objects.all()
        serializer = serializer_compromiso_pago(snippets, many=True)
        return Response(serializer.data)
class verDetalleCompromisosPago(APIView):
    def get(self, request, pk, format=None):
        #id_compromiso=request.data['id_compromiso_pago']
        try:
            snippets = detalle_compromiso_de_pago.objects.filter(id_compromiso_pago=pk)
            serializer_det_comp = serializer_detalle_compromiso_de_pago(snippets, many=True)
            return Response(serializer_det_comp.data)
        except:
            return Response({
                "message": "no se encuentra el item"
            })
class actualizarPagos(APIView):
    def patch(self, request, format=None):
        compromiso_id = request.data["id_compromiso_pago"]
        nro_cuota = request.data["numero_cuota"]
        id_administrador = request.data["id_administrador"]

        try:
            admin = administrador.objects.get(id=id_administrador)
            try:
                compromiso_consulta = compromiso_pago.objects.get(id=compromiso_id)
                if nro_cuota == 1:
                    try:
                        detalle_compr = detalle_compromiso_de_pago.objects.get(id_compromiso_pago=compromiso_consulta.id, numero_cuota=nro_cuota)
                        detalle_compr.esta_pagado = True
                        detalle_compr.save
                        serializer_detalle = serializer_detalle_compromiso_de_pago(detalle_compr, data=request.data, partial=True)
                        if serializer_detalle.is_valid(raise_exception=True):
                            update_detalle = serializer_detalle.save()
                        
                        serializer_tesor = registro_tesoreria.objects.get(id_detalle_compromiso=detalle_compr.id)
                        serializer_tesor.esta_pagado = True
                        serializer_tesor.fecha_pago = datetime.datetime.now()
                        serializer_tesor.admin = admin
                        serializer_tesor.save()

                        serializer_insc = serializer_inscripcion(data=serializer_detalle.data)
                        if serializer_insc.is_valid(raise_exception=True):
                            serializer_insc.save()
                        
                        return Response({
                            "message": "Primer pago realizado correctamente, creado nueva inscripcion"
                        })
                    except detalle_compromiso_de_pago.DoesNotExist:
                        pass
                else:
                    try:
                        detalle_compr = detalle_compromiso_de_pago.objects.get(id_compromiso_pago=compromiso_consulta.id, numero_cuota=nro_cuota)
                        detalle_compr.esta_pagado = True
                        detalle_compr.save
                        serializer_detalle = serializer_detalle_compromiso_de_pago(detalle_compr, data=request.data, partial=True)
                        if serializer_detalle.is_valid(raise_exception=True):
                            update_detalle = serializer_detalle.save()

                        serializer_tesor = registro_tesoreria.objects.get(id_detalle_compromiso=detalle_compr.id)
                        serializer_tesor.esta_pagado = True
                        serializer_tesor.fecha_pago = datetime.datetime.now()
                        #serializer_tesor.admin = 1
                        serializer_tesor.save()
                        return Response({
                            "detalle_act_data": serializer_detalle.data
                        })
                    except detalle_compromiso_de_pago.DoesNotExist:
                        return Response({"message":"No existe el detalle"})
            except compromiso_pago.DoesNotExist:
                return Response({"message":"No existe el compromiso"})
        except administrador.DoesNotExist:
            return Response({"message":"No se encuentra el administrador"})
class aprobarDocumentosInscripcion(APIView):
    def get(self, request, pk, format=None):
        documentos_est = documentos_inscripcion.objects.filter(id_inscripcion=pk)
        serializer = serializer_documentos_inscripcion_mostrar(documentos_est, many=True)
        return Response(serializer.data)
    def patch(self, request, format=None):
        id_administrador = request.data['id_administrador']
        documento_insc_id = request.data["id_documento_inscripcion"]
        try:
            admin = administrador.objects.get(id=id_administrador)
            try:
                documento_ = documentos_inscripcion.objects.get(id=documento_insc_id)
                try:                    
                    dict = {
                        "id_administrador": admin.id,
                        "esta_aprobado": True
                    }
                    dict = json.dumps(dict)
                    dict = json.loads(dict)
                    doc_rev = documentos_inscripcion_revision.objects.get(id_documento_inscripcion=documento_.id)
                    serializer_upt = serializer_documentos_inscripcion_revision(doc_rev, data=dict, partial=True)
                    if serializer_upt.is_valid(raise_exception=True):
                        serializer_upt.save()
                        documento_.esta_aprobado = True
                        documento_.save()

                        #REVISAR SI YA SON TODOS LOS ACTUALIZADOS
                        inscr_ = documentos_inscripcion.objects.filter(id_inscripcion=documento_.id_inscripcion)
                        final_result = True
                        for i in inscr_:
                            final_result = final_result and i.esta_aprobado

                        if final_result == True:
                            inscripcion_ = inscripcion.objects.get(id=inscr_[0].id_inscripcion.id)
                            get_preinsc = inscripcion_.id_compromiso_pago.id_preinscripcion
                            nombre_completo = str(get_preinsc)
                            nombres = get_preinsc.dni_persona.nombres
                            apPaterno = get_preinsc.dni_persona.apellido_paterno
                            apMaterno = get_preinsc.dni_persona.apellido_materno
                            dni = get_preinsc.dni_persona.dni
                            password = generarPass(nombre_completo, dni)
                            print(password)
                            correo = generarEmail(dni)
                            nombre_usuario = dni
                            dict={
                                "username": nombre_usuario,
                                "email": correo,
                                "password": password,
                                "user_type": "3",
                                "first_name": nombres,
                                "last_name": apPaterno,
                                "sur_name": apMaterno,
                            }
                            serializer_newuser = serializer_user(data=dict)
                            if serializer_newuser.is_valid(raise_exception=True):
                                serializer_newuser.save()
                                dict_est = {
                                    "id_inscripcion": inscripcion_.id,
                                    "user_type": serializer_newuser.data['id'],
                                }
                                serializer_est = serializer_estudiante_xd(data=dict_est)
                                if serializer_est.is_valid(raise_exception=True):
                                    serializer_est.save()                            
                                    inscripcion_.estado_finalizado=True
                                    inscripcion_.save()
                            return Response({"message":"Estudiante creado"})                    
                        return Response({"message":"Aprobado correctamente"})
                except documentos_inscripcion_revision.DoesNotExist:
                    return Response({"message":"No se encuentran datos documento inscripcion rev"})
            except documentos_inscripcion.DoesNotExist:
                return Response({"message":"No se encuentran datos documentos inscripcion"})
        except administrador.DoesNotExist:
            return Response({"message":"No se encuentran el admin"})
class documentosRequisito(APIView):
    def get(self, request, pk,format=None):
        preinsc_consulta = preinscripcion.objects.get(id=pk)        
        ciclo = preinsc_consulta.id_ciclo.id
        snippets = documento_solicitado_ciclo.objects.filter(id_ciclo=ciclo)
        cantidad = snippets.count()
        serializer_requisitos = serializer_documentos_requisito_inscripcionver(snippets, many=True)
        return Response({
            "data": serializer_requisitos.data,
            "cantidad": cantidad
        })
# ···················· ENDREGION ADMIN ·····················}}}
class DocumentosInscripcionViewset(viewsets.ViewSet):
    def list(self,request):
        docs=documentos_inscripcion.objects.all()
        serializer=serializer_documentos_inscripcion(docs,many=True,context={"request":request})
        response_dict={"error":False,"message":"All Customer Request Data","data":serializer.data}
        return Response(response_dict)

    def create(self, request):
        serializer=serializer_documentos_inscripcion(data=request.data,context={"request":request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            #Crear registros para la revision
            id_ = serializer.data['id']
            data = {}
            data = json.dumps(data)
            data = json.loads(data)
            data['id_documento_inscripcion'] = id_
            serializer_doc_rev = serializer_documentos_inscripcion_revision(data=data)
            if serializer_doc_rev.is_valid(raise_exception=True):
                serializer_doc_rev.save()

            return Response({"message":"Creado con exito"})
        return Response({"message":"Error al crear datos"})

    def retrieve(self, request, pk=None):
        queryset = documentos_inscripcion.objects.all()
        customer_request = get_object_or_404(queryset, pk=pk)
        serializer = serializer_documentos_inscripcion(customer_request, context={"request": request})

        serializer_data = serializer.data

        return Response({"error": False, "message": "Single Data Fetch", "data": serializer_data})

    def update(self,request,pk=None):
        try:
            queryset=documentos_inscripcion.objects.all()
            customer_request=get_object_or_404(queryset,pk=pk)
            serializer=serializer_documentos_inscripcion(customer_request,data=request.data,context={"request":request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            dict_response={"error":False,"message":"Successfully Updated Customer Data"}
        except:
            dict_response={"error":True,"message":"Error During Updating Customer Data"}

        return Response(dict_response)
class verDocumentosPorEstudiante(APIView):
    def get(self, request, pk, format=None):
        inscr_ = documentos_inscripcion.objects.filter(id_inscripcion=pk)
        serializer = serializer_documentos_inscripcion(inscr_, many=True)
        return Response(serializer.data)
#··················· REGION VISTAS DE ADMIN ·······················{{{
class procesoCiclo(APIView):
    def get(self, request, format=None):
        snippets = ciclo.objects.all()
        serializer = serializer_ciclo(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        datos = request.data
        #DATOS PARA VALIDACION DE FECHAS - CICLO
        fecha_ini_ciclo = datos['fecha_inicio_ciclo']
        fecha_fin_ciclo = datos['fecha_fin_ciclo']
        dias_ciclo = validarFechas(fecha_ini_ciclo, fecha_fin_ciclo)
        #DATOS PARA VALIDACION DE FECHAS - PREINSCRIPCION
        fecha_ini_preinsc = datos['fecha_inicio_preinscripcion']
        fecha_fin_preinsc = datos['fecha_fin_preinscripcion']
        dias_preins = validarFechas(fecha_ini_preinsc, fecha_fin_preinsc)
        #DATOS PARA VALIDACION DE FECHAS - INSCRIPCION
        fecha_ini_insc = datos['fecha_inicio_inscripcion']
        fecha_fin_insc = datos['fecha_fin_inscripcion']
        dias_insc = validarFechas(fecha_ini_insc, fecha_fin_insc)
        serializer_cic = serializer_ciclo(data=datos)

        if dias_ciclo > 0:
            if dias_preins > 0:
                if dias_insc > 0:
                    if serializer_cic.is_valid(raise_exception=True):            
                        save_serializer = serializer_cic.save()
                        return Response(serializer_cic.data)
                else:
                    return Response({"message": "Asegurece de configurar adecuadamente las fechas de la etapa de inscripcion"}) 
            else:
                return Response({"message": "Asegurece de configurar adecuadamente las fechas de la etapa de preinscripcion"}) 
        else:
            return Response({"message": "Asegurece de configurar adecuadamente las fechas que va durar ciclo"})       

    def put(self, request, pk, format=None):
        try:
            ciclo_consulta = ciclo.objects.get(id=pk)
            serializer_cons = serializer_ciclo(ciclo_consulta, data=request.data, partial=True)
            if serializer_cons.is_valid(raise_exception=True):
                serializer_cons.save()
                return Response(serializer_cons.data)

        except ciclo.DoesNotExsist:
            return Response({
                "error": "No existe registro con ese codigo"
            })
class padronCursosGeneral(APIView):
    def get(self, request, pk=None, activo=None,format=None):
        if pk:
            try:
                curso = padron_curso.objects.get(id=pk)
                serializer = serializer_padron_curso(curso)
                return Response(serializer.data)
            except padron_curso.DoesNotExist:
                return Response({
                    "error":"Objeto no existe"
                })
        if activo is None:
            cursos = padron_curso.objects.all()
            serializer = serializer_padron_curso(cursos, many=True)
            return Response(serializer.data)
        else:
            cursos = padron_curso.objects.filter(estado=True)
            serializer = serializer_padron_curso(cursos, many=True)
            return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = serializer_padron_curso(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        try:
            curso = padron_curso.objects.get(id=pk)
            serializer = serializer_padron_curso(curso,data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
        except padron_curso.DoesNotExist:
            return Response({
                "error":"No existe objeto"
            })
    
    def delete(self, request, pk, format=None):
        try:
            curso = padron_curso.objects.get(id=pk)
            curso.delete()
            return Response({"message": "Objecto eliminado"})
        except padron_curso.DoesNotExist:
            return Response({
                "error":"No existe objeto"
            })
class padronCursoGrupo(APIView):
    def get(self, request, pk=None, grupo=None, format=None):
        if pk is None and grupo is None:
            snippets = padron_cursos_grupo.objects.all()
            serializer = serializer_padron_curso_grupo_mostrar(snippets, many=True)
            return Response(serializer.data)
        elif pk is None and grupo is not None:
            snippets = padron_cursos_grupo.objects.filter(id_grupo_academico=grupo)
            serializer = serializer_padron_curso_grupo_mostrar(snippets, many=True)
            return Response(serializer.data)
        else:
            try:
                snippet = padron_cursos_grupo.objects.get(id=pk)
                serializer = serializer_padron_curso_grupo_mostrar(snippet)
                return Response(serializer.data)
            except padron_cursos_grupo.DoesNotExist:
                return Response({"message":"No hay datos"})
    
    def post(self, request, format=None):
        serializer = serializer_padron_curso_grupo(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        try:
            obj_curso_grup = padron_cursos_grupo.objects.get(id=pk)
            serializer = serializer_padron_curso_grupo(obj_curso_grup, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
        except padron_cursos_grupo.DoesNotExist:
            return Response({"message":"No hay datos"})
    
    def delete(self, request, pk, format=None):
        try:
            obj_curso_grup = padron_cursos_grupo.objects.get(id=pk)
            obj_curso_grup.delete()
            return Response({"message":"Objeto eliminado"})
        except padron_cursos_grupo.DoesNotExist:
            return Response({"message":"No hay datos"})

    def post(self, request, format=None):
        new_data = serializer_padron_curso_grupo(data=request.data)
        if new_data.is_valid(raise_exception=True):
            new_data.save()
            return Response(new_data.data)
class horarioCurso(APIView):
    def get(self, request, ciclo, pk=None, format=None):
        if pk is None:
            snippets = horario.objects.filter(id_ciclo=ciclo)
            serializer = serializer_horario_mostrar(snippets, many=True)
            return Response(serializer.data)
        else:
            try:
                snippet = horario.objects.get(id=pk)
                serializer = serializer_horario_mostrar(snippet)
                return Response(serializer.data)
            except horario.DoesNotExist:
                return Response({
                    "error": "No se encuentra el curso que se ingreso"
                })
    def post(self, request, format=None):
        serializer = serializer_horario(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
    def put(self, request, pk, format=None):
        try:
            horario_ = horario.objects.get(id=pk)
            serializer = serializer_horario(horario_, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
        except horario.DoesNotExist:
            return Response({"message":"No hay datos"})
    def delete(self, request, pk, format=None):
        try:
            horario_ = horario.objects.get(id=pk)
            horario_.delete()
            return Response({"message":"Se ha elminado correctamente"})
        except horario.DoesNot:
            return Response({"message":"No hay datos"})
class horarioCursoConDias(APIView):
    def get(self, request, pk, format=None):
        try:
            id_horarios = horario_curso.objects.filter(id_horario=pk)
            serializer = serializer_horario_curso_mostrar(id_horarios, many=True)
            return Response(serializer.data)               
        except padron_cursos_grupo.DoesNotExist:
            return Response({"message":"No existe tal curso"})
    
    def post(self, request, format=None):
        serializer = serializer_horario_curso(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        
    def put(self, request, pk, format=None):
        try:
            horario_curso_ = horario_curso.objects.get(id=pk)
            serializer = serializer_horario_curso(horario_curso_, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
        except horario_curso.DoesNotExist:
            return Response({"message":"No hay datos"})

    def delete(self, request, pk, format=None):
        try:
            horario_curso_ = horario_curso.objects.get(id=pk)
            horario_curso_.delete()
            return Response({"message":"Se ha eliminado correctamente"})
        except horario_curso.DoesNot:
            return Response({"message":"No hay datos"})      
#··················· ENDREGION VISTAS DE ADMIN ·······················}}}

#······················ REGION CONSULTAS ·····························{{{
class preinscripciones(APIView):
    def get(self, request, format=None):
        snippets = preinscripcion.objects.all()
        serializer = serializer_preinscripcion_most(snippets, many=True)
        return Response(serializer.data)
class inscripciones(APIView):
    def get(self, request, format=None):
        snippets = inscripcion.objects.all()
        serializer = serializer_inscripcion_most(snippets, many=True)
        return Response(serializer.data)
class estudiantes(APIView):
    def get(self, request, format=None):
        snippets = estudiante.objects.all()
        serializer = serializer_estudiante_most(snippets, many=True)
        return Response(serializer.data)
# ······················ ENDREGION CONSULTAS ··················}}}


#······················ REGION PAGO-PROTO ·····························{{{
class cicloActivo(APIView):
    def get(self, request, format=None):
        snippets = ciclo.objects.filter(activo=True)
        serializer = serializer_ciclo(snippets, many=True)
        return Response(serializer.data)
class listadoPagosCiclo(APIView):
    def get(self, request, pk,format=None):
        snippets = pago.objects.filter(id_ciclo=pk)
        serializer = serializer_pago(snippets, many=True)
        return Response(serializer.data)
class definirPago(APIView):
    def post(self, request, format=None):
        cantidad = request.data['cantidad_pagos']
        for i in range(0, cantidad):
            data = json.dumps(request.data)
            data = json.loads(data)
            data['nro_cuotas'] = (i+1)
            data['tipo_colegio'] = 'PU'
            serializer = serializer_pago(data=data)
            if serializer.is_valid(raise_exception=True):
                save_ser = serializer.save()
        for i in range(0, cantidad):
            data = json.dumps(request.data)
            data = json.loads(data)
            data['nro_cuotas'] = (i+1)
            data['tipo_colegio'] = 'PR'
            serializer = serializer_pago(data=data)
            if serializer.is_valid(raise_exception=True):
                save_ser = serializer.save()
        return Response({
            "message": "success"
        })
class listaDetallePago_porPago(APIView):
    def get(self, request, pk, format=None):
        snippets = detalle_pago.objects.filter(id_pago=pk)
        serializer = serializer_detalle_pago(snippets, many=True)
        return Response(serializer.data)
class detalle_pago_algo(APIView):
    def post(self, request, format=None):
        serializer = serializer_detalle_pago_det(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
    def put(self, request, pk, format=None):
        try:
            obj_detalle_pago = detalle_pago.objects.get(id=pk)
            serializer = serializer_detalle_pago_det(obj_detalle_pago, data=request.data,partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
        except detalle_pago.DoesNotExist:
            return Response({
                "error": "data not found"
            })
# ······················ ENDREGION PAGO ··················}}}
class addPagos(APIView):
    def post(self, request,pk, format=None):
        #ciclo = request.data['id_ciclo']
        pagos_exists = pago.objects.filter(id_ciclo=pk).count()
        print("pagos total",pagos_exists)
        if pagos_exists > 0:
            to_add = int(pagos_exists/2) + 1
            print("pagos a agregar",to_add)
            data = json.dumps(request.data)
            data = json.loads(data)
            data['nro_cuotas'] = to_add
            data['tipo_colegio'] = 'PR'
            data['monto_total'] = 0
            
            serializer_pub = serializer_pago(data = data)
            if serializer_pub.is_valid(raise_exception=True):
                save_pub = serializer_pub.save()

            data['tipo_colegio'] = 'PU'
            serializer_priv = serializer_pago(data = data)
            if serializer_priv.is_valid(raise_exception=True):
                save_pri = serializer_priv.save()
            return Response({
                "publico": serializer_pub.data,
                "privado": serializer_priv.data
            })
        else:
            data = json.dumps(request.data)
            data = json.loads(data)
            data['nro_cuotas'] = 1
            data['tipo_colegio'] = 'PR'
            data['monto_total'] = 0
            
            serializer_pub = serializer_pago(data = data)
            if serializer_pub.is_valid(raise_exception=True):
                save_pub = serializer_pub.save()
            data['tipo_colegio'] = 'PU'
            serializer_priv = serializer_pago(data = data)
            if serializer_priv.is_valid(raise_exception=True):
                save_pri = serializer_priv.save()
            return Response({
                "publico": serializer_pub.data,
                "privado": serializer_priv.data
            })
class deletePagos(APIView):
    def delete(self, request, pk ,format=None):
        priv = pago.objects.filter(id_ciclo=pk, tipo_colegio='PR').last()
        pub = pago.objects.filter(id_ciclo=pk, tipo_colegio='PU').last()
        serializer_priv = serializer_pago(priv)        
        serializer_pub = serializer_pago(pub)
        priv.delete()
        pub.delete()
        return Response({
            "priv": serializer_priv.data,
            "pub": serializer_pub.data
        })
# ························ REGION DOCENTE ····················{{{
class inicioDocente(APIView):
    def get(self, request, pk, format=None):
        #id_docente = request.data['id_docente']
        try:
            #recuperar docente
            det_docente = docente.objects.get(id=pk)
            #recuperar horarios y cursos por ciclo activo
            horarios = horario.objects.filter(id_docente=det_docente.id, id_ciclo__activo=True)
            #serializer = serializer_horario_mostrar(horarios, many=True)
            lista = []
            for i in horarios:                
                tempo = {}
                snippets = horario_curso.objects.filter(id_horario = i.id)
                serializer = serializer_horario_curso_mostrar(snippets, many=True)
                tempo["curso"] = i.id_padron_cursos_grupo.id_padron_curso.nombre_curso
                tempo["datos"] = serializer.data  
                lista.append(tempo)
            return Response(lista)
        except docente.DoesNotExist:
            return Response({"message":"No hay datos del docente"})
class seleccionarCurso(APIView):
    def get(self, request,pk, format=None):
        try:
            get_horario = horario.objects.get(id=pk)
            #get_horario = horario.objects.get(id=pk)
            return Response({
                "nombre_curso": get_horario.id_padron_cursos_grupo.id_padron_curso.nombre_curso,
                "abreviacion": get_horario.id_padron_cursos_grupo.id_padron_curso.abreviacion,
                "grupo_acad": get_horario.id_padron_cursos_grupo.id_grupo_academico.abreviacion,
                "enlace_meet": get_horario.enlace_meet
            })
        except horario.DoesNotExist:
            return Response({"message":"No hay datos"})
class sesionClase(APIView):
    def post(self, request, format=None):
        id_docente = request.data['id_docente']
        id_curso = request.data['id_curso']
        get_horario = horario.objects.get(id_padron_cursos_grupo=id_curso, id_docente=id_docente)
        data = json.dumps(request.data)
        data = json.loads(data)
        data['id_horario'] = get_horario.id
        
        serializer = serializer_asistencia_docente(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
class verAsistenciaCurso(APIView):
    def get(self, request, ciclo, pk=None, format=None):
        if pk is not None:
            estudiante_curso_ = estudiante_horario.objects.get(id=pk)
            snippets = asistencia_estudiante.objects.filter(id_estudiante_horario__id_estudiante=estudiante.id)
            serializer = serializer_asistencia_estudiante(snippets, many=True)
            return Response(serializer.data)
        else:
            snippets = asistencia_estudiante.objects.filter(id_horario_estudiante__id_ciclo=ciclo)            
            serializer = serializer_asistencia_estudiante(snippets, many=True)
            return Response(serializer.data)
class generarAsistencias(APIView):
    def post(self, request, pk, format=None):
        horario_det = horario.objects.get(id=pk)
        estudiantes = estudiante_horario.objects.filter(id_horario=horario_det.id)
        print(estudiantes)
        for i in estudiantes:
            dict = {}
            new_data = json.dumps(dict)
            new_data = json.loads(new_data)
            new_data['id_estudiante_horario'] = i.id
            print(new_data)
            serializer = serializer_asistencia_estudiante(data=new_data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()

        dia_actual = datetime.date.today()
        asistencias_dia = asistencia_estudiante.objects.filter(id_estudiante_horario__id_horario=pk, fecha_sesion__startswith=str(dia_actual))
        serializer = serializer_asistencia_estudiante_mostrar(asistencias_dia, many=True)
        return Response(serializer.data)
class registrarAsistencia(APIView):
    def patch(self, request, pk,format=None):
        id_estudiante = request.data['id_estudiante']
        horario_est = estudiante_horario.objects.get(id_estudiante=id_estudiante, id_horario = pk)
        dia_actual = datetime.date.today()
        registro_asistencia_del_dia = asistencia_estudiante.objects.get(fecha_sesion__startswith=str(dia_actual), id_estudiante_horario=horario_est)
        registro_asistencia_del_dia.estado_asistencia = True
        registro_asistencia_del_dia.save()
        serializer = serializer_asistencia_estudiante(registro_asistencia_del_dia)
        return Response(serializer.data)
class materialCurso(APIView):
    def get(self, request, horario, pk=None, format=None):
        if pk is None:
            materiales = material_curso.objects.filter(id_horario=horario)
            serializer = serializer_material_curso_mostrar(materiales, many=True)
            return Response(serializer.data)
        else:
            try:
                material = material_curso.objects.get(id=pk)
                serializer = serializer_material_curso_mostrar(material)
                return Response(serializer.data)
            except material_curso.DoesNotExist:
                return Response({"message": "No existe objeto"})
    def post(self, request, format=None):
        serializer = serializer_material_curso(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
    
    def put(self, request, horario, pk, format=None):
        try:
            material_upt = material_curso.objects.get(id=pk, id_horario=horario)
            serializer = serializer_material_curso(material_upt, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
        except material_curso.DoesNotExist:
            return Response({"message":"No hay datos"})

    def delete(self, request, horario, pk, format=None):
        try:
            material_del = material_curso.objects.get(id=pk, id_horario=horario)
            material_del.delete()
            return Response({"message":"Objeto eliminado"})
        except material_curso.DoesNotExist:
            return Response({"message":"No hay datos"})
class comentariosClase(APIView):
    def get(self, request, horario, pk=None, format=None):
        if pk is None:
            comentarios = comentarios_clase.objects.filter(id_horario=horario)
            serializer = serializer_comentario_clase_mostrar(comentarios, many=True)
            return Response(serializer.data)
        else:
            try:
                comentario = comentarios_clase.objects.get(id=pk)
                serializer = serializer_comentario_clase_mostrar(comentario)
                return Response(serializer.data)
            except comentarios_clase.DoesNotExist:
                return Response({"message": "No existe objeto"})
    
    def post(self, request, format=None):
        serializer = serializer_comentarios_clase(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
    
    def put(self, request, horario, pk, format=None):
        try:
            comentario_upt = comentarios_clase.objects.get(id=pk, id_horario=horario)
            serializer = serializer_comentarios_clase(comentario_upt, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
        except comentarios_clase.DoesNotExist:
            return Response({"message":"No hay datos"})

    def delete(self, request, horario, pk, format=None):
        try:
            comentarios_del = comentarios_clase.objects.get(id=pk, id_horario=horario)
            comentarios_del.delete()
            return Response({"message":"Objeto eliminado"})
        except comentarios_clase.DoesNotExist:
            return Response({"message":"No hay datos"})
class balotaCurso(APIView):
    def get(self, request, curso_grupo, pk=None, format=None):
        if pk is None:
            balotas = balota_preguntas_curso.objects.filter(id_padron_curso_grupo=curso_grupo)
            serializer = serializer_balota_preguntas_curso_mostrar(balotas, many=True)
            return Response(serializer.data)
        else:
            try:
                balota = balota_preguntas_curso.objects.get(id_padron_curso_grupo=curso_grupo,id=pk)
                serializer = serializer_balota_preguntas_curso_mostrar(balota)
                return Response(serializer.data)
            except balota_preguntas_curso.DoesNotExist:
                return Response({"message":"No hay datos"})
    def post(self, request, curso_grupo, format=None):
        serializer = serializer_balota_preguntas_curso(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
    
    def put(self, request, curso_grupo, pk, format=None):
        try:
            balota_upt = balota_preguntas_curso.objects.get(id=pk, id_padron_curso_grupo= curso_grupo)
            serializer = serializer_balota_preguntas_curso(balota_upt, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
        except balota_preguntas_curso.DoesNotExist:
            return Response({"message":"No hay datos"})
    
    def delete(self, request, curso_grupo, pk, format=None):
        try:
            balota_del = balota_preguntas_curso.objects.get(id=pk, id_padron_curso_grupo=curso_grupo)
            balota_del.delete()
            return Response({"message":"Objeto eliminado"})
        except balota_preguntas_curso.DoesNotExist:
            return Response({"message":"No hay datos"})
class alternativasBalotario(APIView):
    def get(self, request, balota, pk=None,  format=None):
        if pk is None:
            alternativa_curso_grup = alternativas_balotario.objects.filter(id_balota = balota)
            serializer = serializer_alternativas_balota_mostrar(alternativa_curso_grup, many=True)
            return Response(serializer.data)
        else:
            try:
                alternativa_curso_grup = alternativas_balotario.objects.get(id_balota = balota, id=pk)
                serializer = serializer_alternativas_balota_mostrar(alternativa_curso_grup)
                return Response(serializer.data)
            except alternativas_balotario.DoesNotExist:
                return Response({"message":"No hay datos"})

    def post(self, request, balota, format=None):
        valor_alternativa = request.data['es_respuesta']
        alternativas = alternativas_balotario.objects.filter(id_balota=balota)
        if alternativas.count() == 5:
            return Response({"message": "Alcanzo el maximo de alternativas para esta pregunta"})
        cont_verdaderos = 0
        for i in alternativas:
            if i.es_respuesta == True:
                cont_verdaderos += 1
        if cont_verdaderos >= 0 and valor_alternativa==False:
            serializer = serializer_alternativas_balotario(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
        elif cont_verdaderos == 0 and valor_alternativa==True:
            serializer = serializer_alternativas_balotario(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
        else:
            return Response({"Error": "Ya existe una respuesta correcta para esa pregunta"})

    def put(self, request, balota, pk, format=None):
        valor_alternativa = request.data['es_respuesta']
        alternativas = alternativas_balotario.objects.filter(id_balota=balota)
        try:
            alternativa_upt = alternativas_balotario.objects.get(id=pk,id_balota=balota)
            valor_alternativa = request.data['es_respuesta']
            #RECUPERAR DEMAS ALTERNATIVAS Y VER SI YA HAY UNA RESPUETA CORRECTA
            alternativas = alternativas_balotario.objects.filter(id_balota=balota)
            cont_verdaderos = 0
            for i in alternativas:
                if i.es_respuesta == True:
                    cont_verdaderos += 1
            #VALIDAR LO ANTERIOR CON EL REQUEST DADO
            if cont_verdaderos >= 0 and valor_alternativa==False:
                serializer = serializer_alternativas_balotario(alternativa_upt, data=request.data)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    return Response(serializer.data)
            elif cont_verdaderos == 0 and valor_alternativa==True:
                serializer = serializer_alternativas_balotario(alternativa_upt, data=request.data)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    return Response(serializer.data)
            else:
                return Response({"Error": "Ya existe una respuesta correcta para esa pregunta"})
            
        except alternativas_balotario.DoesNotExist:
            return Response({"message": "no hay datos"})

    def delete(self, request, balota, pk, format=None):
        try:
            alternativa_upt = alternativas_balotario.objects.get(id=pk, id_balota=balota)
            alternativa_upt.delete()
            return Response({"message":"Eliminado correctamente"})
        except alternativas_balotario.DoesNotExist:
            return Response({"message": "no hay datos"})
# ···························· USING VIEWSET ························
class MaterialCursoViewset(viewsets.ViewSet):
    def list(self,request):
        materiales = material_curso.objects.all()
        serializer = serializer_material_curso_mostrar(materiales,many=True,context={"request":request})
        response_dict = {
                "error":False,
                "message":"Todos los objetos de la tabla recuperados",
                "data":serializer.data
            }
        return Response(response_dict)

    def create(self, request):
        serializer = serializer_material_curso(data=request.data,context={"request":request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = material_curso.objects.all()
        customer_request = get_object_or_404(queryset, pk=pk)
        serializer = serializer_material_curso_mostrar(customer_request, context={"request": request})

        serializer_data = serializer.data

        return Response({
            "error": False,
            "message": "Single Data Fetch",
            "data": serializer_data
        })

    def update(self,request,pk=None):
        try:
            queryset = material_curso.objects.all()
            customer_request = get_object_or_404(queryset,pk=pk)
            serializer = serializer_material_curso(customer_request,data=request.data,context={"request":request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            dict_response={
                "error":False,
                "message":"Datos actualizados"
            }
        except:
            dict_response={
                "error":True,
                "message":"Error durante el proceso de actualizacion"
            }

        return Response(dict_response)  

    def delete(self, request, pk, format=None):
        try:
            queryset = material_curso.objects.all()
            customer_request = get_object_or_404(queryset,pk=pk)
            customer_request.delete()
            dict_response={
                "error":False,
                "message":"Objeto eliminado correctamente"
            }
        except:
            dict_response={
                "error":True,
                "message":"Error durante el proceso de eliminacion"
            }
        return Response(dict_response)
class ComentariosClaseViewset(viewsets.ViewSet):
    def list(self,request):
        materiales = comentarios_clase.objects.all()
        serializer = serializer_comentario_clase_mostrar(materiales,many=True,context={"request":request})
        response_dict = {
                "error":False,
                "message":"Todos los objetos de la tabla recuperados",
                "data":serializer.data
            }
        return Response(response_dict)

    def create(self, request):
        serializer = serializer_comentarios_clase(data=request.data,context={"request":request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = comentarios_clase.objects.all()
        customer_request = get_object_or_404(queryset, pk=pk)
        serializer = serializer_comentario_clase_mostrar(customer_request, context={"request": request})

        serializer_data = serializer.data

        return Response({
            "error": False,
            "message": "Single Data Fetch",
            "data": serializer_data
        })

    def update(self,request,pk=None):
        try:
            queryset = comentarios_clase.objects.all()
            customer_request = get_object_or_404(queryset,pk=pk)
            serializer = serializer_comentarios_clase(customer_request,data=request.data,context={"request":request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            dict_response={
                "error":False,
                "message":"Datos actualizados"
            }
        except:
            dict_response={
                "error":True,
                "message":"Error durante el proceso de actualizacion"
            }

        return Response(dict_response)  

    def delete(self, request, pk, format=None):
        try:
            queryset = comentarios_clase.objects.all()
            customer_request = get_object_or_404(queryset,pk=pk)
            customer_request.delete()
            dict_response={
                "error":False,
                "message":"Objeto eliminado correctamente"
            }
        except:
            dict_response={
                "error":True,
                "message":"Error durante el proceso de eliminacion"
            }
        return Response(dict_response)

# ························ ENDREGION DOCENTE ····················}}}
#························ REGON ESTUDIANTE ·····················{{{
class inicioEstudiante(APIView):
    def get(self, request, format=None):
        try:
            id_estudiante = request.data['id_estudiante']
            #recuperar horarios y cursos
            est_horarios = estudiante_horario.objects.filter(id_estudiante=id_estudiante)
            #serializer = serializer_horario_mostrar(eest_horarios, many=True)
            lista = []        
            for i in est_horarios:                
                tempo = {}
                snippets = horario_curso.objects.filter(id_horario = i.id_horario.id)
                serializer = serializer_horario_curso_mostrar(snippets, many=True)
                tempo["curso"] = i.id_horario.id_padron_cursos_grupo.id_padron_curso.nombre_curso
                tempo["datos"] = serializer.data  
                lista.append(tempo)
            return Response(lista)
        except estudiante.DoesNotExist:
            return Response({"message":"No hay datos del estudiante"})
class seleccionarCursoEstudiante(APIView):
    def get(self, request, pk, format=None):
        try:
            get_horario = horario.objects.get(id=pk)
            #get_horario = horario.objects.get(id=pk)
            return Response({
                "nombre_curso": get_horario.id_padron_cursos_grupo.id_padron_curso.nombre_curso,
                "abreviacion": get_horario.id_padron_cursos_grupo.id_padron_curso.abreviacion,
                "grupo_acad": get_horario.id_padron_cursos_grupo.id_grupo_academico.abreviacion,
                "enlace_meet": get_horario.enlace_meet,
                "nombre_docente" : str(get_horario.id_docente)
            })
        except horario.DoesNotExist:
            return Response({"message":"No hay datos"})
class comentariosClaseEstudiante(APIView):
    def get(self, request, horario, pk=None, format=None):
        if pk is None:
            comentarios = comentarios_clase.objects.filter(id_horario=horario)
            serializer = serializer_comentario_clase_mostrar(comentarios, many=True)
            return Response(serializer.data)
        else:
            try:
                comentario = comentarios_clase.objects.get(id=pk)
                serializer = serializer_comentario_clase_mostrar(comentario)
                return Response(serializer.data)
            except comentarios_clase.DoesNotExist:
                return Response({"message": "No existe objeto"})
    
    def post(self, request, horario, format=None):
        serializer = serializer_comentarios_clase(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
    
    def put(self, request, horario, pk, format=None):
        try:
            comentario_upt = comentarios_clase.objects.get(id=pk, id_horario=horario)
            serializer = serializer_comentarios_clase(comentario_upt, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
        except comentarios_clase.DoesNotExist:
            return Response({"message":"No hay datos"})

    def delete(self, request, horario, pk, format=None):
        try:
            comentarios_del = comentarios_clase.objects.get(id=pk, id_horario=horario)
            comentarios_del.delete()
            return Response({"message":"Objeto eliminado"})
        except comentarios_clase.DoesNotExist:
            return Response({"message":"No hay datos"})
class materialCursoEstudiante(APIView):
    def get(self, request, horario, pk=None, format=None):
        if pk is None:
            materiales = material_curso.objects.filter(id_horario=horario)
            serializer = serializer_material_curso_mostrar(materiales, many=True)
            return Response(serializer.data)
        else:
            try:
                material = material_curso.objects.get(id=pk)
                serializer = serializer_material_curso_mostrar(material)
                return Response(serializer.data)
            except material_curso.DoesNotExist:
                return Response({"message": "No existe objeto"})
class verNotasEstudiante(APIView):
    def get(self, request, pk, format=None):        
        examen_est = examen_estudiante.objects.filter(id_estudiante=pk)
        serializer = serializer_examen_estudiante_mostrar(examen_est, many=True)
        return Response(serializer.data)
class verPagosEstudiante(APIView):
    def get(self, request, pk, format=None):
        estudiante_det = estudiante.objects.get(id=pk)
        id_compromiso_est = estudiante_det.id_inscripcion.id_compromiso_pago
        snippets = detalle_compromiso_de_pago.objects.filter(id_compromiso_pago = id_compromiso_est)
        serializer = serializer_detalle_compromiso_de_pago(snippets, many=True)
        return Response(serializer.data)
class verAsistenciaEstudiante(APIView):
    def get(self, request, pk, format=None):
        horario_est = estudiante_horario.objects.filter(id_estudiante=pk)
        dict = {}
        for i in horario_est:
            snippets = asistencia_estudiante.objects.filter(id_estudiante_horario=i.id)
            serializer = serializer_asistencia_estudiante(snippets, many=True)
            dict[str(i.id_horario.id_padron_cursos_grupo.id_padron_curso.nombre_curso)] = serializer.data
        return Response(dict)
            #return Response(serializer.data)
#························ ENDREGION ESTUDIANTE··················}}}

#························ REGION EXAMEN ··················{{{
class programarExamen(APIView):
    def get(self, request, ciclo, pk=None):
        if pk is None:
            snippets = examen.objects.filter(id_ciclo=ciclo)
            return Response(serializer_examen(snippets, many=True).data)
        else:
            snippet = examen.objects.get(id=pk)
            return Response(serializer_examen(snippet).data)
    def post(self, request, ciclo):
        if request.data['tipo_examen']=='SIMULACRO':
            serializer = serializer_examen(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                grupos_examen = grupo_academico.objects.all()
                for i in grupos_examen:
                    dict={}
                    dict['id_grupo_academico'] = i.id
                    dict['id_examen'] = serializer.data['id']
                    serializer_exagrupo = serializer_examen_grupo(data=dict)
                    if serializer_exagrupo.is_valid(raise_exception=True):
                        serializer_exagrupo.save()
                return Response({"message":"Creado correctamente"})
        
        else:
            serializer = serializer_examen(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
class listarDetalleExamenGrupo(APIView):
    def get(self, request, ciclo, pk=None, format=None):
        if pk is None:
            snippets = examen_grupo.objects.filter(id_examen__id_ciclo=ciclo)
            serializer = serializer_examen_grupo(snippets, many=True)
            return Response(serializer.data)
        else:
            try:
                snippet = examen_grupo.objects.get(id=pk)
                serializer = serializer_examen_grupo(snippet)
                return Response(serializer.data)
            except examen_grupo.DoesNotExist:
                return Response({
                    "error":"No existen datos"
                })
#············· AUTOMATICO ·····························
class crearExamenGrupoPreguntas(APIView):
    def post(self, request, pk, format=None):
        try:
            examen_grupo_ = examen_grupo.objects.get(id=pk)
            if examen_grupo_.finalizado == False:
                id_grupo = examen_grupo_.id_grupo_academico.id
                cursos = padron_cursos_grupo.objects.filter(id_grupo_academico=id_grupo)
                print(cursos)
                #Revisar si todos los cursos tienen al menos la cantidad minima de preguntas en su balotario
                for i in cursos:
                    max_preguntas = i.nro_preguntas_examen
                    preguntas_balotario = balota_preguntas_curso.objects.filter(id_padron_curso_grupo=i.id)
                    if max_preguntas > preguntas_balotario.count():
                        return Response({
                            "error": "La cantidad de preguntas no es suficiente",
                            "Curso": i.id_padron_curso.nombre_curso
                        })
                for i in cursos:
                    #extrer cantidad de preguntas por curso
                    max_preguntas = i.nro_preguntas_examen
                    #listar balotarios segun cursos
                    preguntas_balotario = balota_preguntas_curso.objects.filter(id_padron_curso_grupo=i.id)
                    if max_preguntas > preguntas_balotario.count():
                        return Response({
                            "error":"La cantidad de preguntas del balotario no es suficiente"
                        })
                    else:
                        #tomar una cantidad fija de preguntas para un determinado curso
                        lista = random.sample(list(preguntas_balotario), max_preguntas)
                        for j in lista:
                            dict ={
                                "id_examen_grupo": pk,
                                "id_balota_curso": j.id
                            }
                            serializer_preg_examen = serializer_preguntas_examen_grupo(data=dict)
                            if serializer_preg_examen.is_valid(raise_exception=True):
                                serializer_preg_examen.save()
                examen_grupo_.finalizado = True
                examen_grupo_.save()                               
                return Response({"message": "successful"})
            else:
                return Response({"message": "El examen ya tiene sus preguntas asignadas"})
        except examen_grupo.DoesNotExist:
            return Response({"message": "No existe examen con ese ID"})
#············· MANUAL ·····························
class crearExamenGrupoManual(APIView):
    def get(self, request, examen_pk, curso_pk=None, format=None):
        if curso_pk is None:
            try:
                #Recuperamos el examen segun el id dado
                examen_grupo_ = examen_grupo.objects.get(id=examen_pk)
                #Sacamos sus datos (ciclo y grupo academico con el objetivo de hacer filtros)
                id_grupo = examen_grupo_.id_grupo_academico.id
                #Filtramos  los cursos segun el grupo academico del exxamen actual
                cursos_ = padron_cursos_grupo.objects.filter(id_grupo_academico=id_grupo)
                serializer = serializer_padron_curso_grupo_mostrar(cursos_, many=True)
                return Response(serializer.data)
            except examen_grupo.DoesNotExist:
                return Response({"message":"No hay datos"})
        else:
            try:
                #Recuperamos el examen segun el id dado
                examen_grupo_ = examen_grupo.objects.get(id=examen_pk)
                #Sacamos sus datos (ciclo y grupo academico con el objetivo de hacer filtros)
                id_grupo = examen_grupo_.id_grupo_academico.id
                #Filtramos  los cursos segun el grupo academico del exxamen actual
                curso_ = padron_cursos_grupo.objects.get(id_grupo_academico=id_grupo, id=curso_pk)
                serializer = serializer_padron_curso_grupo_mostrar(curso_)
                return Response(serializer.data)
            except examen_grupo.DoesNotExist:
                return Response({"message":"No hay datos"})

    def post(self, request):
        serializer = serializer_preguntas_examen_grupo(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
#························ ENDREGION EXAMEN ··················}}}

# ············ REGION SINCRONIZAR INFRAESTRUCTURA ···············{{{
@api_view(['POST'])
def sincronizarEEPP(request):
    eepp_bd = escuela_profesional.objects.all()
    if eepp_bd.count() == 0:
        eepp_uniq = escuelasProfesionales()
        eepp_ = json.dumps(eepp_uniq)
        eepp_ = json.loads(eepp_)
        for i in eepp_:
            i['codigo_escuela'] = i['codigo']
            i['nombre_escuela_profesional'] = i['nombre']
            i['abreviacion'] = i['codigo']
            del i['nombre']
            del i['codigo']
        for i in eepp_:
            serializer_crear = serializer_escuela_profesional(data=i)
            if serializer_crear.is_valid(raise_exception=True):
                serializer_crear.save()

        esc_act = escuela_profesional.objects.all()
        serializer_res = serializer_escuela_profesional(esc_act, many=True)
        return Response(serializer_res.data)
    
    else:
        eepp_uniq = escuelasProfesionales()
        eepp_ = json.dumps(eepp_uniq)
        eepp_ = json.loads(eepp_)
        for i in eepp_:
            i['codigo_escuela'] = i['codigo']
            i['nombre_escuela_profesional'] = i['nombre']
            i['abreviacion'] = i['codigo']
            del i['nombre']
            del i['codigo']
            try:                    
                esc_act = escuela_profesional.objects.get(codigo_escuela=i['codigo_escuela'])
                serializer_act = serializer_escuela_profesional(esc_act, data = i)
                if serializer_act.is_valid(raise_exception=True):
                    serializer_act.save()
            except:
                serializer_crear = serializer_escuela_profesional(data = i)
                if serializer_crear.is_valid(raise_exception=True):
                    serializer_crear.save()
        
        esc_act = escuela_profesional.objects.all()
        serializer_res = serializer_escuela_profesional(esc_act, many=True)
        return Response(serializer_res.data)
@api_view(['POST'])
def sincronizarPabellones(request):
    pabellones_q = pabellon.objects.all()
    if pabellones_q.count() == 0:
        pabellones_uniq = pabellones()
        pabellon_ = json.dumps(pabellones_uniq)
        pabellon_ = json.loads(pabellon_)
        for i in pabellon_:
            i['codigo_pabellon'] = i['codigo']
            i['nombre_pabellon'] = i['nombre']
            del i['nombre']
            del i['codigo']
        for i in pabellon_:
            serializer_crear = serializer_pabellon(data=i)
            if serializer_crear.is_valid(raise_exception=True):
                serializer_crear.save()

        pabellon_act = pabellon.objects.all()
        serializer_res = serializer_pabellon(pabellon_act, many=True)
        return Response(serializer_res.data)
    else:
        pabellon_uniq = pabellones()
        pabellon_ = json.dumps(pabellon_uniq)
        pabellon_ = json.loads(pabellon_)
        for i in pabellon_:
            i['codigo_pabellon'] = i['codigo']
            i['nombre_pabellon'] = i['nombre']
            del i['nombre']
            del i['codigo']
            try:                    
                pab_act = pabellon.objects.get(codigo_pabellon=i['codigo_pabellon'])
                serializer_act = serializer_pabellon(pab_act, data = i)
                if serializer_act.is_valid(raise_exception=True):
                    serializer_act.save()
            except:
                serializer_crear = serializer_pabellon(data = i)
                if serializer_crear.is_valid(raise_exception=True):
                    serializer_crear.save()
        
        pab_act = pabellon.objects.all()
        serializer_res = serializer_pabellon(pab_act, many=True)
        return Response(serializer_res.data)
@api_view(['POST'])
def sincronizarAulas(request):
    aulas_q = aula.objects.all()
    if aulas_q.count() == 0:
        aulas_uniq = aulas()
        aulas_ = json.dumps(aulas_uniq)
        aulas_ = json.loads(aulas_)
        for i in aulas_:
            i['codigo_aula'] = i['codigo']
            i['sillas_fijas'] = i['sillasFijas']
            i['sillas_moviles'] = i['sillasMoviles']
            i['capacidad'] = i['sillasMoviles'] + i['sillasFijas']
            del i['codigo']
            del i['sillasFijas']
            del i['sillasMoviles']
        for i in aulas_:
            try:
                pabellon_rec = pabellon.objects.get(codigo_pabellon=i['codigoPabellon'])
                i['id_pabellon'] = pabellon_rec.id
                serializer_crear = serializer_aula(data=i)
                if serializer_crear.is_valid(raise_exception=True):
                    serializer_crear.save()
            except:
                return Response({"message":"Error"})

        aulas_t = aula.objects.all()
        serializer_res = serializer_aula(aulas_t, many=True)
        return Response(serializer_res.data)
    else:
        aulas_uniq = aulas()
        aulas_ = json.dumps(aulas_uniq)
        aulas_ = json.loads(aulas_)
        for i in aulas_:
            i['codigo_aula'] = i['codigo']
            i['sillas_fijas'] = i['sillasFijas']
            i['sillas_moviles'] = i['sillasMoviles']
            i['capacidad'] = i['sillasMoviles'] + i['sillasFijas']
            del i['codigo']
            del i['sillasFijas']
            del i['sillasMoviles']
            try:
                aula_act = aula.objects.get(codigo_aula=i['codigo_aula'])
                serializer_act = serializer_aula(aula_act, data = i, partial=True)
                if serializer_act.is_valid(raise_exception=True):
                    serializer_act.save()
            except:
                pabellon_rec = pabellon.objects.get(codigo_pabellon=i['codigoPabellon'])
                i['id_pabellon'] = pabellon_rec.id
                serializer_crear = serializer_aula(data = i)
                if serializer_crear.is_valid(raise_exception=True):
                    serializer_crear.save()
        
        aula_act = aula.objects.all()
        serializer_res = serializer_aula(aula_act, many=True)
        return Response(serializer_res.data)

class algo(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        return Response({
            "user": user,
            "all": request.data
        })

class crearUser(APIView):
    def post(self, request, *args, **kwargs):
        serializer_ = serializer_user(data=request.data)
        if serializer_.is_valid(raise_exception=True):
            serializer_.save()
            return Response(serializer_.data)
#·············· REGION SINCRONIZAR INFRAESTRUCTURA ·············}}}