import socket, os, json, atexit, ssl, getpass, click, sys

from prettytable import PrettyTable
from fabric.api import *
from fabric.contrib.files import exists

@task
def putFile(localPath=None, destinationPath=None, owner=None, fileMode=None, createDir=None):
	yes = set(['yes','y', 'ye', ''])
	no = set(['no','n'])
	if localPath is None:
		localPath = raw_input("Enter the absolute local path to the file you wish to transfer:")
		if os.path.isfile(localPath) is False:
			sys.stdout.write("Your local path/file is wrong, try again")
			quit()
	if destinationPath is None:
		destinationPath = raw_input("Enter the path you wish to drop this file:")
	if owner is None:
		owner = raw_input("Enter the file owner and group(format:$owner.$group):")
	if fileMode is None:
		fileMode = raw_input("Enter the file permissions(4 digits):")
		if len(fileMode) != 4:
			sys.stdout.write("Please enter at least 4 digits")
			quit()
	if createDir is None:
		choice = raw_input("Do you need to create the remote directory on the server(s)?:").lower()
		if choice in yes:
		   choice = True
		elif choice in no:
		   choice = False
		else:
		   sys.stdout.write("Please respond with 'yes' or 'no'")
		   quit()
		if choice == True:
			newdir=destinationPath.split("/")
			del newdir[-1]
			newdir="/".join(newdir)
			sudo("mkdir -p %s" % (newdir))
			sudo("sudo chown -R %s %s" % (owner,newdir))
	put(localPath, destinationPath, mode=fileMode, use_sudo=True)
	run("sudo chown %s %s" % (owner,destinationPath))
