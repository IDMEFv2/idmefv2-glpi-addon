#!/bin/bash

DOCKER_ADDON_URL=http://127.0.0.1:5000
DOCKER_TESTSERVER_URL=http://127.0.0.1:9999

TMPDIR=./tmp

function usage()
{
    echo >&2 "Usage: $0 [-u ADDON_URL] [-t TESTSERVER_URL] IDMEFV2"
    echo >&2 "Send a IDMEFv2 message to the add-on server"
    echo >&2 "Examples:"
    echo >&2 "$0 -u http://addon:5555/dns -t http://testserver:9999 test1.json"
    echo >&2 "   Send test1.json to addon and send result to testserver"
    echo >&2 "$0 -u http://addon:5555/glpi test2.json"
    echo >&2 "   Send test2.json to addon without further validation"
    echo >&2 ""
    echo >&2 "Arguments:"
    echo >&2 "  IDMEFV2             IDMEFv2 JSON file to send"
    echo >&2 ""
    echo >&2 "Options:"
    echo >&2 "  -u ADDON_URL        URL of add-on server to POST to"
    echo >&2 "  -t TESTSERVER_URL   URL of test server for message validation"
    echo >&2 "                      If no test server specified, message will not be sent for validation"
    echo >&2 ""

    exit 1
}

function process_file()
{
    sed -e "s/@@UUID@@/$(uuidgen)/" -e "s/@@DATETIME@@/$(date --iso-8601=seconds)/" "$1"
}

function post()
{
    echo >&2 "POST request to $1"
    curl -s -X POST --json "@$2" "$1"
}

ADDON_URL=
TESTSERVER_URL=
while getopts "u:t:h" opt; do
    case $opt in
	u)
        ADDON_URL=$OPTARG
	    ;;
    t)
        TESTSERVER_URL=$OPTARG
        ;;
	h)
	    usage
	    ;;
	\?)
	    usage
	    ;;
	:)
	    usage
	    ;;
    esac
done
shift $((OPTIND-1))

mkdir -p $TMPDIR
IDMEFV2=$1
PROCESSED_IDMEFV2=$(mktemp --tmpdir=$TMPDIR tmp.idmefv2.XXXXXXXXXX)
process_file "$IDMEFV2" > "$PROCESSED_IDMEFV2"
ADDON_RESPONSE=$(mktemp --tmpdir=$TMPDIR tmp.response.XXXXXXXXXX)
post "$ADDON_URL" "$PROCESSED_IDMEFV2" > "$ADDON_RESPONSE"
if [ ! -z "$TESTSERVER_URL" ] ; then
    post "$TESTSERVER_URL" "$ADDON_RESPONSE"
fi
#rm $PROCESSED_IDMEFV2 $ADDON_RESPONSE

#post '{"Source":[{"IP":"192.168.1.11"}],"Target":[{"IP": "192.168.2.11"}]}' /null

#post '{"Source":[{"IP":"8.8.8.8"}],"Target":[{"Hostname":"www.teclib.com"}]}' /dns

#post '{"Source":[{"IP":"192.168.1.11"}],"Target":[{"IP": "192.168.2.11"}]}' /glpi
