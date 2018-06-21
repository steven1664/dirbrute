#!/usr/bin/python3
import argparse
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import sys
import threading


def parsefile(files1):
    http_hosts = []
    for file1 in files1:
        with open(file1, 'r') as f:
            for line in f:
                http_hosts.append(line.rstrip())

    return http_hosts

def webcheck(url, web_dir, ext=''):
    try:
        if url.endswith('/') or web_dir.startswith('/'):
            web_host = url + web_dir + ext
        else:
            web_host = url + '/' + web_dir + ext
        r = requests.head(web_host, verify=False)
        if r.status_code != 404:
            print(web_host + ' - ' + str(r.status_code))

    except Exception:
        pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--extension", help="Provide a file extension for discovery of specific file types")
    parser.add_argument("-f", "--file", help="Provide a text file with directories or files to check for", nargs="+")
    parser.add_argument("-u", "--url", help="Provide a url for discovering files or directories")
    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit()
    if not args.url:
        print('No URL provided!' + '\n')
        parser.print_help()
        sys.exit()
    if not args.file:
        print('No File value was provided!' + '\n')
        parser.print_help()
        sys.exit()

    web_brute = parsefile(args.file)

    threads = []
    for host in web_brute:
        if args.extension:
            t = threading.Thread(target=webcheck, args=(args.url, host, args.extension), daemon=True)
        else:
            t = threading.Thread(target=webcheck, args=(args.url, host), daemon=True)
        threads.append(t)
        t.start()
    for thread in threading.enumerate():
        if thread is not threading.currentThread():
            thread.join(timeout=5.0)
