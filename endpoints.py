# -*- coding:utf-8 -*-
import urllib.parse

USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'

BASE_URL = 'https://www.instagram.com'
LOGIN_URL = 'https://www.instagram.com/accounts/login/ajax/'
ACCOUNT_MEDIAS = "http://www.instagram.com/graphql/query/?query_hash=42323d64886122307be10013ad2dcc44&variables=%s"
ACCOUNT_PAGE = 'https://www.instagram.com/%s'
MEDIA_LINK = 'https://www.instagram.com/p/%s'
INSTAGRAM_CDN_URL = 'https://scontent.cdninstagram.com/'
ACCOUNT_JSON_PRIVATE_INFO_BY_ID = 'https://i.instagram.com/api/v1/users/%s/info/'
FOLLOWERS_URL = 'https://www.instagram.com/graphql/query/?query_id=17851374694183129&id={{accountId}}&first={{count}}&after={{after}}'
FOLLOWING_URL = 'https://www.instagram.com/graphql/query/?query_id=17874545323001329&id={{accountId}}&first={{count}}&after={{after}}'
COMMENTS_BEFORE_COMMENT_ID_BY_CODE = 'https://www.instagram.com/graphql/query/?query_hash=33ba35852cb50da46f5b5e889df7d159&variables=%s'
LIKES_BY_SHORTCODE = 'https://www.instagram.com/graphql/query/?query_id=17864450716183058&variables=%s'
MEDIA_JSON_BY_TAG = 'https://www.instagram.com/explore/tags/%s/?__a=1&max_id=%s'
GENERAL_SEARCH = 'https://www.instagram.com/web/search/topsearch/?query=%s'
MEDIA_JSON_BY_LOCATION_ID = 'https://www.instagram.com/explore/locations/%s/?__a=1&max_id=%s'
ACCOUNT_JSON_INFO = 'https://www.instagram.com/%s/?__a=1'
USER_STORIES_LINK = 'https://www.instagram.com/graphql/query/?query_id=17890626976041463&variables=%s'
STORIES_LINK = 'https://www.instagram.com/graphql/query/?query_id=17873473675158481&variables=%s'
LIKE_URL = 'https://www.instagram.com/web/likes/%s/like/'
UNLIKE_URL = 'https://www.instagram.com/web/likes/%s/unlike/'
ADD_COMMENT_URL = 'https://www.instagram.com/web/comments/%s/add/'
DELETE_COMMENT_URL = 'https://www.instagram.com/web/comments/%s/delete/%s/'

def get_account_media_url(variables):
    return ACCOUNT_MEDIAS % urllib.parse.quote(variables)


def get_account_page_link(user_name):
    return ACCOUNT_PAGE % user_name


def get_media_url(media_url):
    return media_url.rstrip('/') + '/?__a=1'


def get_media_page_link(code):
    return MEDIA_LINK % urllib.parse.quote(code)


def get_account_json_private_info_link_by_account_id(id):
    return ACCOUNT_JSON_PRIVATE_INFO_BY_ID % urllib.parse.quote(str(id))


def get_followers_json_link(account_id, count, after=''):
    url = FOLLOWERS_URL.replace('{{accountId}}', urllib.parse.quote(account_id))
    url = url.replace('{{count}}', urllib.parse.quote(str(count)))

    if after == '':
        url = url.replace('&after={{after}}', '')
    else:
        url = url.replace('{{after}}', urllib.parse.quote(after))

    return url


def get_following_json_link(account_id, count, after=''):
    url = FOLLOWING_URL.replace('{{accountId}}', urllib.parse.quote(account_id))
    url = url.replace('{{count}}', urllib.parse.quote(str(count)))

    if after == '':
        url = url.replace('&after={{after}}', '')
    else:
        url = url.replace('{{after}}', urllib.parse.quote(after))

    return url


def get_comments_before_comment_id_by_code(variables):
    return COMMENTS_BEFORE_COMMENT_ID_BY_CODE % urllib.parse.quote(variables)


def get_medias_json_by_tag_link(tag, max_id=''):
    return MEDIA_JSON_BY_TAG % (urllib.parse.quote(tag), urllib.parse.quote(max_id))


def get_general_search_json_link(query):
    return GENERAL_SEARCH % urllib.parse.quote(query)


def get_medias_json_by_location_id_link(facebook_location_id, max_id=''):
    return MEDIA_JSON_BY_LOCATION_ID % (urllib.parse.quote(str(facebook_location_id)), urllib.parse.quote(max_id))


def get_account_json_link(username):
    return ACCOUNT_JSON_INFO % urllib.parse.quote(str(username))


def get_user_stories_link(variables):
    return USER_STORIES_LINK % urllib.parse.quote(variables)


def get_stories_link(variables):
    return STORIES_LINK % urllib.parse.quote(variables)


def get_like_url(media_id):
    return LIKE_URL % urllib.parse.quote(str(media_id))


def get_unlike_url(media_id):
    return UNLIKE_URL % urllib.parse.quote(str(media_id))


def get_add_comment_url(media_id):
    return ADD_COMMENT_URL % urllib.parse.quote(str(media_id))


def get_delete_comment_url(media_id, comment_id):
    return DELETE_COMMENT_URL % (urllib.parse.quote(str(media_id)), urllib.parse.quote(str(comment_id)))


def get_last_likes_by_code(variables):
    return LIKES_BY_SHORTCODE % urllib.parse.quote(variables)