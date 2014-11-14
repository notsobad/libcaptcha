## libCaptcha

Code stealed from [django-simple-captcha](https://github.com/mbi/django-simple-captcha/tree/master/captcha), removed django dependence, so you can use it in any other project.


Usage:
	
	from libcaptcha.utils import captcha_image
	
	key = 'asdfawfs(*9asdfasdfaksj92_++|_]{}'
	data = captcha_image(key, 'test', 2)
	open('x.png', 'w').write(data)