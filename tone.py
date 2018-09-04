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
    import requests
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

def tweeper(moody_user):
    """
    Return a sample list of tweets.

    @type   s         :  string
    @param  moody_user:  twitter user handle
    @return           :  list of tweets(sample)
    """
    sample_list = ["Such a smart, talented and kind person "\
                   "who‘ll be hugely missed.",
                   "I’m married to the bottle too. Ironically, you’re gonna "\
                   "want to unscrew it on your wedding night. Congratulations!",
                   "This one is my most favourite 😍 🙈🙈🙈 😘😘 Have a lo... 😊😊"
                   ]
    return sample_list


def removenonascii(s):
    """
    Remove Non ascii characters.

    @type   s :  string
    @param  s :  string to be stripped off non-ascii characters
    @return   :  non-ascii stripped string
    """
    return "".join(i for i in s if ord(i) < 128)

def moody(moody_user):
    """
    Returns a json dump of topmost tweet with mood points.

    @type   s          :  string
    @param  moody_user :  twitter user handle
    @return            :  json dump
    """
    import os
    import json
    from watson_developer_cloud import ToneAnalyzerV3
    ta_username, ta_password = open("/home/sarbamoy/Desktop/IBM_credentials").read().split()

    tone_analyzer = ToneAnalyzerV3(
        username=ta_username,
        password=ta_password,
        version='2017-09-21')

    texts = get_tweets(moody_user)

    texts = removenonascii(texts)
    print(texts+"\n")
    tone_analysis = tone_analyzer.tone(
            {'text': texts},
            'application/json')
    return(json.dumps(tone_analysis, indent=2))

print(moody("vancityreynolds"))