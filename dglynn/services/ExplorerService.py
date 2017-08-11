import os
import mimetypes
mimetypes.init()

# Helper imports.
from dglynn.helpers.HumanReadableBytes import HumanReadableBytes



class FileInfo(object):
	''' Gets and stores information about the file '''
	def __init__(self, path):
		super(FileInfo, self).__init__()
		# Guess the mime type.
		self.mime = mimetypes.guess_type( path )[0]
		# The file name.
		self.name = os.path.basename( path )
		# The file path.
		self.path = path
		# Total size of the file in human readable bytes.
		self.size = HumanReadableBytes.execute( os.stat(path).st_size )



class FolderInfo(object):
	''' Gets and stores information about the folder '''
	def __init__(self, path):
		super(FolderInfo, self).__init__()
		# The folder name.
		self.name = os.path.basename( path )
		# The folder path.
		self.path = path
		# Total size of folder in human readable bytes.
		byts = sum( [sum( map(lambda fname: os.path.getsize( os.path.join(directory, fname) ), files) ) for directory, folders, files in os.walk(path)] )
		self.size = HumanReadableBytes.execute( byts )
		


class Folder(object):
	''' Stores the path and the lists of folders and files '''
	def __init__(self, path, folders, files):
		super(Folder, self).__init__()
		self.path    = path
		self.folders = folders
		self.files   = files


		
class ExplorerService(object):

	STATIC_PATH = 'static'
	MEDIA_PATH  = 'media'

	def getFullPath(url):
		''' Returns the full-path from a url '''
		return os.path.join(
			ExplorerService.STATIC_PATH,
			ExplorerService.MEDIA_PATH,
			os.path.join( *url.split('/') ) )
		
	def getFolderContents(path):
		''' Returns a contents object that contains a list of files and a list of folders '''
		# Get a list of folder_names and file_names in a directory.
		contents = [content for content in os.listdir( path )]
		# Get the list of File objects from the contents list.
		files    = [ExplorerService.getFileInfo  ( os.path.join(path, file) )   for file   in contents if os.path.isfile( os.path.join(path, file  ) )]
		# Get the list of Folder objects from the contents list.
		folders  = [ExplorerService.getFolderInfo( os.path.join(path, folder) ) for folder in contents if os.path.isdir ( os.path.join(path, folder) )]
		# Return a Contents object.
		return Folder(path, folders, files).__dict__

	def getFolderInfo(path):
		return FolderInfo(path).__dict__

	def getFileInfo(path):
		return FileInfo(path).__dict__

