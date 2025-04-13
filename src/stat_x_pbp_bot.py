import time
import datetime
from stat_request import stat_request
from stat_parsing import stat_parse
from stat_formatter import stat_format
from stat_secret_headers import get_secret
from stat_x_post import x_post
from aws_lambda_powertools import Logger

def handler(event, context):
    logging = Logger()
    logging.info("lambda started")
    team = event['team']
    eventId = event['eventId']
    previousStats = event['stats'] if 'stats' in event else { "previousData": [], "currentInning": "", "dueUp": []}
    if ('secrets' not in event):
        event['secrets'] = get_secret()
    secrets = event['secrets']
    response = stat_request(team, eventId)
    if ("error" in response):
        print(response["error"])
        return {
            'statusCode': 400,
            'error': response["error"]
        }

    stats = stat_parse(response["content"])
    currentPost = stat_format(stats, previousStats)
    
    retStats = { 
        "currentInning": stats["currentInning"], 
        "previousData": stats["previousData"], 
        "dueUp": stats["dueUp"], 
    }
    event['stats'] = retStats
    event['post'] = currentPost
    logging.info("post: " + currentPost)

    responseCode = x_post(secrets, currentPost)
    logging.info("response_code:" + str(responseCode))
    return event
