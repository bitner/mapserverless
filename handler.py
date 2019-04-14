# Adopted from https://github.com/dschep/serverless-cgi
import json
import os
from shutil import copyfile
from subprocess import check_output
from urllib.parse import urlencode
import base64
from pathlib import Path


def mapserv(event, context):
    queryparams=event['queryStringParameters'] or {}
    

    env = os.environ.copy()
    env.update(**{f'HTTP_{name.upper().replace("-", "_")}': value
                  for name, value in event.get('headers', {}).items()})

    # script = event['pathParameters']['path']
    env.update(
        MS_MAPFILE='map.map',
        MS_MAP_NO_PATH='nomap',
        MS_TEMPPATH='/tmp/',
        MS_OPENLAYERS_JS_URL='https://www.mapserver.org/lib/OpenLayers-ms60.js',
        SERVER_SOFTWARE='serverless-cgi/0.1',
        SERVER_NAME=event['headers'].get('Host', ''),
        GATEWAY_INTERFACE='CGI/1.1',
        SERVER_PROTOCOL='HTTP/1.1',
        SERVER_PORT=event['headers'].get('X-Forwarded-Port', '' ),
        REQUEST_METHOD=event['httpMethod'],
        PATH_INFO='',  # TODO
        PATH_TRANSLATED='',  # TODO
        SCRIPT_NAME='',  # TODO
        QUERY_STRING=urlencode(queryparams),
        REMOTE_ADDR=event['requestContext']['identity']['sourceIp'],
        CONTENT_TYPE=event['headers'].get('Content-Type'),
        CONTENT_LENGTH=(len(event['body'])
                        if event.get('body') is not None
                        else 0),
        PROJ_LIB="/opt/share/proj"
    )
    for key, value in env.items():
        try:
            os.environ[key]=value
        except:
            pass

    if not queryparams:
            body=Path('ol.html').read_text().replace('<server>',env['SERVER_NAME'])
            return {
                "statusCode": 200,
                "body": body,
                "headers": {'Content-Type': 'text/html'}
            }

    headers={}
    header, body = check_output(['mapserv']).split(b'\r\n\r\n',1)
    header=header.decode()
    key, value = header.split(': ',1)
    headers[key]=value
    headers['Access-Control-Allow-Origin']='*'
    headers['Access-Control-Allow-Headers']='Content-Type'
    headers['Access-Control-Allow-Methods']='OPTIONS,GET'


    if value=='image/png':
        response=base64.encodebytes(body).decode()
        b64="true"
    else:
        response=body.decode()
        b64="false"

    response = {
        "statusCode": 200,
        "body": response,
        "headers": headers,
        "isBase64Encoded": b64
    }

    return response
