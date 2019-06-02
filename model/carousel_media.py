# -*- coding:utf-8 -*-


class CarouselMedia(object):

    def __init__(self):
        self.__type = ''
        self.__image_low_resolution_url = ''
        self.__image_thumbnail_url = ''
        self.__image_standard_resolution_url = ''
        self.__image_high_resolution_url = ''
        self.__video_low_resolution_url = ''
        self.__video_standard_resolution_url = ''
        self.__video_low_bandwidth_url = ''
        self.__video_views = ''

    def get_type(self):
        return self.__type

    def set_type(self, type_value):
        self.__type = type_value
        return self

    def get_image_low_resolution_url(self):
        return self.__image_high_resolution_url

    def set_image_low_resolution_url(self, image_low_resolution_url):
        self.__image_low_resolution_url = image_low_resolution_url
        return self

    def get_image_thumbnail_url(self):
        return self.__image_thumbnail_url

    def set_image_thumbnail_url(self, image_thumbnail_url):
        self.__image_thumbnail_url = image_thumbnail_url
        return self

    def get_image_standard_resolution_url(self):
        return self.__image_standard_resolution_url

    def set_image_standard_resolution_url(self, image_standard_resolution_url):
        self.__image_standard_resolution_url = image_standard_resolution_url
        return self

    def get_image_high_resolution_url(self):
        return self.__image_high_resolution_url

    def set_image_high_resolution_url(self, image_high_resolution_url):
        self.__image_high_resolution_url = image_high_resolution_url
        return self

    def get_video_low_resolution_url(self):
        return self.__video_low_resolution_url

    def set_video_low_resolution_url(self, video_low_resolution_url):
        self.__video_low_resolution_url = video_low_resolution_url
        return self

    def get_video_standard_resolution_url(self):
        return self.__video_standard_resolution_url

    def set_video_standard_resolution_url(self, video_standard_resolution_url):
        self.__video_standard_resolution_url = video_standard_resolution_url
        return self

    def get_video_low_bandwidth_url(self):
        return self.__video_low_bandwidth_url

    def set_video_low_bandwidth_url(self, video_low_bandwidth_url):
        self.__video_low_bandwidth_url = video_low_bandwidth_url
        return self

    def get_video_views(self):
        return self.__video_views

    def set_video_views(self, video_views):
        self.__video_views = video_views
        return self


