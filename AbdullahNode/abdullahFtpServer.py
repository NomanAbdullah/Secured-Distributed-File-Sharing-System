#!/usr/bin/python

"""
Project Name: A Secured Distributed File Sharing System

Project Authors: 
[+] Name: Abdullah Al Noman
[+] Mougoue Kakanou Rolly
[+] Name: Tankoua Njassep Jorest Brice
"""

from urllib.request import FTPHandler
import abdullahNodeConfig
import logging, os, hashlib
from pyftpdlib.authorizers import DummyAuthorizer, AuthenticationFailed
#from pyftpdlib.handlers import ThrottledDTPHandler, TLS_FTPHandler
from pyftpdlib.handlers import ThrottledDTPHandler, FTPHandler
from pyftpdlib.servers import ThreadedFTPServer # threaded ftp serve

class DummySHA1Authorizer(DummyAuthorizer):

    # function for authentication validation
    def validate_authentication(self, username, password, handler):
        hash_ = hashlib.sha1(password.encode('utf-8')).hexdigest()
        # error handling
        try:
            if self.user_table[username]['pwd'] != hash_:
                raise KeyError
        except KeyError:
            raise AuthenticationFailed

def main():

    # generate hash from plain password
    password = abdullahNodeConfig.ftpPass
    hash_ = hashlib.sha1(password.encode('utf-8')).hexdigest() 

    authorizer = DummySHA1Authorizer() # dummy authorizer for managing 'virtual' users

    # defining user and path
    authorizer.add_user(abdullahNodeConfig.ftpUser, hash_, homedir=abdullahNodeConfig.ftpPath, perm=abdullahNodeConfig.ftpPerm) # set username, password & homedirectory for the user
    
    dtp_handler = ThrottledDTPHandler
    dtp_handler.read_limit = 1048576  # 1024 Kb/sec (1024 * 1024)
    dtp_handler.write_limit = 1048576  # 1024 Kb/sec (1024 * 1024)

    # TLS FTP handler class
    handler = FTPHandler
    handler.authorizer = authorizer

    # TLS FTP handler class
    #handler = TLS_FTPHandler
    #handler.certfile = 'keycert.pem'
    #handler.authorizer = authorizer

    # the tls ftp handler use the alternative dtp handler class
    handler.dtp_handler = dtp_handler

    # store server logs
    logging.basicConfig(filename='/var/log/abdullahFTPServer.log', level=logging.DEBUG)

    # customised banner for clients
    handler.banner = "Welcome to AbdullahNODE!"

    server = ThreadedFTPServer((abdullahNodeConfig.ftpHost,abdullahNodeConfig.ftpPort), handler)    # binding the port and host for the ftp server

    # limiting connection
    server.max_cons = 256
    server.max_cons_per_ip = 5
    
    # Start the AbdullahFTP server
    print ("Starting AbdullahFTPServer Server on port:",abdullahNodeConfig.ftpPort)
    server.serve_forever()  

 # Closing all the threads of the TLS ftp server-client connections    
def stopftp():
    print ("Stopping AbdullahFTPServer Server on port:",abdullahNodeConfig.ftpPort)
    main.server.close_all()  

if __name__ == "__main__":
    main()