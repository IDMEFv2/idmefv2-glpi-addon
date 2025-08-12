from .process import NullProcessor, ReverseDNSProcessor, DNSProcessor

def test_null():
    message = {'foo': 1, 'bar': 2}
    p = NullProcessor(None)
    assert p.process(message) is message

IDMEFV2_1 =  {
    'Version': '2.D.V04',
    'ID': 'ead7600d-c954-4390-bc76-4cf94e509698',
    'CreateTime': '2021-11-26T16:30:12.313039',
    'Category': ['Recon.Scanning'],
    'Priority': 'Low',
    'Description' : '$.alert.category',
    "Analyzer": {
        "IP": "127.0.0.1",
        "Name": "suricata",
        "Model": "Suricata NIDS",
        "Type": "Cyber",
        "Category": [ "NIDS" ],
        "Data": [ "Network"],
        "Method": [ "Signature"]
    },
    'Source': [
        {
            'IP': '8.8.8.8',
            'Port': ['9999'],
            'Protocol': [ 'HTTP'],
        },
    ],
    'Target': [
        {
            'IP': '217.70.184.55',
            'Port': [ 80],
        },
    ],
}

IDMEFV2_2 =  {
    'Version': '2.D.V04',
    'ID': 'ead7600d-c954-4390-bc76-4cf94e509698',
    'CreateTime': '2021-11-26T16:30:12.313039',
    'Category': ['Recon.Scanning'],
    'Priority': 'Low',
    'Description' : '$.alert.category',
    "Analyzer": {
        "IP": "127.0.0.1",
        "Name": "suricata",
        "Model": "Suricata NIDS",
        "Type": "Cyber",
        "Category": [ "NIDS" ],
        "Data": [ "Network"],
        "Method": [ "Signature"]
    },
    'Source': [
        {
            'Hostname': 'dns.google.com',
            'Port': ['9999'],
            'Protocol': [ 'HTTP'],
        },
    ],
    'Target': [
        {
            'Hostname': 'www.teclib.com',
            'Port': [ 80],
        },
    ],
}

def test_reverse_dns_1():
    rp = ReverseDNSProcessor(None)
    o = rp.process(IDMEFV2_1)
    assert 'Hostname' in o.get('Source')[0]
    assert isinstance(o.get('Source')[0]['Hostname'], str)
    assert 'google' in o.get('Source')[0]['Hostname']
    assert 'Hostname' in o.get('Target')[0]
    assert isinstance(o.get('Target')[0]['Hostname'], str)
    assert 'gandi' in o.get('Target')[0]['Hostname']

def test_dns_1():
    p = DNSProcessor(None)
    o = p.process(IDMEFV2_2)
    assert 'IP' in o.get('Source')[0]
    assert isinstance(o.get('Source')[0]['IP'], str)
    assert '8.8.' in o.get('Source')[0]['IP']
    assert 'IP' in o.get('Target')[0]
    assert isinstance(o.get('Target')[0]['IP'], str)
    assert '217.70.184.56' in o.get('Target')[0]['IP']
