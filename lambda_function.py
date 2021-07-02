import sys
import json
from random import randint
from logging import INFO, DEBUG
from logging import getLogger, StreamHandler, basicConfig

import requests_oauthlib
import yaml

import secret.config as config

# about log
basicConfig(stream=sys.stdout,
            level=INFO,
            format="%(asctime)s [%(filename)s:%(lineno)d] %(levelname)-8s %(message)s")
logger = getLogger(__name__)
logger.setLevel(DEBUG)


def lambda_handler(event, context):
    logger.info('process start.')
    twitter = MyTwitter(config.CONSUMER_KEY,
                        config.CONSUMER_SECRET,
                        config.ACCESS_TOKEN,
                        config.ACCESS_TOKEN_SECRET)

    # decide tweet sentence
    with open('static/data.yml', encoding='utf-8') as file:
        obj = yaml.safe_load(file)
        dialogue = obj['dialogue']
    sentence = dialogue[randint(0, len(dialogue) - 1)]
    logger.debug('tweet sentence: \r\n' + sentence)

    # post tweet
    res = twitter.post_tweet(sentence)
    print(res.content.decode())
    if res.status_code == 200:
        logger.info('tweet success.')
    else:
        logger.error('tweet failed.')
        logger.info('response: ' + res.content.decode())

    # end
    logger.info('Process End.')
    return {
        'statusCode': 200,
        'body': json.dumps('Success')
    }


class MyTwitter:
    """exec twitter API access.
    """

    def __init__(self, ck, cs, at, ats):
        self.twitter = requests_oauthlib.OAuth1Session(ck, cs, at, ats)

    def post_tweet(self, sentence):
        url = "https://api.twitter.com/1.1/statuses/update.json"
        res = self.twitter.post(url, params={"status": sentence})
        return res


if __name__ == '__main__':
    lambda_handler(None, None)
