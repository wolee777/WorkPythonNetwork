#sensor_NET_Client_Manage_ClassLib.py
from multiprocessing import Process, Queue
from sensor_NET_ClassLib import USonicProcess, TempHumiProcess, LightProcess
import sys

class SensorClientView:
    def __init__( self ):
        print( '[SensorClientView __init__]' )
    def main_menu( self ):
        menu = '''
1. Sensor Measure 주기 변경
2. Sensor Measure stop
0. 종료
select menu : '''
        func_dict = { 1:self.measureCycleChange, 2:self.measureStop }

        while True:
            print( menu, end = ' ' )
            selectMenu = int( input() )

            if selectMenu == 0:
                break
            elif 1 <= selectMenu <= 2:
                func_dict[ selectMenu ]()
        return

    def measureCycleChange( self ):
        print( 'Sensor Measure Cycle Change' )
        return

    def measureStop( self ):
        print( 'Sensor Measure Cycle Change' )
        return

if __name__ == '__main__':
    sensorClientView = SensorClientView()
    sensorClientView.main_menu()
