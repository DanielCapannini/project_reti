# -*- coding: utf-8 -*-
"""
Created on Mon May 23 17:20:36 2022

@author: daniel.capannini@studio.unibo.it
matricola: 0000971194
"""

import socket as sk
import os

sock = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)

server_address = ('localhost', 10000)
BUFFER_SIZE = 4096
welcom_message = '\r per avere lista file: LIST\r\n\r per ricevere file: GET file_name\r\n\r per inviare file: PUT file name\r\n\r per chiudere connessime: EXIT\r\n'

print(welcom_message)
while True:
    file_name = os.listdir('./file_client/')
    imp = input('inserisci comando: ')
    
    if imp == 'EXIT':
        sock.close()
        break
    
    #controllo se il messaggio da tastiera ha senso
    imp_message = imp.split(' ')
    if len(imp_message)!=1 and file_name.__contains__(imp_message[1]) and imp_message[0] == 'GET':
        print('file gia presente')
    elif len(imp_message)!=1 and not file_name.__contains__(imp_message[1]) and imp_message[0] == 'PULL':
        print('file non presente')
    elif imp != 'LIST' and imp_message[0] != 'GET' and imp_message[0] != 'PULL':
        print('comando non valido')
    else:
        try:
            sent = sock.sendto(imp.encode(), server_address)  #invio messaggio al server
            data, server = sock.recvfrom(BUFFER_SIZE)         #ricezione messaggio di risposta
            
            print('dati in transito')
            if imp == 'LIST':
                print ( data.decode('utf8'))
                
            if imp.startswith('GET'):     #gestione GET
                
                if data == 'non presente nome file'.encode() or data == 'file non presente'.encode():
                    print ( data.decode('utf8'))
                    
                else:
                    with open('./file_client/'+imp_message[1], "wb") as f:
                        f.write(data)
                        while True:
                            bytes_read, server = sock.recvfrom(BUFFER_SIZE)
                            if bytes_read == 'fine_fine'.encode():
                                break
                            f.write(bytes_read)
                    f.close()
            
            if imp.startswith('PUT'):     #gestione PUT
                if data.decode() == 'non presente nome file' or data.decode() == 'file gia presente':
                    print ( data.decode('utf8'))
                elif data.decode() == 'GET':
                    with open('./file_client/'+imp_message[1], 'rb') as f:
                        while True:
                            bytes_read = f.read(BUFFER_SIZE)
                            if not bytes_read:
                                sent = sock.sendto('fine_fine'.encode(), server_address)
                                break
                            sent = sock.sendto(bytes_read, server_address)
                            print(bytes_read)
                        f.close()
        except Exception as info:
            print(info)
                    
