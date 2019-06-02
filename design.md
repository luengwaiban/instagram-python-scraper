### instagram-python-scraper设计

<pre>

ver 1.0
|- instagram-python-scraper  
    |-exception  [定义了一些exception(notfound、auth等)]
    |-model  [定义了一些model，用来将一些ins的实体信息转化为对象(account、media、tag、story、comment等，使用的时候可以考虑将对象转为dict)，并将Traits中的InitializerTrait.php翻译成InitializerModel.py放到此处，ArrayLikeTrait.php的方法暂时没有用到所以先不编写,InitializerModel.py为model类型的顶层，BaseModel.py继承自InitializerModel.py，然后account、media、tag等继承自BaseModel.py]
    (model类型的文件，属性建议直接全部写成私有变量，然后再写N个getter)
    |-TowStepVerification  [用来通过命令行验证账号并登录，需要用户输入验证码，用邮箱或者手机接收吧大概是，暂时先不编写]
    |-endPoints.py  [与请求url相关的文件，对所有会用到的请求放在这个文件统一管理，里面有很多相关方法]
    |-instagram.py  [整个程序的入口，定义了很多方法来获取你想要的东西]

</pre>
