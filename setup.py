from setuptools import setup, find_packages
setup(name='libcaptcha',
	version='0.1',
	py_modules=find_packages(),
	#py_modules=['libcaptcha'],
	include_package_data=True,
	description="A captcha package",
)
