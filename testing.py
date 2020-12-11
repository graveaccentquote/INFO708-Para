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