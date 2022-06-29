import glob

from herast.schemes_storage import SchemesStorage
from herast.schemes.base_scheme import Scheme
from herast.tree.matcher import Matcher

from typing import Dict, Optional

import herast.idb_settings as idb_settings
import herast.herast_settings as herast_settings


schemes_storages : Dict[str, SchemesStorage] = {}
passive_schemes = {}

def initialize():
	load_all_storages()

def get_passive_matcher():
	matcher = Matcher()
	for s in get_passive_schemes():
		matcher.add_scheme(s)
	return matcher

def add_passive_scheme(scheme):
	if not isinstance(scheme, Scheme):
		return

	passive_schemes[scheme.name] = scheme

def get_passive_schemes():
	return [s for s in passive_schemes.values()]

def load_all_storages():
	for folder in herast_settings.get_herast_folders():
		load_storage_folder(folder)
	for file in herast_settings.get_herast_files():
		load_storage_file(file)

def load_storage_folder(folder_name: str) -> None:
	for full_path in glob.iglob(folder_name + '/**/**.py', recursive=True):
		load_storage_file(full_path)

def load_storage_file(filename: str) -> bool:
	storage = SchemesStorage.from_file(filename)
	if storage is None:
		print("[!] WARNING: failed to load", filename, "storage")
		return False

	storage.enabled = filename in idb_settings.get_enabled_idb()
	schemes_storages[filename] = storage
	return True

def get_storages_folders():
	global_folders = herast_settings.get_herast_folders()
	idb_folders = idb_settings.get_idb_folders()
	return global_folders + idb_folders

def get_storage(filename: str) -> Optional[SchemesStorage]:
	return schemes_storages.get(filename, None)

def get_enabled_storages():
	return [s for s in schemes_storages.values() if s.enabled]

def disable_storage(storage_path):
	storage = get_storage(storage_path)
	if storage is None:
		return
	storage.disable()

def enable_storage(storage_path):
	storage = get_storage(storage_path)
	if storage is None:
		return
	storage.enable()

def reload_storage(storage_path):
	storage = get_storage(storage_path)
	if storage is None:
		return
	storage.reload()