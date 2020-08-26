#sensor_NET_ClassLib.py
from multiprocessing import Process, Queue
from GPIO_ClassLib import USONIC
from I2C_ClassLib import LIGHT, TEMP_HUMI

import sqlite3
import socket
import time, datetime

class NetClient():
    def __init__( self, hostIP, hostPort ):
        self.host = hostIP
        self.port = hostPort

        self.sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
        self.server_address = ( self.host, self.port )
        self.sock.connect( self.server_address )

    def __del__( self ):
        self.sock.close()
        print( "Closing connection to the server" )

    def sendData( self, data ):
        try:
            print( "Sending --> {0}".format( data ) )
            self.sock.send( data.encode() )

        except socket.errno as e:
            print( "Socket error: %s" %str(e) )
        except Exception as e:
            print( "Other exception: %s" %str(e) )

    def receiveData( self ):
        try:
            receiveData = self.sock.recv( 20 ).decode()
            print( "Receiving --> {0}\n".format( receiveData ) )

        except socket.errno as e:
            print( "Socket error: %s" %str(e) )
        except Exception as e:
            print( "Other exception: %s" %str(e) )

        return receiveData

class USonicProcess( Process, NetClient ):
    def __init__( self, host, port ):
        Process.__init__( self, name = "USonicProcess" )
        NetClient.__init__( self, host, port )

        self.ports = ( 0, 1 )
        self.direction = ( 'out', 'in' )
        self.usonic = USONIC( self.ports, self.direction )

        self.value = 0
        self.measureCycle()
        print( '[USonicProcess __init__]' )

    def __del__( self ):
        print( '[USonicProcess __del__]' )

    def measureCycle( self ):
        conn = sqlite3.connect( 'sensorinfo.db' )
        with conn:
            cursor = conn.cursor()
            cursor.execute( 'SELECT * FROM sensor_info WHERE kind = ? and apply = 0', ( 'MEASU', ) )
            for row in cursor.fetchall():
                self.value = row[2]
                date = row[4]
                time = row[5]

        if self.value == 0:
            self.value = 30
        else:
            conn = sqlite3.connect( 'sensorinfo.db' )
            with conn:
                cursor = conn.cursor()
                cursor.execute( 'UPDATE sensor_info SET apply = ? WHERE kind = ? and date = ? and time = ?', ( 1, 'MEASU', date, time ) )
                conn.commit()

    def run( self ):
        try:
            loop = True

            print( "Ultrasonic:UltraSonic looping....." )
            while loop:
                print( "Ultrasonic:UltraSonic process....." )
                self.usonic.USONIC_send()
                self.usonic.USONIC_receive()

                now = datetime.datetime.now()
                measuredate = now.strftime( '%Y-%m-%d' )
                measuretime = now.strftime( '%H:%M:%S' )
                distance = str( '{0:5.2f}'.format( self.usonic.USONIC_getDistance() ) )
                print( '\n[sleep : {0}]\n[{1}]\n[{2}]\n[{3}]\n[{4}]\n'.format( self.value, 'MEASU', measuredate, measuretime, distance ) )

                self.sendData( 'MEASU' )
                self.sendData( measuredate )
                self.sendData( measuretime )
                self.sendData( distance )
                time.sleep( self.value )

        except ( RuntimeError ):
            print( "Runtime Error" )

        except KeyboardInterrupt:
            sys.exit()

        finally:
            self.sendData( 'END' )

