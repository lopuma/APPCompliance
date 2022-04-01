#! /bin/bash
. tsocks on
servidores=$(cat /tmp/remotes.txt)

SSHPASS=BailaconLOP2020
export SSHPASS

echo $SSHPASS

for host in $servidores; do 
	sshpass -e ssh-copy-id $host
	scp /tmp/sudo_itss_preg4.sh  $host:/tmp/
done

for host in $servidores; do
	ssh -t $host 'sudo /tmp/sudo_itss_preg4.sh;
	rm /tmp/sudo_itss_preg4.sh &> /dev/null;
	user=$(logname);
	rm /home/${user^^}/.ssh/authorized_keys &> /dev/null;
	rm /home/${user,,}/.ssh/authorized_keys &> /dev/null'
done
sleep 10s
