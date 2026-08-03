#!/usr/bin/env python3

# Convert IANA Enterprise Numbers to JSON
#
# TODO: Deal with "misformatted" lines in input better.
#
# (c) 2018 Markus Juenemann <markus&juenemann.net>

import json
import requests

data = {}

resp = requests.get('https://www.iana.org/assignments/enterprise-numbers/enterprise-numbers')

number = None
organization = None
contact = None
email = None

for line in resp.text.splitlines():
    if line.startswith('      '):
        email = line.strip()

        if number is not None and organization is not None and contact is not None and email is not None :
            try:
                data[int(number)] = {'organization': organization, 'contact': contact, 'email': email}
            except Exception as e:
                print(e, number, organization, contact, email)
        else:
            print('Data missing', number, organization, contact, email)

        number = None
        organization = None
        contact = None
        email = None

    elif line.startswith('    '):
        contact = line.strip()

    elif line.startswith('  '):
        organization = line.strip()

    else:
        number = line.strip()


with open('enterprise.json', 'wt') as fp:
    json.dump(data, fp, indent=2)
