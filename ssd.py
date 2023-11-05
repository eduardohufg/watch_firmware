from machine import Pin, SoftI2C, RTC
import time
import ssd1306
import framebuf
from oled import Write
from oled.fonts import ubuntu_mono_12 as u12
from oled.fonts import ubuntu_mono_15 as u15
from oled.fonts import ubuntu_mono_20 as u20
import time
from umqttsimple import MQTTClient
import ubinascii
import machine
import micropython
import network
import esp
esp.osdebug(None)
import gc
gc.collect()


ssid = '23Cha'
password = 'familachavez123'
mqtt_server = '192.168.0.13'

client_id = ubinascii.hexlify(machine.unique_id())
topic_sub = b'notification'
topic_pub = b'hello'

last_message = 0
message_interval = 5
counter = 0

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  pass

print('Connection successful')
print(station.ifconfig())









SDA_PIN = 6
SCL_PIN = 7

# using SoftI2C
i2c = SoftI2C(sda=Pin(SDA_PIN), scl=Pin(SCL_PIN))
display = ssd1306.SSD1306_I2C(128, 64, i2c)

(year, month, mday, weekday, hour, minute, second, milisecond) = RTC().datetime()
RTC().init((year, month, mday, weekday, hour, minute, second, milisecond))

write12 = Write(display, u12)
write15 = Write(display, u15)
write20 = Write(display, u20)

def sub_cb(topic, msg):
  print((topic, msg))
  if topic == b'notification' and msg == b'received':
    print('ESP received hello message')

def connect_and_subscribe():
  global client_id, mqtt_server, topic_sub
  client = MQTTClient(client_id, mqtt_server)
  client.set_callback(sub_cb)
  client.connect()
  client.subscribe(topic_sub)
  print('Connected to %s MQTT broker, subscribed to %s topic' % (mqtt_server, topic_sub))
  return client

def restart_and_reconnect():
  print('Failed to connect to MQTT broker. Reconnecting...')
  time.sleep(10)
  machine.reset()

try:
  client = connect_and_subscribe()
except OSError as e:
  restart_and_reconnect()


def show_wifi_status(status,x,y):
    wifi = bytearray(b'\x00\x00\x00\x00\x1f\xf0x<\xe3\x8e\x8f\xe2883\x98\x0f\xe0\x0c`\x03\x80\x03\x80\x03\x80\x00\x00\x00\x00')
    wifi_no = bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')

    if status == 1:
        bwifi = framebuf.FrameBuffer(wifi, 15,15, framebuf.MONO_HLSB)
        display.blit(bwifi,x,y)
        display.show()
    else:
        bwifi = framebuf.FrameBuffer(wifi_no, 15,15, framebuf.MONO_HLSB)
        display.blit(bwifi,x,y)
        display.show()

def show_battery(bat,x,y):
    cien = bytearray(b'\x1f\xff\xff\x00 \x00\x00\x80.\xee\xee\x80n\xee\xee\x80n\xee\xee\x80n\xee\xee\x80n\xee\xee\x80.\xee\xee\x80 \x00\x00\x80\x1f\xff\xff\x00')
    ochenta = bytearray(b'\x1f\xff\xff\x00 \x00\x00\x80 \xee\xee\x80`\xee\xee\x80`\xee\xee\x80`\xee\xee\x80`\xee\xee\x80 \xee\xee\x80 \x00\x00\x80\x1f\xff\xff\x00')
    secenta = bytearray(b'\x1f\xff\xff\x00 \x00\x00\x80 \x0e\xee\x80`\x0e\xee\x80`\x0e\xee\x80`\x0e\xee\x80`\x0e\xee\x80 \x0e\xee\x80 \x00\x00\x80\x1f\xff\xff\x00')
    cuarenta = bytearray(b'\x1f\xff\xff\x00 \x00\x00\x80 \x00\xee\x80`\x00\xee\x80`\x00\xee\x80`\x00\xee\x80`\x00\xee\x80 \x00\xee\x80 \x00\x00\x80\x1f\xff\xff\x00')
    veinte = bytearray(b'\x1f\xff\xff\x00 \x00\x00\x80 \x00\x0e\x80`\x00\x0e\x80`\x00\x0e\x80`\x00\x0e\x80`\x00\x0e\x80 \x00\x0e\x80 \x00\x00\x80\x1f\xff\xff\x00')
    cero = bytearray(b'\x1f\xff\xff\x00 \x00\x00\x80 \x00\x00\x80`\x00\x00\x80`\x00\x00\x80`\x00\x00\x80`\x00\x00\x80 \x00\x00\x80 \x00\x00\x80\x1f\xff\xff\x00')

    porcentage = [cien, ochenta, secenta, cuarenta, veinte, cero]
    
    if(bat >=80 and bat <=110):
        fb = framebuf.FrameBuffer(porcentage[0], 25,10, framebuf.MONO_HLSB)
        display.blit(fb,x,y)
        display.show()
    if(bat >=60 and bat <=79):
        fb = framebuf.FrameBuffer(porcentage[1], 25,10, framebuf.MONO_HLSB)
        display.blit(fb,x,y)
        display.show()
    if(bat >=40 and bat <=59):
        fb = framebuf.FrameBuffer(porcentage[2], 25,10, framebuf.MONO_HLSB)
        display.blit(fb,x,y)
        display.show()
    if(bat >=20 and bat <=39):
        fb = framebuf.FrameBuffer(porcentage[3], 25,10, framebuf.MONO_HLSB)
        display.blit(fb,x,y)
        display.show()
    if(bat >=0 and bat <=19):
        fb = framebuf.FrameBuffer(porcentage[4], 25,10, framebuf.MONO_HLSB)
        display.blit(fb,x,y)
        display.show()


