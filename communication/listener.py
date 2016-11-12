# Socket listener for boat clients
import socket

class BoatsinkerListener():
    def __init__(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port

    def connect(self):
        self.socket.connect((self.host, self.port))
    
    def close(self):
        try:
            self.socket.close()
        except:
            print('Error closing socket')

    def send(self, msg):
        msgStr = msg.to_string() + '\n'
        print('Sending message: ' + msgStr)
        sent = 0
        msg = bytes(msgStr, 'utf-8')
        length = len(msg)
        while sent < length:
            just_sent = self.socket.send(msg[sent:])
            if just_sent is 0:
                raise Exception('socket connection broken')
            sent = sent + just_sent

    def receive(self):
        buf = self.socket.recv(1024)
        strBuf = ''
        buffering = True
        while buffering:
            strBuf = buf.decode('utf-8')
            if '\n' in strBuf:
                (msg, strBuf) = strBuf.split('\n', 1)
                buf = bytes(strBuf, 'utf-8')
                yield msg
            else:
                more_buf = self.socket.recv(1024)
                if not more_buf:
                    buffering = False
                else:
                    buf += more_buf
        if buf:
            yield buf.decode('utf-8')

