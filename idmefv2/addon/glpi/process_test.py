from .process import NullProcessor, ReverseDNSProcessor

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

def test_reverse_dns():
    rp = ReverseDNSProcessor(None)
    o = rp.process(IDMEFV2_1)
    assert 'Hostname' in o.get('Source')[0]
