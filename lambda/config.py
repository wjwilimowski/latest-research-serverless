import os


def __config(name: str, default_value: str = None):
    var = os.environ.get(name) or default_value
    if var is None:
        raise EnvironmentError(f'{var} is not configured')

    return var


__MAX_TWEET_SEARCH_QUERY_CHARS = 512
__DEFAULT_TWEET_SEARCH_QUERY = '("najnowsze badania" OR "najnowszych badań" OR "najnowszymi badaniami" OR "najnowszym badaniom") -is:reply -is:retweet'

TWITTER_API_TOKEN = __config('TWITTER_API_TOKEN')
TWEET_SEARCH_QUERY = __config('TWEET_SEARCH_QUERY', __DEFAULT_TWEET_SEARCH_QUERY)
TWITTER_API_RECENT_TWEETS_URL = __config('TWITTER_API_RECENT_TWEETS_URL', 'https://api.twitter.com/2/tweets/search/recent')
MAX_TWEETS = int(__config('MAX_TWEETS', '50'))

if len(TWEET_SEARCH_QUERY) > __MAX_TWEET_SEARCH_QUERY_CHARS:
    raise EnvironmentError(f'TWEET_SEARCH_QUERY configured is {len(TWEET_SEARCH_QUERY)} characters long, which is '
                           f'more than the maximum of {__MAX_TWEET_SEARCH_QUERY_CHARS}')

if MAX_TWEETS <= 0:
    raise EnvironmentError(f'MAX_TWEETS was configured to be {MAX_TWEETS} but should be non-negative')