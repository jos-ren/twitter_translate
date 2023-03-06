from googletrans import Translator
import tweepy
import requests
import os
from config import *

# for v2 features
client = tweepy.Client(
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
    access_token=access_token,
    access_token_secret=access_token_secret,
    bearer_token=bearer_token
)

# for v1.1 features
auth = tweepy.OAuth1UserHandler(
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret
)

api = tweepy.API(auth)


def main():
    # canada's user id
    print(get_tweets(12, 2459609448))

# retrieves tweets
def get_tweets(num_tweets, user_id):
    resp = client.get_users_tweets(user_id, expansions='attachments.media_keys', media_fields=['url', 'alt_text'], max_results=num_tweets, exclude='retweets')

    i = 1
    while i < len(resp.data)+1:
        text = translate(str(resp.data[len(resp.data)-i]))
        url = resp.includes['media'][len(resp.data)-i]['url']
        # if text is longer than 280, split it into 2 posts
        if len(text) > 280:
            split_strings = []
            for index in range(0, len(text), 260):
                split_strings.append(text[index: index + 260])
            y = 1
            new_list = []
            for x in split_strings:
                new_list.append(f"({y}/{len(split_strings)}) " + x)
                y += 1
            # first make the first tweet
            first_twt = post_tweets(new_list[0], url)
            # then make the second one reply to the first
            post_reply(new_list[1], first_twt[0]['id'])
        else:
            post_tweets(text, url)
        print(i, "tweet is posted")
        i += 1
    return "All Done"


# translates tweets to french
def translate(text):
    translator = Translator()
    translated = translator.translate(text, dest='fr')
    tweet_text = getattr(translated, 'text')
    return tweet_text.split('https')[0]


# posts translated tweets onto my page
def post_tweets(text, url):
    # we need this workaround since we cannot access a tweets media_ids unless its uploaded using v1.1
    # download the tweets img, and download it
    response = requests.get(url)
    file = open("temp_image.png", "wb")
    file.write(response.content)
    file.close()
    # upload the temp img using v1.1 to twitters db
    media = api.media_upload(filename="temp_image.png",
                             media_category='tweet_image')
    # removes the temp img file
    os.remove('temp_image.png')
    tweet = client.create_tweet(text=text, media_ids=[media.media_id_string])
    return tweet


# if tweet longer than 280, reply to first tweet with this second one
def post_reply(text, twt_id):
    tweet = client.create_tweet(text=text, in_reply_to_tweet_id=twt_id)
    return tweet


if __name__ == "__main__":
    main()

# # for deleting all tweets
# resp = client.get_users_tweets(1548484047839453185, max_results=100)
# # print(resp.data[0].id)
# for tweets in resp.data:
#     client.delete_tweet(id=tweets.id)
#     print(tweets.id, "is deleted")