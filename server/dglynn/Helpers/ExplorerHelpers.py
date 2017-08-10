import os
import mimetypes
mimetypes.init()

from flask import request

from dglynn.Helpers.HumanReadableBytes import HumanReadableBytes

class File(object):
	def __init__(self, path):
		super(File, self).__init__()
		self.mime = mimetypes.guess_type( path )[0]
		self.name = os.path.basename( path )
		self.path = path
		self.size = HumanReadableBytes.execute( os.stat(path).st_size )
		self.type = self.__class__.__name__
		self.url  = request.path
		


class Folder(object):
	def __init__(self, path):
		super(Folder, self).__init__()
		self.name = os.path.basename( path )
		self.path = path
		byts = sum( [sum( map(lambda fname: os.path.getsize( os.path.join(directory, fname) ), files) ) for directory, folders, files in os.walk(path)] )
		self.size = HumanReadableBytes.execute( byts )
		self.type = self.__class__.__name__
		


class GetFolderContents(object):
	def execute(path):
		contents = [content for content in os.listdir( path )]
		files    = [File  ( os.path.join(path, file  ) ).__dict__  for file   in contents if os.path.isfile( os.path.join(path, file  ) )]
		folders  = [Folder( os.path.join(path, folder) ).__dict__  for folder in contents if os.path.isdir ( os.path.join(path, folder) )]
		return files, folders