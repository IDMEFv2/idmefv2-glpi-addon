import copy
from .process import NullProcessor, DNSProcessor


def test_null():
    message = {"foo": 1, "bar": 2}
    p = NullProcessor()
    before = copy.deepcopy(message)
    p.process(message)
    assert message == before


def test_reverse_dns_1():
    p = DNSProcessor()
    m = IDMEFV2_1
    p.process(m)
    assert "Hostname" in m.get("Source")[0]
    assert isinstance(m.get("Source")[0]["Hostname"], str)
    assert "google" in m.get("Source")[0]["Hostname"]
    assert "Hostname" in m.get("Target")[0]
    assert isinstance(m.get("Target")[0]["Hostname"], str)
    assert "gandi" in m.get("Target")[0]["Hostname"]


def test_dns_1():
    p = DNSProcessor()
    m = IDMEFV2_2
    p.process(m)
    assert "IP" in m.get("Source")[0]
    assert isinstance(m.get("Source")[0]["IP"], str)
    assert "8.8." in m.get("Source")[0]["IP"]
    assert "IP" in m.get("Target")[0]
    assert isinstance(m.get("Target")[0]["IP"], str)
    assert "217.70.184.56" in m.get("Target")[0]["IP"]


IDMEFV2_1 = {
    "Version": "2.D.V04",
    "ID": "ead7600d-c954-4390-bc76-4cf94e509698",
    "CreateTime": "2021-11-26T16:30:12.313039",
    "Category": ["Recon.Scanning"],
    "Priority": "Low",
    "Description": "$.alert.category",
    "Analyzer": {
        "IP": "127.0.0.1",
        "Name": "suricata",
        "Model": "Suricata NIDS",
        "Type": "Cyber",
        "Category": ["NIDS"],
        "Data": ["Network"],
        "Method": ["Signature"],
    },
    "Source": [
        {
            "IP": "8.8.8.8",
            "Port": ["9999"],
            "Protocol": ["HTTP"],
        },
    ],
    "Target": [
        {
            "IP": "217.70.184.55",
            "Port": [80],
        },
    ],
}

IDMEFV2_2 = {
    "Version": "2.D.V04",
    "ID": "ead7600d-c954-4390-bc76-4cf94e509698",
    "CreateTime": "2021-11-26T16:30:12.313039",
    "Category": ["Recon.Scanning"],
    "Priority": "Low",
    "Description": "$.alert.category",
    "Analyzer": {
        "IP": "127.0.0.1",
        "Name": "suricata",
        "Model": "Suricata NIDS",
        "Type": "Cyber",
        "Category": ["NIDS"],
        "Data": ["Network"],
        "Method": ["Signature"],
    },
    "Source": [
        {
            "Hostname": "dns.google.com",
            "Port": ["9999"],
            "Protocol": ["HTTP"],
        },
    ],
    "Target": [
        {
            "Hostname": "www.teclib.com",
            "Port": [80],
        },
    ],
}
