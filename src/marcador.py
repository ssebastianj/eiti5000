#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Sebastian J. Seba

import serial
from time import sleep

def main():
    PUERTO = 2
    ESPERA_LLAMADA = 8
    ESPERA_COLGAR = 2
    
    with open('llamadas.txt', 'r') as archivo: 
        llamadas = archivo.readlines()
    
    if llamadas:
        try:
            print u'Conectando a módem en {0}...'.format(serial.device(PUERTO))
            modem = serial.Serial(PUERTO, timeout=1)
            
            print obtener_registros(modem)
            
            for llamada in llamadas:
                print 'Marcando: {0}'.format(llamada)
                modem.write('ATD' + llamada.strip() + '\r')
                sleep(ESPERA_LLAMADA)
                print modem.read(modem.inWaiting())
                    
                print 'Colgando...'
                modem.write('ATH\r')
                sleep(ESPERA_COLGAR)
                print modem.read(modem.inWaiting())

                sleep(2)
                
            print u'Cerrando conexión...'
            modem.close()
            print 'Terminado. Presione ENTER para salir.'
            raw_input()        
        except serial.SerialException:
            print 'Error al conectarse al puerto' \
                  '{0} ({1})'.format(PUERTO, serial.device(PUERTO))
    else:
        print 'El archivo de llamadas no contiene ninguna llamada.'

def obtener_registros(modem):
    registros = {}
    # Obtener los primeros 10 registros del modem
    for j in xrange(0, 11):
        modem.write('ATS' + str(j) + '?\r')
        sleep(1.5)
        reg = modem.read(modem.inWaiting())
        reg = reg.strip('\r\n').splitlines()
        registros['S' + str(j)] = reg[2]
    return registros

if __name__ == '__main__':
    main()
