#sensor_NET_Monitor_ClassLib.py
import sqlite3
import sys

class SensorMonitorView:
    def __init__( self ):
        self.sensorKind = ( 'MEASU', 'TEMPE', 'HUMID', 'LIGHT' )

    def main_menu( self ):
        menu = '''
1. 초음파 센서 측정값 보기
2. 온도 센서 측정값 보기
3. 습도 센서 측정값 보기
4. 조도 센서 측정값 보기
0. 종료
select menu : '''

        while True:
            print( menu, end = ' ' )
            selectMenu = int( input() )

            if selectMenu == 0:
                break
            elif 1 <= selectMenu <= 4:
                self.viewMeasurement( selectMenu - 1 )
        return

    def viewMeasurement( self, index ):
        loop = True
        conn = sqlite3.connect( 'sensor.db' )

        try :
            while ( loop ):
                searchDate = input( '\n검색할 날짜를 입력하세요[YYYY-MM-DD] : ' )
                with conn:
                    cursor = conn.cursor()
                    count = 0
                    cursor.execute( 'SELECT * FROM sensor_measure WHERE kind = ? and date = ?', ( self.sensorKind[index], searchDate ) )
                    print()
                    for row in cursor.fetchall():
                        count += 1
                        print( '{0:10} {1:8} {2:5} {3:>11.5f}'.format( row[1], row[2], row[3], row[4] ) )
                    print( 'total : {0:>10}\n'.format( count ) )
                select = input( '계속 하시겠습니까? [y/n] : ' )
                while ( select.upper() != 'Y' and select.upper() != 'N' ):
                    select = input( '계속 하시겠습니까? [y/n] : ' )
                if select.upper() != 'Y':
                    loop = False

        except FileNotFoundError:
            pass

        finally:
            conn.close()
        return

if __name__ == '__main__':
    sensorMonitorView = SensorMonitorView()
    sensorMonitorView.main_menu()
