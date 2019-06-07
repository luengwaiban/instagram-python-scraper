# -*- coding:utf-8 -*-
from instagram_scraper.instagram import InstagramScraper

proxies = {
    'http': 'http://127.0.0.1:1087',
    'https': 'http://127.0.0.1:1087',
}

instagram = InstagramScraper()
instagram.set_proxies(proxies)


# example:
#
account = instagram.get_account('shaq')
account_id = account.get_id()
print(account._id)
#
#
# account_by_id = instagram.get_account_by_id('11859524403')
# print(account_by_id.__dict__)
#
#
# medias = instagram.get_media_by_user_id(account.get_id(), 63)
# print(len(medias))
# print(medias[0].__dict__)
#
#
# media_by_url = instagram.get_media_by_url('https://www.instagram.com/p/BxtNOPqlobR/')
# print(media_by_url.__dict__)
# print(media_by_url.get_comments()[0].__dict__)
# print(len(media_by_url.get_comments()))
#
#
# media_paginate = instagram.get_paginate_medias('shaq')
# print(media_paginate['meidas'], media_paginate['max_id'])
#
#
# instagram.with_credentials('luengwaiban@gmail.com', 'shinelam123456')
# res = instagram.login()
# following = instagram.get_following('206034174')
# followers = instagram.get_followers('206034174')
# print(len(following))
# print(len(followers))

# instagram.with_credentials('407261380@qq.com', 'shine-lam123456')  verify needed account

# tag_medias = instagram.get_medias_by_tag('football', 67)
# print(len(tag_medias))
# print(tag_medias[0].__dict__)
#
#
# tag_medias_paginate = instagram.get_paginate_medias_by_tag('football')
# print(len(tag_medias_paginate['medias']))
# print(tag_medias_paginate)
# tag_medias_paginate2 = instagram.get_paginate_medias_by_tag('football', tag_medias_paginate['max_id'])
# print(len(tag_medias_paginate2['medias']))
# print(tag_medias_paginate2)
#
#
# top_tag_medias = instagram.get_current_top_medias_by_tag_name('football')
# print(len(top_tag_medias))
# print(top_tag_medias[0].__dict__)
#
#
# search_username_accounts = instagram.search_accounts_by_username('luengwaiban')
# print(search_username_accounts[0].__dict__)
# print(len(search_username_accounts))
#
#
# tags_search = instagram.search_tags_by_tag_name('football')
# print(tags_search[0].__dict__)
# print(tags_search[2].get_name())
# print(len(tags_search))
#
#
# location = instagram.get_location_by_id(1)
# print(location.__dict__)
# print(location.get_name())
#
#
# medias_by_location_id = instagram.get_medias_by_location_id(1, 84)
# print(medias_by_location_id[0].__dict__)
# print(len(medias_by_location_id))
#
#
# top_medias_by_location_id = instagram.get_current_top_medias_by_location_id(1)
# print(top_medias_by_location_id[0].__dict__)
# print(len(top_medias_by_location_id))
#
#
# this method need to login
# instagram.with_credentials('luengwaiban@gmail.com', 'shinelam123456')
# res = instagram.login()
# medias_from_feed = instagram.get_medias_from_feed('shaq', 56)
# print(medias_from_feed[0].__dict__)
# print(len(medias_from_feed))
#
#
# this method need to login
# instagram.with_credentials('luengwaiban@gmail.com', 'shinelam123456')
# res = instagram.login()
# stories = instagram.get_stories()
# print(stories[0].__dict__)
# print(len(stories))
#
#
# this method need to login
# instagram.with_credentials('luengwaiban@gmail.com', 'shinelam123456')
# res = instagram.login()
# medias = instagram.get_medias('luengwaiban', 10)
# media_id = medias[1].get_id()
# instagram.like(media_id)
#
# unlike the same post
# instagram.unlike(media_id)
#
#
# instagram.with_credentials('luengwaiban@gmail.com', 'shinelam123456')
# res = instagram.login()
# medias = instagram.get_medias('luengwaiban', 10)
# media_id = medias[0].get_id()
# # add a comment
# comment = instagram.add_comment(media_id, 'this is comment 2')
# print(comment)
# # # replied a comment
# comment2 = instagram.add_comment(media_id, 'this is comment 3 to reply comment 2', comment)
#
#
# # delete comment
# instagram.with_credentials('luengwaiban@gmail.com', 'shinelam123456')
# res = instagram.login()
# medias = instagram.get_medias('luengwaiban',10)
# media_code = medias[0].get_short_code()
# media_id = medias[0].get_id()
# comments = instagram.get_media_comments_by_code(media_code, 10)
# comment_id = comments[1].get_id()
# comment_text = comments[1].get_text()
# print(comment_id)
# print(comment_text)
# instagram.delete_comment(media_id, comment_id)
#
#
# instagram.with_credentials('luengwaiban@gmail.com', 'shinelam123456')
# res = instagram.login()
# medias = instagram.get_medias('luengwaiban',10)
# media_code = medias[0].get_short_code()
# likes = instagram.get_media_likes_by_code(media_code, 20, '')
# print(likes[0].get_id())
# print(likes[0].get_username())