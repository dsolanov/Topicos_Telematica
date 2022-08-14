import socket
from typing import final

from matplotlib.pyplot import connect

print('')
# definimos puerto y host
HOST, PORT = '127.0.0.1', 8080

# se define el funcionamiento con TCP e IPV4 junto con la creacion y vinculacion del socket a un host y un puerto
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversocket.bind((HOST, PORT))
serversocket.listen(1)

print('Servidor en el Puerto: ', PORT)
print('')

# Escuchar continuamente
while True:
    connection, address = serversocket.accept()
    request = connection.recv(1024).decode('utf-8')
    #print(request)

    string_list = request.split(' ')
    method = string_list[0]
    requesting_file = string_list[1]

    print('El Cliente pidio: ', requesting_file)

    myFile = requesting_file.split('?')[0]
    myFile = myFile.lstrip('/')

    if (myFile == ''):
        myFile = 'index.html'

    try:
        file = open(myFile, 'rb')
        response = file.read()
        file.close()

    # devolver cabeceras
        header = 'HTTP/1.1 200 OK\n'

        if(myFile.endswith('.jpg')):
           mimetype = 'image/jpeg'
        elif(myFile.endswith('.jpeg')):
            mimetype = 'image/jpeg'  
        elif(myFile.endswith('.doc')):
            mimetype = 'application/msword'
        elif(myFile.endswith('.csv')):
           mimetype = 'text/csv'
        elif(myFile.endswith('.pdf')):
            mimetype = 'application/pdf'
        elif(myFile.endswith('.xls')):
            mimetype = 'application/vnd.ms-excel'
        else:
            mimetype = 'text/html'
        header += 'Content-Type: ' + str(mimetype) + '\n\n'

    except Exception as e:
        #CONTROLANDO EL ERROR
        header = 'HTTP/1.1 404 Not Found\n\n'
        response = '<html><body>WE ARE SORRY\n ERROR 404\n File not found</body></html>'.encode('utf-8')

    final_response = header.encode('utf-8')
    final_response += response
    connection.send(final_response)
    connection.close()