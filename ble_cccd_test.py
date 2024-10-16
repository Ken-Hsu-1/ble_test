# ble_scan_connect.py:
from bluepy.btle import Peripheral, UUID
from bluepy.btle import Scanner, DefaultDelegate

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)
    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print ("Discovered device", dev.addr)
        elif isNewData:
            print ("Received new data from", dev.addr)

class MyDelegate(DefaultDelegate):
    def __init__(self, params):
        DefaultDelegate.__init__(self)
        # ... initialise here

    def handleNotification(self, cHandle, data):
        print ("notify new data : ", data)
        # ... perhaps check cHandle
        # ... process 'data

scanner = Scanner().withDelegate(ScanDelegate())
devices = scanner.scan(10.0)
n=0
addr= []
for dev in devices:
    print ("%d: Device %s (%s), RSSI=%d dB" % (n, dev.addr, dev.addrType, dev.rssi))
    addr.append(dev.addr)
    n += 1
    for (adtype, desc, value) in dev.getScanData():
        print ("  %s = %s" % (desc, value))
        if desc == "Complete Local Name":
            print ("00000000000000000000000000000000000000000000")

number = input('Enter your device number: ')
print ('Device', number)
num= int(number)
print (addr[num])
#
print ("Connecting...")
dev = Peripheral(addr[num], 'random').withDelegate(MyDelegate())
#
print ("Services...")
for svc in dev.services:
    print (str(svc))
#
try:
    testService = dev.getServiceByUUID(UUID(0xfff0))
    for ch in testService.getCharacteristics():
        print (str(ch))
#
    ch= dev.getCharacteristics(uuid=UUID(0xfff1))[0]
    if (ch.supportsRead()):
            print (ch.read())

    print ('ask for notify')
    for desriptor in dev.getDescriptors():
        if (desriptor.uuid == 0x2902):
            CCCD_handle = desriptor.handle
            dev.writeCharacteristic(CCCD_handle, bytes([0, 1]))

    print("notify set completed")

    while True:
        if dev.waitForNotifications(10.0):
        # handleNotification() was called
            continue
        print("Waiting...")

#
finally:
    dev.disconnect()