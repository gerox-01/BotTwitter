import schedule
import tweepy as tp
import time
import random
from key import key, secret, consumer_key, consumer_secret

consumer_key = consumer_key
consumer_secret = consumer_secret

key = key
secret = secret

auth = tp.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(key, secret)

api = tp.API(auth, wait_on_rate_limit=True)


reply_message = ['Cul', 'Oh no!', ':)', 'IDK', 'Thats great']
profanity = ['tonto', 'subnormal', 'loco', 'gonorrea', 'hdpm', 'hijo de puta']

# api.update_status(status='Hello, world!')


def read_last_id():
    file = open('last_id.txt', 'r')
    id = int(file.read().strip())
    file.close()
    return id


def store_last_id(id):
    file = open('last_id.txt', 'w')
    file.write(str(id))
    file.close()


def reply_and_block(tweet):
    in_reply_to_status_id = tweet.id
    api.update_status('see you later! 😡'
    )
    store_last_id(in_reply_to_status_id)
    api.create_block(tweet.user.screen_name)


def reply(tweet):
    in_reply_to_status_id = tweet.id
    status = random.choice(reply_message)
    api.update_status(status)
    store_last_id(in_reply_to_status_id)


def tweet():
    # api.update_status(status='Hello, world!')
    # api.update_status(status='Tweet from my house! 🤖👀')
    # api.update_with_media(filename='/home/jose/Pictures/wallpaper.jpg', status='Tweet from my house! 🤖👀')
    status = api.update_status('Tweet from my house! 🤖👀')
    api.update_status(status)


def check_mention():
    mentions = api.mentions_timeline()
    for tweet in reversed(mentions):
        print(tweet.text)
        if any(x in tweet.text for x in profanity):
            reply_and_block(tweet)
        else:
            reply(tweet)


def main():
    print('Empezo')
    schedule.every(7).seconds.do(check_mention)
    schedule.every(1).day.at("18:35").do(tweet)
    # schedule.every(12).hours.do(tweet)
    # schedule.every(1).day.at("06:00").do(tweet)
    # schedule.every().day.at('20:00').do(tweet)

    while True:
        try:
            schedule.run_pending()
            time.sleep(5)
        except tp.TweepyException as e:
            raise e


if __name__ == '__main__':
    main()
