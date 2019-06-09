# instagram-python-scraper
A instagram scraper wrote in python.Get medias, account, videos, comments without authentication.Comment and like action also supported.  
Similar to instagram-php-scraper. Enjoy it! ☺️  
**Any star or contribution would be appreciated if it is helpful for you ~** 🙋‍♂️🌚

## install
You can simply run this command:  
```
pip install instagram-python-scraper
```
Or you can also download it directly and install the libs that recorded in require.txt first.  
Run the command below:
```
pip install -r require.txt
```

## usages
Some methods require authentication:
```python
from instagram_scraper.instagram import InstagramScraper

instagram = InstagramScraper()

# authentication supported
instagram.with_credentials('your account', 'your password')
res = instagram.login()

followers = instagram.get_followers('206034174', 20, 20, True)
print(followers[0])

```
If you use authentication the program will cache the user session by default so that you don't need to gain session everytime.  
But if you want to disable the user session cache, just assign `True` to login() method:
```python
from instagram_scraper.instagram import InstagramScraper

instagram = InstagramScraper()

instagram.with_credentials('your account', 'your password')
res = instagram.login(True)
```
Besides, account verification is also supported by default.
When a account verification is needed, you will receive a active code by email or something and you should then input the code in terminal
to finish verification.  
  
Many of the methods do not require authentication:
```python
from instagram_scraper.instagram import InstagramScraper

instagram = InstagramScraper()

account = instagram.get_account('shaq')
account_id = account.get_id()
print(account._id)
```
  
Using proxy for requests:
```python
from instagram_scraper.instagram import InstagramScraper

proxies = {
    'http': 'http://127.0.0.1:1087',
    'https': 'http://127.0.0.1:1087',
}

instagram = InstagramScraper()
instagram.set_proxies(proxies)

account = instagram.get_account('shaq')
account_id = account.get_id()
print(account._id)
```

## more usages
See [more usages](https://github.com/luengwaiban/instagram-python-scraper/blob/master/more_usages.md)  

once again:  
**Any star or contribution would be appreciated if it is helpful for you ~** 🙋‍♂️🌚

## other
php library:https://github.com/postaddictme/instagram-php-scraper
