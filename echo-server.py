import socket

HOST = '127.0.0.1' 
PORT = 9000

server_socket = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
server_socket.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )

server_socket.bind( ( HOST, PORT ) )
server_socket.listen()
client_socket, addr = server_socket.accept()

print( '[ Server Message : Connected by {} ]'.format( addr ) )

while True:
    data = client_socket.recv( 1024 )
    if not data:
        break
    
    print( '[ Server Message : received from [{0}] -> {1} ]'.format( addr, data.decode() ) )

    client_socket.sendall( data )

client_socket.close()
server_socket.close()

print( '[ Stop Server ]' )
