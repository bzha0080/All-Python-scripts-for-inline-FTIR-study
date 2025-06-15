import serial 
from time import sleep
from datetime import datetime

class SF10():
    def __init__(self, port, name = 'UNKNOWN (SF10)'):
        '''
        port: str
            port number, e.g. COM3
        '''
        
        self.con = serial.Serial(port)
        
        print('self.con: {}'.format(self.con))
        self.name = name 
        
        print('{} at {}'.format(self.name, self.con.port))

    def __repr__(self) -> str:
        return 'Peristaltic pump (SF10)'

    def start(self, info= True):
        '''
        Starts the pump
        '''
        sleep(1)
        command = 'START'
        arg = bytes(str(command), 'utf8') + b'\r'

        self.con.write(arg)

        action = '{}:\t\tStarted.'.format(self.name)
        sleep(0.05)
        print(action)


    def stop(self, info = True):
        '''
        stops the pump
        '''
        command = 'STOP'
        arg = bytes(str(command), 'utf8') + b'\r'

        self.con.write(arg)

        action = '{}:\t\tStoped.'.format(self.name)
        sleep(0.05)
        print(action)

    def changeFlowrate(self, flowrate, start = True, info = True):
        '''
        flowrate: float
            flowrate in ml/min
        '''
        command = 'SETFLOW {}\n'.format(flowrate)
        self.con.write(bytes(str(command), 'utf8'))
        
        today = datetime.now()
        currenttime = today.strftime("%H:%M:%S")

        action = '{}:\t\tFlowrate changed to {} mL/min at {}'.format(self.name, flowrate, currenttime)
        if info:
            print(action)
        if start:
            self.start()
