if __name__ == "__main__":

    import os
    import json
    from watson_developer_cloud import ToneAnalyzerV3

    ta_username = os.environ['watson_tau']
    ta_password = os.environ['watson_tap']

    tone_analyzer = ToneAnalyzerV3(
        username=ta_username,
        password=ta_password,
        version='2017-09-21')

    text = 'Insert sample text'

    tone_analysis = tone_analyzer.tone(
        {'text': text},
        'application/json')
    print(json.dumps(tone_analysis, indent=2))
