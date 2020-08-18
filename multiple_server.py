import socket

HOST = '127.0.0.1' 
PORT = 9000       

print( '[ Server info : ( {}:{} ) ]'.format( HOST, PORT ) )
with socket.socket( socket.AF_INET, socket.SOCK_STREAM ) as s:
    s.bind( ( HOST, PORT ) )
    s.listen()
    conn, addr = s.accept()
    with conn:
        print( '[ Server Message : Connected by {} ]'.format( addr ) )
        while True:
            try:
                data = int( conn.recv( 2 ) )
            except ValueError:
                print( '[ Server Message ( Exception ) : non numeric' )
            if data > 1 and data < 99:
                send_message = []
                for i in range( 1, 10 ):
                    multiple = data * i
                    send_message.append( '{0:2d} X {1:2d} = {2:2d}\n'.format( data, i, multiple ) )
                conn.sendall( send_message )
                conn.send( 'end' )
                print( '[ Server Message : normal send OK! {} ]' )
            else:
                conn.send( 'Error data' )
                conn.send( 'end' )
                print( '[ Server Message : abnormal send OK! {} ]' )

print( 'Stop Server' )            
