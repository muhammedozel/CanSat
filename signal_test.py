import sys
import time
import serial

# 0b 01010101 -> U
MUSTER = chr(0b01010101)
PAKET_INTERVALL = 0.1
AUSWERTE_ZEIT = 5.0
BAUDRATE = 9600


def sendeschleife(schnittstelle):
    sendeziel = serial.Serial(port=schnittstelle, baudrate=BAUDRATE)
    while True:
        sendeziel.write(MUSTER)
        sendeziel.flush()
        time.sleep(PAKET_INTERVALL)


def empfangsschleife(schnittstelle):
    empfangsziel = serial.Serial(port=schnittstelle, baudrate=BAUDRATE, timeout=PAKET_INTERVALL)
    while True:
        angekommen = 0
        fehlerhaft = 0
        verloren = 0
        start = time.time()
        jetzt = start
        gelesen = ""
        while jetzt - start < AUSWERTE_ZEIT:
            # der Timeout beendet den Lesevorgang immer vorzeitig
            gelesen += empfangsziel.read(10000)
            jetzt = time.time()
        for zeichen in gelesen:
            if zeichen == MUSTER:
                angekommen += 1
            else:
                fehlerhaft += 1
        erwartete_pakete = (jetzt - start) / PAKET_INTERVALL
        verloren = erwartete_pakete - len(gelesen)
        print "%d (korrekt) / %d (fehlerhaft) / %d (verloren)" % (angekommen, fehlerhaft, verloren)


if __name__ == "__main__":
    aufgabe, schnittstelle = sys.argv[1:]
    if aufgabe == "send":
        sendeschleife(schnittstelle)
    elif aufgabe == "receive":
        empfangsschleife(schnittstelle)
    else:
        print >>sys.stderr, "Ungueltige Eingabe. 'send' oder 'receive'"

