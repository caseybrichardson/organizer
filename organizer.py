""" ------------------------------------------------------------- """
"""

Doc Organizer

Program by: Casey Richardson

Date created: May 6, 2013

Description: Scans through a folder and places items with extensions in specified folder. Uses a json file for the extension mapping.

""" 
""" ------------------------------------------------------------- """

import sys, os, json, glob, shutil
from optparse import OptionParser

def main():
	# Create parser and setup options
	parser = OptionParser(usage='usage: %prog [options] <filename>')

	parser.add_option('-p', '--path', dest='path', help='Path to directory where the program will be run')
	parser.add_option('-c', '--copy', action='store_true', dest='copy', default=False, help='Only copies files into the new folder.')
	parser.add_option('-v', '--verbose', action='store_true', dest='verbose', help='Turns on verbose output')
	parser.add_option('-q', '--quiet', action='store_false', dest='verbose', help='Turns off verbose output')

	# Get the arguments and parse them
	(options, args) = parser.parse_args()

	# Make sure we at least have a filename
	if len(args) < 1:
		parser.error('Need a mapping file')

	# The directory the program is running in
	progcontext = '.' if options.path == None else options.path

	if options.verbose:
		print 'Program context is: ' + progcontext

	# Read the mapping file the user gave us
	mappingdict = read_mapping(args[0])

	# Get the files from the directory we're organizing
	files = fetch_files(progcontext)

	# Loop through each file
	for f in files:
		# Get the filename and file extension
		filename, fileextension = os.path.splitext(f)

		# Get just the file path and the filename by itself
		justpath, justfile = os.path.split(f)

		# Check if the files extension is in the file mapping
		if fileextension in mappingdict:
			if options.verbose:
				print 'Moving: ' + justfile + ' to folder: ' + mappingdict[fileextension]

			# Create the folder for the file
			create_folder(progcontext, mappingdict[fileextension], options)

			# Move or copy the file into the new directory
			if options.copy:
				shutil.copy2(f, os.path.join(os.path.join(progcontext, mappingdict[fileextension]), justfile))
			else:
				os.rename(f, os.path.join(os.path.join(progcontext, mappingdict[fileextension]), justfile))
		else:
			continue

# Creates a folder with the given name at the given path, unless the directory exists
def create_folder(path, name, opts):
	directory = os.path.join(path, name)
	if os.path.exists(directory):
		if opts.verbose:
			print 'Path: ' + directory + ' already exists'
		return
	else:
		os.makedirs(directory)
		if opts.verbose:
			print 'Path: \"' + directory + '\" was created'
		return

# Reads the users mapping file from the mapping file path
def read_mapping(file):
	if os.path.isfile(file):
		try:
			mapping = json.load(open(file))
		except ValueError:
			print 'Badly formatted JSON'
			sys.exit()

		return mapping
	else:
		print 'Cannot read mapping file'
		sys.exit(-1)

# Gets all the files with any extension from the given path
def fetch_files(path):
	if os.path.isdir(path):
		files = glob.glob(os.path.join(path, '*.*'))

		if len(files) == 0:
			print 'No files to move'
			sys.exit(0)
		else:
			return files
	else:
		print 'Given path is not a directory'
		sys.exit(-1)

if __name__ == '__main__':
	main()