import os

class MediaFolderPrefix(object):
	STATIC_PATH = 'static'
	MEDIA_PATH  = 'media'
	def execute():
		return os.path.join(
			MediaFolderPrefix.STATIC_PATH,
			MediaFolderPrefix.MEDIA_PATH )


class UrlToFolderPath(object):
	def execute(url):
		return os.path.join( *url.split('/') )