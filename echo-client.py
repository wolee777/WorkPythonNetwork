import socket

HOST = '127.0.0.1'
PORT = 9000

client_socket = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
client_socket.connect( ( HOST, PORT ) )

client_socket.sendall( 'Hi Server~~~'.encode() )

data = client_socket.recv( 1024 )
print( '\t[ Client Message : Received : {} ]'.format( repr( data.decode() ) ) )

client_socket.close()
print( '\t[ stop client ]' )
