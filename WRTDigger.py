import sys
import itertools
import requests


# http://stackoverflow.com/questions/20525330/python-generate-a-list-of-ip-
#addresses-from-user-input
def ip_gen(input_string):
  octets = input_string.split('.')
  chunks = [map(int, octet.split('-')) for octet in octets]
  ranges = [range(c[0], c[1] + 1) if len(c) == 2 else c for c in chunks]

  for address in itertools.product(*ranges):
    yield '.'.join(map(str, address))


# http://stackoverflow.com/questions/6999565/python-https-get-with-basic-
# authentication
def knock_on(address):
  cred = 'YWRtaW46YWRtaW4='
  #cred = 'YWRtaW46MFREalUzYXZEbVlCYjVMVnhIRzE='
  headers = {'Authorization': 'Basic %s' % cred}
  r = requests.get(address, headers=headers)
  #return r.text
  return r.headers, r.text


# Main
def main():
  url_list = []

 # Generating the IPs from the a given range.
  try:
    for address in ip_gen('192.168.1.1-1'):
      target_url = "http://%s/" % address
      #print(target_url)
      url_list.append(target_url)
  except Exception:
      sys.exit("[-] Problem generating the IP addresses")

  # Receiving the request text and headers.
  try:
    (res_headers, res_text) = knock_on(target_url)
    #print(res_headers['server'])
    #print(res_text)
    if 'Intoto Http Server' in res_headers['server']:
      print('yes')
  except Exception:
    sys.exit("[-] No service for host")


if __name__ != "__main__":
  sys.exit("[!] NO WAY!")
else:
  main()