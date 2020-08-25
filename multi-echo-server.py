from multiprocessing import Process
import socket
import time

HOST = '127.0.0.1'  
PORT = 9000        

def client_process( client_socket, addr ):
    with client_socket as cs:
        print( '[ Server Message : Connected by {} ]'.format( addr ) )
        while True:
            data = cs.recv( 1024 )
            if not data:
                break
            cs.sendall( data )
            time.sleep( 5 )

def server_process():
    print( '[ Server info : ( {}:{} ) ]'.format( HOST, PORT ) )
    with socket.socket( socket.AF_INET, socket.SOCK_STREAM ) as s:
        s.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )
        s.bind( ( HOST, PORT ) )
        while True:
            s.listen()
            conn, addr = s.accept()
            p = Process( target = client_process, args = ( conn, addr, ) )
            p.start()

    print( '[ Stop Server ]' )

if __name__ == '__main__':
    server_process()
