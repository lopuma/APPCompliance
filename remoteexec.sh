#! /bin/bash
servidores=$(cat /tmp/remotes.txt)
SSHPASS=Dopracau2000lopo
export SSHPASS

for host in $servidores; do 
	sshpass -e ssh-copy-id $host
	scp /tmp/sudo_itss_preg4.sh  $host:/tmp/
done

for host in $servidores; do
	ssh $host 'sudo /tmp/sudo_itss_preg4.sh;
	rm /tmp/sudo_itss_preg4.sh &> /dev/null;
	user=$(logname);
	rm /home/${user^^}/.ssh/authorized_keys &> /dev/null;
	rm /home/${user,,}/.ssh/authorized_keys &> /dev/null'
done