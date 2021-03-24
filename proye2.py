from time import delay, time
from gpio import * 
from email import *



def onEmailReceive(sender, subject, body):
    if subject == "ventiladores":
        if body == "prender":
            print("prende email")
            customWrite(0,2)
            customWrite(1,2)
        elif body == "apagar":
            print("apaga email")
            customWrite(0,0)
            customWrite(1,0)

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

    
    print("COrriendo")
    # ?pins usados/ variables
    pinMode(0,OUTPUT)
    pinMode(1,OUTPUT)
    pinMode(2,INPUT)
    pinMode(3,INPUT)

    loop=True
    prendido=False
    timer= time()
    EmailClient.send("data@gmail.com", "Correiendo", "Ventiladores")
    while loop:
        EmailClient.receive()
        hey=customRead(0)
        if customRead(0)=='2' and not prendido:
            prendido=True
            timer= time()+15
            print("entro email si")
        elif customRead(0)==2 and prendido:
            prendido=False
            print("entro email no")


        if digitalRead(2)==0 and digitalRead(3)==0:
            delay(1000)  
        elif digitalRead(3)==HIGH:
            print("prende")
            timer= time()+15
            prendido=True
        elif digitalRead(2)==1023:
            timer= time()+10
        
        
        if time()>=timer and prendido:
            prendido=False
            print("Apaga")
            customWrite(0,0)
            customWrite(1,0)
            digitalWrite(0,0)
            digitalWrite(1,0)
            print(prendido,customRead(0),customRead(1))
        elif prendido:
            print("prendioo")
            customWrite(0,2)
            customWrite(1,2)
        elif not prendido:
            print("apagooo")
            customWrite(0,0)
            customWrite(1,0)


if __name__=="__main__":
    main()
