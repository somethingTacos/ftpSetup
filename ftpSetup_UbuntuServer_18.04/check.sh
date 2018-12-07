#!/bin/bash
printf "gathering some info..."
vsftpd_installed=0
check_vsftpd=(`apt-cache policy vsftpd | grep "Installed:" `)
[ ! "${check_vsftpd[1]}" == "(none)" ] && vsftpd_installed=1

echo "vsftpd_installed="$vsftpd_installed > info.py

printf " Done\n"
