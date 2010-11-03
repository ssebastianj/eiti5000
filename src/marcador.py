#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Sebastián J. Seba"
__email__ = "ssebastianj[at]gmail.com"
__license__ = "GPL3"

from optparse import OptionParser
from time import sleep
import serial
import sys

def main():
    parser = OptionParser()
    parser.add_option("-f", "--file", action="store", type="string", 
                      dest="calls_file")
    parser.add_option("-c", "--call-delay", action="store", type="int",
                      dest="call_delay", default=30)
    parser.add_option("-h", "--hangup-delay", action="store", type="int",
                      dest="hangup_delay", default=2)
    parser.add_option("-w", "--redial-delay", action="store", type="int",
                      dest="redial_delay", default=0)
        
    PORT = 2
    CALL_DELAY = 8
    HANG_UP_DELAY = 2
    CALLS_FILE = 'llamadas.txt'
    
    with open(CALLS_FILE, 'r') as fcalls: 
        calls = fcalls.readlines()
    
    if calls:
        try:
            print u'Conectando a módem en {0}...'.format(serial.device(PORT))
            modem = serial.Serial(PORT, timeout=1)
            
            print get_registers(modem)
            
            for call in calls:
                print 'Marcando: {0}'.format(call)
                modem.write('ATD' + call.strip() + '\r')
                sleep(CALL_DELAY)
                print modem.read(modem.inWaiting())
                    
                print 'Colgando...'
                modem.write('ATH\r')
                sleep(HANG_UP_DELAY)
                print modem.read(modem.inWaiting())

                sleep(2)
                
            print u'Cerrando conexión...'
            modem.close()
            print 'Terminado. Presione ENTER para salir.'
            raw_input()        
        except serial.SerialException:
            print 'Error al conectarse al puerto' \
                  '{0} ({1})'.format(PORT, serial.device(PORT))
    else:
        print 'El archivo de llamadas no contiene ninguna llamada.'

def get_registers(modem):
    registers = {}
    for j in xrange(0, 11):
        modem.write('ATS' + str(j) + '?\r')
        sleep(1.5)
        reg = modem.read(modem.inWaiting())
        reg = reg.strip('\r\n').splitlines()
        registers['S' + str(j)] = reg[2]
    return registers

if __name__ == '__main__':
    main()
