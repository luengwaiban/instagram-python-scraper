# -*- coding:utf-8 -*-
import requests
import re
import json
import hashlib
import model
import endpoints
# import sys

# 一次设置proxy的办法，将它设置在一次session会话中，这样就不用每次都在调用requests的时候指定proxies参数了
# s = requests.session()
# s.proxies = {'http': '121.193.143.249:80'}


class InstagramScraper(object):

    HTTP_NOT_FOUND = 404
    HTTP_OK = 200
    HTTP_FORBIDDEN = 403
    HTTP_BAD_REQUEST = 400
    MAX_COMMENTS_PER_REQUEST = 300
    MAX_LIKES_PER_REQUEST = 300
    PAGING_TIME_LIMIT_SEC = 1800  # 30 mins time limit on operations that require multiple requests
    PAGING_DELAY_MINIMUM_MICROSEC = 1000000  # 1 sec min delay to simulate browser
    PAGING_DELAY_MAXIMUM_MICROSEC = 3000000  # 3 sec min delay to simulate browser

    def __init__(self):
        self.__req = requests.session()
        self.paging_time_limit_sec = self.PAGING_TIME_LIMIT_SEC
        self.paging_delay_minimum_microsec = self.PAGING_DELAY_MINIMUM_MICROSEC
        self.paging_delay_maximum_microsec = self.PAGING_DELAY_MAXIMUM_MICROSEC
        self.__user_session = None
        self.__session_name = None
        self.__session_password = None
        self.__rhx_gis = ''

    def set_proxies(self, proxy):
        if proxy and isinstance(proxy, dict):
            self.__req.proxies = proxy

    def generate_header(self, user_session=None, gis_token=''):
        header = {
            'user-agent': endpoints.USER_AGENT,
        }
        if user_session and isinstance(user_session, dict):
            cookies = ''
            for value, key in user_session.items():
                cookies += key + "=" + value + "; "

            csrf = user_session['csrftoken'] and user_session['x-csrftoken'] or user_session['csrftoken']

            header['cookies'] = cookies
            header['referer'] = endpoints.BASE_URL + '/'
            header['csrftoken'] = csrf

        if gis_token:
            header['x-instagram-gis'] = gis_token
        return header

    def get_shared_data(self, html=''):
        """get window._sharedData from page,return the dict loaded by window._sharedData str
        """
        if html:
            target_text = html
        else:
            header = self.generate_header(self.__user_session)
            response = self.__req.get(endpoints.BASE_URL, headers=header)
            target_text = response.text
        regx = r"\s*.*\s*<script.*?>.*_sharedData\s*=\s*(.*?);<\/script>"
        match_result = re.match(regx, target_text, re.S)
        data = json.loads(match_result.group(1))

        return data

    def get_rhx_gis(self):
        """get the rhx_gis value from sharedData
        """
        if self.__rhx_gis:
            return self.__rhx_gis
        share_data = self.get_shared_data()
        return share_data['rhx_gis']

    def get_account(self, user_name):
        """get the account info by username
        :param user_name:
        :return:
        """
        url = endpoints.get_account_page_link(user_name)
        header = self.generate_header(self.__user_session)
        response = self.__req.get(url, headers=header)
        data = self.get_shared_data(response.text)
        account = self.resolve_account_data(data)
        return account

    def get_media_by_user_id(self, user_id, count=50, max_id=''):
        """get media info by user id
        :param user_id:
        :param count:
        :param max_id:
        :return:
        """
        index = 0
        medias = []
        has_next_page = True
        while index <= count and has_next_page:
            variables = json.dumps({
                'id': str(user_id),
                'first': count,
                'after': str(max_id)
            }, separators=(',', ':'))  # 不指定separators的话key:value的:后会默认有空格，因为其默认separators为(', ', ': ')
            url = endpoints.get_account_media_url(variables)
            header = self.generate_header(self.generate_instagram_gis(variables))
            response = self.__req.get(url, headers=header)

            media_json_data = json.loads(response.text)
            media_raw_data = media_json_data['data']['user']['edge_owner_to_timeline_media']['edges']

            if not media_raw_data:
                return medias

            for item in media_raw_data:
                if index == count:
                    return medias
                index += 1
                medias.append(self.general_resolve_media(item['node']))
            max_id = media_json_data['data']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']
            has_next_page = media_json_data['data']['user']['edge_owner_to_timeline_media']['page_info']['has_next_page']
        return medias

    def get_media_by_url(self, media_url):
        response = self.__req.get(endpoints.get_media_url(media_url), headers=self.generate_header())
        media_json = json.loads(response.text)
        return self.general_resolve_media(media_json['graphql']['shortcode_media'])

    def generate_instagram_gis(self, varibles):
        rhx_gis = self.get_rhx_gis()
        gis_token = rhx_gis + ':' + varibles
        x_instagram_token = hashlib.md5(gis_token.encode('utf-8')).hexdigest()
        return x_instagram_token



    def general_resolve_media(self, media):
        res = {
            'id': media['id'],
            'type': media['__typename'][5:].lower(),
            'content': media['edge_media_to_caption']['edges'][0]['node']['text'],
            'title': 'title' in media and media['title'] or '',
            'shortcode': media['shortcode'],
            'preview_url': endpoints.BASE_URL + '/p/' + media['shortcode'],
            'comments_count': media['edge_media_to_comment']['count'],
            'likes_count': media['edge_media_preview_like']['count'],
            'dimensions': 'dimensions' in media and media['dimensions'] or {},
            'display_url': media['display_url'],
            'owner_id': media['owner']['id'],
            'thumbnail_src': 'thumbnail_src' in media and media['thumbnail_src'] or '',
            'is_video': media['is_video'],
            'video_url': 'video_url' in media and media['video_url'] or ''
        }
        return res

    def resolve_account_data(self, account_data):
        account = {
            'country': account_data['country_code'],
            'language': account_data['language_code'],
            'biography': account_data['entry_data']['ProfilePage'][0]['graphql']['user']['biography'],
            'followers_count': account_data['entry_data']['ProfilePage'][0]['graphql']['user']['edge_followed_by']['count'],
            'follow_count': account_data['entry_data']['ProfilePage'][0]['graphql']['user']['edge_follow']['count'],
            'full_name': account_data['entry_data']['ProfilePage'][0]['graphql']['user']['full_name'],
            'id': account_data['entry_data']['ProfilePage'][0]['graphql']['user']['id'],
            'is_private': account_data['entry_data']['ProfilePage'][0]['graphql']['user']['is_private'],
            'is_verified': account_data['entry_data']['ProfilePage'][0]['graphql']['user']['is_verified'],
            'profile_pic_url': account_data['entry_data']['ProfilePage'][0]['graphql']['user']['profile_pic_url_hd'],
            'username': account_data['entry_data']['ProfilePage'][0]['graphql']['user']['username'],
        }
        return account


# account = get_account('shaq')

# result = get_media_by_user_id(account['id'], 56)

# media = get_media_by_url('https://www.instagram.com/p/Bw3-Q2XhDMf/')

# print(len(result))
# print(InstagramScraper.BASE_URL)

proxies = {
    'http': 'http://127.0.0.1:1087',
    'https': 'http://127.0.0.1:1087',
}

instagram = InstagramScraper()
instagram.set_proxies(proxies)
account = instagram.get_account('shaq')
medias = instagram.get_media_by_user_id(account['id'], 63)
print(len(medias))