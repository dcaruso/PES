# Instalación de Docker

## Linux

```
    $ sudo apt-get install apt-transport-https dirmngr
    $ sudo echo 'deb https://apt.dockerproject.org/repo debian-stretch main' >> /etc/apt/sources.list
    $ sudo apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D
    $ sudo apt-get update
    $ sudo apt-get install docker-engine
    $ sudo usermod -a -G docker $USER
```

## Windows

Ver tutorial: https://docs.docker.com/docker-for-windows/install/
Nota: Si usan una versión Home de Windows, el proceso es ligeramente diferente. Fijarse bien.

# Trabajar sobre la imagen de docker

## Construir el contenedor en tu host

En una consola (Linux) o `cmd` (Windows), correr lo siguiente para traerse la imagen

```
    $ docker pull dcaruso/pes_image
```

Este proceso demora tiempo ya que se está descargando la imagen desde internet e instalandola en su sistema y se debe hacer una única vez o si la imagen se actualiza, se puede correr nuevamente.

## Uso del contenedor

Luego para usar siempre la imagen, en la consola correr:

### Linux

```
    $ docker run -p 8888:8888 --privileged -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix -v /dev/video0:/dev/video0 -v ${PWD}:/home/pesuser/pes --user pesuser -it dcaruso/pes_image
```

### Windows

```
    $ docker run -p 8888:8888 --privileged --name pes -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix -v /dev/video0:/dev/video0 -v %cd%:/home/pesuser/pes --user pesuser -it dcaruso/pes_image
```     

si no funciona, probar este:
 
``` 
    $ docker run -p 8888:8888 --privileged --name pes -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix -v /dev/video0:/dev/video0 -v /dev/bus/usb:/dev/bus/usb -v /%cd%:/home/pesuser/pes --user pesuser -it dcaruso/pes_image
```

## Setup
Una vez dentro del contenedor del `pes_image` correr:

```
    pesuser@5ff40f427922:~$ ./setup.sh
```

Esto se debe hacer una sola vez y se engarga de traer el repositorio de github de la cátedra a un directorio especifico. Este directorio estará compartido con el host, de forma de poder acceder fuera del docker tambien.

## Al tener ya creado el contenedor
Es posible que la imagen no desaparezca cuando lo cierran. Solo lo hará si queda inactiva un tiempo. Si se levanta otro contenedor con la imagen, será como 'empezar de cero'.
Para asegurarse correr el comando
```
    $ docker container ls -a
```
Debe verse el contenedor cuyo nombre es PES (si usaron el comando de más arriba), estará detenido.
Volver a correrlo con
```
    $ docker run pes
    $ docker attach pes
```
El segundo comando es para entrar a la terminal desde el contenedor.

## Levantar jupyter notebook

```
    pesuser@5ff40f427922:~$ ./run_jupyter.sh
```

Si todo ha salido bien, deberías ver como respuesta algo parecido a esto:

```
[I 20:28:00.611 NotebookApp] Writing notebook server cookie secret to /home/pesuser/.local/share/jupyter/runtime/notebook_cookie_secret
[W 20:28:00.729 NotebookApp] All authentication is disabled.  Anyone who can connect to this server will be able to run code.
[I 20:28:00.748 NotebookApp] Serving notebooks from local directory: /home/pesuser
[I 20:28:00.749 NotebookApp] The Jupyter Notebook is running at:
[I 20:28:00.749 NotebookApp] http://(5ff40f427922 or 127.0.0.1):8888/
[I 20:28:00.749 NotebookApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).
[W 20:28:00.749 NotebookApp] No web browser found: could not locate runnable browser.
[W 20:28:09.153 NotebookApp] Clearing invalid/expired login cookie username-localhost-8888

```

### Linux

Tenés que abrir un navegador web (chrome, firefox, el que tengas instalado) e ir a `http://localhost:8888/tree`

### Windows

Tenés que abrir un navegador web (chrome, firefox, el que tengas instalado) e ir a `http://127.0.0.1:8888/`
