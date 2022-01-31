import serial

ser=serial.Serial('COM4',9600)

while True:
    sp=[]
    data=str(ser.readline()).split(':')
    topic=data[0].split("'")[1]
    value=data[1].split("\\r")[0]
    sp.append(topic)
    sp.append(value)
    print("topic: {}, value: {}".format(sp[0],sp[1]))
