import hashlib
import json
import os
import zipfile

HON_PATH='C:\Program Files\Heroes of Newerth x64'

EXCLUDED_FILE_MATCHERS = [
  '.honmod',
  'resources999.s2z',
  'HoN_ModMan.exe',
  'manifest.xml',
  'GPUCache',
  'Ionic.Zip.Reduced.dll',  # for mod manager
  'debug.log',
  'changed.txt',
  'shadercache.xml',
  'shadercache2.xml'
]

checksums = {}
for root, dirs, files in os.walk(HON_PATH, topdown=True):
   for name in files:
      path = os.path.join(root, name)
      relative_path = os.path.join(os.path.relpath(root, HON_PATH), name)
      if relative_path.startswith('.\\'):
        relative_path = relative_path.replace('.\\', '')

      skip = False
      for excluded_file_matcher in EXCLUDED_FILE_MATCHERS:
        if excluded_file_matcher in relative_path:
          print('Skipping: ' + relative_path)
          skip = True
      if skip:
        continue
        
      # NOTE: `.s2z` files are just `.zip` files. Computing a checksum on the
      # compressed file is unreliable. Instead, iterate through the archive
      # and extract the pre-computed CRC-32 values.
      if '.s2z' in name and os.path.getsize(path) > 0:
        z=zipfile.ZipFile(path,'r')
        for info in z.infolist():
          filename = info.filename.replace('/', '\\')
          checksums[os.path.join(relative_path, filename)] = hex(info.CRC)
      else:  # Compute a MD5
        with open(path, 'rb') as file:
          data = file.read()
          checksum = hashlib.md5(data).hexdigest()
          checksums[relative_path] = checksum

outfile_path = 'hon_checksum_dump.json'
with open(outfile_path, 'w') as outfile:
  print('Dumping checksum dict as json to: ' + outfile_path)
  json.dump(checksums, outfile, indent=4)