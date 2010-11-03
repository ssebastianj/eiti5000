#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Sebastián J. Seba"
__email__ = "ssebastianj[at]gmail.com"
__license__ = "GPL3"

from optparse import OptionParser
from time import sleep
import serial

def main():
    parser = OptionParser()
    usg = "Usage: %prog [-p PORT_NUMBER] [-c CALL_DELAY]" + "[-u HANGUP_DELAY] [-v REDIAL_DELAY] archivo_llamadas"
    parser.set_usage(usg)
    parser.add_option("-p", "--port", action="store", type="int",
                      dest="port_number", 
                      help="Numero de puerto COM a utilizar [Obligatorio]")
    parser.add_option("-c", "--call-delay", action="store", type="int",
                      dest="call_delay", default=30,
                      help="Tiempo, en segundos, a esperar luego de realizar " \
                      "una llamada [Default: %default]")
    parser.add_option("-u", "--hangup-delay", action="store", type="int",
                      dest="hangup_delay", default=2,
                      help="Tiempo, en segundos, a esperar luego de cortar " \
                      "una llamada [Default: %default]")
    parser.add_option("-w", "--redial-delay", action="store", type="int",
                      dest="redial_delay", default=2,
                      help="Tiempo, en segundos, a esperar entre llamadas" \
                      "[Default: %default]")
    (options, args) = parser.parse_args()

    if len(args) == 0:
        parser.error("Pruebe '" + parser.get_prog_name() + " --help' para mas informacion.")
    elif options.port_number is None:
        parser.error('Debe ingresar un numero de puerto COM.')
    else:
        with open(args[0], 'r') as fcalls: 
            calls = fcalls.readlines()
        
        if calls:
            try:
                print u'Conectando a módem en {0}...'.format(serial.device(
                                                             options.port_number - 1))
                modem = serial.Serial(options.port_number - 1, timeout=1)
                
                for call in calls:
                    print 'Marcando: {0}'.format(call)
                    modem.write('ATD' + call.strip() + '\r')
                    sleep(options.call_delay)
                    print modem.read(modem.inWaiting())
                        
                    print 'Colgando...'
                    modem.write('ATH\r')
                    sleep(options.hangup_delay)
                    print modem.read(modem.inWaiting())
                    sleep(options.redial_delay)
                    
                print u'Cerrando conexión...'
                modem.close()
                print 'Terminado. Presione ENTER para salir.'
                raw_input()        
            except serial.SerialException:
                print 'Error al conectarse al puerto' \
                      '{0} ({1})'.format(options.port_number - 1,
                                         serial.device(options.port_number - 1))
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
