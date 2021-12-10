import requests
import json
import datetime
import hashlib
#......................CAMPO DE CONSULTAS PIDE..........................
def consultaDNI(dni):
    url = 'https://sysapis.uniq.edu.pe/pide/reniec?dni='+str(dni)
    response = requests.get(url)
    if response.status_code == 200:
        status = 200
        text = response.json()
        textjson = json.dumps(text)
        textjson = json.loads(textjson)
        dict = {
            "dni" : str(dni),
            "nombres" : textjson['nombres'],
            "apellido_paterno" : textjson['apellidoPaterno'],
            "apellido_materno" : textjson['apellidoMaterno'],            
            "direccion" : textjson['direccion']
        }
        return status, json.dumps(dict,indent=4)
    else:
        status = 404
        dictio = {
            "message": "no se obtuvo datos"
        }
        return status, json.dumps(dictio,indent=4)
def extraerDepartamentos():
    url = "https://sysapis.uniq.edu.pe/api/dev/external/ubigeos?tipo=D"
    response = requests.get(url)    
    return response.json()
def extraerProvincia(departamento):
    url = "https://sysapis.uniq.edu.pe/api/dev/external/ubigeos?tipo=P&padre="+str(departamento)
    response = requests.get(url)
    return response.json()
def extraerDistrito(provincia):
    url = "https://sysapis.uniq.edu.pe/api/dev/external/ubigeos?tipo=I&padre="+str(provincia)
    response = requests.get(url)
    return response.json()
def consultaColegios(distrito):
    url = "https://sysapis.uniq.edu.pe/api/dev/external/escuelas?ubigeo="+str(distrito)
    response = requests.get(url)
    return response.json()
def validarFechas(fecha1, fecha2):
    #Considerar la fecha2 como la que cierra el periodo entre dos fechas
    return (fecha2 - fecha1).days
def validarEtapasPreinsInsc(fecha_ini_ciclo, fecha_fin_ciclo, fecha_ini_preins, fecha_fin_preins, fecha_ini_insc, fecha_fin_insc):
    
    pass


# ·············· GENERACION DE CODIGOS PARA PROCESOS ··············
def generarCod(dni, nro_ciclo, nro_cuota,tipo_colegio):
    if tipo_colegio=='PR':
        cod = 'UCEPR'+dni+'C'+str(nro_ciclo)+'-C'+str(nro_ciclo)+'CU'+str(nro_cuota)+tipo_colegio
    else:
        cod = 'UCEPR'+dni+'C'+str(nro_ciclo)+'-'+tipo_colegio+'C'+str(nro_ciclo)+'CU'+str(nro_cuota)
    return cod

def generarPass(nombre_completo, dni):
    full_text = nombre_completo+dni
    hash_object = hashlib.sha256(bytes(full_text, encoding='utf-8'))
    hex_dig = hash_object.hexdigest()
    password = hex_dig[7]+hex_dig[17]+dni+hex_dig[37]+hex_dig[47]
    return password

def generarEmail(dni, nombre_completo=None):
    if nombre_completo is None:
        return dni+'@uniq.edu.pe'
    else: 
        return nombre_completo.split('')[2]+dni+'@uniq.edu.pe'

#··············· INFRAESTRUCTURA ACADEMICA ····················
def escuelasProfesionales():
    url = "https://sysapis.uniq.edu.pe/api/dev/academico/escuelas-profesionales"
    response = requests.get(url)
    return response.json()
def pabellones():
    url = "https://sysapis.uniq.edu.pe/api/dev/infraestructura/pabellones"
    response = requests.get(url)
    return response.json()
def aulas():
    url = "https://sysapis.uniq.edu.pe/api/dev/infraestructura/aulas"
    response = requests.get(url)
    return response.json()




def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)