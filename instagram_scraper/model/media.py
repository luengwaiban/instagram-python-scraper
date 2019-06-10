# -*- coding:utf-8 -*-

from instagram_scraper.model.base_model import BaseModel
from urllib.parse import urlparse
from instagram_scraper import endpoints, model


class Media(BaseModel):

    TYPE_IMAGE = 'image'
    TYPE_VIDEO = 'video'
    TYPE_SIDECAR = 'sidecar'
    TYPE_CAROUSEL = 'carousel'

    def __init__(self, props=None):
        self._id = ''
        self._short_code = ''
        self._created_time = 0
        self._type = ''
        self._link = ''
        self._height = 0
        self._width = 0
        self._image_low_resolution_url = ''
        self._image_thumbnail_url = ''
        self._image_standard_resolution_url = ''
        self._image_high_resolution_url = ''
        self._square_images = []
        self._carousel_media = []
        self._caption = ''
        self._is_caption_edited = False
        self._is_ad = False
        self._video_low_resolution_url = ''
        self._video_standard_resolution_url = ''
        self._video_low_bandwidth_url = ''
        self._video_views = 0
        self._video_url = ''
        # account object
        self._owner = None
        self._owner_id = 0
        self._likes_count = 0
        self._location_id = 0
        self._location_name = ''
        self._comments_count = 0
        self._comments = []
        self._has_more_comments = False
        self._comments_next_page = ''
        self._sidecar_medias = []
        self._location_slug = ''
        self._title = ''
        super(Media, self).__init__(props)

    @staticmethod
    def get_id_from_code(code):
        alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_'
        id = 0
        for i in range(len(code)):
            c = code[i]
            id = id * 64 + alphabet.index(c)
        return id

    # todo: translate the remaining methods

    @staticmethod
    def get_code_from_id(id):
        parts = id.split('_')
        id = parts[0]
        alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_'
        code = ''
        while id > 0:
            remainder = id % 64
            id = (id - remainder) / 64
            code = alphabet[remainder] + code
        return code

    @staticmethod
    def get_link_from_id(id):
        code = Media.get_code_from_id(id)
        return endpoints.get_media_page_link(code)

    def get_id(self):
        return self._id

    def get_short_code(self):
        return self._short_code

    def get_created_time(self):
        return self._created_time

    def get_type(self):
        return self._type

    def get_link(self):
        return self._link

    def get_image_low_resolution_url(self):
        return self._image_low_resolution_url

    def get_image_thumbnail_url(self):
        return self._image_thumbnail_url

    def get_image_standard_resolution_url(self):
        return self._image_standard_resolution_url

    def get_image_high_resolution_url(self):
        return self._image_high_resolution_url

    def get_square_images(self):
        return self._square_images

    def get_carousel_media(self):
        return self._carousel_media

    def get_caption(self):
        return self._caption

    def is_caption_edited(self):
        return self._is_caption_edited

    def is_ad(self):
        return self._is_ad

    def get_video_low_resolution_url(self):
        return self._video_low_resolution_url

    def get_video_standard_resolution_url(self):
        return self._video_standard_resolution_url

    def get_video_low_bandwidth_url(self):
        return self._video_standard_resolution_url

    def get_video_views(self):
        return self._video_views

    def get_height(self):
        return self._height

    def get_width(self):
        return self._width

    def get_video_url(self):
        return self._video_url

    def get_owner_id(self):
        return self._owner_id

    def get_likes_count(self):
        return self._likes_count

    def get_location_id(self):
        return self._location_id

    def get_location_name(self):
        return self._location_name

    def get_comments_count(self):
        return self._comments_count

    def get_comments(self):
        """
        :return: comments list
        """
        return self._comments

    def has_more_comments(self):
        return self._has_more_comments

    def get_comments_next_page(self):
        return self._comments_next_page

    def get_sidecar_medias(self):
        """
        :return: sidecar media list
        """
        return self._sidecar_medias

    def get_location_slug(self):
        return self._location_slug

    def _init_properties_custom(self, value, prop, dictionary):
        if prop == 'id':
            self._id = value
        elif prop == 'type':
            self._type = value
        elif prop == 'created_time':
            self._created_time = int(value)
        elif prop == 'code':
            self._short_code = value
            self._link = endpoints.get_media_page_link(self._short_code)
        elif prop == 'link':
            self._link = value
        elif prop == 'comments':
            self._comments_count = dictionary[prop]['count']
        elif prop == 'likes':
            self._likes_count = dictionary[prop]['count']
        elif prop == 'display_resources':
            for media in value:
                if media['config_width'] == 640:
                    self._image_thumbnail_url = media['src']
                elif media['config_width'] == 750:
                    self._image_low_resolution_url = media['src']
                elif media['config_width'] == 1080:
                    self._image_standard_resolution_url = media['src']
        elif prop == 'thumbnail_resources':
            square_images_url = []
            for square_image in value:
                square_images_url.append(square_image['src'])
            self._square_images = square_images_url
        elif prop == 'display_url':
            self._image_high_resolution_url = value
        elif prop == 'display_src':
            self._image_high_resolution_url = value
            if hasattr(self, '_type'):
                self._type = self.TYPE_IMAGE
        elif prop == 'thumbnail_src':
            self._image_thumbnail_url = value
        elif prop == 'carousel_media':
            self._type = self.TYPE_CAROUSEL
            self._carousel_media = []
            for carousel_dict in dictionary["carousel_media"]:
                Media.__set_carousel_media(dictionary, carousel_dict, self)
        elif prop == 'caption':
            self._caption = dictionary[prop]
        elif prop == 'video_views':
            self._video_views = value
            self._type = self.TYPE_VIDEO
        elif prop == 'videos':
            self._video_low_resolution_url = dictionary[prop]['low_resolution']['url']
            self._video_standard_resolution_url = dictionary[prop]['standard_resolution']['url']
            self._video_low_bandwidth_url = dictionary[prop]['low_bandwidth']['url']
        elif prop == 'video_resources':
            for video in value:
                if video['profile'] == 'MAIN':
                    self._video_standard_resolution_url = video['src']
                elif video['profile'] == 'BASELINE':
                    self._video_low_resolution_url = video['src']
                    self._video_low_bandwidth_url = video['src']
        elif prop == 'location':
            self._location_id = dictionary[prop] and dictionary[prop]['id'] or self._location_id
            self._location_name = dictionary[prop] and dictionary[prop] or self._location_name
            self._location_slug = dictionary[prop] and dictionary[prop] or self._location_slug
        elif prop == 'user':
            self._owner = model.Account.create(dictionary[prop])
        elif prop == 'is_video':
            if bool(value):
                self._type = self.TYPE_VIDEO
        elif prop == 'video_url':
            self._video_standard_resolution_url = value
            self._video_url = value
        elif prop == 'video_duration':
            self._video_duration = value
        elif prop == 'video_view_count':
            self._video_views = value
        elif prop == 'caption_is_edited':
            self._is_caption_edited = value
        elif prop == 'is_ad':
            self._is_ad = value
        elif prop == 'taken_at_timestamp':
            self._created_time = value
        elif prop == 'shortcode':
            self._short_code = value
            self._link = endpoints.get_media_page_link(self._short_code)
        elif prop == 'dimensions':
            self._height = value['height']
            self._width = value['width']
        elif prop == 'title':
            self._title = value
        elif prop == 'edge_media_to_comment' or prop == 'edge_media_to_parent_comment':
            if 'count' in dictionary[prop].keys():
                self._comments_count = int(dictionary[prop]['count'])
            if 'edges' in dictionary[prop].keys() and isinstance(dictionary[prop]['edges'], list):
                for comment_data in dictionary[prop]['edges']:
                    self._comments.append(model.Comment.create(comment_data['node']))
            if 'page_info' in dictionary[prop].keys() and 'has_next_page' in dictionary[prop]['page_info'].keys():
                self._has_more_comments = bool(dictionary[prop]['page_info']['has_next_page'])
            if 'page_info' in dictionary[prop].keys() and 'end_cursor' in dictionary[prop]['page_info'].keys():
                self._comments_next_page = dictionary[prop]['page_info']['end_cursor']
        elif prop == 'edge_media_preview_like':
            self._likes_count = dictionary[prop]['count']
        elif prop == 'edge_liked_by':
            self._likes_count = dictionary[prop]['count']
        elif prop == 'edge_media_to_caption':
            if isinstance(dictionary[prop]['edges'], list) and dictionary[prop]['edges']:
                first_caption = dictionary[prop]['edges'][0]
                if isinstance(first_caption, dict) and 'node' in first_caption.keys():
                    if isinstance(first_caption['node'], dict) and 'text' in first_caption['node'].keys():
                        self._caption = dictionary[prop]['edges'][0]['node']['text']
        elif prop == 'edge_sidecar_to_children':
            if isinstance(dictionary[prop]['edges'], dict):
                pass
            for edge in dictionary[prop]['edges']:
                if 'node' in edge.keys():
                    continue
                self._sidecar_medias.append(self.create(edge['node']))
        elif prop == 'owner':
            self._owner = model.Account.create(dictionary[prop])
        elif prop == 'date':
            self._created_time = int(value)
        elif prop == '__typename':
            if value == 'GraphImage':
                self._type = self.TYPE_IMAGE
            elif value == 'GraphVideo':
                self._type = self.TYPE_VIDEO
            elif value == 'GraphSidecar':
                self._type = self.TYPE_SIDECAR

        if not self._owner_id and self._owner:
            self._owner_id = self.get_owner().get_id()

    @staticmethod
    def __set_carousel_media(media_dict, carousel_dict, instance):
        carousel_media_obj = model.CarouselMedia()
        carousel_media_obj.set_type(carousel_dict['type'])

        if 'images' in carousel_dict.keys():
            carousel_images = Media.__get_image_urls(carousel_dict['images']['standard_resolution']['url'])
            carousel_media_obj.set_image_low_resolution_url(carousel_images['low'])
            carousel_media_obj.set_image_high_resolution_url(carousel_images['thumbnail'])
            carousel_media_obj.set_image_thumbnail_url(carousel_images['high'])
            carousel_media_obj.set_image_thumbnail_url(carousel_images['standard'])

        if carousel_media_obj.get_type() == Media.TYPE_VIDEO:
            if 'video_views' in media_dict.keys():
                carousel_media_obj.set_video_views(carousel_dict['video_views'])
            if 'videos' in carousel_dict.keys():
                carousel_media_obj.set_video_low_resolution_url(carousel_dict['videos']['low_resolution']['url'])
                carousel_media_obj.set_video_standard_resolution_url(carousel_dict['videos']['standard_resolution']['url'])
                carousel_media_obj.set_video_low_bandwidth_url(carousel_dict['videos']['low_bandwidth']['url'])
            instance.carousel_media.append(carousel_media_obj)

        return media_dict

    @staticmethod
    def __get_image_urls(image_url):
        parse_res = urlparse(image_url)
        parts = parse_res.path.split('/')
        image_name = parts[-1]
        urls = {
            'thumbnail': endpoints.INSTAGRAM_CDN_URL + 't/s150x150/' + image_name,
            'low': endpoints.INSTAGRAM_CDN_URL + 't/s320x320/' + image_name,
            'standard': endpoints.INSTAGRAM_CDN_URL + 't/s640x640/' + image_name,
            'high': endpoints.INSTAGRAM_CDN_URL + 't/' + image_name,
        }
        return urls

    def get_owner(self):
        """
        :return: account object
        """
        return self._owner
