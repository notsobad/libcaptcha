import sys
import random
import re
import tempfile
import os
import subprocess
import settings
import helpers

try:
	from cStringIO import StringIO
except ImportError:
	from io import BytesIO as StringIO

try:
	from PIL import Image, ImageDraw, ImageFont
except ImportError:
	import Image
	import ImageDraw
	import ImageFont

import json

NON_DIGITS_RX = re.compile('[^\d]')
# Distance of the drawn text from the top of the captcha image
from_top = 4


def getsize(font, text):
	if hasattr(font, 'getoffset'):
		return [x + y for x, y in zip(font.getsize(text), font.getoffset(text))]
	else:
		return font.getsize(text)


def captcha_image(text, scale=1):

	if settings.CAPTCHA_FONT_PATH.lower().strip().endswith('ttf'):
		font = ImageFont.truetype(settings.CAPTCHA_FONT_PATH, settings.CAPTCHA_FONT_SIZE * scale)
	else:
		font = ImageFont.load(settings.CAPTCHA_FONT_PATH)
	size = getsize(font, text)
	size = (size[0] * 2, int(size[1] * 1.4))
	if settings.CAPTCHA_BACKGROUND_COLOR == "transparent":
		image = Image.new('RGBA', size)
	else:
		image = Image.new('RGB', size, settings.CAPTCHA_BACKGROUND_COLOR)

	try:
		PIL_VERSION = int(NON_DIGITS_RX.sub('', Image.VERSION))
	except:
		PIL_VERSION = 116
	xpos = 2

	charlist = []
	for char in text:
		if char in settings.CAPTCHA_PUNCTUATION and len(charlist) >= 1:
			charlist[-1] += char
		else:
			charlist.append(char)
	for char in charlist:
		fgimage = Image.new('RGB', size, settings.CAPTCHA_FOREGROUND_COLOR)
		charimage = Image.new('L', getsize(font, ' %s ' % char), '#000000')
		chardraw = ImageDraw.Draw(charimage)
		chardraw.text((0, 0), ' %s ' % char, font=font, fill='#ffffff')
		if settings.CAPTCHA_LETTER_ROTATION:
			if PIL_VERSION >= 116:
				charimage = charimage.rotate(random.randrange(*settings.CAPTCHA_LETTER_ROTATION), expand=0, resample=Image.BICUBIC)
			else:
				charimage = charimage.rotate(random.randrange(*settings.CAPTCHA_LETTER_ROTATION), resample=Image.BICUBIC)
		charimage = charimage.crop(charimage.getbbox())
		maskimage = Image.new('L', size)

		maskimage.paste(charimage, (xpos, from_top, xpos + charimage.size[0], from_top + charimage.size[1]))
		size = maskimage.size
		image = Image.composite(fgimage, image, maskimage)
		xpos = xpos + 2 + charimage.size[0]

	image = image.crop((0, 0, xpos + 1, size[1]))
	draw = ImageDraw.Draw(image)

	for f in settings.noise_functions():
		draw = f(draw, image)
	for f in settings.filter_functions():
		image = f(image)

	out = StringIO()
	image.save(out, "PNG")
	return out.getvalue()


if __name__ == '__main__':
	text = helpers.random_char_challenge()[1]
	out = captcha_image(text, 2)
	print out
