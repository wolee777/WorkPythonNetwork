import gpio_server_led_motor as GPIO
from multiprocessing import Process
import socket

HOST = '192.168.101.101' 
PORT = 9000       

# sensor initialize
GPIO.led_init()
GPIO.led_all_off()

GPIO.motor_init()

# sensor action list
actions = { 'DC-ST': GPIO.motor_stop, 'LD1ON': GPIO.led_1_on, 'LD2ON': GPIO.led_2_on,
            'LD1OF': GPIO.led_1_off, 'LD2OF': GPIO.led_2_off, 'LDAON': GPIO.led_all_on,
            'LDAOF': GPIO.led_all_off, 'LDBLK': GPIO.led_blink, 'DCFOR': GPIO.motor_forword, 'DCBAK': GPIO.motor_backword }
action_codes = actions.keys()

def client_process( client_socket, addr ):
    with client_socket as cs:
        print( '[ Server Message : Connected by {} ]'.format( addr ) )
        while True:
            data = cs.recv( 5 ).decode()
            print( '[ Server Message : Receive message [ {} ] - {} ]'.format( addr, data ) )

            if data in action_codes:
                print( '[ Server Message : sensor action {} ]'.format( actions[ data ] ) )
                actions[ data ]()
                cs.send( 'action - OK!!!'.encode() )
            else:
                break

def server_process():
    print( '[ Server info : ( {}:{} ) ]'.format( HOST, PORT ) )
    with socket.socket( socket.AF_INET, socket.SOCK_STREAM ) as ss:
        ss.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )
        ss.bind( ( HOST, PORT ) )
        while True:
            ss.listen()
            conn, addr = ss.accept()
            p = Process( target = client_process, args = ( conn, addr, ) )
            p.start()
    print( 'Stop Server' )            

if __name__ == '__main__':
    server_process()