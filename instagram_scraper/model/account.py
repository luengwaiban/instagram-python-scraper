# -*- coding:utf-8 -*-

from instagram_scraper.model.base_model import BaseModel
from instagram_scraper import model


class Account(BaseModel):

    def __init__(self, prop=None):
        self.account_uesrname_id = ''
        self._username = ''
        self._full_name = ''
        self._profile_pic_url = ''
        self._profile_pic_url_hd = ''
        self._biography = ''
        self._external_url = ''
        self._follows_count = 0
        self._followed_by_count = 0
        self._media_count = 0
        self._is_private = False
        self._is_verified = False
        self._is_loaded = False
        self._medias = {}
        self._blocked_by_viewer = False
        self._country_block = False
        self._followed_by_Viewer = False
        self._follows_viewer = False
        self._has_channel = False
        self._has_blocked_viewer = False
        self._highlight_reel_count = 0
        self._has_requested_viewer = False
        self._is_business_account = False
        self._is_joined_recently = False
        self._business_category_name = ''
        self._business_email = ''
        self._business_phone_number = ''
        self._business_address_json = '{}'
        self._requested_by_viewer = False
        self._connected_fb_page = ''
        super(Account, self).__init__(prop)

    def get_id(self):
        return self._id

    def is_loaded(self):
        return self._is_loaded

    def get_username(self):
        return self._username

    def get_full_name(self):
        return self._full_name

    def get_profile_pic_url(self):
        return self._profile_pic_url

    def get_profile_pic_url_hd(self):
        return self._profile_pic_url_hd and self._profile_pic_url_hd or self._profile_pic_url

    def get_biography(self):
        return self._biography

    def get_external_url(self):
        return self._external_url

    def get_follows_count(self):
        return self._follows_count

    def get_followed_by_count(self):
        return self._followed_by_count

    def get_media_count(self):
        return self._media_count

    def is_private(self):
        return self._is_private

    def is_verified(self):
        return self._is_verified

    def get_medias(self):
        return self._medias

    def is_blocked_by_viewer(self):
        return self._blocked_by_viewer

    def is_country_block(self):
        return self._country_block

    def is_followed_by_viewer(self):
        return self._followed_by_Viewer

    def is_follows_viewer(self):
        return self._follows_viewer

    def is_has_channel(self):
        return self._has_channel

    def is_has_blocked_viewer(self):
        return self._has_blocked_viewer

    def get_highlight_reel_count(self):
        return self._highlight_reel_count

    def is_has_requested_viewer(self):
        return self._has_requested_viewer

    def is_business_account(self):
        return self._is_business_account

    def is_joined_recently(self):
        return self._is_joined_recently

    def get_business_category_name(self):
        return self._business_category_name

    def get_business_email(self):
        return self._business_email

    def get_business_phone_number(self):
        return self._business_phone_number

    def get_business_address_json(self):
        return self._business_address_json

    def is_requested_by_viewer(self):
        return self._requested_by_viewer

    def get_connected_fb_page(self):
        return self._connected_fb_page

    def add_media(self, media):
        self._medias.update(media)
        return self

    def _init_properties_custom(self, value, prop, dictionary):
        # print(prop, value)
        if prop == 'id':
            self._id = value
        elif prop == 'pk':
            self._id = value
        elif prop == 'username':
            self._username = value
        elif prop == 'full_name':
            self._full_name = value
        elif prop == 'profile_pic_url':
            self._profile_pic_url = value
        elif prop == 'profile_pic_url_hd':
            self._profile_pic_url_hd = value
        elif prop == 'biography':
            self._biography = value
        elif prop == 'external_url':
            self._external_url = value
        elif prop == 'edge_follow':
            self._follows_count = dictionary[prop]['count'] and dictionary[prop]['count'] or 0
        elif prop == 'edge_followed_by':
            self._followed_by_count = dictionary[prop]['count'] and int(dictionary[prop]['count']) or 0
        elif prop == 'follower_count':
            self._followed_by_count = value
        elif prop == 'edge_owner_to_timeline_media':
            self._init_media(dictionary[prop])
        elif prop == 'is_private':
            self._is_private = bool(value)
        elif prop == 'is_verified':
            self._is_verified = bool(value)
        elif prop == 'blocked_by_viewer':
            self._blocked_by_viewer = bool(value)
        elif prop == 'country_block':
            self._country_block = bool(value)
        elif prop == 'followed_by_viewer':
            self._followed_by_viewer = value
        elif prop == 'follows_viewer':
            self._follows_viewer = value
        elif prop == 'has_channel':
            self._has_channel = bool(value)
        elif prop == 'has_blocked_viewer':
            self._has_blocked_viewer = bool(value)
        elif prop == 'highlight_reel_count':
            self._highlight_reel_count = int(value)
        elif prop == 'has_requested_viewer':
            self._has_requested_viewer = bool(value)
        elif prop == 'is_business_account':
            self._is_business_account = bool(value)
        elif prop == 'is_joined_recently':
            self._is_joined_recently = bool(value)
        elif prop == 'business_category_name':
            self._business_category_name = value and value or ''
        elif prop == 'business_email':
            self._business_email = value
        elif prop == 'business_phone_number':
            self._business_phone_number = value
        elif prop == 'business_address_json':
            self._business_address_json = value
        elif prop == 'requested_by_viewer':
            self._requested_by_viewer = bool(value)
        elif prop == 'connected_fb_page':
            self._connected_fb_page = value and value or ''

    def _init_media(self, dictionary):
        self._media_count = dictionary['count'] and dictionary['count'] or 0
        if not self._media_count or 'edges' in dictionary.keys() or not isinstance(dictionary['edge'], dict):
            return

        nodes = dictionary['edges']
        for media_dictionary in nodes:
            media = model.Media.create(media_dictionary['node'])
            if isinstance(media, model.Media):
                self.add_media(media)
