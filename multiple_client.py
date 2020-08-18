import socket

HOST = '127.0.0.1'  
PORT = 9000       

with socket.socket( socket.AF_INET, socket.SOCK_STREAM ) as s:
    s.connect( ( HOST, PORT ) )
    select = int( input( 'Input multiple number ( 1 ~ 99, QUIT : other number ): ' ) )
    while select >= 1 and select <= 99:
        s.send( str( select ).encode() )
        datas = s.recv( 108 )
        
        print( '[ Client Message : Received : ]' )  
        print( datas )          
        for data in datas:
            print( data )
        select = int( input( 'Input multiple number ( 1 ~ 99, QUIT : other number ): ' ) )

print( '[ Stop Client]' )
