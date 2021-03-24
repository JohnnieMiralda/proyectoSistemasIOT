from email import *
from time import *
from gpio import * 

def onEmailReceive(sender, subject, body):
    if subject == "porton":
        if body == "abrir":
            print("abrir email")
            customWrite(9,"abrierto")
            customWrite(7,1)
        elif body == "cerrar":
            customWrite(9,"cerrado")
            print("cerrar email")
            customWrite(7,0)


def onEmailSend(status):
	print("send status: " + str(status))

def main():
    EmailClient.setup(
        "iot@gmail.com",
        "gmail.com",
        "iot",
        "iot"
    )

    EmailClient.onReceive(onEmailReceive)
    EmailClient.onSend(onEmailSend)

    EmailClient.send("data@gmail.com", "Correiendo", "Porton")
    loop=True
    estado=True
    timer= time()
    pinMode(0,INPUT)
    pinMode(1,INPUT)
    pinMode(2,OUTPUT)
    pinMode(3,INPUT)
    pinMode(7,OUTPUT)
    pinMode(8,OUTPUT)
    pinMode(9,OUTPUT)
# check email once a while
    while loop:
        EmailClient.receive()
        if digitalRead(0)==0 and digitalRead(1)==0:
            delay(1000)
            if estado and customRead(7)=='1':
                estado=True
                timer= time()+5
                if digitalRead(3)== 0:
                    customWrite(2,2)
            elif not estado and customRead(7)=='0':
                estado=False
                timer= time()+5
                if digitalRead(3)== 0:
                    customWrite(2,2)
        elif digitalRead(0)==1023 or digitalRead(1)==HIGH:
            estado= not estado
            timer= time()+5
            if digitalRead(3)== 0:
                customWrite(2,2)

            if estado:
                customWrite(9,"cerrando")
                print("cerrando")
                for i in range(100,0,-10):
                    customWrite(8,1)
                    delay(1000)
                customWrite(9,"cerrado")
                customWrite(7,0)
            else:
                customWrite(9,"abriendo")
                print("abriedno")
                for i in range(0,110,10):
                    customWrite(8,i)
                    delay(1000)
                customWrite(9,"abrierto")
                customWrite(7,1)

        if time()>=timer:
            customWrite(2,0)

if __name__ == "__main__":
	main()