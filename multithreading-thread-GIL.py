from threading import Thread
from multiprocessing import Process, Queue
import time

def work( id, start, end, result ):
    total = 0

    for i in range( start, end ):
        total += i

    result.append( total )

def workP( id, start, end, result ):
    total = 0

    for i in range( start, end ):
        total += i

    result.put( total )

if __name__ == '__main__':
    START, END = 0, 100000000
    result = []

    th1 = Thread( target = work, args = ( 1, START, END, result ) ) 
    
    start = time.time()
    th1.start()
    th1.join()
    stop = time.time()

    print( f'Result : { sum( result ) } - time { stop - start }' )
    print()

    result = []
    th2 = Thread( target = work, args = ( 2, START, END // 2, result ) )
    th3 = Thread( target = work, args = ( 3, END // 2, END, result ) ) 
    
    start = time.time()
    th2.start()
    th3.start()
    th2.join()
    th3.join()
    stop = time.time()

    print( f'Result : { sum( result ) } - time { stop - start }' )
    print()

    result = Queue()
    p1 = Process( target = workP, args = ( 1, START, END // 2, result ) )
    p2 = Process( target = workP, args = ( 2, END // 2, END, result ) ) 
    
    start = time.time()
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    stop = time.time()

    result.put( 'STOP' )
    total = 0
    while True:
        tmp = result.get()
        if tmp == 'STOP':
            break
        else:
            total += tmp
    print( f'Result : { total } - time { stop - start }' )
