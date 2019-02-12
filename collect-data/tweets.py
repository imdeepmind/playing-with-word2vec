from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json

ckey=""
csecret=""
atoken=""
asecret=""

f= open("tweets.csv","w+")
f.write('text,username,date\n')

class streamData(StreamListener):
    def on_data(self, dt):
        data = json.loads(dt)
        
        try:
            tweet = ""
            if 'retweeted_status' in data:
                if 'extended_tweet' in data['retweeted_status']:
                    tweet = data['retweeted_status']['extended_tweet']['full_text']
            
            if tweet is "":
                tweet = data['text']
                        
            line = data['text'].replace('\n', '').replace(',', '') + ',' + data["user"]["screen_name"] + ',' + data['created_at']
            f.write(line+ '\n')
            print('--tweet saved--')
            
        except:
            pass

        return True

    def on_error(self, status):
        print(status)


auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

twitterStream = Stream(auth, streamData())
twitterStream.filter(languages=["en"], track=["a", "the", "i", "you", "u"])

