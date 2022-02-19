#Imports
from key import key, secret, consumer_key, consumer_secret
import schedule
import tweepy
from time import sleep
import csv
import random


#Consumer key and secret from Twitter Developer
consumer_key = consumer_key
consumer_secret = consumer_secret
key = key
secret = secret

#Auth
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(key, secret)

#API
api = tweepy.API(auth, wait_on_rate_limit=True)

#Arreglos correspodientes para replicar un mensaje, buscar el tweet, tweets bulgares y tweets aleatorios
reply_message = ['Cul', 'Oh no!', ':)', 'IDK', 'Thats great']
message_search = ['Platzi', 'platzi', '@platzi', '@freddier']
profanity = ['tonto', 'subnormal', 'loco', 'gonorrea', 'hdpm', 'hijo de puta']
message = ['Tweet from my house! 🤖👀', 'Hi everyone! 😎', 'Take care of the planet ☢', 'Student at Platzi 💚', 'I like u 💬', 'Better say it today']

replies = []

#Lee el ultimo id del archivo
def read_last_id():
    file = open('last_id.txt', 'r')
    id = int(file.read().strip())
    file.close()
    return id

#Escribe el id de un tweet
def store_last_id(id):
    file = open('last_id.txt', 'w')
    file.write(str(id))
    file.close()

#Reply tweet y bloquea
def reply_and_block(tweet):
    in_reply_to_status_id = tweet.id
    api.update_status('See you later! 😡', in_reply_to_status_id,
                      auto_populate_reply_metadata=True)
    store_last_id(in_reply_to_status_id)
    api.create_block(tweet.user.screen_name)


#Tweet aleatorio
def tweet():
    status = api.update_status(random.choice(message))
    api.update_status(status, auto_populate_reply_metadata=True)

#Valida el tweet si es bulgar o no
def check_tweet():
    print('Checkeando...')
    mentions = api.mentions_timeline()
    for tweet in reversed(mentions):
        print(tweet.text)
        if any(x in tweet.text for x in profanity):
            reply_and_block(tweet)
        else:
            favoriteandrt()

#Le da favorito a los tweets y RT
def favoriteandrt():
    for tweet in tweepy.Cursor(api.search_tweets, q=random.choice(message_search), result_type='recent', count=10).items(10):
        try:
            if tweet.favorited == False:
                tweet.favorite()
                print('Favorited the tweet %s' % tweet.user.screen_name)

                with open('replies_clean.csv', 'a', encoding="utf-8") as f:
                    csv_writer = csv.DictWriter(f, fieldnames=('user', 'text'))
                    # csv_writer.writeheader()
                    for tweet in replies:
                        row = {'user': tweet.user.screen_name,
                               'text': tweet.text.replace('\n', ' ')}
                        csv_writer.writerow(row)
            
            sleep(10)

            if tweet.retweeted == False:
                tweet.retweet()
                print('Retweeted')

            sleep(10)

        except tweepy.TweepyException as e:
            raise e

        except StopIteration:
            break

#Funcion principal
def main():
    print('Start')
    schedule.every(30).minutes.do(check_tweet)
    schedule.every(1).day.at("10:00").do(tweet)

    while True:
        try:
            schedule.run_pending()
            sleep(5)
        except tweepy.TweepyException as e:
            raise e
        except StopIteration:
            break

#Entrypoint
if __name__ == '__main__':
    main()
