#!/usr/bin/env sh
# Thanks Andres Demski for this tool!!  

APP=${@:-/bin/bash}

IMAGE=pes_image

DOCKER_BASHRC=/tmp/.docker_${USER}_bashrc

rm -rf ${DOCKER_BASHRC} 2>/dev/null
cp ${HOME}/.bashrc ${DOCKER_BASHRC} 2>/dev/null
echo "PS1=\"(docker) \$PS1\"" >> ${DOCKER_BASHRC}

docker run \
    -v ${HOME}:${HOME} \
    -v /etc/passwd:/etc/passwd:ro \
    -v /etc/shadow:/etc/shadow:ro \
    -v /etc/group:/etc/group:ro \
    -v /tmp:/tmp \
    -v ${DOCKER_BASHRC}:${HOME}/.bashrc \
    -v /var/run/dbus:/var/run/dbus \
    -v /usr/share/git/completion:/usr/share/git/completion \
    --privileged \
    --net=host \
    -i -w $PWD -t -u $(id -u):$(id -g) --rm \
    -e DISPLAY=$DISPLAY \
    --group-add=plugdev \
    --group-add=sudo \
    $IMAGE \
    $APP
