"""
Implementation of Mood Detection from tweets.

Scrapes Twitter(currently) for most recent tweets
by a person (given user handle).

Detects mood/ tone of tweets using IBM Watson Tone Analyser.

Displays mood.
"""


def get_tweets(query):
    """
    Return topmost tweet from actual list of tweets.

    @type   s         :  string
    @param  moody_user:  twitter user handle
    @return           :  list of tweets(actual)
    """
    import time
    # install selenium https://pypi.python.org/pypi/selenium
    from selenium import webdriver

    # Setting up parameters
    url = u'https://twitter.com/'
    time_sleep = 2
    browser = webdriver.Firefox()
    browser.get(url+query)
    time.sleep(time_sleep)
    tweets = [p.text for p in browser.find_elements_by_class_name('tweet-text')]
    return tweets[0]

def remove_non_ascii(text):
    """
    Remove Non ascii characters.

    @type   s :  string
    @param  s :  string to be stripped off non-ascii characters
    @return   :  non-ascii stripped string
    """
    return "".join(i for i in text if ord(i) < 128)

def moody(moody_user):
    """
    Return a json dump of topmost tweet with mood points.

    @type   s          :  string
    @param  moody_user :  twitter user handle
    @return            :  json dump
    """
    from watson_developer_cloud import ToneAnalyzerV3
    ta_username, ta_password = open("/home/sarbamoy/Desktop/IBM_credentials").read().split()

    tone_analyzer = ToneAnalyzerV3(
        username=ta_username,
        password=ta_password,
        version='2017-09-21')

    texts = get_tweets(moody_user)

    texts = remove_non_ascii(texts)
    print(texts+"\n")
    tone_analysis = tone_analyzer.tone(
        {'text': texts},
        'application/json')
    return tone_analysis

def isemotional(tone):
    """
    Return if tone is an emotional one.

    @type   s    :  string
    @param  tone :  tone
    @return      :  boolean true or false
    """
    if tone in ('anger', 'fear', 'joy', 'sadness'):
        return True

    return False

def recommend_playlist(moody_user):
    """
    Returns a recommended YouTube playlist on basis of mood

    @type   s          :  string
    @param  moody_user :  twitter user handle
    @return            :  url of recommended playlist
    """
    # The service can return results for the following tone IDs:
    # `anger`, `fear`, `joy`, and `sadness` (emotional tones); `analytical`, `confident`,
    # and `tentative` (language tones).
    tone_json = moody(moody_user)
    tones_list = tone_json["document_tone"]["tones"]

    mood = ""
    max_score = -1
    playlist_url = ""
    
    for tone in enumerate(tones_list):
        if isemotional(tone[1]["tone_id"]) and tone[1]["score"] > max_score:
            max_score = tone[1]["score"]
            mood = tone[1]["tone_id"]

    if max_score <= 0:
        return "Sorry, could not find an emotional tone."

    if mood == "anger":
        playlist_url = "https://www.youtube.com/watch?v=Q1jE25zn8RU"
    if mood == "fear":
        playlist_url = "https://www.youtube.com/watch?v=xo1VInw-SKc&list="\
        	"PLIeiyBOIivZNqYgeJTdamFTXdQwNzDIiD"
    if mood == "joy":
        playlist_url = "https://www.youtube.com/watch?v=LjhCEhWiKXk&list="\
        	"PL1VuYyZcPYIJTP3W_x0jq9olXviPQlOe1"
    if mood == "sadness":
        playlist_url = "https://www.youtube.com/watch?v=aJOTlE1K90k&list="\
        	"PL4QNnZJr8sRPeLgoOL9t4V-18xRAuqe_f"

    return playlist_url

print(recommend_playlist("vancityreynolds"))
