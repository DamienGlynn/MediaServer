import os
import json
from flask import Flask, request, jsonify

from dglynn.services.ExplorerService import ExplorerService

class FileServer(Flask):
	def __init__(self, name, host='0.0.0.0', port=5001, debug=True, threaded=True):
		super(FileServer, self).__init__( name )
		# Set the properties.
		self.host     = host
		self.port     = port
		self.debug    = debug
		self.threaded = threaded
		self.url_map.strict_slashes = False
		# Set the routes.
		self._routes()

	def _routes(self):
		self.add_url_rule('/',           view_func=self._catch_all)
		self.add_url_rule('/<path:url>', view_func=self._catch_all)

	def _catch_all(self, url='/'):
		# Convert the url into a system specific directory path.
		path = ExplorerService.getFullPath( url )
		# If the path points to a folder.
		if os.path.isdir( path ):
			# Handle the folder.
			return self._handle_folder( path )
		# If the path points to a file.
		elif os.path.isfile( path ):
			# Handle the file.
			return self._handle_file( path )
		# Not a file or folder, so we'll return an empty object.
		return jsonify({})
		
	def _handle_folder(self, path):
		# Get the contents of a folder.
		contents = ExplorerService.getFolderContents( path )
		# Add the request path.
		contents['url'] = request.path
		# Return the folder information.
		return jsonify(contents)
		
	def _handle_file(self, path):
		# Get information about a file.
		file = ExplorerService.getFileInfo( path )
		# Add the request path.
		file['url'] = request.path
		# Return the file information.
		return jsonify( file )

	def start(self):
		self.run(
			host     = self.host,
			port     = self.port,
			debug    = self.debug,
			threaded = self.threaded )


if __name__ == '__main__':

	FileServer('FileServer', port=6001).start()