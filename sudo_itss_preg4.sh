#!/bin/bash

function ZY.1.2.3(){
    value=$(ls -la /etc/profile.d/secondary_logging_IBM.sh 2>&1)
    if [[ "$value" == *"No such"* || "$value" == *"No existe"* ]]; then
        resultado_ZY123="NO"
        message_ZY123="$value"
        echo -e "Checking for \e[31mZY.1.2.3 Logging ....\e[0m $resultado_ZY123 : '$message_ZY123'"
    else
        resultado_ZY123="YES"
        message_ZY123=""
        echo -e "Checking for \e[33mZY.1.2.3 Logging ....\e[0m $resultado_ZY123 : '$message_ZY123'"
    fi
}

function ZY.1.2.4(){
    value=$(ls -la /etc/logrotate.conf 2>&1)
    if [[ "$value" == *"No such"* || "$value" == *"No existe"* ]]; then
        resultado_ZY124="NO"
        message_ZY124="$value"
        echo -e "Checking for \e[31mZY.1.2.4 Logging ....\e[0m $resultado_ZY124 : '$message_ZY124'"
    else
        resultado_ZY124="YES"
        message_ZY124=""
        echo -e "Checking for \e[33mZY.1.2.4 Logging ....\e[0m $resultado_ZY124 : '$message_ZY124'"
    fi
}

function ZY.1.2.5(){
    value=$(cat /etc/sudoers 2>&1)
    if [[ "$value" == *"Permission denied"* || "$value" == *"No existe"* ]]; then
        resultado_ZY125="NO"
        message_ZY125="$value"
        echo -e "Checking for \e[31mZY.1.4.5 System Settings ....\e[0m $resultado_ZY125 : '$message_ZY125'"
    else
        resultado_ZY125="YES"
        message_ZY125=""
        echo -e "Checking for \e[33mZY.1.4.5 System Settings ....\e[0m $resultado_ZY125 : '$message_ZY125'"
    fi
}

#clear
sleep 0.5s    
echo -e "\e[32m----------------------------INICIO----------------------------\e[0m"
echo ""
echo -e "SERVIDOR : \e[1;34m$HOSTNAME\e[0m"
echo ""
sleep 0.5s    
ZY.1.2.3
sleep 0.5s    
ZY.1.2.4
sleep 0.5s    
ZY.1.2.5
sleep 0.5s
echo ""
echo -e "\e[32m-----------------------------FIN------------------------------\e[0m"
echo ""
 

