# Simple example of reading the MCP3008 analog input channels and printing
# them all out.
# Author: Tony DiCola
# License: Public Domain
import time

# Import SPI library (for hardware SPI) and MCP3008 library.
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008


# Software SPI configuration:
#CLK  = 4
#MISO = 22
#MOSI = 27
#CS   = 17
#mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

# Hardware SPI configuration:
# fonctionne avec montage harware, entree 7, vRef par pont diviseur
SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))


print('Reading MCP3008 values, press Ctrl-C to quit...')
print('-' * 57)
# Main program loop.
# Vref = 0.295 = 1023
minT = 100
maxT = 0
try:
   while True:
     t = float(mcp.read_adc(5)) * 580 / 10 / 1024
     maxT = max( maxT, t)
     minT = min( minT, t)
     print(" Min: {:04.1f}   Max: {:04.1f}   Ecart {:03.1f}".format(minT, maxT, maxT-minT) )
     time.sleep(1)
except KeyboardInterrupt:
   pass
finally:
   print( "Ecart maxi releve : {:05.2f}".format(maxT-minT) )
