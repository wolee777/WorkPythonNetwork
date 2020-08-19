import socket

HOST = '192.168.101.101'  
PORT = 9000       

with socket.socket( socket.AF_INET, socket.SOCK_STREAM ) as s:
    s.connect( ( HOST, PORT ) )
    select = int( input( 'Input multiple number ( 1 ~ 99, QUIT : other number ): ' ) )
    while select >= 1 and select <= 99:
        s.send( str( select ).encode() )
        
        print( '[ Client Message : Received : ]' )
        recv_messages = []

        recv_message = s.recv( 1024 ).decode() 
        print( recv_message )

        select = int( input( 'Input multiple number ( 1 ~ 99, QUIT : other number ): ' ) )

print( '[ Stop Client]' )
