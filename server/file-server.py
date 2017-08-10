import os
import json
from flask import Flask, request, jsonify

from dglynn.Helpers.HumanReadableBytes import HumanReadableBytes
from dglynn.Helpers.UrlHelpers         import MediaFolderPrefix, UrlToFolderPath
from dglynn.Helpers.ExplorerHelpers    import File, Folder, GetFolderContents

class FileServer(Flask):
	def __init__(self, name, host='0.0.0.0', port=5001, debug=True, threaded=True):
		super(FileServer, self).__init__( name )
		self.host     = host
		self.port     = port
		self.debug    = debug
		self.threaded = threaded
		self.url_map.strict_slashes = False
		self._routes()

	def _routes(self):
		self.add_url_rule('/',           view_func=self._catch_all)
		self.add_url_rule('/<path:url>', view_func=self._catch_all)

	def _catch_all(self, url='/'):
		path = os.path.join(
			MediaFolderPrefix.execute(),
			UrlToFolderPath.execute( url ) )
		if os.path.isdir( path ):
			return self._handle_folder( path )
		elif os.path.isfile( path ):
			return self._handle_file( path )
		return '{}'
		
	def _handle_folder(self, path):
		files, folders = GetFolderContents.execute( path )
		return jsonify({
			'contents' : {
				'files'        : files,
				'folders'      : folders
			},
			'path': path,
			'url' : request.path })
		
	def _handle_file(self, path):
		return jsonify( File(path).__dict__ )

	def start(self):
		self.run(
			host     = self.host,
			port     = self.port,
			debug    = self.debug,
			threaded = self.threaded )


if __name__ == '__main__':
	FileServer('FileServer', port=6001).start()