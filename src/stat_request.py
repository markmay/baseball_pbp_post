import requests
import base64
from stat_decoding import decode_response 

def stat_request(team, eventId):
    baseUrl = 'https://stats.statbroadcast.com/interface/webservice/stats?data='
    data = f'event={eventId}&xml={team}/{eventId}.xml&xsl=baseball/sb.bsgame.views.broadcast.xsl&sport=bsgame&filetime=1&type=statbroadcast&start=true'
    encodedData = base64.b64encode(data.encode("ascii")).decode('ascii')
    url = baseUrl + encodedData
    r = requests.get(url)
    if (r.status_code == 200):
        content = decode_response(r.content)
        return { "content": content }
    elif r.status_code == 404:
        return { "error": r.status_code, "content": "" }
    else:
        return { "error": r.status_code}

