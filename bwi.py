#!/usr/bin/env python
# coding:utf-8
# author TL

""" bandwagonhost vps info look up """
import os
import sys
import ConfigParser
import requests
import getopt
from bs4 import BeautifulSoup

def readcfg(path):
    """ read cfg file """
    cfgdict = {}
    try:
        if os.path.isfile(path) and os.access(path, os.R_OK):
            parser = ConfigParser.RawConfigParser()
            if len(parser.read(path)) <= 0:
                sys.exit('no cfg file')
            try:
                cfgdict['local_use'] = parser.getint('info', 'local_use')
                cfgdict['manage_host'] = parser.get('info', 'manage_host')
                cfgdict['manage_pass'] = parser.get('info', 'manage_pass')
            except ConfigParser.Error as ex:
                sys.exit(ex)
            if cfgdict['local_use'] == 0:
                if parser.has_option('info', 'vps_ip'):
                    cfgdict['vps_ip'] = parser.get('info', 'vps_ip')
            else:
                cfgdict['vps_ip'] = getlocalip()

        else:
            sys.exit('not a regular file or can\'t read')
    except (OSError, TypeError) as ex:
        sys.exit(ex)
    return cfgdict

def getlocalip():
    """ getlocalip """
    import socket
    return ([(s.connect(('8.8.8.8', 80)), \
            s.getsockname()[0], s.close()) \
            for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1])

def reqstatus(cfgdict):
    """ request to bandwagonhost kiwivm """
    infodict = {}
    payload = {}

    payload['login'] = cfgdict['vps_ip']
    payload['password'] = cfgdict['manage_pass']
    req = requests.post('%s?mode=login' % cfgdict['manage_host'], data=payload)
    # only 200 is success not other code (run once)
    if req.status_code != 200:
        sys.exit('req not success')
    else:
        req = requests.get('%skiwi-main-controls.php' % cfgdict['manage_host'],\
                cookies=req.cookies)
        soup = BeautifulSoup(req.text)
        # quick and dirty
        infolist = [tag for tag in soup.find_all('font')]
        if len(infolist) == 5:
            infodict['ram'] = infolist[0].string
            infodict['swap'] = infolist[1].string
            infodict['disk'] = infolist[2].string
            infodict['reset'] = infolist[3].string
            infodict['bandwidth'] = infolist[4].string
        else:
            sys.exit('parse error and exit.')
    return infodict


def showinfo(cfgdict, infodict, showlist):
    """ show info """
    print '----------------------------------------'
    if 'node' in showlist:
        print 'Node IP: ' + cfgdict['vps_ip']
    if 'ram' in showlist:
        print 'RAM:     ' + infodict['ram']
    if 'swap' in showlist:
        print 'SWAP:    ' + infodict['swap']
    if 'disk' in showlist:
        print 'DISK:    ' + infodict['disk']
    if 'reset' in showlist:
        print 'Reset:   ' + infodict['reset']
    if 'bandwidth' in showlist:
        print 'BW:      ' + infodict['bandwidth']
    if 'time' in showlist:
        from time import localtime, strftime
        print 'TIME:    ' + strftime('%Y-%m-%d %H:%M:%S', localtime())
    print '----------------------------------------'

def usage():
    """ usage """
    print """
    python bwi.py         -c config file path
                          -s show info switch
           example:
           python bwi.py -c ./bwi.cfg -s 'node ram swap disk reset bandwidth time'
          """

def main():
    """ main """
    optdict = {'config_path': None,
               'show_info': None}
    try:
        options, _ = getopt.getopt(sys.argv[1:], 'c:s:h', ['config=', 'show=', 'help'])
        for opt, args in options:
            if opt == '-c' or opt == '--config':
                optdict['config_path'] = args
            if opt == '-s' or opt == '--show':
                optdict['show_info'] = args
            if opt == '-h' or opt == '--help':
                sys.exit(usage())
    except getopt.GetoptError as ex:
        sys.exit(ex)
    cfgdict = readcfg(optdict['config_path']) \
            if optdict['config_path'] is not None \
            else readcfg('./bwi.cfg')
    showlist = list(optdict['show_info'].split(' ')) \
            if optdict['show_info'] is not None and optdict['show_info'] != '' \
            else ['node', 'ram', 'swap', 'disk', 'reset', 'bandwidth', 'time']
    infodict = reqstatus(cfgdict)
    showinfo(cfgdict, infodict, showlist)

if __name__ == '__main__':
    main()
