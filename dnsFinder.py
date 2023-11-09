#!/usr/bin/env python3
# to run the tool ./dnsFinder.py google.com

# pip3 install dnspython
import dns.resolver

# access to the command-line arguments passed to the script import sys
import sys

# dns record types to chek
# ipv4 Address record, IPv6 address record, Name server record, Mail exchange record, Canonical name record, Pointer record, Start of authority record, Sender Policy Framework record, Service record, Text record
dns_record_types = ['A', 'AAAA', 'NS', 'MX',
                    'CNAME', 'PTR', 'SOA', 'SPF', 'SRV', 'TXT']

try:
    # use the domain name as the first argument when executing the script
    domain_name = sys.argv[1]

except IndexError:
    print('[-] format should be -->  python3 dnsfinder.py domain_name')
    print('[-] quitting...')
    quit()

for record in dns_record_types:
    try:
        # according to the dnspython documentation
        # resolve different records for a domain
        answer = dns.resolver.resolve(domain_name, record)

        print(f'\n[+] {record} records')
        print('---------------------------------')

        for item in answer:
            # to_text() convert DNS record objects into its textual representation
            print(item.to_text())

    # if the domain does not exist
    except dns.resolver.NXDOMAIN:
        print(f'[-] it seems {domain_name} does not exist.')
        print('quitting...')
        quit()

    # handling no answer error
    except dns.resolver.NoAnswer:
        pass

    # handling keyboard interrupt error
    # except KeyboardInterrupt:
    #     print('keyboard interrupt')
    #     print('quitting...')
    #     quit()
#else :
    #print('no records found')
