#! /bin/bash
error='\e[0;1;31;48m'
completed='\e[0;1;5;38;5;48m'
reset='\e[0m'
. tsocks on

servidores=$(cat /tmp/remotes.txt)

SSHPASS=BailaconLOP4040
export SSHPASS

echo $SSHPASS

# function start(){
# # 	# for host in $servidores; do
# 	sudo /tmp/sudo_itss_preg4.sh;
# 	rm /tmp/sudo_itss_preg4.sh &> /dev/null;
# 	user=$(logname);
# 	rm /home/${user^^}/.ssh/authorized_keys &> /dev/null;
# 	rm /home/${user,,}/.ssh/authorized_keys &> /dev/null
# # done
# }


function start(){
	echo -e "\n\tSALUDO $host\n"
	ssh -t $host 'sudo /tmp/sudo_itss_preg4.sh;
	rm /tmp/sudo_itss_preg4.sh &> /dev/null;
	user=$(logname);
	rm /home/${user^^}/.ssh/authorized_keys &> /dev/null;
	rm /home/${user,,}/.ssh/authorized_keys &> /dev/null'
}

for host in $servidores; do 
	echo $host
	sshpass -e ssh-copy-id $host
	EXIT=$?
	echo "---------error ----------- $EXIT"
	if [ $EXIT == 0 ]; then
		echo -e "\n$completed Copiando clave publica y ejecutando script. $reset [cod] $EXIT\n"
		scp /tmp/sudo_itss_preg4.sh  $host:/tmp/
		echo "HOST que si $host"
		start "$host"
	elif [ $EXIT == 6 ]; then # pedir perimsis de conexion
		scp /tmp/sudo_itss_preg4.sh  $host:/tmp/
	else
		echo -e "\n$error Permission denied, password not valid, please try again. $reset [cod] $EXIT\n"
	fi
done

# for host in $servidores; do 
# 	sshpass -e ssh-copy-id $host
# 	EXIT=$?
# 	if [ $EXIT == 0 ]; then
# 		echo -e "\n$red VAL EXIT $reset $EXIT\n"
# 		scp /tmp/sudo_itss_preg4.sh  $host:/tmp/
# 	fi
# done
# echo "EXIT DESPUES DE COPIAR CLAVES $EXIT"

# if [ $EXIT == 0 ]; then
# 	start "esy9d7l1@10.132.73.0"
# else
# 	echo -e "\n$error No se ha completado $reset\n"
# fi

# for host in $servidores; do
# 	EX=$?
# 	echo "\n\tEXS $EX\n"
 
# 	ssh -t $host 'sudo /tmp/sudo_itss_preg4.sh;
# 	rm /tmp/sudo_itss_preg4.sh &> /dev/null;
# 	user=$(logname);
# 	rm /home/${user^^}/.ssh/authorized_keys &> /dev/null;
# 	rm /home/${user,,}/.ssh/authorized_keys &> /dev/null'
# done


sleep 10s
