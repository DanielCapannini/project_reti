# -*- coding: utf-8 -*-
"""
Created on Mon May 23 16:34:32 2022

@author: daniel
"""

import socket as sk
import os

#creiamo il socket
sock = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
#associamo il socket alla porta
server_address = ('localhost', 10000)
print ('\n\r starting up on %s port %s' % server_address)
sock.bind(server_address)

BUFFER_SIZE = 4096

while True:
    file_name = os.listdir('./file_server/') #elenco file presenti
    
    try:
        print('\n\r waiting to receive message...')
        data, address = sock.recvfrom(BUFFER_SIZE)
        print (data.decode('utf8'))
        
        if data.decode('utf8') == 'LIST': #gestione comando LIST
            data_list = ' '.join(file_name)
            data_message='lista file: '+data_list
            sent = sock.sendto(data_list.encode(), address)
            print(data_list)
            print ('sent %s bytes back to %s' % (sent, address))
            
        if data.decode('utf8').startswith('GET'):   #gestione comando GET
            data_get = data.decode('utf8').split(' ')
            
            if len(data_get) == 1 or data_get[1] == '':
                data_message = 'non presente nome file'
                sent = sock.sendto(data_message.encode(), address)
                print(data_message)
                print ('sent %s bytes back to %s' % (sent, address))
            elif not file_name.__contains__(data_get[1]):
                data_message = 'file non presente'
                sent = sock.sendto(data_message.encode(), address)
                print(data_message)
                print ('sent %s bytes back to %s' % (sent, address))
            else:
                with open('./file_server/'+data_get[1], 'rb') as f:
                    while True:
                        bytes_read = f.read(BUFFER_SIZE)
                        if not bytes_read:
                            sent = sock.sendto('fine_fine'.encode(), address)
                            break
                        sent = sock.sendto(bytes_read, address)
                        print(bytes_read)
                    f.close()
                    
        if data.decode('utf8').startswith('PUT'):  #gestione comando PUT
            data_pull = data.decode('utf8').split(' ')
            if file_name.__contains__(data_pull[1]):
                data_message = 'file gia presente'
                sent = sock.sendto(data_message.encode(), address)
                print ('sent %s bytes back to %s' % (sent, address))
            elif len(data_pull) == 1 or data_pull[1] == '':
                data_message = 'non presente nome file'
                sent = sock.sendto(data_message.encode(), address)
                print(data_message)
                print ('sent %s bytes back to %s' % (sent, address))
            else:
                data_message = 'GET'
                sent = sock.sendto(data_message.encode(), address)
                with open('./file_server/'+data_pull[1], "wb") as f:
                    while True:
                        bytes_read, server = sock.recvfrom(BUFFER_SIZE)
                        if bytes_read == 'fine_fine'.encode():
                            break
                        f.write(bytes_read)
                f.close()

    except Exception as info:
        print(info)