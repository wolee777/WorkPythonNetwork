import socket

HOST = '127.0.0.1' 
PORT = 9000       

print( '[ Server info : ( {}:{} ) ]'.format( HOST, PORT ) )
with socket.socket( socket.AF_INET, socket.SOCK_STREAM ) as s:
    s.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )
    s.bind( ( HOST, PORT ) )
    s.listen()
    conn, addr = s.accept()
    with conn:
        print( '[ Server Message : Connected by {} ]'.format( addr ) )
        while True:
            try:
                data = int( conn.recv( 2 ) )
                print( '[ Server Message : Receive message {} ]'.format( data ) )

                if data > 1 and data < 99:
                    send_message = ""
                    for i in range( 1, 10 ):
                        multiple = data * i
                        send_message += '{0:2d} X {1:2d} = {2:2d}\n'.format( data, i, multiple )
                    print( '[ Server Message : Send message {} ]'.format( send_message ) )   
                    conn.send( send_message.encode() )
                    
                    print( '[ Server Message : normal send OK! ]' )
                else:
                    conn.sendall( b'0' )
                    print( '[ Server Message : abnormal send OK! ]' )

            except ValueError:
                print( '[ Server Message ( Exception ) : non numeric' )
                print( '[ Server Message ( Exception ) : close client connection' )
                break
                
print( 'Stop Server' )            
