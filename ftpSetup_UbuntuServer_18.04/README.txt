This is what's going to happen... maybe...
- a new user will be made for ftp only (you choose the name / pass)
- [optional] full system update (indexes, packages, all the things)
- vsftpd will be installed if it isn't already
- vsftpdl.conf will be replaced
- ufw will be enabled and ports 20,21,990,40000-50000 (all tpc) will allow traffic
- some files will be created/altered: vsftpd.conf(alt), vsftpd.userlist(add), /bin/ftponly(add), /etc/shells(alt)
- [optional] append custom command prompt to current user's bashrc file
I'm probably forgetting something, but whatever.

   !!! RUN THIS AT YOUR OWN RISK !!!
