import config
import requests
import logging

logger = logging.getLogger()

__headers = {"Authorization": f"Bearer {config.TWITTER_API_TOKEN}"}


def get_updated_tweets(since_id: str, existing_tweets: list) -> (str, list):

    new_tweet_ids = __get_tweet_ids(since_id)

    if len(new_tweet_ids) > 0:
        since_id = new_tweet_ids[0]

    tweets = __get_updated_tweets_list(new_tweet_ids, existing_tweets)

    logger.info(f'number new tweets: {len(new_tweet_ids)}, since_id: {since_id}')

    return since_id, tweets


def __get_updated_tweets_list(new_tweets, existing_tweets):
    combined_tweets = new_tweets + existing_tweets
    latest_n_tweets = combined_tweets[:config.MAX_TWEETS]

    return latest_n_tweets


def __get_tweet_ids(since_id):
    tweet_ids = []
    current_next_token = None
    while len(tweet_ids) <= config.MAX_TWEETS:

        part_tweet_ids, next_token = __get_part_tweet_ids(since_id, current_next_token)
        current_next_token = next_token

        if part_tweet_ids is not None:
            tweet_ids.extend(part_tweet_ids)

        if current_next_token is None:
            break

    return tweet_ids


def __get_part_tweet_ids(since_id, next_token) -> (list, str):
    params = {"query": config.TWEET_SEARCH_QUERY, "expansions": "author_id"}
    if since_id is not None:
        params['since_id'] = since_id
    if next_token is not None:
        params['next_token'] = next_token

    r = requests.get(config.TWITTER_API_RECENT_TWEETS_URL, headers=__headers, params=params)
    if not r.ok:
        logger.error(r.text)

        return None, None

    response = r.json()

    data = response.get('data') or []
    tweet_ids = [tweet['id'] for tweet in data]
    next_next_token = __read_next_token(response.get('meta'))

    return tweet_ids, next_next_token


def __read_next_token(meta):
    if meta is not None:
        return meta.get('next_token')

    return None
