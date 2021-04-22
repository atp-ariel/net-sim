from strategy_detection import IStrategy_Detection
from frame import Frame
from util import mult_x

class  CRC16_Detection(IStrategy_Detection):
    def mod2(self, data):
        Glist = [1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1]
        Wordlist =  [int(d) for d in str(bin(data))[2:]]
        while len(Glist) <= len(Wordlist) and Wordlist:
            if Wordlist[0] == Glist[0]:
                del Wordlist[0]
                for j in range(len(Glist)-1):
                    Wordlist[j] ^= Glist[j+1]
            while Wordlist and Wordlist[0] == 0:
                del Wordlist[0]
        if not Wordlist:
            return 0
        else:
            CRCstring = ''.join(str(e) for e in Wordlist)
            CRCdata = int(CRCstring,2)
            return CRCdata
    
    def apply(self, data):
        stringdata = data + "0"*16    
        dataM = int(stringdata,2)                      
        CRC = self.mod2(dataM)                         
        CRCfix = format(CRC, 'b').zfill(16)
        Tstring = mult_x(data + CRCfix, 8)
        return [mult_x(bin(len(Tstring)//8)[2:],8),Tstring]
    
    def check(self, frame):
        f = Frame(frame)
        return f.detection_code == self.apply(f.data)[1]