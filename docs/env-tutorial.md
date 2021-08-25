Creación de un Environment de Python
Gracias por la guía al compañero Axel Gómez.

Primero descargar [Python 2.7.10](https://www.python.org/downloads/release/python-2710/) (esta versión ya trae el pip instalado)
Luego instalar virtualenv:
```
$ python -m pip install --user virtualenv
```
Con virtualenv instalado generar un environment con python2.7 en una carpeta local (en el ejemplo: E:\UTN\PES\ENV_py2.7, pero uds coloquen su ruta).
```
$ python -m virtualenv --python=C:\Python27\python.exe E:\UTN\PES\ENV_py2.7
```
Activar el enviroment creando un archivo .bat con el siguiente contenido:
```
start cmd /k “E: & cd E:\UTN\PES & E:\UTN\PES\ENV_py2.7\Scripts\activate & cd E:\UTN\PES\repo\pes”
```
Nota: en el ejemplo se hace un clon del repo de pes en E:\UTN\PES\repo\pes. Ustedes pongan las rutas que correspondan a donde tengan el repo.

Luego de crear el .bat hacerle click derecho -> correr con permisos de administrador (si no lo hacen puede que no instale algunas de las librerías que vienen ahora)
Ya dentro del entorno limpio en python 2.7 instalar:
```
$ python -m pip install jupyterlab
$ python -m pip install numpy==1.16.6 scipy==1.1.0 Pillow==5.2.0 matplotlib==2.2.3 html5lib==1.0.1 jedi==0.10.0 jsonschema==2.6.0 qtconsole==4.4.1
```
(pueden copiar y pegar los comandos, sin el $)

Para instalar OPENCV deben descargarse el archivo .whl del siguiente link:[OpenCV](https://www.lfd.uci.edu/~gohlke/pythonlibs/#opencv)
Elijan la versión que corresponda a su sistema operativo. En mi caso es windows de 64 bits. Luego correr el comando con ese archivo.
```
$ python -m pip install opencv_python-2.4.13.7-cp27-cp27m-win_amd64.whl
```
Para instalar DeModel, tienen que descargarlo de acá: [DeModel](http://www.dilloneng.com/demodel.html)
el link directo es: [Package DeModel](http://www.dilloneng.com/uploads/2/1/2/2/21220816/demodel-0.2.tar.gz)

Ojo es un tar.gz si usan windows necesitarán descomprimirlo con 7zip o winrar creo que lo abrirá también.
Dentro tiene una carpeta llamada deModel-0.2
Correr este comando:
```
$ python deModel-0.2/setup.py install
```
Nota: tienen que poner los archivos (tanto el de OpenCV como el de DeModel) en el directorio en que esté parado el enviroment.

Documentación de las versiones instaladas:
matplotlib==2.2.3
https://matplotlib.org/2.2.3/

numpy==1.16.6
https://docs.scipy.org/doc/numpy-1.16.1/reference/

scipy==1.1.0
https://docs.scipy.org/doc/scipy-1.1.0/reference/
