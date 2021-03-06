import logging, os, inspect, imp, re

global base_dir
global commands
commands = {}

def modules_in_dir(path):
	result = set()
	for entry in os.listdir(path):
		if os.path.isfile(os.path.join(path, entry)):
			matches = re.search("(.+\.py)$", entry)
			if matches:
				result.add(matches.group(0))
	return result

def import_dir(path):
	search_path = os.path.join(base_dir, path)
	for filename in sorted(modules_in_dir(search_path)):
		module_name, ext = os.path.splitext(filename)
		fp, path_name, description = imp.find_module(module_name, [search_path,])
		module = imp.load_module(module_name, fp, path_name, description)

def add_command(name):
	frame = inspect.stack()[1]
	filename = os.path.relpath(frame[0].f_code.co_filename, base_dir)
	def wrapper(function):
		commands[name] = function
		return function
	return wrapper