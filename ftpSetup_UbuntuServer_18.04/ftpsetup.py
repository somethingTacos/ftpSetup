import os

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

#print warning
print(bcolors.WARNING + "-----" + bcolors.FAIL + " READ BELOW " + bcolors.WARNING + "-----" + bcolors.ENDC)
os.system("cat README.txt")
print(bcolors.WARNING + "----------------------" + bcolors.ENDC)

#functions
def printTag(message, tag, color):
    if color == "GREEN":
        print(bcolors.ENDC + "[ " + bcolors.OKGREEN + tag + bcolors.ENDC + " ] " + message)
    if color == "RED":
        print(bcolors.ENDC + "[ " + bcolors.FAIL + tag + bcolors.ENDC + " ] " + message)
    if color == "YELLOW":
        print(bcolors.ENDC + "[ " + bcolors.WARNING + tag + bcolors.ENDC + " ] " + message)
    return;
def bashrcAlter():
    me = os.environ['SUDO_USER']
    os.system("echo '' >> /home/{0}/.bashrc".format(me))
    line1 = "THEIP=$(ifconfig | grep 'inet '| grep -v '127.0.0.1' | cut -d: -f2 | awk '{ print $2}')"
    line2 = 'PS1="\[\\033[01;31m\]\\u@"$THEIP" \w $\[\\033[00m\] ";'
    bashrc_file = "/home/{0}/.bashrc".format(me)

    with open(bashrc_file,"a") as textFile:
        print("{}".format(line1), file=textFile)
        print("{}".format(line2), file=textFile)
        
    print()
    print("You will need to source the .bashrc file, or\n wait for you next reboot to see the new custom prompt")
    return;
def updateAll():
    print(bcolors.WARNING + "Starting System update..." + bcolors.ENDC)
    print(bcolors.HEADER + "Syncing package indexes..." + bcolors.ENDC)
    os.system("apt-get update -y")
    print(bcolors.HEADER + "Upgrading packages..." + bcolors.ENDC)
    os.system("apt-get upgrade -y")
    print(bcolors.HEADER + "Running dist-upgrade..." + bcolors.ENDC)
    os.system("apt-get dist-upgrade -y")
    print()
    printTag("System Update","DONE","GREEN")
    print()
    return;
def startInstall():
    if vsftpd_installed == 1:
        print(bcolors.OKGREEN + "vsftpd is installed  :)" + bcolors.ENDC)
    else:
        print(bcolors.FAIL + "vsftpd needs to be installed..." + bcolors.ENDC)
        os.system("apt-get install vsftpd -y")
        printTag("Installing vsftpd","Done","GREEN")

        
    print(bcolors.WARNING + "Setting up vsftpd" + bcolors.ENDC)
    #configure firewall
    print(bcolors.HEADER + "Adding Firewall rules..." + bcolors.ENDC)
    os.system("cp /etc/vsftpd.conf /etc/vsftpd.conf.orig")
    os.system("ufw enable")
    os.system("ufw allow 20/tcp")
    os.system("ufw allow 21/tcp")
    os.system("ufw allow 990/tcp")
    os.system("ufw allow 40000:50000/tcp")
    printTag("Firewall Setup","DONE","GREEN")
    #configure newUser
    print(bcolors.HEADER + "Configuring " + newUserName + "'s ftp dir..." + bcolors.ENDC)
    os.system("mkdir /home/{0}/ftp".format(newUserName))
    os.system("chown nobody:nogroup /home/{0}/ftp".format(newUserName))
    os.system("chmod a-w /home/{0}/ftp".format(newUserName))
    os.system("mkdir /home/{0}/ftp/files".format(newUserName))
    os.system("chown {0}:{0} /home/{0}/ftp/files".format(newUserName))
    printTag("FTP dir","SETUP","GREEN")
    #copy new config
    print(bcolors.HEADER + "coping new vsftpd config..." + bcolors.ENDC)
    os.system("mv /etc/vsftpd.conf /etc/vsftpd.conf.orig")
    os.system("cp vsftpd.conf /etc/")
    printTag("vsftpd config","DONE","GREEN")
    #add ftponly shell
    print(bcolors.HEADER + "Adding ftponly shell..." + bcolors.ENDC)
    os.system('echo "{0}" >> /etc/vsftpd.userlist'.format(newUserName))
    os.system('echo "#!/bin/sh" > /bin/ftponly')
    os.system('echo "This user can only be used for FTP" >> /bin/ftponly')
    os.system("chmod a+x /bin/ftponly")
    os.system('echo "/bin/ftponly" >> /etc/shells')
    os.system("usermod {0} -s /bin/ftponly".format(newUserName))
    printTag("ftponly shell","ADDED","GREEN")
    printTag("vsftpd setup","DONE","GREEN")
    print(bcolors.WARNING + "restarting vsftpd service..." + bcolors.ENDC)
    os.system("systemctl restart vsftpd")
    printTag("vsftpd service restart","DONE","GREEN")
    return;

#continue?
start = input("Start? (y/[n]): ")
if start == "y":
    altBRC = input("\nAppend new PS1 format to bashrc file?\n\nExample: <name>@<IP> <working dir>\n\nAppend? (y/[n]): ")
    updatePlox = input("\nUpdate All the things? (y/[n]): ")
    print("Starting Intallation...")
    os.system("./check.sh")
    from info import *
    os.system('rm info.py')
    newUserName = input("Enter a new username for ftponly user: " )
    os.system("adduser {0}".format(newUserName))
    if updatePlox == "y":
        updateAll()
    startInstall()
    if altBRC == "y":
        bashrcAlter()
    print()
    printTag("Installation","COMPLETE","GREEN")
    print()
else:
    print("well... never mind then...")
    print()
    printTag("Installation","Aborted","RED")
    print()