def frame(status):
    if status:
        display.line(0,0,128,0,1)
        display.line(0,0,0,64,1)
        display.line(0,63,128,63,1)
        display.line(127,0,127,63,1)
    else:
        display.line(0,0,128,0,0)
        display.line(0,0,0,64,0)
        display.line(0,64,128,63,0)
        display.line(127,0,127,63,0)
            
def show_day(form, size, x, y):
    list_day = ['Lun.','Mar.','Mie.','Jue.','Vie.','Sab.','Dom.']
    list_day_tot = ['Lunes','Martes','Miercoles','Jueves','Viernes','Sabado','Domingo']
    if size == 20:
        write = Write(display, u20)
    elif size == 15:
        write = Write(display, u15)
    else:
        write = Write(display, u12)
    if form ==0:
        write.text(list_day[RTC().datetime()[3]], x, y)
    elif form ==1:
        write.text(list_day_tot[RTC().datetime()[3]], x, y)
    else:
        write.text(list_day[RTC().datetime()[3]], x, y)
    display.show()
    
    
    
def show_hour(form, size, x, y):
    #display.fill(0)
    list_num =['00','01','02','03','04','05','06','07','08','09']
    
    if size == 20:
        write = Write(display, u20)
    elif size == 15:
        write = Write(display, u15)
    else:
        write = Write(display, u12)
        
    if form == 0:
        if (RTC().datetime()[4]==0):
            write.text('12', x, y)
            write.text("a.m.", x+39,y)
        elif (RTC().datetime()[4]<10):
            write.text(list_num[RTC().datetime()[4]], x, y)
            write.text("a.m.", x+39,y)
        elif (RTC().datetime()[4]>12):
            if((RTC().datetime()[4]-12)<10):
                write.text(list_num[RTC().datetime()[4]-12], x, y)
                write.text("p.m.", x+39,y)
            else:
                write.text(str(RTC().datetime()[4]-12), x, y)
                write.text("p.m.", x+39,y)    
        else:
            write.text(str(RTC().datetime()[4]), x, y)
        write.text(':', x+15, y)
        if (RTC().datetime()[5]<10):
            write.text(list_num[RTC().datetime()[5]], x+22, y)
        else:
            write.text(str(RTC().datetime()[5]), x+22, y)
        display.show()
        
    elif form == 1:
        if (RTC().datetime()[4]<10):
            write.text(list_num[RTC().datetime()[4]], x, y)
        else:
            write.text(str(RTC().datetime()[4]), x, y)
        write.text(':', x+15, y)
        if (RTC().datetime()[5]<10):
            write.text(list_num[RTC().datetime()[5]], x+22, y)
        else:
            write.text(str(RTC().datetime()[5]), x+22, y)
        display.show()
        
    elif form == 2:
        if (RTC().datetime()[4]<10):
            write.text(list_num[RTC().datetime()[4]], x, y)
        else:
            write.text(str(RTC().datetime()[4]), x, y)
        write.text(':', x+15, y)
        if (RTC().datetime()[5]<10):
            write.text(list_num[RTC().datetime()[5]], x+22, y)
        else:
            write.text(str(RTC().datetime()[5]), x+22, y)
        write.text(':', x+37, y)
        if (RTC().datetime()[6]<10):
            write.text(list_num[RTC().datetime()[6]], x+45, y)
        else:
            write.text(str(RTC().datetime()[6]), x+45, y)
        display.show()     
    
    

def show_date(form, size, x, y):
    #display.fill(0)
    list_num =['00','01','02','03','04','05','06','07','08','09']
    list_month =['ENE','FEB','MAR','ABR','MAY','JUN','JUL','AGO','SEP','OCT','NOV','DIC']
    
    if size == 20:
        write = Write(display, u20)
    elif size == 15:
        write = Write(display, u15)
    else:
        write = Write(display, u12)
        
    if form == 0:
        if (RTC().datetime()[2]<10):
            write.text(list_num[RTC().datetime()[2]], x, y)
        else:
            write.text(str(RTC().datetime()[2]), x, y)
        write.text(list_month[RTC().datetime()[1]-1], x+18, y)
        display.show()
    
    elif form == 1:
        if (RTC().datetime()[2]<10):
            write.text(list_num[RTC().datetime()[2]], x, y)
        else:
            write.text(str(RTC().datetime()[2]), x, y)
        write.text('/', x+15, y)
        if (RTC().datetime()[1]<10):
            write.text(list_num[RTC().datetime()[1]], x+22, y)
        else:
            write.text(str(RTC().datetime()[1]), x+22, y)
        display.show()
        
    elif form == 2:
        if (RTC().datetime()[2]<10):
            write.text(list_num[RTC().datetime()[2]], x, y)
        else:
            write.text(str(RTC().datetime()[2]), x, y)
        write.text('/', x+15, y)
        if (RTC().datetime()[1]<10):
            write.text(list_num[RTC().datetime()[1]], x+22, y)
        else:
            write.text(str(RTC().datetime()[1]), x+22, y)
        write.text('/', x+37, y)
        write.text(str(RTC().datetime()[0]), x+45, y)
        display.show()     
   

battery = 0
while(True):
    
    try:
        client.check_msg()
        if (time.time() - last_message) > message_interval:
            msg = b'Hello #%d' % counter
            print('pub')
            client.publish(topic_pub, msg)
            last_message = time.time()
            counter += 1
    except OSError as e:
        restart_and_reconnect()

    show_date(0,15,31,2)
    show_hour(0,15,0,17)
    show_day(0,15,0,0)
    
    show_wifi_status(1,83,0)
    
    
    
    battery = 100
    show_battery(battery,102,0)
    
    time.sleep(1)
    
    show_wifi_status(0,83,0)
    
    battery = 19
    
    show_battery(battery,102,0)
    
    