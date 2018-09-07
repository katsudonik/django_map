from selenium import webdriver
from PIL import Image

def shot_png(url, width, height, save_path):
	driver = webdriver.PhantomJS(executable_path='/usr/local/bin/phantomjs')
	driver.set_window_size(width, height)
	driver.get(url)
	driver.save_screenshot(save_path + ".png")
	driver.close()
def convert_to_jpg(path, quality):
	input_im = Image.open(path + ".png")
	rgb_im = input_im.convert('RGB')
	rgb_im.save(path + ".jpg",quality=quality)

# url = 'http://localhost:80/cgi-bin/polyline/polyline.py'
# width = 1922
# quality = 30
# save_path = '/var/www/html/polyline'
def shot_jpg(url, width, height, quality, save_path):
	shot_png(url, width, height, save_path)
	convert_to_jpg(save_path, quality)
