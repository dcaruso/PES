echo "***********************************************************************************************"
echo "* Chequear de instalar uinput primero segun: https://github.com/tuomasjjrasanen/python-uinput *"
echo "***********************************************************************************************"
sudo modprobe uinput
sudo chmod 777 /dev/uinput
echo ">> End setup!"
