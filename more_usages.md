## more usages
#### get_account
```python
from instagram_scraper.instagram import InstagramScraper

instagram = InstagramScraper()
account = instagram.get_account('shaq')
account_id = account.get_id()
account_uesrname = account.get_username()
print(account._id)
print(account_uesrname)
```

#### get_account_by_id
```python
from instagram_scraper.instagram import InstagramScraper

instagram = InstagramScraper()
account_by_id = instagram.get_account_by_id('11859524403')
print(account_by_id.get_username())
```

#### get_medias
```python
from instagram_scraper.instagram import InstagramScraper

instagram = InstagramScraper()
medias = instagram.get_medias('luengwaiban', 10)
print(len(medias))
print(medias[0].get_short_code())
```

#### get_media_by_user_id
```python
from instagram_scraper.instagram import InstagramScraper

instagram = InstagramScraper()
account = instagram.get_account('shaq')
medias = instagram.get_media_by_user_id(account.get_id(), 63)
print(len(medias))
print(medias[0].get_caption())
```

#### get_media_by_url
```python
from instagram_scraper.instagram import InstagramScraper

instagram = InstagramScraper()
media_by_url = instagram.get_media_by_url('https://www.instagram.com/p/BxtNOPqlobR/')
print(media_by_url.get_id())
print(media_by_url.get_comments()[0].__dict__)
print(len(media_by_url.get_comments()))
```

#### get_paginate_medias 
```python
from instagram_scraper.instagram import InstagramScraper

instagram = InstagramScraper()
# get medias page by page, out of loop
media_paginate = instagram.get_paginate_medias('shaq')
media_paginate2 = instagram.get_paginate_medias('shaq', media_paginate['max_id'])
print(media_paginate['meidas'], media_paginate['max_id'])
print(media_paginate2['meidas'], media_paginate2['max_id'])
```

#### get_medias_by_tag
```python
from instagram_scraper.instagram import InstagramScraper

instagram = InstagramScraper()
tag_medias = instagram.get_medias_by_tag('football', 67)
print(len(tag_medias))
print(tag_medias[0].get_image_high_resolution_url())
```

#### tag_medias_paginate
```python
from instagram_scraper.instagram import InstagramScraper

instagram = InstagramScraper()
tag_medias_paginate = instagram.get_paginate_medias_by_tag('football')
print(len(tag_medias_paginate['medias']))
print(tag_medias_paginate)
tag_medias_paginate2 = instagram.get_paginate_medias_by_tag('football', tag_medias_paginate['max_id'])
print(len(tag_medias_paginate2['medias']))
print(tag_medias_paginate2)
```

#### get_current_top_medias_by_tag_name
```python
from instagram_scraper.instagram import InstagramScraper

instagram = InstagramScraper()
top_tag_medias = instagram.get_current_top_medias_by_tag_name('football')
print(len(top_tag_medias))
print(top_tag_medias[0].get_likes_count())
```

#### get_medias_by_location_id
```python
from instagram_scraper.instagram import InstagramScraper

instagram = InstagramScraper()
medias_by_location_id = instagram.get_medias_by_location_id(1, 84)
print(medias_by_location_id[0].__dict__)
print(medias_by_location_id[0].get_link())
print(len(medias_by_location_id))
```

#### get_current_top_medias_by_location_id
```python
from instagram_scraper.instagram import InstagramScraper

instagram = InstagramScraper()
top_medias_by_location_id = instagram.get_current_top_medias_by_location_id(1)
print(top_medias_by_location_id[0].__dict__)
print(top_medias_by_location_id[0].get_link())
print(len(top_medias_by_location_id))
```

#### get_medias_from_feed
```python
# this method need to login
from instagram_scraper.instagram import InstagramScraper

instagram = InstagramScraper()
instagram.with_credentials('your account', 'your password')
res = instagram.login()

medias_from_feed = instagram.get_medias_from_feed('shaq', 56)
print(medias_from_feed[0].get_link())
print(len(medias_from_feed))
```

#### get_stories
```python
# this method need to login, get the stories of logged in account
from instagram_scraper.instagram import InstagramScraper

instagram = InstagramScraper()
instagram.with_credentials('your account', 'your password')
res = instagram.login()

stories = instagram.get_stories()
print(stories[0].get_stories())
print(len(stories))
```

#### get_following
```python
# this method need to login
from instagram_scraper.instagram import InstagramScraper

instagram = InstagramScraper()
instagram.with_credentials('your account', 'your password')
res = instagram.login()
account = instagram.get_account('shaq')
following = instagram.get_following(account.get_id())
print(following[0]['id'])
```

#### get_followers
```python
from instagram_scraper.instagram import InstagramScraper

instagram = InstagramScraper()
instagram.with_credentials('your account', 'your password')
res = instagram.login()
account = instagram.get_account('shaq')
followers = instagram.get_followers(account.get_id())
print(followers[0]['id'])
```

#### search_accounts_by_username
```python
from instagram_scraper.instagram import InstagramScraper

instagram = InstagramScraper()
search_username_accounts = instagram.search_accounts_by_username('luengwaiban')
print(search_username_accounts[0].get_full_name())
print(len(search_username_accounts))
```

#### search_tags_by_tag_name
```python
from instagram_scraper.instagram import InstagramScraper

instagram = InstagramScraper()
tags_search = instagram.search_tags_by_tag_name('football')
print(tags_search[0].__dict__)
print(tags_search[2].get_name())
print(len(tags_search))
```

#### get_location_by_id
```python
from instagram_scraper.instagram import InstagramScraper

instagram = InstagramScraper()
location = instagram.get_location_by_id(1)
print(location.__dict__)
print(location.get_name())
```

#### like & unlike
```python
from instagram_scraper.instagram import InstagramScraper

instagram = InstagramScraper()
# these methods need to login
instagram.with_credentials('your account', 'your password')
res = instagram.login()

medias = instagram.get_medias('luengwaiban', 10)
media_id = medias[1].get_id()
instagram.like(media_id)

# unlike the same post
instagram.unlike(media_id)
```

#### add_comment
```python
from instagram_scraper.instagram import InstagramScraper

instagram = InstagramScraper()
instagram.with_credentials('your account', 'your password')
res = instagram.login()
medias = instagram.get_medias('luengwaiban', 10)
media_id = medias[0].get_id()
# add a comment
comment = instagram.add_comment(media_id, 'this is comment 2')
print(comment)
# # replied a comment
comment2 = instagram.add_comment(media_id, 'this is comment 3 to reply comment 2', comment)
```

#### delete_comment
```python
# delete comment
from instagram_scraper.instagram import InstagramScraper

instagram = InstagramScraper()
instagram.with_credentials('your account', 'your password')
res = instagram.login()
medias = instagram.get_medias('luengwaiban',10)
media_code = medias[0].get_short_code()
media_id = medias[0].get_id()
comments = instagram.get_media_comments_by_code(media_code, 10)
comment_id = comments[1].get_id()
comment_text = comments[1].get_text()
print(comment_id)
print(comment_text)
instagram.delete_comment(media_id, comment_id)
```

#### get_media_likes_by_code
```python
from instagram_scraper.instagram import InstagramScraper

instagram = InstagramScraper()
instagram.with_credentials('your account', 'your password')
res = instagram.login()
medias = instagram.get_medias('luengwaiban',10)
media_code = medias[0].get_short_code()
likes = instagram.get_media_likes_by_code(media_code, 20, '')
print(likes[0].get_id())
print(likes[0].get_username())
```