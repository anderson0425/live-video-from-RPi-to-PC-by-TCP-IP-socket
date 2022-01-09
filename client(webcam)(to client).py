#-*- encoding:utf-8 -*-

#若遇到無法開啟相機，可能是卡片有裝motion，相機資源被motion daemon占用
#只要在終端機輸入
#$ sudo /etc/init.d/motion stop
#即可停止motion daemon，
#也就能成功使用相機資源(能使用)

import socket
import cv2
import numpy

#client傳給server的文字訊息
clientMessage_01 = 'len ok!'
clientMessage_02 = 'img ok and show ok!!'

TCP_IP = "192.168.43.2"
TCP_PORT = 8000

sock = socket.socket()
sock.connect((TCP_IP, TCP_PORT))
print("connect!")

def recvall(sock, count):
    buf = b'' #bytes type
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf

while 1:
    #print("hi 0")
    
    #--------------------------------------------
    #當呼叫send的時候，資料並不是即時發給客戶端的。
    # 而是放到了系統的socket傳送緩衝區裡，
    # 等緩衝區滿了、或者資料等待超時了，資料才會傳送，
    # 所以有時候傳送太快的話，前一份資料還沒有傳給客戶端，
    # 那麼這份資料和上一份資料一起發給客戶端的時候就會造成“粘包” 。
    #(這也是為什麼接收端接收到的資料是幾份資料混雜起來的)
    #--------------------------------------------

    #接收圖片長度
    length_btyes = sock.recv(1024)  
    #一次REQUEST只會接收 1024 bytes長度的資料，當達1024時，就會輸出中止訊號，並且要等待下次的recv()。 
    # 若不希望中止，則可以使用recvall()。

    #print(length_btyes)

    #用於處理utf8 decode無法成功執行的問題
    #為了迴避UnicodeDecodeError: 'utf-8' codec can't decode byte 0xff in position 5: invalid start byte
    #選擇犧牲少數幾個無法decode的值
    try:
        length_int = int(length_btyes.decode("utf-8"))  #decode UTF-8 encoded bytes to a Unicode string.
        
#        print(length_int) #FIXME:DEBUG用
    except: #utf8_decode_error
        print("error at: decode UTF-8 encoded bytes to a Unicode string.")


    #確認接收到len後，client傳"len ok!"給server
    #這樣server才會繼續send()
    #如此是避免Server太早開始send()，這樣會造成buffer可能出現兩種data，造成黏包。
    #---------------------------------------------------------
    sock.sendall(clientMessage_01.encode("utf-8"))
    #---------------------------------------------------------   

    #接收圖片本身
    stringData = recvall(sock, length_int)

    #檢驗收到的圖片是否正確  是否出現黏包
#    print((list(stringData))[:3])#FIXME:DEBUG用
#    print((list(stringData))[-3:])#FIXME:DEBUG用

    #img decode
    #先進行btyes to str 的decode，再進行jpg的decode
    data = numpy.fromstring(stringData, dtype='uint8')  #stringData 是一大串類似  '\x01\x02'  這樣的東西的字串
    decimg=cv2.imdecode(data,1)  #解碼圖片

    decimg = cv2.flip(decimg, 0) ##垂直翻轉 #FIXME:根據不同攝像頭，這個可以更改
    cv2.putText(decimg, "at client", (10, 60), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
    cv2.imshow('CLIENT2',decimg)
    cv2.waitKey(30)

    #展示完圖片後，接著client會告訴server可以傳下一張圖片過來了
    #---------------------------------------------------------  
    sock.sendall(clientMessage_02.encode("utf-8"))
    #---------------------------------------------------------  
    
    print("Get one")


sock.close()
cv2.destroyAllWindows()