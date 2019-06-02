# -*- coding:utf-8 -*-
import time


class InitializerModel(object):

    def __init__(self, props=None):
        self._is_new = True
        self._is_loaded = False
        self._is_load_empty = True
        self._modified = int(time.time())
        self._is_auto_construct = False
        # Dict of initialization data
        self.data = {}
        if not hasattr(self, '_init_properties_map') or not self._init_properties_map:
            self._init_properties_map = {}
        # initialization begin
        self._general_initialize(props)

    def _general_initialize(self, props=None):
        self._before_init()
        if self._is_auto_construct:
            self._init_auto()
        elif not props:
            if not isinstance(props, dict):
                raise TypeError('props should be dict')
            self._init_defaults()
        else:
            self._init(props)
        self._after_init()

    def _before_init(self):
        """
        protected method
        :return:
        """
        return self

    def _init_auto(self):
        """
        better not to override this method, or change it at your own risk
        :return:
        """
        for prop, value in self.__dict__.items():
            if prop in self._init_properties_map.keys() and self._init_properties_map[prop] and callable(getattr(self, self._init_properties_map[prop], None)):
                getattr(self, self._init_properties_map[prop])(value, prop)
        self._is_new = False
        self._is_loaded = True
        self._is_load_empty = False

    def _init_defaults(self):
        return self

    def _init(self, props=None):
        if not isinstance(props, dict):
            raise TypeError('props should be dict')

        for prop, value in props.items():
            if callable(getattr(self, '_init_properties_custom', None)):
                getattr(self, '_init_properties_custom')(value, prop, props)
            elif prop in self._init_properties_map.keys():
                method_or_prop = self._init_properties_map[prop]
                if callable(getattr(self, method_or_prop, None)):
                    # if there is callable method then use it firstly
                    getattr(self, method_or_prop)(value, prop, props)
                elif hasattr(self, method_or_prop):
                    # if there is property then it just assign value
                    setattr(self, method_or_prop, value)
                else:
                    # otherwise fill help data array for following initialization
                    self.data[method_or_prop] = value
                    self.data[prop] = value

        self._is_new = False
        self._is_loaded = True
        self._is_load_empty = False

        return self

    def _after_init(self):
        return self

    @classmethod
    def create(cls, props=None):
        """
        the expose method to create a model object
        :param props:
        :return:
        """
        return cls(props)

    def _to_dict(self):
        res = {}
        for key, value in self._init_properties_map:
            if hasattr(self, key):
                res[key] = getattr(self, key)
            else:
                res[key] = None
        return res

    def _init_properties(self, value, *keys):
        for key in keys:
            if hasattr(self, key):
                setattr(self, key, value)
                return self
        return self



