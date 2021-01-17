import os


def f(name):
    info('process')
    print ('hello', name)
    
def f2(arg):
    arg.put("This message brought to you by a queue ")
    
def f3(arg):
    #arg.send("This message brought to you via a 2-way pipe")
    print(arg.recv())
    arg.close()
    
def info(title):
    print (title)
    print ('module name:', __name__)
    if hasattr(os, 'getppid'):  # only available on Unix
        print ('parent process:', os.getppid())
    print ('process id:', os.getpid())


    ###Hello world
    # p = Process(target=f, args=('world',))
    # p.start()
    # p.join()
    
    ### Queue
    # q = Queue()
    # p = Process(target=f2, args=(q,))
    # p.start()
    # print (q.get())
    # p.join()

    ### Pipe
    # parent_conn, child_conn = Pipe()
    # p = Process(target=f3, args=(child_conn,))
    # p.start()
    # parent_conn.send("toto")
    # #print (parent_conn.recv()) 
    # p.join()