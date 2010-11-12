#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Sebastián J. Seba"
__version__ = "1.3"
__license__ = """This program is free software: you can redistribute it and/or
                 modify it under the terms of the GNU General Public License
                 as published by the Free Software Foundation, either version
                 3 of the License, or (at your option) any later version.
                 This program is distributed in the hope that it will be useful,
                 but WITHOUT ANY WARRANTY; without even the implied warranty of
                 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
                 GNU General Public License for more details.
                 You should have received a copy of the GNU General Public License
                 along with this program.  If not, see <http://www.gnu.org/licenses/>.
                 """

from optparse import OptionParser
from time import sleep
import serial

def main(): 
    parser = _get_arguments()
    (options, args) = parser.parse_args()

    if len(args) == 0:
        parser.print_usage()
        print u"Pruebe '{0} --help' para más información." \
              .format(parser.get_prog_name())
    elif options.device is None:
        print u'Debe proporcionar un dispositivo.'
    else:
        filename = args[0]
        with open(filename, 'r') as fcalls: 
            calls = fcalls.readlines()
            
        modem = None
        remaining_calls = calls
        if calls:
            try:
                print u'Conectando a modem en {0}...'.format(options.device)
                modem = serial.Serial(options.device, timeout=1)
                        
                total = len(calls)
                for i, call in enumerate(calls, 1):
                    print '{0}/{1}] Marcando: {2}'.format(str(i), total, call)
                    modem.write('ATD{0}\r'.format(call.strip()))
                    sleep(options.call_delay)
                    data = modem.read(modem.inWaiting())
                    if data.find('OK\r\n') != -1:
                        remaining_calls.remove(call)
                    print data
                    
                    print 'Colgando...'
                    modem.write('ATH\r')
                    sleep(options.hangup_delay)
                    print modem.read(modem.inWaiting())
                    sleep(options.redial_delay)
            except serial.SerialException:
                print 'Error al conectarse al puerto {0}' \
                      .format(options.device)
            except KeyboardInterrupt:
                print 'Cancelando marcado...'
                modem.write('ATH\r')
                sleep(options.hangup_delay)
                exit(0)
            finally:
                if options.delete_calls:
                    print 'Actualizando archivo de llamadas...'
                    _update_calls_file(filename, remaining_calls)
                print u'Cerrando conexión con modem...'
                if modem is not None and modem.isOpen(): 
                    modem.close()
                
            try:
                if not options.autoclose:
                    print 'Terminado. Presione ENTER para salir.'
                    raw_input()
            except KeyboardInterrupt: 
                exit(0)
        else: 
            print 'El archivo de llamadas no contiene ninguna llamada.'

def _update_calls_file(filename, remaining_calls):
    with open(filename, 'w') as fcalls:
        fcalls.writelines(remaining_calls)

def _get_arguments():
    parser = OptionParser(usage="Usage: %prog [-d DEVICE]"
        " [-c CALL_DELAY]\n                 "
        "  [-u HANGUP_DELAY] [-r REDIAL_DELAY]\n"
        "                   [-a] archivo_llamadas",
        version=__version__)
    parser.add_option("-d", "--device", action="store", type="string",
                      dest="device",
                      help="Dispositivo a utilizar. Puede ser de la forma " \
                      "COMx o /dev/ttySx o cualquier otra cadena que " \
                      "represente un dispositivo [Obligatorio]")
    parser.add_option("-c", "--call-delay", action="store", type="int",
                      dest="call_delay", default=30,
                      help="Tiempo (en segundos) a esperar luego de realizar "
                           "una llamada [Default: %default]")
    parser.add_option("-u", "--hangup-delay", action="store", type="int",
                      dest="hangup_delay", default=2,
                      help="Tiempo (en segundos) a esperar luego de cortar "
                           "una llamada [Default: %default]")
    parser.add_option("-r", "--redial-delay", action="store", type="int",
                      dest="redial_delay", default=2,
                      help="Tiempo (en segundos) a esperar entre llamadas"
                           "[Default: %default]")
    parser.add_option("-a", "--autoclose", action="store_true", default=False,
                      dest="autoclose", help="Cerrar programa al finalizar. "
                           "Al utilizar esta opcion no sera necesario "
                           "presionar la tecla ENTER para salir.")
    parser.add_option("-n", "--no-delete-calls", action="store_false", 
                      default=True, dest="delete_calls", 
                      help="Utilice esta opcion si no desea que las " \
                      "llamadas realizadas sean eliminadas.")
    return parser

if __name__ == '__main__':
    main()
