# Sistema Académico CEPRE - UNIQ
#### **Being developed by**:
- **Corporacion Juñuy S.A.C.** - [Sitio Web](https://junuy.net.pe/).
#### **Client**:
- **UNIVERSIDAD NACIONAL INTERCULTURAL DE QUILLABAMBA** - [UNIQ](https://uniq.edu.pe/).
---
##

## Informacion del sistema 
Sistema que servira para la gestion y administracion del centro pre-universitario CEPRE - UNIQ
### **Herramientas utilizadas para el desarrollo del sistema**
* _[Python v3.x](https://www.python.org/)_
* _[Django v3.x.x](https://www.djangoproject.com)_
* _[Django Rest Framework 3.x.x](https://www.django-rest-framework.org/)_
* _[MySQL v5.7](https://www.mysql.com/)_
* _[Docker](https://www.docker.com)_

### **Despliegue de proyecto en local:**
* Clonar el repositorio mediante HTTPS con: _"git clone https://gitlab.com/renanfer14.ls/sys-cepru.git"_ o tambien
* Clonar el repositorio mediante SSH con: _"git clone git@gitlab.com:renanfer14.ls/sys-cepru.git"_

* [WINDOWS] Crear un entorno virtual con python 3.x con el comando: **python -m venv nombre_entorno_virtual** y seguidamente ubicarse en nombre_entorno_virtual/Scripts/ y activar el entorno virtual con el comando **activate**
* [LINUX/UBUNTU] Crear un entorno virtual con python 3.x con el comando: **python3 -m venv nombre_entorno_virtual** y seguidamente ejecutar **source nombre_entorno_virtual/bin/activate** y listo.
* o a traves de la libreria [virtualenv](https://developer.mozilla.org/es/docs/Learn/Server-side/Django/development_environment) con el comando: **mkvirtualenv nombre_entorno_virtual**
* Una vez activo el entorno virtual, situarse en la raiz del sistema y proceder a instalar las dependecias que se detallan en el archivo **requirements.txt**, esto mediante el comando **pip/pip3 install -r requirements.txt**.
* Configure las variables del entorno virtual creando un archivo *.env* que debera estar dentro de la carpeta /cepru segun se detalla en el archivo *.env.example* (de ser necesario)
* Con las configuraciones ya listas ejecute: **python manage.py migrate** para habilitar las tablas en la base de datos
* Ejecute el comando **python manage.py createsuperuser** para generar un usuario de acceso
* Ejecute **python manage.py runserver** y dirijase a su navegador en el puerto http://127.0.0.1:8000 o localhost:8000 en el cual se desplegara la ejecucion del servidor
* para finalizar su sesion desde la ventana de comandos presione **CTRL + C** para detener el servidor y el comando *deactivate* o tambien dirjirse a la carpeta nombre_entorno_virtual/Scripts/ y escribir *deactivate.bat*

