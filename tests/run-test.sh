#!/bin/bash

URL=http://127.0.0.1:5000

function post()
{
    echo "POST request to ${URL}$2"
    curl -X POST -H "Content-Type: application/json" -d "$1" ${URL}$2
}

post '{"Source":[{"IP":"192.168.1.11"}],"Target":[{"IP": "192.168.2.11"}]}' /null

post '{"Source":[{"IP":"8.8.8.8"}],"Target":[{"Hostname":"www.teclib.com"}]}' /dns

post '{"Source":[{"IP":"192.168.1.11"}],"Target":[{"IP": "192.168.2.11"}]}' /glpi
