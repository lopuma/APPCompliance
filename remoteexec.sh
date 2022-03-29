#! /bin/bash
servidores=$(cat /tmp/remotes.txt)

<<<<<<< HEAD
SSHPASS=Dopracau2000lopo
=======
SSHPASS=w6EjLf88eBh4UOJ
>>>>>>> 282f4bf5f988b13e11305979656d4b45d697c572
export SSHPASS

for host in $servidores; do 
	sshpass -e ssh-copy-id $host
	scp /home/esy9d7l1/Alvaro/Desarrollo/Bash/sudo_itss_preg4.sh  $host:/tmp/
done

for host in $servidores; do
	ssh $host 'sudo /tmp/sudo_itss_preg4.sh;
	rm /tmp/sudo_itss_preg4.sh &> /dev/null;
	user=$(logname);
	rm /home/${user^^}/.ssh/authorized_keys &> /dev/null;
	rm /home/${user,,}/.ssh/authorized_keys &> /dev/null'
done
