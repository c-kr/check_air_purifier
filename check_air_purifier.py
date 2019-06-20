#!/usr/bin/env python3
import sys
import argparse
from airctrl import airctrl as air
import pprint

class AirClient(air.AirClient):

    def get_status(self, debug=False):
        url = 'http://{}/di/v1/products/1/air'.format(self._host)
        status = self._get(url)
        return self._dump_status(status, debug=debug)

    def get_wifi(self):
        url = 'http://{}/di/v1/products/0/wifi'.format(self._host)
        wifi = self._get(url)
        return wifi

    def get_firmware(self):
        url = 'http://{}/di/v1/products/0/firmware'.format(self._host)
        firmware = self._get(url)
        return firmware

    def get_filters(self):
        values = {}
 
        url = 'http://{}/di/v1/products/1/fltsts'.format(self._host)
        filters = self._get(url)
        #print('Pre-filter and Wick: clean in {} hours'.format(filters['fltsts0']))
        values['Pre-filter and Wick'] = filters['fltsts0']
        if 'wicksts' in filters:
            values['Wick filter'] = filters['wicksts']
        #    print('Wick filter: replace in {} hours'.format(filters['wicksts']))
        values['Active carbon filter'] = filters['fltsts2']
        values['HEPA filter'] = filters['fltsts1']
        #print('Active carbon filter: replace in {} hours'.format(filters['fltsts2']))
        #print('HEPA filter: replace in {} hours'.format(filters['fltsts1']))
 
        return values


    def _dump_status(self, status, debug=False):
        values = {}        

        if debug:
            pprint.pprint(status)
            pprint()
        if 'pwr' in status:
            pwr = status['pwr']
            pwr_str = {'1': 'ON', '0': 'OFF'}
            pwr = pwr_str.get(pwr, pwr)
            values['Power'] = pwr
            #print('[pwr]   Power: {}'.format(pwr))
        if 'pm25' in status:
            pm25 = status['pm25']
            values['PM25'] = pm25
            #print('[pm25]  PM25: {}'.format(pm25))
        if 'rh' in status:
            rh = status['rh']
            values['Humidity'] = rh
            #print('[rh]    Humidity: {}'.format(rh))
        if 'rhset' in status:
            rhset = status['rhset']
            values['Target humidity'] = rhset
            #print('[rhset] Target humidity: {}'.format(rhset))
        if 'iaql' in status:
            iaql = status['iaql']
            values['Allergen index'] = iaql
            #print('[iaql]  Allergen index: {}'.format(iaql))
        if 'temp' in status:
            temp = status['temp']
            values['Temperature'] = temp
            #print('[temp]  Temperature: {}'.format(temp))
        if 'func' in status:
            func = status['func']
            func_str = {'P': 'Purification', 'PH': 'Purification & Humidification'}
            func = func_str.get(func, func)
            values['Function'] = func
            #print('[func]  Function: {}'.format(func))
        if 'mode' in status:
            mode = status['mode']
            mode_str = {'P': 'auto', 'A': 'allergen', 'S': 'sleep', 'M': 'manual', 'B': 'bacteria', 'N': 'night'}
            mode = mode_str.get(mode, mode)
            values['Mode'] = mode
            #print('[mode]  Mode: {}'.format(mode))
        if 'om' in status:
            om = status['om']
            om_str = {'s': 'silent', 't': 'turbo'}
            om = om_str.get(om, om)
            values['Fan Speed'] = om
            #print('[om]    Fan speed: {}'.format(om))
        if 'aqil' in status:
            aqil = status['aqil']
            values['Light brightness'] = aqil
            #print('[aqil]  Light brightness: {}'.format(aqil))
        if 'uil' in status:
            uil = status['uil']
            uil_str = {'1': 'ON', '0': 'OFF'}
            uil = uil_str.get(uil, uil)
            values['Button Light'] = uil
            #print('[uil]   Buttons light: {}'.format(uil))
        if 'ddp' in status:
            ddp = status['ddp']
            ddp_str = {'1': 'PM2.5', '0': 'IAI'}
            ddp = ddp_str.get(ddp, ddp)
            values['Used Index'] = ddp
            #print('[ddp]   Used index: {}'.format(ddp))
        if 'wl' in status:
            wl = status['wl']
            values['Water level'] = wl
            #print('[wl]    Water level: {}'.format(wl))
        if 'cl' in status:
            cl = status['cl']
            values['Child lock'] = cl
            #print('[cl]    Child lock: {}'.format(cl))
        if 'dt' in status:
            dt = status['dt']
            if dt != 0:
                values['Timer'] = dt
                #print('[dt]    Timer: {} hours'.format(dt))
        if 'dtrs' in status:
            dtrs = status['dtrs']
            if dtrs != 0:
                values['Times minutes'] = dtrs
                #print('[dtrs]  Timer: {} minutes left'.format(dtrs))
        if 'err' in status:
            err = status['err']
            if err != 0:
                err_str = {49408: 'no water', 32768: 'water tank open'}
                err = err_str.get(err, err)
                values['Error'] = err
                #print('-'*20)
                #print('Error: {}'.format(err))
        return values

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-H', '--hostname', required=True, type=str,
                        help='Hostname / IP of air purifier')
    parser.add_argument('-m', '--mode', required=True, choices=['deviceinfo','filters','airquality'], type=str,
                        help='mode to check')
    parser.add_argument('-w', '--warning', type=float,
                        help='Warning threshold')
    parser.add_argument('-c', '--critical', type=float,
                        help='Critical threshold')
    args = parser.parse_args()

    mode = args.mode
    warning = args.warning
    critical = args.critical

    message = ''
    perfdata = ''
    RC = [0]
    RCStatus = ('OK','WARNING','CRITICAL','UNKNOWN')

    c = AirClient(args.hostname)
    c.load_key()

    if mode == 'deviceinfo':
        status = c.get_status()
        wifi = c.get_wifi()
        firmware = c.get_firmware()

        #message += 'Power: {}\n'.format(status['Power'])

        for item,value in status.items():
            if item in ['Button Light','Child lock','Fan Speed','Light brightness','Mode','Used Index','Power','Humidity','Target humidity','Temperature','Function','Water level']:
                message += '{} is {} - '.format(item,value)

            if item in ['Fan Speed','Light brightness','Humidity','Target humidity','Temperature','Water level']:
                perfdata += "'{}'={} ".format(item,value)

        for item,value in firmware.items():
            message += '{} is {} - '.format(item,value)
        for item,value in wifi.items():
            message += '{} is {} - '.format(item,value)

    if mode == 'filters':
        filters = c.get_filters()
        for filter,hours in filters.items():
            if hours <= critical:
                message += '{} is critical ({} hours remaining) - '.format(filter,hours)
                RC.append(2)
            elif hours <= warning:
                message += '{} is warning ({} hours remaining) - '.format(filter,hours)
                RC.append(1)
            else:
                message += '{} is ok ({} hours remaining) - '.format(filter,hours)
            perfdata += "'{}'={} ".format(filter,hours)

    if mode == 'airquality':
        airquality = c.get_status()
        allergenindex = airquality['Allergen index']
        pm25 = airquality['PM25']
        if allergenindex >= critical:
            message += 'Allergen index is critical ({}) - '.format(allergenindex)
            RC.append(2)
        elif allergenindex >= warning:
            message += 'Allergen index is warning ({}) - '.format(allergenindex)
            RC.append(1)
        else:
            message += 'Allergen index is ok ({}) - '.format(allergenindex)
            RC.append(0)
        message += 'PM25 is {} - '.format(pm25)
        perfdata += "'Allergen index'={} ".format(allergenindex)
        perfdata += "'PM25'={} ".format(pm25)

    print('{}: {}|{}'.format(RCStatus[max(RC)],message[:-3],perfdata))
    sys.exit(max(RC))
