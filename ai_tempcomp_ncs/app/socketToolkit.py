
import socket

class socket_class:
    def __init__(self):
        self.c_sharp_IP = '127.0.01'
        self.c_sharp_port= 9052
        self.python_IP = '127.0.01'
        self.python_port= 9051

        self.ServerAddress= (self.python_IP, self.python_port)
        self.ServerSocket = socket.socket()
    def send_csharp(self,msg):
        '''
        python as client,c# as server
        '''
        ClientSocket = socket.socket()
        ServerAddress = (self.c_sharp_IP, self.c_sharp_port)
        ClientSocket.connect(ServerAddress)
        msg_bytes=str.encode(msg)
        ClientSocket.send(msg_bytes)
        ClientSocket.send(b'!')
        ClientSocket.send(b"")
        ClientSocket.close()

    def listen_csharp(self):
        '''
        python as server ,c# as client
        '''
        self.ServerSocket.bind(self.ServerAddress)
        print('wait for client..')
        print('Socket Startup')

    def RecieveImg_from_csharp(self,stop_recieve):
        start_save_img=False
        self.ServerSocket.listen(1)
        c,address = self.ServerSocket.accept()

        if c != 0:
            s = "recieve0.bmp"
            f = open(s,"wb")
            condition = True
            ID_str=""
            while condition:
                image  = c.recv(307200)
                if(len(image)<10) and (len(image)>1):

                    ID_str=str(image.decode("utf-8", errors="replace"))
                    start_position=ID_str.index("I")
                    Img_ID_numb=ID_str[start_position+1:start_position+2]

                #當收到c# Image ID指令後開始可以存圖
                elif(len(image)>10):
                    start_save_img=True        

                if str(image) == "b''":
                    condition = False
                elif str(image.decode("utf-8", errors="replace")) == "A": 
                    stop_recieve=True
                
                if(start_save_img==True):
                    f.write(image)
        return stop_recieve

