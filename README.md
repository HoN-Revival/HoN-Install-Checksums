# HoN-Install-Checksums
A project to track checksum dumps from actual HoN installs to be used to test/validate the custom installer.

## How to use?

The script traverses the files of a HoN install directory and computes a mapping of the `md5` checksums of each file. It skips some custom and dynamic
files such as `.honmod`, `GPUCcache`, `resources999.s2z` and so forth.

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
{"avcodec-x64-58.dll": "4b3bf8f8c06d76cec90657c00d612028", "avdevice-x64-58.dll": "f797e34cb08518cda932e9cddb2c03ed",
"avfilter-x64-7.dll": "b4b2d554a451480c51675b37f7e4e0f9", "avformat-x64-58.dll": "38c25db5309c364fdfeeecd0df3ade39",
"avutil-x64-56.dll": "aac015dae2439d2bec35a3e970f9dc08", "ca-bundle.crt": "e617b745e14a8b19ec050e8a673ac0b8",
"change_log.txt": "ca3665dfcff2fb2e2923309df35794b2", "change_log_color.txt": "0badb67ec590fed8b7301338d28022ca",
"change_log_color_history.txt": "279777370d26da50f1a2b29be58a3312",

// And so on

}
```

## Backed up official checksums

Eventually I hope to capture the checksum for every install'able version, such that the custom [HoN Installer](https://github.com/HoN-Revival/HoN-Installer) can verify
that it installed correctly.

These backups can be found in the [Checksum Dumps](https://github.com/HoN-Revival/HoN-Install-Checksums/tree/main/checksum%20dumps) folder.

For now, I am just backing up installs and updates directly from the HoN servers. If this cannot be completed in time, we may need to compute these based on backed up
files.
