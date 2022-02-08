#!/bin/bash
# VARIABLES
miLista=(
    'Añadir Descripcion.'
    "MINAGE - Linux"
    'MAXAGE - Linux'
    'Listar CUENTAS - Linux'
    'MINAGE - Aix'
    'MAXAGE - Aix'
    'Listar CUENTAS de MINAGE- Aix'
    'Listar CUENTAS de MAXAGE- Aix'
    'MINLEN Sistemas Aix'
    'LIstar MINLEN Sistemas Aix'
    'Salir'
)

user=$(logname)
home="/home/${user}/Compliance/"

function descripcion_delMenu() {
    index=0
    for item in "${miLista[@]}"; do
        ((index = index + 1))
        echo -e "$index.-\t   ${item}"
    done
}

function logWarn() {
    START='\033[01;33m'
    END='\033[00;00m'
    MESSAGE=${@:-""}
    echo -e "${START}${MESSAGE}${END}"
}

function logInfo() {
    START='\033[01;32m'
    END='\033[00;00m'
    MESSAGE=${@:-""}
    echo -e "${START}${MESSAGE}${END}"
}

function logError() {
    START='\033[01;31m'
    END='\033[00;00m'
    MESSAGE=${@:-""}
    echo -e "${START}${MESSAGE}${END}"
}

function log() {
    MESSAGE=${@:-""}
    echo -e "${MESSAGE}"
}
# FUNCION CONTINUAR CON EL SCRIPT
function continuar() {
    while true; do
        log ""
        read -p "Desea Continuar S/N? : " yn
        case $yn in
        [Ss]*)
            clear
            menu
            break
            ;;
        [Nn]*)
            logError "Finaliza la Ejecución. !"
            exit
            ;;
        *) logWarn "\nSeleccione Si o No." ;;
        esac
    done
}

function add () {
    rm -f ${home}'descripciones.txt'
    nohup gedit ${home}'descripciones.txt' </dev/null >nohup.out 2>nohup.err &
}

function command_sed () {
    sed -i 's/:ES//g' "${home}descripciones.txt"
    sed -i 's/:CZ//g' "${home}descripciones.txt"
    sed -i 's/:DE//g' "${home}descripciones.txt"
}

function listar_linux () {
    command_sed
    cat  ${home}'descripciones.txt' | awk '{print "chage -l "$2}'
    cat  ${home}'descripciones.txt' | awk '{print "chage -l "$2}' > ${home}'resultado.txt'
    gedit ${home}'resultado.txt'
}

function listarMaxage_aix () {
    command_sed
    cat ${home}'descripciones.txt' | awk '{print "lsuser -a maxage "$2}'        
    cat ${home}'descripciones.txt' | awk '{print "lsuser -a maxage "$2}' > ${home}'resultado.txt'     
    gedit ${home}'resultado.txt'
}

function listarMinage_aix () {
    command_sed
    cat ${home}'descripciones.txt' | awk '{print "lsuser -a minage "$2}'        
    cat ${home}'descripciones.txt' | awk '{print "lsuser -a minage "$2}' > ${home}'resultado.txt'      
    gedit ${home}'resultado.txt'
}

function minage_linux () {
    command_sed
    cat ${home}'descripciones.txt' | awk '{print "chage -m 1 "$2}'
    cat ${home}'descripciones.txt' | awk '{print "chage -m 1 "$2}' > ${home}'resultado.txt'
    gedit ${home}'resultado.txt'
}

function minage_aix () {
    command_sed
    cat ${home}'descripciones.txt' | awk '{print "chuser minage=1 "$2}'    
    cat ${home}'descripciones.txt' | awk '{print "chuser minage=1 "$2}' > ${home}'resultado.txt'
    gedit ${home}'resultado.txt'
}

function maxage_linux () {
    command_sed
    cat  ${home}'descripciones.txt' | awk '{print "chage -M 90 "$2}'
    cat  ${home}'descripciones.txt' | awk '{print "chage -M 90 "$2}' > ${home}'resultado.txt'
    gedit ${home}'resultado.txt'
}

function maxage_aix () {
    command_sed
    cat ${home}'descripciones.txt' | awk '{print "chuser maxage=13 "$2}'        
    cat ${home}'descripciones.txt' | awk '{print "chuser maxage=13 "$2}' > ${home}'resultado.txt'       
    gedit ${home}'resultado.txt'
}

function minlen () {
    command_sed
    cat  ${home}'descripciones.txt' | awk '{print "chsec -f /etc/security/user -s "$2 " -a minlen=14"}'
    cat  ${home}'descripciones.txt' | awk '{print "chsec -f /etc/security/user -s "$2 " -a minlen=14"}' > ${home}'resultado.txt'
    gedit ${home}'resultado.txt'
}

function listar_minlen () {
    command_sed
    cat  ${home}'descripciones.txt' | awk '{print "chsec -f /etc/security/user -s "$2 " -a minlen"}'
    cat  ${home}'descripciones.txt' | awk '{print "chsec -f /etc/security/user -s "$2 " -a minlen"}' > ${home}'resultado.txt'
    gedit ${home}'resultado.txt'
}

# FUNCION MENU
function menu() {
    while true; do
        echo -e "\t********************************"
        descripcion_delMenu
        echo -e "\t********************************"
        log ""
        read -p "Seleccione una opcion de 1 a ${#miLista[@]} ? : " op
        case $op in
        1)
            clear
            logInfo "Copia y Pega las DESCRIPCIONES, en el fichero descripciones.txt !\n"
            add
            menu
            #continuar
            break
            ;;
        2)
            clear
            logInfo "MINAGE Sistemas Linux!\n"
            minage_linux
            log ""
            menu
            #continuar
            break
            ;;
        3)
            clear
            logInfo "MAXAGE Sistemas Linux!\n"
            maxage_linux
            log ""
            menu
            #continuar
            break
            ;;
        4)
            clear
            logInfo "LISTAR CUENTAS para Sistemas Linux!\n"
            listar_linux
            log ""
            menu
            #continuar
            break
            ;;
        5)
            clear
            logInfo "MINAGE para Sistemas Aix !\n"
            minage_aix
            log ""
            menu
            #continuar
            break
            ;;
        6)
            clear
            logInfo "MAXAGE para Sistemas Aix !\n"
            maxage_aix
            log ""
            menu
            #continuar
            break
            ;;
        7)
            clear
            logInfo "LISTAR CUENTAS de MINAGE para Sistemas Aix !\n"
            listarMinage_aix
            log ""
            menu
            #continuar
            break
            ;;
        8)
            clear
            logInfo "LISTAR CUENTAS de MAXAGE para Sistemas Aix !\n"
            listarMaxage_aix
            log ""
            menu
            #continuar
            break
            ;;
        9)
            clear
            logInfo "EDITAR CUENTAS para MINLEN para Sistemas Aix !\n"
            minlen
            log ""
            menu
            #continuar
            break
            ;;
        10)
            clear
            logInfo "LISTAR CUENTAS para MINLEN para Sistemas Aix !\n"
            listar_minlen
            log ""
            menu
            #continuar
            break
            ;;
        ${#miLista[@]})
            logError "Gracias !Hasta pronto! 😎\n\n"
            break
            ;;
        *) logWarn "\nSeleccione una Opción de 1 a ${#miLista[@]}.\n" ;;
        esac
    done
}
log ""
clear
menu