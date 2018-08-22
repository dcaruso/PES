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

# Trabajar sobre la imagen de docker

## Construir el contenedor en tu host

En una consola (Linux) o `cmd` (Windows), correr lo siguiente para traerse la imagen

```
	$ docker pull dcaruso/pes_image
```

Este proceso demora tiempo ya que se está descargando la imagen desde internet e instalandola en su sistema y se debe hacer una única vez o si la imagen se actualiza, se puede correr nuevamente.

## Uso del contenedor

Luego para usar siempre la imagen, en la consola correr:

```
 	$ docker run -p 8888:8888 --user pesuser -t -i dcaruso/pes_image
```

## Levantar jupyter notebook

Una vez dentro del contenedor del `pes_image` correr:

```
	pesuser@052c9b73f1e5:~$ jupyter notebook --ip 0.0.0.0
```

Si todo ha salido bien, deberías ver como respuesta algo parecido a esto:

```
	[I 02:53:36.756 NotebookApp] Writing notebook server cookie secret to /home/pesuser/.local/share/jupyter/runtime/notebook_cookie_secret
	[I 02:53:36.909 NotebookApp] Serving notebooks from local directory: /home/pesuser
	[I 02:53:36.909 NotebookApp] The Jupyter Notebook is running at:
	[I 02:53:36.909 NotebookApp] http://(052c9b73f1e5 or 127.0.0.1):8888/?token=968d04208a2b662b3bde4fff11996d74d89e9b925eaa7845
	[I 02:53:36.910 NotebookApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).
	[W 02:53:36.910 NotebookApp] No web browser found: could not locate runnable browser.
	[C 02:53:36.910 NotebookApp] 
    
    Copy/paste this URL into your browser when you connect for the first time,
    to login with a token:
        http://(052c9b73f1e5 or 127.0.0.1):8888/?token=968d04208a2b662b3bde4fff11996d74d89e9b925eaa7845
```

Tenés que abrir un navegador web (chrome, firefox, el que tengas instalado) e ir a `http://localhost:8888/tree`

Ahi te va a pedir el token de login, tenés que copiar el token que te tiró por consola, para el ejemplo sería: `968d04208a2b662b3bde4fff11996d74d89e9b925eaa7845`
