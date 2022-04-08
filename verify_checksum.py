import hashlib
import json
import os
import zipfile

HON_INSTALL_PATH='C:\Program Files\Heroes of Newerth x64'
# TODO: Take in the architecture, version, and os as input arguments
HON_CHECKSUM_REL_PATH='checksum dumps\\wac\\x86_64\\4.10.1.json'

EXCLUDED_FILE_MATCHERS = [
  '.honmod',
  'resources999.s2z',
  'HoN_ModMan.exe',
  'manifest.xml',
  'GPUCache',
  'Ionic.Zip.Reduced.dll',  # for mod manager
  'debug.log',
  'changed.txt',
]

def validate_checksum(checksum, expected_checksum, relative_path):
  if not expected_checksum:
    print(f'Extra file found: {relative_path} : {checksum}')
    return False
  if checksum != expected_checksum:
    print(f'Checksum mismatch! File: {relative_path}\nExpected checksum: {expected_checksum}\nActual checksum: {checksum}')
    return False
  return True

checksums = None
with open(HON_CHECKSUM_REL_PATH, 'r') as checksum_file:
  data = checksum_file.read()
  checksums = json.loads(data)

if not checksums:
  print('Cannot open checksum file at: ' + HON_CHECKSUM_REL_PATH)
  exit(1)
  
checksum_failed = False
for root, dirs, files in os.walk(HON_INSTALL_PATH, topdown=True):
   for name in files:
      path = os.path.join(root, name)
      relative_path = os.path.join(os.path.relpath(root, HON_INSTALL_PATH), name)
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
      if '.s2z' in name:
        z = zipfile.ZipFile(path,'r')
        for info in z.infolist():
          checksum = hex(info.CRC)
          filename = info.filename.replace('/', '\\')
          zip_relative_path = os.path.join(relative_path, filename)
          expected_checksum = checksums.get(zip_relative_path, '')
          success = validate_checksum(checksum, expected_checksum, zip_relative_path)
          if not success:
            checksum_failed = True
      else:  # verify MD5
        with open(path, 'rb') as file:
          data = file.read()
          checksum = hashlib.md5(data).hexdigest()
          expected_checksum = checksums.get(relative_path, '')
          success = validate_checksum(checksum, expected_checksum, relative_path)
          if not success:
            checksum_failed = True


if checksum_failed:
  print('\nChecksum failed :(')
else:
  print('\nChecksum verified! Congrats! Your install is good :)')