#!/bin/bash

DOCKER_ADDON_URL=http://127.0.0.1:5000
DOCKER_TESTSERVER_URL=http://127.0.0.1:9999

TMPDIR=./tmp

function usage()
{
    echo >&2 "Usage: $0 [-u ADDON_URL] [-t TESTSERVER_URL] IDMEFV2"
    echo >&2 "Send a IDMEFv2 message to the add-on server"
    echo >&2 "Examples:"
    echo >&2 "  $0 -u http://addon:5555/dns -t http://testserver:9999 test1.json"
    echo >&2 "    Send test1.json to addon and send result to testserver"
    echo >&2 "  $0 -u http://addon:5555/glpi test2.json"
    echo >&2 "    Send test2.json to addon without further validation"
    echo >&2 ""
    echo >&2 "Defaults URL, when running this script on host and addon in docker:"
    echo >&2 "  ADDON_URL=$DOCKER_ADDON_URL"
    echo >&2 "  TESTSERVER_URL=$DOCKER_TESTSERVER_URL"
    echo >&2 "Ports may change if customized using configuration file"
    echo >&2 ""
    echo >&2 "Arguments:"
    echo >&2 "  IDMEFV2             IDMEFv2 JSON file to send"
    echo >&2 ""
    echo >&2 "Options:"
    echo >&2 "  -u ADDON_URL        URL of add-on server to POST to"
    echo >&2 "  -t TESTSERVER_URL   URL of test server for message validation"
    echo >&2 "                      If no test server specified, message will not be sent for validation"

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
IDMEFV2=$1
if [ -z "$IDMEFV2" -o -z "ADDON_URL" ] ; then usage; fi

mkdir -p $TMPDIR
PROCESSED_IDMEFV2=$(mktemp --tmpdir=$TMPDIR tmp.idmefv2.XXXXXXXXXX)
process_file "$IDMEFV2" | tee "$PROCESSED_IDMEFV2"
ADDON_RESPONSE=$(mktemp --tmpdir=$TMPDIR tmp.response.XXXXXXXXXX)
post "$ADDON_URL" "$PROCESSED_IDMEFV2" | tee "$ADDON_RESPONSE"
if [ ! -z "$TESTSERVER_URL" ] ; then
    post "$TESTSERVER_URL" "$ADDON_RESPONSE"
fi
rm $PROCESSED_IDMEFV2 $ADDON_RESPONSE
