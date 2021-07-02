import json
from random import randint

import requests_oauthlib
import yaml

import secret.config as config

CK = config.CONSUMER_KEY
CS = config.CONSUMER_SECRET
AT = config.ACCESS_TOKEN
ATS = config.ACCESS_TOKEN_SECRET


def lambda_handler(event, context):
    twitter = requests_oauthlib.OAuth1Session(CK, CS, AT, ATS)  # 認証処理
    url = "https://api.twitter.com/1.1/statuses/update.json"  # ツイートポストエンドポイント
    with open('static/data.yml', encoding='utf-8') as file:
        obj = yaml.safe_load(file)
        dialogue = obj['dialogue']

    tweet = dialogue[randint(0, len(dialogue) - 1)]
    print(tweet)
    params = {"status": tweet}

    res = twitter.post(url, params=params)  # post送信

    if res.status_code == 200:  # 正常投稿出来た場合
        print("Success.")
    else:  # 正常投稿出来なかった場合
        print("Failed. : %d" % res.status_code)

    return {
        'statusCode': 200,
        'body': json.dumps('Success')
    }


if __name__ == '__main__':
    lambda_handler(None, None)
