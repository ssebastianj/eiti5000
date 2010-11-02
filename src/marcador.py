#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Sebastian J. Seba

import serial
from time import sleep

def main():
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
    # Obtener los primeros 10 registers del modem
    for j in xrange(0, 11):
        modem.write('ATS' + str(j) + '?\r')
        sleep(1.5)
        reg = modem.read(modem.inWaiting())
        reg = reg.strip('\r\n').splitlines()
        registers['S' + str(j)] = reg[2]
    return registers

if __name__ == '__main__':
    main()
