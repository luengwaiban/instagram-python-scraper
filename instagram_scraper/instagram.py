# -*- coding:utf-8 -*-
import requests
import re
import json
import hashlib
from instagram_scraper import endpoints, helper, model, two_step_verification, exception, cache
import random
import time


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
        self.__user_session = {}
        self.__session_name = None
        self.__session_password = None
        self.__rhx_gis = ''
        self.__user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'

    def set_proxies(self, proxy):
        if proxy and isinstance(proxy, dict):
            self.__req.proxies = proxy

    def disable_proxies(self):
        self.__req.proxies = {}

    def get_user_agent(self):
        return self.__user_agent

    def set_user_agent(self, user_agent):
        self.__user_agent = user_agent

    def generate_header(self, user_session=None, gis_token=''):
        header = {
            'user-agent': self.get_user_agent(),
        }
        if user_session and isinstance(user_session, dict):
            cookies = ''
            for key, value in user_session.items():
                cookies += key + "=" + value + "; "

            csrf = 'csrftoken' in user_session and user_session['csrftoken'] or ('x-csrftoken' in user_session and user_session['x-csrftoken'] or '')

            header['cookie'] = cookies
            header['referer'] = endpoints.BASE_URL + '/'
            header['x-csrftoken'] = csrf

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
        if not match_result:
            return None
        data = json.loads(match_result.group(1))

        return data

    def get_rhx_gis(self):
        """
        get the rhx_gis value from sharedData
        """
        if self.__rhx_gis:
            return self.__rhx_gis
        share_data = self.get_shared_data()
        return share_data['rhx_gis']

    def generate_instagram_gis(self, varibles):
        rhx_gis = self.get_rhx_gis()
        gis_token = rhx_gis + ':' + varibles
        x_instagram_token = hashlib.md5(gis_token.encode('utf-8')).hexdigest()
        return x_instagram_token

    def with_credentials(self, username, password, session_folder='./cache_files/session'):
        """
        collect and cache(maybe) the username, password for logging in
        :param username:
        :param password:
        :param session_folder:
        :return:
        """
        session_cache = cache.Cache.create('disk')
        session_cache.set_cache_storage_dir(session_folder)
        self.__session_name = username
        self.__session_password = password

    def is_logged_in(self, session=None):
        """
        judge if a user has logged in
        :param session:
        :return:
        """
        if not session or 'sessionid' not in session:
            return False
        session_id = session['sessionid']
        csrf_token = session['csrftoken']
        header = {
            'cookie': "ig_cb=1; csrftoken="+csrf_token+"; sessionid="+session_id+";",
            'referer': endpoints.BASE_URL + '/',
            'x-csrftoken': csrf_token,
            'x-CSRFToken': csrf_token,
            'user-agent': self.get_user_agent()
        }
        response = self.__req.get(endpoints.BASE_URL, headers=header)
        if response.status_code != self.HTTP_OK:
            return False

        cookies = self.get_cookie(response)
        if 'ds_user_id' not in cookies:
            return False

        return True

    def verify_two_step(self, response, cookies, two_step_verificator):
        """
        if an account is unusual, it needs to be verified
        :param response:
        :param cookies:
        :param two_step_verificator:
        :return:
        """
        new_cookies = self.get_cookie(response)
        cookies.update(new_cookies)
        cookies_string = ''
        for name, value in cookies.items():
            cookies_string += name + '=' + value + '; '
        header = {
            'cookie': cookies_string,
            'referer': endpoints.LOGIN_URL,
            'x-csrftoken': cookies['csrftoken'],
            'user-agent': self.get_user_agent()
        }

        json_body = json.loads(response.text)
        url = endpoints.BASE_URL + json_body['checkpoint_url']
        response = self.__req.get(url, headers=header)
        shared_data = self.get_shared_data(response.text)
        if shared_data:
            choices = helper.get_from_dict(shared_data, ['entry_data', 'Challenge', 0, 'extraData', 'content', 3, 'fields', 0, 'values'])
            fields = helper.get_from_dict(shared_data, ['entry_data', 'Challenge', 0, 'fields'])
            if (not choices) and fields:
                if 'email' in fields:
                    choices.append({'label': 'Email: '+fields['email'], 'value': 1})
                if 'phone_number' in fields:
                    choices.append({'label': 'Phone: ' + fields['phone_number'], 'value': 0})

            if choices:
                selected_choice = two_step_verificator.get_verification_type(choices)
                response = self.__req.post(url, headers=header, data={'choice': selected_choice})

        if not re.search('name="security_code"', response.text):
            raise exception.InstagramAuthError('Something went wrong when try two step verification. Please report issue.', response.status_code)

        security_code = two_step_verificator.get_security_code()

        post_data = {
            'csrfmiddlewaretoken': cookies['csrftoken'],
            'verify': 'Verify Account',
            'security_code': security_code
        }

        # todo: it seems this method doesn't work perfectly, need to be fixed(response(cookie/session) doesn't look like what I am expecting)
        response = self.__req.post(url, headers=header, data=post_data)

        if response.status_code != self.HTTP_OK:
            raise exception.InstagramAuthError('Something went wrong when try two step verification and enter security code. Please report issue.', response.status_code)

        return response

    def login(self, force=False, two_step_verificator=True):
        if not self.__session_name and not self.__session_password:
            raise exception.InstagramError('User credentials not provided')

        if two_step_verificator == True:
            two_step_verificator = two_step_verification.ConsoleVerification()

        session_cache = cache.Cache.create('disk')
        session = session_cache.get(self.__session_name)

        if force or not self.is_logged_in(session):
            response = self.__req.get(endpoints.BASE_URL)
            if response.status_code != self.HTTP_OK:
                error_msg = 'Response code is: ' + str(response.status_code) + '. Body: ' + response.content + ' Something went wrong. Please report issue.'
                raise exception.InstagramError(error_msg, response.status_code)
            csrf_token = ''
            res = re.search(r'"csrf_token":"(.*?)"', response.text)
            if res and res.group(1):
                csrf_token = res.group(1)
            cookies = self.get_cookie(response)
            mid = cookies['mid']
            header = {
                'cookie': "ig_cb=1; csrftoken=" + csrf_token + "; mid=" + mid + ";",
                'referer': endpoints.BASE_URL + '/',
                'x-csrftoken': csrf_token,
                'x-CSRFToken': csrf_token,
                'user-agent': self.get_user_agent()
            }

            response = self.__req.post(endpoints.LOGIN_URL, headers=header, data={'username': self.__session_name, 'password': self.__session_password})
            json_body = json.loads(response.text)

            if response.status_code != self.HTTP_OK:
                if response.status_code == self.HTTP_BAD_REQUEST and 'message' in json_body and json_body['message'] == 'checkpoint_required' and two_step_verificator:
                    response = self.verify_two_step(response, cookies, two_step_verificator)
                elif isinstance(response.status_code, str) or (isinstance(response.status_code, int) and isinstance(response.content, str)):
                    error_msg = 'Response code is: ' + str(response.status_code) + '. Body: ' + response.content + ' Something went wrong. Please report issue.'
                    raise exception.InstagramError(error_msg, response.status_code)
                else:
                    raise exception.InstagramError('Something went wrong. Please report issue.', response.status_code)

            if not re.search('<html', response.text) and re.match('{.*}', response.text):
                json_body = json.loads(response.text)

            if 'authenticated' in json_body and not json_body['authenticated']:
                raise exception.InstagramError('User credentials are wrong.', response.status_code)

            cookies = self.get_cookie(response)
            cookies['mid'] = mid
            session_cache.set(self.__session_name, cookies)
            self.__user_session = cookies
        else:
            self.__user_session = session

        return self.generate_header(self.__user_session)

    def get_account(self, user_name):
        """
        get the account info by username
        :param user_name:
        :return:
        """
        url = endpoints.get_account_page_link(user_name)
        header = self.generate_header(self.__user_session)
        response = self.__req.get(url, headers=header)

        if response.status_code == self.HTTP_NOT_FOUND:
            raise exception.InstagramNotFoundError('Account with given username does not exist.')
        if response.status_code != self.HTTP_OK:
            error_msg = 'Response code is: ' + str(response.status_code) + '. Body: ' + response.content + ' Something went wrong. Please report issue.'
            raise exception.InstagramError(error_msg, response.status_code)

        data = self.get_shared_data(response.text)

        account_data = helper.get_from_dict(data, ['entry_data', 'ProfilePage', 0, 'graphql', 'user'])
        if not account_data:
            raise exception.InstagramNotFoundError('Account with this username does not exist')

        account = model.Account.create(account_data)
        return account

    def get_account_by_id(self, id):
        """
        get the account info by user_id
        :param id:
        :return:
        """
        username = self.get_username_by_id(id)
        return self.get_account(username)

    def get_username_by_id(self, id):
        """
        get user name from user_id
        :param id:
        :return:
        """
        url = endpoints.get_account_json_private_info_link_by_account_id(id)
        header = self.generate_header(self.__user_session)
        response = self.__req.get(url, headers=header)

        if response.status_code == self.HTTP_NOT_FOUND:
            raise exception.InstagramNotFoundError('Account with given username does not exist.')
        if response.status_code != self.HTTP_OK:
            error_msg = 'Response code is: ' + str(response.status_code) + '. Body: ' + response.content + ' Something went wrong. Please report issue.'
            raise exception.InstagramError(error_msg, response.status_code)

        data = json.loads(response.text)
        if not data:
            raise exception.InstagramError('Response is not JSON')

        if data['status'] != 'ok':
            raise exception.InstagramError('message' in data.keys() and data['message'] or 'Unknown error')

        return data['user']['username']

    def get_medias(self, username, count=20, max_id=''):
        """
        get medias by username
        :param username:
        :param count:
        :param max_id:
        :return:
        """
        account = self.get_account(username)
        return self.get_media_by_user_id(account.get_id(), count, max_id)

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
            # if you don't specify separators,the form of 'key:value' will have a space behind the ':',because the default separators is (', ', ': '), it will fail in making a request
            variables = json.dumps({
                'id': str(user_id),
                'first': count,
                'after': str(max_id)
            }, separators=(',', ':'))
            url = endpoints.get_account_media_url(variables)
            # instagram has removed rhx_gis token from page and x-gis-token in request header since 2019-05-21 am,but it's better to keep it here temporarily
            # header = self.generate_header(self.__user_session, self.get_rhx_gis())
            header = self.generate_header(self.__user_session)
            response = self.__req.get(url, headers=header)

            if response.status_code != self.HTTP_OK:
                error_msg = 'Response code is: ' + str(response.status_code) + '. Body: ' + response.content + ' Something went wrong. Please report issue.'
                raise exception.InstagramError(error_msg, response.status_code)

            media_json_data = json.loads(response.text)

            if not isinstance(media_json_data, dict):
                error_msg = 'Response code is: ' + str(response.status_code) + '. Body: ' + response.content + ' Something went wrong. Please report issue.'
                raise exception.InstagramError(error_msg, response.status_code)

            media_raw_data = media_json_data['data']['user']['edge_owner_to_timeline_media']['edges']

            if not media_raw_data:
                return medias

            for item in media_raw_data:
                if index == count:
                    return medias
                index += 1
                medias.append(model.Media.create(item['node']))
            max_id = media_json_data['data']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']
            has_next_page = media_json_data['data']['user']['edge_owner_to_timeline_media']['page_info']['has_next_page']
        return medias

    def get_media_by_url(self, media_url):
        """
        get a media obj by url
        :param media_url:
        :return:
        """
        if not re.match(r'^https?:/{2}\w.+$', media_url):
            raise exception.InstagramError('Malformed media url')

        response = self.__req.get(endpoints.get_media_url(media_url), headers=self.generate_header(self.__user_session))

        if response.status_code == self.HTTP_NOT_FOUND:
            raise exception.InstagramNotFoundError('Account with given username does not exist.')
        if response.status_code != self.HTTP_OK:
            error_msg = 'Response code is: ' + str(response.status_code) + '. Body: ' + response.content + ' Something went wrong. Please report issue.'
            raise exception.InstagramError(error_msg, response.status_code)

        media_json = json.loads(response.text)
        if not helper.get_from_dict(media_json, ['graphql', 'shortcode_media']):
            raise exception.InstagramError('Media with this code does not exist')

        return model.Media.create(media_json['graphql']['shortcode_media'])

    def get_media_by_code(self, media_code):
        """
        get media by media code
        :param media_code:
        :return:
        """
        url = endpoints.get_media_page_link(media_code)
        return self.get_media_by_url(url)

    def get_paginate_medias(self, username, max_id='', count=50):
        """
        get a single page medias, largest number of count is 50
        :param username:
        :param max_id:
        :param count:
        :return:
        """
        index = 0
        account = self.get_account(username)
        has_next_page = False
        medias = []

        to_return = {
            'medias': medias,
            'max_id': max_id,
            'has_next_page': has_next_page
        }

        if count > 50:
            count = 50

        variables = json.dumps({
            'id': str(account.get_id()),
            'first': count,
            'after': str(max_id)
        }, separators=(',', ':'))

        url = endpoints.get_account_media_url(variables)
        # instagram has removed rhx_gis token from page and x-gis-token in request header since 2019-05-21 am,but it's better to keep it here temporarily
        # header = self.generate_header(self.__user_session, self.get_rhx_gis())
        header = self.generate_header(self.__user_session)
        response = self.__req.get(url, headers=header)

        if response.status_code != self.HTTP_OK:
            error_msg = 'Response code is: ' + str(response.status_code) + '. Body: ' + response.content + ' Something went wrong. Please report issue.'
            raise exception.InstagramError(error_msg, response.status_code)

        media_json_data = json.loads(response.text)

        if not isinstance(media_json_data, dict):
            error_msg = 'Response code is: ' + str(response.status_code) + '. Body: ' + response.content + ' Something went wrong. Please report issue.'
            raise exception.InstagramError(error_msg, response.status_code)

        media_raw_data = media_json_data['data']['user']['edge_owner_to_timeline_media']['edges']

        if not media_raw_data:
            return to_return

        for media_dict in media_raw_data:
            if index == count:
                break
            index += 1
            medias.append(model.Media.create(media_dict['node']))

        max_id = media_json_data['data']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']
        has_next_page = media_json_data['data']['user']['edge_owner_to_timeline_media']['page_info']['has_next_page']

        to_return = {
            'medias': medias,
            'max_id': max_id,
            'has_next_page': has_next_page
        }

        return to_return

    def get_medias_by_tag(self, tag, count=20, max_id='', min_timestamp=None):
        """
        get media by specified tag, precise matching
        :param tag:
        :param count:
        :param max_id:
        :param min_timestamp:
        :return:
        """
        index = 0
        medias = []
        media_ids = []
        has_next_page = True
        while index < count and has_next_page:
            response = self.__req.get(endpoints.get_medias_json_by_tag_link(tag, max_id))

            if response.status_code != self.HTTP_OK:
                error_msg = 'Response code is: ' + str(response.status_code) + '. Body: ' + response.content + ' Something went wrong. Please report issue.'
                raise exception.InstagramError(error_msg, response.status_code)

            cookies = self.get_cookie(response)
            try:
                arr = json.loads(response.text)
            except json.decoder.JSONDecodeError:
                return exception.InstagramError('Response decoding failed. Returned data corrupted or this library outdated. Please report issue')
            if not helper.get_from_dict(arr, ['graphql', 'hashtag', 'edge_hashtag_to_media', 'count']):
                return {}

            nodes = helper.get_from_dict(arr, ['graphql', 'hashtag', 'edge_hashtag_to_media', 'edges'])
            for media_dict in nodes:
                if index == count:
                    return medias
                media = model.Media.create(media_dict['node'])
                if media.get_id() in media_ids:
                    return medias
                if min_timestamp and media.get_created_time() < min_timestamp:
                    return medias
                media_ids.append(media.get_id())
                medias.append(media)
                index += 1

            if not nodes:
                return medias

            max_id = helper.get_from_dict(arr, ['graphql', 'hashtag', 'edge_hashtag_to_media', 'page_info', 'end_cursor'])
            has_next_page = helper.get_from_dict(arr, ['graphql', 'hashtag', 'edge_hashtag_to_media', 'page_info', 'has_next_page'])

        return medias

    def get_paginate_medias_by_tag(self, tag, max_id=''):
        """
        get a single page of medias by tag
        :param tag:
        :param max_id:
        :return:
        """
        has_next_page = True
        medias = []

        to_return = {
            'medias': medias,
            'max_id': max_id,
            'count': 0,
            'has_next_page': has_next_page
        }
        response = self.__req.get(endpoints.get_medias_json_by_tag_link(tag, max_id))
        if response.status_code != self.HTTP_OK:
            error_msg = 'Response code is: ' + str(response.status_code) + '. Body: ' + response.text + ' Something went wrong. Please report issue.'
            raise exception.InstagramError(error_msg, response.status_code)

        cookies = self.get_cookie(response)
        try:
            arr = json.loads(response.text)
        except json.decoder.JSONDecodeError:
            return exception.InstagramError(
                'Response decoding failed. Returned data corrupted or this library outdated. Please report issue')
        if not helper.get_from_dict(arr, ['graphql', 'hashtag', 'edge_hashtag_to_media', 'count']):
            return to_return

        if not helper.get_from_dict(arr, ['graphql', 'hashtag', 'edge_hashtag_to_media', 'count']):
            return to_return

        nodes = helper.get_from_dict(arr, ['graphql', 'hashtag', 'edge_hashtag_to_media', 'edges'])

        if not nodes:
            return to_return

        for media_dict in nodes:
            medias.append(model.Media.create(media_dict['node']))

        max_id = helper.get_from_dict(arr, ['graphql', 'hashtag', 'edge_hashtag_to_media', 'page_info', 'end_cursor'])
        has_next_page = helper.get_from_dict(arr, ['graphql', 'hashtag', 'edge_hashtag_to_media', 'page_info', 'has_next_page'])
        count = helper.get_from_dict(arr, ['graphql', 'hashtag', 'edge_hashtag_to_media', 'count'])

        to_return = {
            'medias': medias,
            'max_id': max_id,
            'count': count,
            'has_next_page': has_next_page
        }
        return to_return

    def get_current_top_medias_by_tag_name(self, tag):
        """
        get the top posts of tag
        :param tag:
        :return:
        """
        response = self.__req.get(endpoints.get_medias_json_by_tag_link(tag))
        if response.status_code == self.HTTP_NOT_FOUND:
            raise exception.InstagramNotFoundError('Account with given username does not exist.')
        if response.status_code != self.HTTP_OK:
            error_msg = 'Response code is: ' + str(response.status_code) + '. Body: ' + response.content + ' Something went wrong. Please report issue.'
            raise exception.InstagramError(error_msg, response.status_code)

        cookies = self.get_cookie(response)
        json_body = json.loads(response.text)
        medias = []
        nodes = helper.get_from_dict(json_body, ['graphql', 'hashtag', 'edge_hashtag_to_top_posts', 'edges'])
        if not nodes:
            return medias
        for media_dict in nodes:
            medias.append(model.Media.create(media_dict['node']))

        return medias


    def get_cookie(self, response):
        """
        get the cookie from a response
        :param response:
        :return:
        """
        cookies = response.cookies.get_dict()
        if 'csrftoken' in cookies:
            self.__user_session['csrftoken'] = cookies['csrftoken']
        return cookies

    def get_media_comments_by_code(self, code, count=10, max_id=''):
        """
        get some comments from media by media_code
        :param code:
        :param count:
        :param max_id:
        :return:
        """
        comments = []
        index = 0
        has_previous = True

        while has_previous and index < count:
            if (count - index) > self.MAX_COMMENTS_PER_REQUEST:
                number_of_comment_to_retrieve = self.MAX_COMMENTS_PER_REQUEST
            else:
                number_of_comment_to_retrieve = count - index

            variables = json.dumps({
                'shortcode': str(code),
                'first': str(number_of_comment_to_retrieve),
                'after': str(max_id)
            }, separators=(',', ':'))

            url = endpoints.get_comments_before_comment_id_by_code(variables)
            header = self.generate_header(self.__user_session)
            response = self.__req.get(url, headers=header)

            if response.status_code != self.HTTP_OK:
                error_msg = 'Response code is: ' + str(response.status_code) + '. Body: ' + response.content + ' Something went wrong. Please report issue.'
                raise exception.InstagramError(error_msg, response.status_code)

            json_data = json.loads(response.text)
            nodes = json_data['data']['shortcode_media']['edge_media_to_comment']['edges']
            for comment_dict in nodes:
                if count == index:
                    return comments
                comments.append(model.Comment.create(comment_dict['node']))
                index += 1

            has_previous = json_data['data']['shortcode_media']['edge_media_to_comment']['page_info']['has_next_page']
            number_of_comments = json_data['data']['shortcode_media']['edge_media_to_comment']['count']
            if count > number_of_comments:
                count = number_of_comments

            if len(nodes) == 0:
                return comments

            max_id = json_data['data']['shortcode_media']['edge_media_to_comment']['page_info']['end_cursor']

        return comments

    def get_media_likes_by_code(self, code, count=20, max_id=''):
        """
        get who likes you from a media by media code
        :param code:
        :param count:
        :param max_id:
        :return:
        """
        remain = count
        number_of_likes_to_retreive = 0
        likes = []
        index = 0
        has_previous = True

        while has_previous and index < count:
            if remain > self.MAX_LIKES_PER_REQUEST:
                number_of_likes_to_retreive = self.MAX_LIKES_PER_REQUEST
                remain -= self.MAX_LIKES_PER_REQUEST
                index += self.MAX_LIKES_PER_REQUEST
            else:
                number_of_likes_to_retreive = remain
                index += remain
                remain = 0

            variables = json.dumps({
                'shortcode': str(code),
                'first': str(number_of_likes_to_retreive),
                'after': str(max_id)
            }, separators=(',', ':'))

            response = self.__req.get(endpoints.get_last_likes_by_code(variables), headers=self.generate_header(self.__user_session))
            if response.status_code != self.HTTP_OK:
                error_msg = 'Response code is: ' + str(response.status_code) + '. Body: ' + response.content + ' Something went wrong. Please report issue.'
                raise exception.InstagramError(error_msg, response.status_code)

            cookies = self.get_cookie(response)
            json_body = json.loads(response.text)
            nodes = helper.get_from_dict(json_body, ['data', 'shortcode_media', 'edge_liked_by', 'edges'])

            if not nodes:
                return likes

            for like_dict in nodes:
                likes.append(model.Like.create(like_dict['node']))

            has_previous = helper.get_from_dict(json_body, ['data', 'shortcode_media', 'edge_liked_by', 'page_info', 'has_next_page'])
            number_of_likes = helper.get_from_dict(json_body, ['data', 'shortcode_media', 'edge_liked_by', 'count'])
            max_id = helper.get_from_dict(json_body, ['data', 'shortcode_media', 'edge_liked_by', 'page_info', 'end_cursor'])

            if count > number_of_likes:
                count = number_of_likes

        return likes


    def get_media_comments_by_media_id(self, media_id, count=10, max_id=''):
        code = model.Media.get_code_from_id(media_id)
        return self.get_media_comments_by_code(code, count, max_id)

    def get_medias_by_location_id(self, facebook_location_id, count=24, max_id=''):
        """
        get medias by location id
        :param facebook_location_id:
        :param count:
        :param max_id:
        :return:
        """
        index = 0
        medias = []
        has_next_page = True

        while index < count and has_next_page:
            response = self.__req.get(endpoints.get_medias_json_by_location_id_link(facebook_location_id, max_id), headers=self.generate_header(self.__user_session))
            if response.status_code != self.HTTP_OK:
                error_msg = 'Response code is: ' + str(response.status_code) + '. Body: ' + response.content + ' Something went wrong. Please report issue.'
                raise exception.InstagramError(error_msg, response.status_code)
            cookies = self.get_cookie(response)
            json_body = json.loads(response.text)
            nodes = helper.get_from_dict(json_body, ['graphql', 'location', 'edge_location_to_media', 'edges'])
            if not nodes:
                return medias
            for media_dict in nodes:
                if index == count:
                    return medias
                medias.append(model.Media.create(media_dict['node']))
                index += 1
            has_next_page = json_body['graphql']['location']['edge_location_to_media']['page_info']['has_next_page']
            max_id = json_body['graphql']['location']['edge_location_to_media']['page_info']['end_cursor']

        return medias

    def get_current_top_medias_by_location_id(self, facebook_location_id):
        """
        get the top medias about location id
        :param facebook_location_id:
        :return:
        """
        response = self.__req.get(endpoints.get_medias_json_by_location_id_link(facebook_location_id), headers=self.generate_header(self.__user_session))
        if response.status_code == self.HTTP_NOT_FOUND:
            raise exception.InstagramNotFoundError("Location with this id doesn't exist.")
        if response.status_code != self.HTTP_OK:
            error_msg = 'Response code is: ' + str(response.status_code) + '. Body: ' + response.content + ' Something went wrong. Please report issue.'
            raise exception.InstagramError(error_msg, response.status_code)

        cookies = self.get_cookie(response)
        json_body = json.loads(response.text)
        edges = helper.get_from_dict(json_body, ['graphql', 'location', 'edge_location_to_top_posts', 'edges'])

        medias = []
        if not edges:
            return medias
        for media_dict in edges:
            medias.append(model.Media.create(media_dict['node']))

        return medias

    def get_medias_from_feed(self, username, count=12):
        """
        get medias from a user account page
        :param username:
        :param count:
        :return:
        """
        medias = []
        index = 0
        response = self.__req.get(endpoints.get_account_json_link(username), headers=self.generate_header(self.__user_session))
        if response.status_code == self.HTTP_NOT_FOUND:
            raise exception.InstagramNotFoundError("Account with given username does not exist.")
        if response.status_code != self.HTTP_OK:
            error_msg = 'Response code is: ' + str(response.status_code) + '. Body: ' + response.content + ' Something went wrong. Please report issue.'
            raise exception.InstagramError(error_msg, response.status_code)

        cookies = self.get_cookie(response)
        json_body = json.loads(response.text)
        if not helper.get_from_dict(json_body, ['graphql', 'user']):
            raise exception.InstagramNotFoundError("Account with given username does not exist.")

        nodes = helper.get_from_dict(json_body, ['graphql', 'user', 'edge_owner_to_timeline_media', 'edges'])
        if not nodes:
            return medias

        for media_dict in nodes:
            if index == count:
                return medias
            medias.append(model.Media.create(media_dict['node']))
            index += 1

        return medias

    def get_stories(self, reel_ids=None):
        """
        get stories
        :param reel_ids:
        :return:
        """
        variables = {
            'precomposed_overlay': False,
            'reel_ids': []
        }
        if not reel_ids:
            response = self.__req.get(endpoints.get_user_stories_link(json.dumps({})), headers=self.generate_header(self.__user_session))
            if response.status_code != self.HTTP_OK:
                error_msg = 'Response code is: ' + str(response.status_code) + '. Body: ' + response.content + ' Something went wrong. Please report issue.'
                raise exception.InstagramError(error_msg, response.status_code)

            json_body = json.loads(response.text)
            edges = helper.get_from_dict(json_body, ['data', 'user', 'feed_reels_tray', 'edge_reels_tray_to_reel', 'edges'])

            if not edges:
                return []

            for edge in edges:
                variables['reel_ids'].append(edge['node']['id'])
        else:
            variables['reel_ids'] = reel_ids

        variables = json.dumps(variables, separators=(',', ':'))
        response = self.__req.get(endpoints.get_stories_link(variables), headers=self.generate_header(self.__user_session))
        if response.status_code != self.HTTP_OK:
            error_msg = 'Response code is: ' + str(response.status_code) + '. Body: ' + response.content + ' Something went wrong. Please report issue.'
            raise exception.InstagramError(error_msg, response.status_code)

        json_body = json.loads(response.text)
        reel_medias = helper.get_from_dict(json_body, ['data', 'reels_media'])
        if not reel_medias:
            return []

        stories = []
        for reel_media in reel_medias:
            user_stories = model.UserStories.create({})
            user_stories.set_owner(model.Account.create(reel_media['user']))
            for item in reel_media['items']:
                user_stories.add_story(model.Story.create(item))
            stories.append(user_stories)

        return stories

    def get_followers(self, account_id, count=20, page_size=20, delayed=True):
        """
        get who are following the account, need to login
        :param account_id:
        :param count:
        :param page_size:
        :param delayed:
        :return:
        """
        # there is a 30 mins duration limited if delayed=True,but I don't know why,so I replace it in other way

        sec = 0
        index = 0
        accounts = []
        end_cursor = ''
        break_out_side = False

        if sec > self.paging_time_limit_sec:
            return accounts

        if count < page_size:
            raise exception.InstagramError('Count must be greater than or equal to page size.')

        while True:
            url = endpoints.get_followers_json_link(account_id, page_size, end_cursor)
            response = self.__req.get(url, headers=self.generate_header(self.__user_session))

            if response.status_code != self.HTTP_OK:
                error_msg = 'Response code is: ' + str(response.status_code) + '. Body: ' + response.content + ' Something went wrong. Please report issue.'
                raise exception.InstagramError(error_msg, response.status_code)

            json_response = json.loads(response.text)
            followed_by = helper.get_from_dict(json_response, ['data', 'user', 'edge_followed_by'])
            if followed_by and followed_by['count'] == 0:
                return accounts

            edges_dict = followed_by['edges']
            if len(edges_dict) == 0:
                raise exception.InstagramError('Failed to get followers of account id ' + account_id + '. The account is private.', self.HTTP_FORBIDDEN)

            for edge in edges_dict:
                accounts.append(edge['node'])
                index += 1
                if index >= count:
                    break_out_side = True
                    break

            if break_out_side:
                break

            page_info = followed_by['page_info']
            if page_info['has_next_page']:
                end_cursor = page_info['end_cursor']
            else:
                break

            if delayed:
                micro_sec = random.randint(self.paging_delay_minimum_microsec, self.paging_delay_maximum_microsec) / (1000 * 1000)
                time.sleep(micro_sec)
                sec += micro_sec

        return accounts

    def get_following(self, account_id, count=20, page_size=20, delayed=True):
        """
        get what account is following, need to login
        :param account_id:
        :param count:
        :param page_size:
        :param delayed:
        :return:
        """
        # there is a 30 mins duration limited if delayed=True,but I don't know why,so I replace it in other way
        sec = 0
        index = 0
        accounts = []
        end_cursor = ''
        break_out_side = False

        if sec > self.paging_time_limit_sec:
            return accounts

        if count < page_size:
            raise exception.InstagramError('Count must be greater than or equal to page size.')

        self.__user_session['target'] = ''
        while True:
            url = endpoints.get_following_json_link(account_id, page_size, end_cursor)
            response = self.__req.get(url, headers=self.generate_header(self.__user_session))

            if response.status_code != self.HTTP_OK:
                error_msg = 'Response code is: ' + str(response.status_code) + '. Body: ' + response.content + ' Something went wrong. Please report issue.'
                raise exception.InstagramError(error_msg, response.status_code)

            json_response = json.loads(response.text)
            followed = helper.get_from_dict(json_response, ['data', 'user', 'edge_follow'])
            if followed and followed['count'] == 0:
                return accounts

            edges_dict = followed['edges']
            if len(edges_dict) == 0:
                raise exception.InstagramError('Failed to get followers of account id ' + account_id + '. The account is private.', self.HTTP_FORBIDDEN)

            for edge in edges_dict:
                accounts.append(edge['node'])
                index += 1
                if index >= count:
                    break_out_side = True
                    break

            if break_out_side:
                break

            page_info = followed['page_info']
            if page_info['has_next_page']:
                end_cursor = page_info['end_cursor']
            else:
                break

            if delayed:
                micro_sec = random.randint(self.paging_delay_minimum_microsec, self.paging_delay_maximum_microsec) / (1000 * 1000)
                time.sleep(micro_sec)
                sec += micro_sec

        return accounts

    def get_location_by_id(self, facebook_location_id):
        """
        get location by facebook location_id
        :param facebook_location_id:
        :return:
        """
        response = self.__req.get(endpoints.get_medias_json_by_location_id_link(facebook_location_id), headers=self.generate_header(self.__user_session))
        if response.status_code == self.HTTP_NOT_FOUND:
            raise exception.InstagramNotFoundError('Account with given username does not exist.')
        if response.status_code != self.HTTP_OK:
            error_msg = 'Response code is: ' + str(response.status_code) + '. Body: ' + response.content + ' Something went wrong. Please report issue.'
            raise exception.InstagramError(error_msg, response.status_code)
        cookies = self.get_cookie(response)

        json_body = json.loads(response.text)
        return model.Location.create(json_body['graphql']['location'])

    def search_accounts_by_username(self, username):
        """
        search an account by username, will match username or fullname
        :param username:
        :return:
        """
        response = self.__req.get(endpoints.get_general_search_json_link(username), headers=self.generate_header(self.__user_session))
        if response.status_code == self.HTTP_NOT_FOUND:
            raise exception.InstagramNotFoundError('Account with given username does not exist.')
        if response.status_code != self.HTTP_OK:
            error_msg = 'Response code is: ' + str(response.status_code) + '. Body: ' + response.content + ' Something went wrong. Please report issue.'
            raise exception.InstagramError(error_msg, response.status_code)

        json_body = json.loads(response.text)
        accounts = []

        if json_body['status'] != 'ok':
            raise exception.InstagramError('Response status is not ok. Something went wrong. Please report issue.')

        users = helper.get_from_dict(json_body, ['users'])
        if not users:
            return accounts

        for account in users:
            accounts.append(model.Account.create(account['user']))

        return accounts

    def search_tags_by_tag_name(self, tag):
        """
        search a tag and return the relevant item
        :param tag:
        :return:
        """
        response = self.__req.get(endpoints.get_general_search_json_link(tag), headers=self.generate_header(self.__user_session))
        if response.status_code == self.HTTP_NOT_FOUND:
            raise exception.InstagramNotFoundError('Account with given username does not exist.')
        if response.status_code != self.HTTP_OK:
            error_msg = 'Response code is: ' + str(response.status_code) + '. Body: ' + response.content + ' Something went wrong. Please report issue.'
            raise exception.InstagramError(error_msg, response.status_code)

        json_body = json.loads(response.text)
        tags = []

        if json_body['status'] != 'ok':
            raise exception.InstagramError('Response status is not ok. Something went wrong. Please report issue.')

        json_body_tags = helper.get_from_dict(json_body, ['hashtags'])
        if not json_body_tags:
            return tags

        for tag in json_body_tags:
            tags.append(model.Tag.create(tag['hashtag']))

        return tags

    def like(self, media_id):
        """
        like a post
        :param media_id:
        :return:
        """
        media_id = isinstance(media_id, model.Media) and media_id.get_id() or media_id
        response = self.__req.post(endpoints.get_like_url(media_id), headers=self.generate_header(self.__user_session))

        if response.status_code != self.HTTP_OK:
            error_msg = 'Response code is: ' + str(response.status_code) + '. Body: ' + response.content + ' Something went wrong. Please report issue.'
            raise exception.InstagramError(error_msg, response.status_code)

        json_body = json.loads(response.text)

        if json_body['status'] != 'ok':
            raise exception.InstagramError('Like operation fail. Or something went wrong. Please report issue.')

    def unlike(self, media_id):
        """
        unlike a post
        :param media_id:
        :return:
        """
        media_id = isinstance(media_id, model.Media) and media_id.get_id() or media_id
        response = self.__req.post(endpoints.get_unlike_url(media_id), headers=self.generate_header(self.__user_session))

        if response.status_code != self.HTTP_OK:
            error_msg = 'Response code is: ' + str(response.status_code) + '. Body: ' + response.content + ' Something went wrong. Please report issue.'
            raise exception.InstagramError(error_msg, response.status_code)

        json_body = json.loads(response.text)

        if json_body['status'] != 'ok':
            raise exception.InstagramError('Like operation fail. Or something went wrong. Please report issue.')

    def add_comment(self, media_id, text, replied_to_comment_id=''):
        """
        add a comment to post
        :param media_id:
        :param text:
        :param replied_to_comment_id:
        :return:
        """
        media_id = isinstance(media_id, model.Media) and media_id.get_id() or media_id
        replied_to_comment_id = isinstance(replied_to_comment_id, model.Comment) and replied_to_comment_id.get_id() or replied_to_comment_id

        data = {'comment_text': text, 'replied_to_comment_id': replied_to_comment_id}
        response = self.__req.post(endpoints.get_add_comment_url(media_id), data=data, headers=self.generate_header(self.__user_session))

        if response.status_code != self.HTTP_OK:
            error_msg = 'Response code is: ' + str(response.status_code) + '. Body: ' + response.content + ' Something went wrong. Please report issue.'
            raise exception.InstagramError(error_msg, response.status_code)

        json_body = json.loads(response.text)

        if json_body['status'] != 'ok':
            raise exception.InstagramError('Comment operation fail. Or something went wrong. Please report issue.')

        return model.Comment.create(json_body)

    def delete_comment(self, media_id, comment_id):
        """
        delete a comment
        :param media_id:
        :param comment_id:
        :return:
        """
        media_id = isinstance(media_id, model.Media) and media_id.get_id() or media_id
        comment_id = isinstance(comment_id, model.Comment) and comment_id.get_id() or comment_id

        response = self.__req.post(endpoints.get_delete_comment_url(media_id, comment_id), headers=self.generate_header(self.__user_session))

        if response.status_code != self.HTTP_OK:
            error_msg = 'Response code is: ' + str(response.status_code) + '. Body: ' + response.content + ' Something went wrong. Please report issue.'
            raise exception.InstagramError(error_msg, response.status_code)

        json_body = json.loads(response.text)

        if json_body['status'] != 'ok':
            raise exception.InstagramError('Delete comment operation fail. Or something went wrong. Please report issue.')