class TempHumiProcess( Process, NetClient ):
    def __init__( self, host, port ):
        Process.__init__( self, name = "TempHumiProcess" )
        NetClient.__init__( self, host, port )

        self.temphumiaddress = 0x40
        self.temphumi = TEMP_HUMI( self.temphumiaddress )

        self.value = 0
        self.measureCycle()
        print( '[TempHumiProcess __init__]' )

    def __del__( self ):
        print( '[TempHumiProcess __del__]' )

    def measureCycle( self ):
        conn = sqlite3.connect( 'sensorinfo.db' )
        with conn:
            cursor = conn.cursor()
            cursor.execute( 'SELECT * FROM sensor_info WHERE kind = ? and apply = 0', ( 'TEMHU', ) )
            for row in cursor.fetchall():
                self.value = row[2]
                date = row[4]
                time = row[5]

        if self.value == 0:
            self.value = 30
        else:
            conn = sqlite3.connect( 'sensorinfo.db' )
            with conn:
                cursor = conn.cursor()
                cursor.execute( 'UPDATE sensor_info SET apply = ? WHERE kind = ? and date = ? and time = ?', ( 1, 'TEMHU', date, time ) )
                conn.commit()

    def run( self ):
        try:
            loop = True

            print( "TempHumi:TempHumi looping....." )
            while loop:
                print( "TempHumi:TempHumi process....." )
                self.temphumi.TEMP_HUMI_commandTemp()
                now = datetime.datetime.now()
                measuredate = now.strftime( '%Y-%m-%d' )
                measuretime = now.strftime( '%H:%M:%S' )
                temp = str( '{0:10.2f}'.format( self.temphumi.TEMP_HUMI_getTemperature() ) )
                print( '\n[sleep : {0}]\n[{1}]\n[{2}]\n[{3}]\n[{4}]\n'.format( self.value, 'TEMPE', measuredate, measuretime, temp ) )

                self.sendData( 'TEMPE' )
                self.sendData( measuredate )
                self.sendData( measuretime )
                self.sendData( temp )

                self.temphumi.TEMP_HUMI_commandHumi()
                now = datetime.datetime.now()
                measuredate = now.strftime( '%Y-%m-%d' )
                measuretime = now.strftime( '%H:%M:%S' )
                humi = '{0:10.2f}'.format( self.temphumi.TEMP_HUMI_getHumidity() )
                print( '\n[sleep : {0}]\n[{1}]\n[{2}]\n[{3}]\n[{4}]\n'.format( self.value, 'HUMID', measuredate, measuretime, humi ) )

                self.sendData( 'HUMID' )
                self.sendData( measuredate )
                self.sendData( measuretime )
                self.sendData( humi )
                time.sleep( self.value )

        except ( RuntimeError ):
            print( "Runtime Error" )

        except KeyboardInterrupt:
            sys.exit()

        finally:
            self.sendData( 'END' )

class LightProcess( Process, NetClient ):
    def __init__( self, host, port ):
        Process.__init__( self, name = "LightProcess" )
        NetClient.__init__( self, host, port )

        self.lightAddress = 0x23
        self.light = LIGHT( self.lightAddress )
        self.value = 0
        self.measureCycle()
        print( '[LightProcess __init__]' )

    def __del__( self ):
        print( '[LightProcess __del__]' )

    def measureCycle( self ):
        conn = sqlite3.connect( 'sensorinfo.db' )
        with conn:
            cursor = conn.cursor()
            cursor.execute( 'SELECT * FROM sensor_info WHERE kind = ? and apply = 0', ( 'LIGHT', ) )
            for row in cursor.fetchall():
                self.value = row[2]
                date = row[4]
                time = row[5]

        if self.value == 0:
            self.value = 30
        else:
            conn = sqlite3.connect( 'sensorinfo.db' )
            with conn:
                cursor = conn.cursor()
                cursor.execute( 'UPDATE sensor_info SET apply = ? WHERE kind = ? and date = ? and time = ?', ( 1, 'LIGHT', date, time ) )
                conn.commit()

    def run( self ):
        try:
            loop = True

            print( "Light:Light looping....." )
            while loop:
                print( "Light:Light process....." )
                now = datetime.datetime.now()
                measuredate = now.strftime( '%Y-%m-%d' )
                measuretime = now.strftime( '%H:%M:%S' )
                light = str( '{0:11.5f}'.format( self.light.LIGHT_readLight( 'ONE_TIME_HIGH_RES_MODE1' )  ) )
                print( '\n[sleep : {0}]\n[{1}]\n[{2}]\n[{3}]\n[{4}]\n'.format( self.value, 'LIGHT', measuredate, measuretime, light ) )

                self.sendData( 'LIGHT' )
                self.sendData( measuredate )
                self.sendData( measuretime )
                self.sendData( light )
                time.sleep( self.value )

        except ( RuntimeError ):
            print( "Runtime Error" )

        except KeyboardInterrupt:
            sys.exit()

        finally:
            self.sendData( 'END' )
