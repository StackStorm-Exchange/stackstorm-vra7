#!/usr/bin/env python

# Python script for configuring vRA7 StackStorm Pack
from __future__ import print_function

import getpass
import subprocess

try:  # Python 2
    input = raw_input
except NameError:  # Python 3 built-in
    pass

configfile = '/opt/stackstorm/configs/vra7.yaml'

hostname = input("hostname (vRA FQDN ex. cloud.company.local): ")

# vRA SSl certification verification configuration
verifyssl = input("verify vRA SSL certificate (true/false) [false]: ")
verifysslvalue = verifyssl or 'vsphere.local'

username = input("username: ")


def pprompt():
    pass1 = getpass.getpass()
    pass2 = getpass.getpass('Retype password: ')
    return (pass1, pass2)


p1, p2 = pprompt()
while p1 != p2:
    print('Passwords do not match. Try again')
    p1, p2 = pprompt()

# vRA tenant configuration
tenant = input("tenant name [vsphere.local]: ")
tenantvalue = tenant or 'vsphere.local'

p = subprocess.Popen(["st2", "key", "set", "vra7_password", p1, "--encrypt"],
                     stdout=subprocess.PIPE)
cmdoutput, err = p.communicate()

config = open(configfile, 'w')
config.write("hostname: " + '"' + str(hostname) + '"' + "\n")
config.write("username: " + '"' + str(username) + '"' + "\n")
config.write('password: "{{st2kv.system.vra7_password}}"' + "\n")
config.write("tenant: " + '"' + str(tenantvalue) + '"' + "\n")
config.write("verify_ssl: " + str(verifyssl) + "\n")
config.close()

print("Successfully configured vRA7 integration pack")
