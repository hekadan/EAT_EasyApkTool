A Script to easily decompile and build APK files. And tool to pull some  files from device.

### Usage
```sh
$ eat.py
usage: Easy APK Tool [-h] [-d APK_FOR_DECODE] [-b SOURCE_DIR]
                     [-s APK_FOR_SIGN] [-j DEX_FILE] [-u APK_FOR_UNZIP]
                     [--tool]

optional arguments:
  -h, --help            show this help message and exit
  -d APK_FOR_DECODE, --decode APK_FOR_DECODE
                        Decode APK file
  -b SOURCE_DIR, --build SOURCE_DIR
                        Build app source to APK and sign
  -s APK_FOR_SIGN, --sign APK_FOR_SIGN
                        Sign APK file
  -j DEX_FILE, --jar DEX_FILE
                        Convert to DEX(APK) to JAR
  -u APK_FOR_UNZIP, --unzip APK_FOR_UNZIP
                        Unzip APK file
  --tool                Tool for Pulling APK, DB file etc
```

### Tool
```sh
$ eat.py --tool
1. Pull APK File
2. Pull DB, Shared Preferences File
3. Pull 1 + 2 (APK, DB)
4. Check Debuggable APK List
===================================
Select Number :
```


### Environment setting
Add below to `~/.bash_profile` file
```
export PATH="$PATH:/Users/sungwonkim/tools/<directory of eat.py>"
```