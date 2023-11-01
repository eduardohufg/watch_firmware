from machine import Pin, SoftI2C, RTC
import time
import ssd1306
import framebuf
from oled import Write
from oled.fonts import ubuntu_mono_12 as u12
from oled.fonts import ubuntu_mono_15 as u15
from oled.fonts import ubuntu_mono_20 as u20


SDA_PIN = 6
SCL_PIN = 7

# using SoftI2C
i2c = SoftI2C(sda=Pin(SDA_PIN), scl=Pin(SCL_PIN))
display = ssd1306.SSD1306_I2C(128, 32, i2c)

(year, month, mday, weekday, hour, minute, second, milisecond) = RTC().datetime()
RTC().init((year, month, mday, weekday, hour, minute, second, milisecond))

write12 = Write(display, u12)
write15 = Write(display, u15)
write20 = Write(display, u20)

def show_battery(bat):
    cien = bytearray(b'\x1f\xff\xff\x00 \x00\x00\x80.\xee\xee\x80n\xee\xee\x80n\xee\xee\x80n\xee\xee\x80n\xee\xee\x80.\xee\xee\x80 \x00\x00\x80\x1f\xff\xff\x00')
    ochenta = bytearray(b'\x1f\xff\xff\x00 \x00\x00\x80 \xee\xee\x80`\xee\xee\x80`\xee\xee\x80`\xee\xee\x80`\xee\xee\x80 \xee\xee\x80 \x00\x00\x80\x1f\xff\xff\x00')
    secenta = bytearray(b'\x1f\xff\xff\x00 \x00\x00\x80 \x0e\xee\x80`\x0e\xee\x80`\x0e\xee\x80`\x0e\xee\x80`\x0e\xee\x80 \x0e\xee\x80 \x00\x00\x80\x1f\xff\xff\x00')
    cuarenta = bytearray(b'\x1f\xff\xff\x00 \x00\x00\x80 \x00\xee\x80`\x00\xee\x80`\x00\xee\x80`\x00\xee\x80`\x00\xee\x80 \x00\xee\x80 \x00\x00\x80\x1f\xff\xff\x00')
    veinte = bytearray(b'\x1f\xff\xff\x00 \x00\x00\x80 \x00\x0e\x80`\x00\x0e\x80`\x00\x0e\x80`\x00\x0e\x80`\x00\x0e\x80 \x00\x0e\x80 \x00\x00\x80\x1f\xff\xff\x00')
    cero = bytearray(b'\x1f\xff\xff\x00 \x00\x00\x80 \x00\x00\x80`\x00\x00\x80`\x00\x00\x80`\x00\x00\x80`\x00\x00\x80 \x00\x00\x80 \x00\x00\x80\x1f\xff\xff\x00')

    porcentage = [cien, ochenta, secenta, cuarenta, veinte, cero]
    
    if(bat >=80 and bat <=110):
        fb = framebuf.FrameBuffer(porcentage[0], 25,10, framebuf.MONO_HLSB)
        display.blit(fb,103,0)
        display.show()
    if(bat >=60 and bat <=79):
        fb = framebuf.FrameBuffer(porcentage[1], 25,10, framebuf.MONO_HLSB)
        display.blit(fb,103,0)
        display.show()
    if(bat >=40 and bat <=59):
        fb = framebuf.FrameBuffer(porcentage[2], 25,10, framebuf.MONO_HLSB)
        display.blit(fb,103,0)
        display.show()
    if(bat >=20 and bat <=39):
        fb = framebuf.FrameBuffer(porcentage[3], 25,10, framebuf.MONO_HLSB)
        display.blit(fb,103,0)
        display.show()
    if(bat >=0 and bat <=19):
        fb = framebuf.FrameBuffer(porcentage[4], 25,10, framebuf.MONO_HLSB)
        display.blit(fb,103,0)
        display.show()
    
def show_date(form, size, x, y):
    display.fill(0)
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
    show_date(0,15,0,0)
    
    battery = 100
    show_battery(battery)
    
    time.sleep(2)
    
    battery = 19
    
    show_battery(battery)
    
    time.sleep(2)
    
    
    

# # 
# #     time.sleep(1)
# #     
# # 
# #     display.text(str(RTC().datetime()[2]), 0, 0)
# #     display.text('/', 15, 0)
# #     display.text(str(RTC().datetime()[1]), 25, 0)
# #     display.text('/', 40, 0)
# #     display.text(str(RTC().datetime()[0]), 50, 0)
# #     
# #     display.line(0,10,128,10,1)
# #     
# #     
# #         
# #     
# #     display.text(str(RTC().datetime()[4]), 30, 18)
# #     display.text(':', 45, 18)
# #     display.text(str(RTC().datetime()[5]), 55, 18)
# #     display.text(':', 70, 18)
# #     if (RTC().datetime()[6]<10):
# #         display.text(list_num[RTC().datetime()[6]], 80, 18)
# #     else: 
# #         display.text(str(RTC().datetime()[6]), 80, 18)
# #     
# # 
# #     
# #     display.show()
# #     
# #     display.fill(0)
# #     


    
    
    



    


    
    
    

