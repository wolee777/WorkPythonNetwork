from multiprocessing import Process
import socket

HOST = '192.168.101.101' 
PORT = 9000       

def client_process( client_socket, addr ):
    with client_socket as cs:
        print( '[ Server Message : Connected by {} ]'.format( addr ) )
        while True:
            try:
                data = int( cs.recv( 2 ) )
                print( '[ Server Message : Receive message [ {} ] - {} ]'.format( addr, data ) )

                if data >= 1 and data <= 99:
                    send_message = ""
                    for i in range( 1, 10 ):
                        multiple = data * i
                        send_message += '{0:2d} X {1:2d} = {2:2d}\n'.format( data, i, multiple )
                    print( '[ Server Message : Send message [ {} ] - {} ]'.format( addr, send_message ) )   
                    cs.send( send_message.encode() )
                    
                    print( '[ Server Message : normal send OK! ]' )
                else:
                    cs.sendall( b'0' )
                    print( '[ Server Message : abnormal send OK! ]' )

            except ValueError:
                print( '[ Server Message ( Exception ) : [ {} ] - out of range'.format( addr ) )
                print( '[ Server Message ( Exception ) : [ {} ] - close client connection'.format( addr ) )
                break


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
                
print( 'Stop Server' )            

if __name__ == '__main__':
    server_process()
