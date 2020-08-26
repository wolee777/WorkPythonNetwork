import socket

HOST = '192.168.101.101'  
PORT = 5000       

actions = [ 'DC-ST', 'LD1ON', 'LD2ON', 'LD1OF', 'LD2OF', 'LDAON', 'LDAOF', 'LDBLK', 'DCFOR', 'DCBAK' ]

menu = '''
1. LED 1 ON
2. LED 2 ON
3. LED 1 OFF
4. LED 2 OFF
5. LED 1/2 ON
6. LED 1/2 OFF
7. LED BLINK
8. DC Motor forword
9. DC Motor backword
0. DC Motor stop
q. quit

select : '''

with socket.socket( socket.AF_INET, socket.SOCK_STREAM ) as s:
    s.connect( ( HOST, PORT ) )

    while True:
        select = input( menu )
        if select.lower() == 'q':
            s.send( b'STOPQ' )
            break
        s.send( actions[ int( select ) ].encode() )

        recv_message = s.recv( 1024 ).decode() 
        print( '[ Client Message : {} ]'.format( recv_message ) )

print( '[ Stop Client]' )
