import hashlib
import json
import os

HON_PATH='C:\Program Files\Heroes of Newerth x64'

EXCLUDED_FILE_MATCHERS = [
  '.honmod',
  'resources999.s2z',
  'HoN_ModMan.exe',
  'manifest.xml',
  'GPUCache',
  'shadercache',
  'Ionic.Zip.Reduced.dll',  # for mod manager
  'debug.log'
]

checksums = {}
for root, dirs, files in os.walk(HON_PATH, topdown=True):
   for name in files:
      path = os.path.join(root, name)

      skip = False
      for excluded_file_matcher in EXCLUDED_FILE_MATCHERS:
        if excluded_file_matcher in path:
          print('Skipping: ' + name)
          skip = True
      if skip:
        continue

      relative_path = os.path.join(os.path.relpath(root, HON_PATH), name)
      if relative_path.startswith('.\\'):
        relative_path = relative_path.replace('.\\', '')
      with open(path, 'rb') as file:
        data = file.read()
        checksum = hashlib.md5(data).hexdigest()
        checksums[relative_path] = checksum

outfile_path = 'hon_checksum_dump.json'
with open(outfile_path, 'w') as outfile:
  print('Dumping checksum dict as json to: ' + outfile_path)
  json.dump(checksums, outfile)