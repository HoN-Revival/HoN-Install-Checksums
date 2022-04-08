# HoN-Install-Checksums
A project to track checksum dumps from actual HoN installs to be used to test/validate the custom installer.

## How to use?

The script traverses the files of a HoN install directory and computes a mapping of the `md5` checksums of each file. It skips some custom and dynamic
files such as `.honmod`, `GPUCcache`, `resources999.s2z` and so forth.

NOTE: For `.s2z` files (which are just custom file extensions for a `.zip` file), `md5` is not reliable on the archive itself. Instead, the `CRC-32` which is precomputed in the zip archive will be checked.

The default path that it checks is for Windows 64-bit install:

```
HON_PATH='C:\Program Files\Heroes of Newerth x64'
```

Simply edit this path if you installed somewhere else.

Then simply run the script:

```
python checksum.py
```

The script may take a minute to traverse all the files. It will output a file called `hon_checksum_dump.json` with a mapping of all of the checksums.

A snippet of that json may look like this:

```
{
    "avcodec-x64-58.dll": "4b3bf8f8c06d76cec90657c00d612028",
    "avdevice-x64-58.dll": "f797e34cb08518cda932e9cddb2c03ed",
    "avfilter-x64-7.dll": "b4b2d554a451480c51675b37f7e4e0f9",
    "avformat-x64-58.dll": "38c25db5309c364fdfeeecd0df3ade39",
    "avutil-x64-56.dll": "aac015dae2439d2bec35a3e970f9dc08",

// And so on

}
```

## Backed up official checksums

Eventually I hope to capture the checksum for every install'able version, such that the custom [HoN Installer](https://github.com/HoN-Revival/HoN-Installer) can verify
that it installed correctly.

These backups can be found in the [Checksum Dumps](https://github.com/HoN-Revival/HoN-Install-Checksums/tree/main/checksum%20dumps) folder.

For now, I am just backing up installs and updates directly from the HoN servers. If this cannot be completed in time, we may need to compute these based on backed up
files.

## Verifying checksums

The default path that it checks is for Windows 64-bit install:

```
HON_INSTALL_PATH='C:\Program Files\Heroes of Newerth x64'
```

For now, the script just hardcodes the relative path to the checksum json:

```
# TODO: Take in the architecture, version, and os as input arguments
HON_CHECKSUM_REL_PATH='checksum dumps\\wac\\x86_64\\4.10.1.json'
```

Simply edit these to point to the appropriate install directory and checksum path.

Then simply run the script:

```
python verify_checksum.py
```

The script may take a minute to traverse all the files.

It will alert you if there are any checksum mismatches. For example:

```
Checksum mismatch! File: avcodec-x64-58.dll
Expected checksum: 4b3bf8f8c06d76cec90657c00d612028
Actual checksum: 3bf9514c7a9bdb244c9cdc6b4f88029f
```

If it succeeds you will see this message:

```
Checksum verified! Congrats! Your install is good :)
```

If there were any issues, you will see this message:

```
checksum failed :(
```
