import eventlet
import time
eventlet.monkey_patch()

def get_credentials(args=None, tenant_name=None):
    d = {}
    d['username'] = args.username
    d['password'] = args.password
    d['auth_url'] = args.auth_url
    if tenant_name:
        d['tenant_name'] = tenant_name
    else:
        d['tenant_name'] = args.tenant_name
    return d

class Excutor(object):
    def __init__(self,thread=100, maxnum=1000, credentials=None):
        self.thread=thread
        self.maxnum=maxnum
        self.curnum=0
        self.failnum=0
        self.pool=eventlet.GreenPool(self.thread)
        self.func = None
        self.threadnum=0
        self.credentials = credentials


    def run(self):
        self.curnum = 0
        self.threadnum = 0
        self.start_time=time.time()
        while True:
            self.threadnum = self.threadnum + 1
            if self.curnum>self.maxnum:
                break
            if (self.threadnum/self.maxnum)>2:
                break
            self.pool.spawn_n(self.test_method)

        self.end_time=time.time()



    def test_method(self):
        pass

    def get_result(self):
        return {'testname': self.__class__.__name__,
                'success': self.curnum-1,
                'failnum': self.failnum,
                'period': self.end_time-self.start_time}
