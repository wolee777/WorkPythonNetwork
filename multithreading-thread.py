from threading import Thread

def work( low, high ):
    total = 0
    for i in range( low, high + 1 ):
        total += i
    print( f'Sub Thread {total}' )

if __name__ == '__main__':
    START, END = 1, 100

    th = Thread( target = work, args = ( START, END ) ) 
    
    th.start()
    th.join()
    
    print( 'Main Thread' )
