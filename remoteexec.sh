#! /bin/bash
servidores=$(cat /tmp/remotes.txt)

SSHPASS=Dopracau2000lopo
export SSHPASS

for i in $servidores; do 
	sshpass -e ssh-copy-id $i
done

for host in $servidores; do
	scp /home/esy9d7l1/Alvaro/Desarrollo/Bash/sudo_itss_preg4.sh  $host:/tmp/
	ssh -t $host 'sudo -S bash -c /tmp/sudo_itss_preg4.sh'
done
