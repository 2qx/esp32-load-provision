

import network
import time

def network_up(display):
    print("Connecting to WiFi", end="")
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect('Wokwi-GUEST', '')

    flash = False
    while not sta_if.isconnected():
        print(".", end="")
        if flash:
            display.write([128, 128, 0, 128])
        else:
            display.show("    ")
        flash = not flash
        time.sleep(0.2)
    display.show("    ")
    print(" Connected!")