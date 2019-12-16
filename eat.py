#!/usr/bin/env python3
import argparse
import os
import sys
import zipfile
import xml.etree.ElementTree as ET
import subprocess


# Path of eat.py
base_path = os.path.split(os.path.abspath(sys.argv[0]))[0]
os_type = ''


def decode_apk(apk_file):
    file_root = os.path.splitext(apk_file)[0]

    print('[-] Decoding APK file...')
    if os_type == 'nt':
        os.system('{}/tools/apktool/apktool.bat d {} -o {}_decode -f'.format(base_path, apk_file, file_root))
    else:
        os.system('{}/tools/apktool/apktool d {} -o {}_decode -f'.format(base_path, apk_file, file_root))
    print('[+] Decoding Fisnished')


def sign_apk(apk_file):
    print('[-] Signing APK file...')
    tool_path = base_path + '/tools/apksigner'
    sign_output = os.path.splitext(apk_file)[0] + '_signed.apk'
    cmd = 'java -jar {}/apksigner.jar sign --key {}/testkey.pk8 --cert {}/testkey.x509.pem --out {} {}'
    os.system(cmd.format(tool_path, tool_path, tool_path, sign_output, apk_file))
    print('[+] Signing Finished')


def build_apk(source_dir):
    """Build by apktool"""
    print('[-] Building APK file...')
    build_output =  source_dir + '.apk'
    if os_type == 'nt':
        os.system('{}/tools/apktool/apktool.bat b {} -o {}'.format(base_path, source_dir, build_output))
    else:
        os.system('{}/tools/apktool/apktool b {} -o {}'.format(base_path, source_dir, build_output))

    sign_apk(build_output)
    print('[+] Building Finished')
    os.remove(build_output)


def dex2jar(apk_file):
    file_root = os.path.splitext(apk_file)[0]
    # unzip_dir = file_root + '_unzip'
    print('[-] Converting DEX to JAR...')
    tool_path = base_path + '/tools/dex2jar'
    if os.name == 'nt':
        os.system('{}/d2j-dex2jar.bat {} -o {}.jar'.format(tool_path, apk_file, file_root))
    else:
        os.system('{}/d2j-dex2jar.sh {} -o {}.jar'.format(tool_path, apk_file, file_root))
    print('[+] Converting Finished')


def unzip_apk(apk_file):
    file_root = os.path.splitext(apk_file)[0]
    unzip_dir = file_root + '_unzip'
    print('[-] Unzipping APK file...')
    with zipfile.ZipFile(apk_file, 'r') as z:
        z.extractall(unzip_dir)
    print('[+] Unzipping Finished')


def print_apk_info(decode_path):
    tree = ET.parse(decode_path + "_decode/AndroidManifest.xml")
    root = tree.getroot()

    print('[-] App Info')
    with open('apk-info.txt', 'w') as fd:

        print('App Permition')
        fd.write('App Permition\n')
        attr_name = '{http://schemas.android.com/apk/res/android}name'
        for child in root.iter('uses-permission'):
            print(' |--> {}'.format(child.attrib[attr_name]))
            fd.write(' |--> {}\n'.format(child.attrib[attr_name]))

        print('Activity')
        fd.write('Activity\n')
        for child in root.iter('activity'):
            print(' |--> {}'.format(child.attrib[attr_name]))
            fd.write(' |--> {}\n'.format(child.attrib[attr_name]))

        print('Debuggale')
        fd.write('Debuggale\n')
        attr_name = '{http://schemas.android.com/apk/res/android}debuggable'
        try:
            for child in root.iter('application'):
                print(' |--> {}'.format(child.attrib[attr_name]))
                fd.write(' |--> {}\n'.format(child.attrib[attr_name]))
        except Exception:
            print(' |-->  false')
            fd.write(' |-->  false\n')


def get_apk_list(data_list=[], search=''):
    print('===================================')
    pack_list = []
    if not data_list:
        result_list = subprocess.check_output('adb shell pm list package -f | grep -i /data/app').strip().split(b'\n')
        if result_list:
            for i, pack in enumerate(result_list):
                pack = pack.decode('utf-8').replace('package:', '').split('=')
                pack_dic = {'num': i, 'name': pack[1], 'path': pack[0]}
                pack_list.append(pack_dic)
                print('{}. {}'.format(i, pack[1]))
    else:
        for data in data_list:
            if search.lower() in data['name'].lower():
                pack_list.append(data)
                print('{}. {}'.format(data['num'], data['name']))
    return pack_list


def apk_list(job):
    pack_list = get_apk_list()

    input_txt = 0
    while(input_txt != ''):
        print('===================================')
        print('Input APK Number or Filtering String (Cancle : Enter, a : All List)')
        input_txt = input('>>  ')
        if input_txt == '':
            continue
        elif input_txt == 'a':
            get_apk_list(pack_list, '') 
        else:
            try:
                input_txt = int(input_txt)
                name = pack_list[input_txt]['name']
                path = pack_list[input_txt]['path']
                if job == 1:
                    pull_apk(name, path)
                elif job == 2:
                    pull_db_file(name)
                elif job == 3:
                    pull_apk(pack_list[input_txt][1], pack_list[input_txt][0])
                    pull_db_file(name)
                break
            except Exception:
                get_apk_list(pack_list, input_txt)  


def pull_apk(name, path):
    print('[-] Pulling APK File... : {}'.format(name))
    os.system('adb pull {}'.format(path))
    print('[+] Pulling Finished!')


def pull_db_file(name):
    print('[-] Pulling DB and shared_prefs File... : {}'.format(name))
    os.system('adb pull /data/data/{}/databases'.format(name))
    os.system('adb pull /data/data/{}/shared_prefs'.format(name))
    print('[+] Pulling Finished!')


def debuggable_apk_list():
    print('===================================')
    result_list = subprocess.check_output('adb shell cat /data/system/packages.list | grep "1 /"', shell=True).strip().split(b'\n')
    if result_list:
        for i, result in enumerate(result_list):
            result = result.decode('utf-8')
            print(i, result.split()[0])
        print('===================================')
    else:
        print('No Debuggable APK!')


def check():
    print("""\
1. Pull APK File
2. Pull DB, Shared Preferences File
3. Pull 1 + 2 (APK, DB)
4. Check Debuggable APK List
===================================""")
    try:
        job = int(input('Select Number : '))
        job = int(job)
        if job == 1 or job == 2 or job == 3:
            apk_list(job)
        elif job == 4:
            debuggable_apk_list()
        else:
            print('Invalid Input Number')
    except Exception:
        print('Input Error!')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Easy APK Tool')
    parser.add_argument('-d', '--decode', dest='apk_for_decode', help='Decode APK file')
    parser.add_argument('-b', '--build', dest='source_dir', help='Build app source to APK and sign')
    parser.add_argument('-s', '--sign', dest='apk_for_sign', help='Sign APK file')
    parser.add_argument('-j', '--jar', dest='dex_file', help='Convert to DEX(APK) to JAR')
    parser.add_argument('-u', '--unzip', dest='apk_for_unzip', help='Unzip APK file')
    parser.add_argument('--tool', action='store_true', help='Tool for Pulling APK, DB file etc')

    args = parser.parse_args()
    os_type = os.name

    if len(sys.argv) == 1:
        parser.print_help()
        exit()

    # Pull APK file
    if args.tool:
        check()

    # Decode
    elif args.apk_for_decode:
        apk_file = os.path.abspath(args.apk_for_decode)
        decode_apk(apk_file)
        print_apk_info(apk_file.rstrip('.apk'))

    # Build
    elif args.source_dir:
        source_dir = os.path.abspath(args.source_dir)
        build_apk(source_dir)

    # Sign
    elif args.apk_for_sign:
        apk_file = os.path.abspath(args.apk_for_sign)
        sign_apk(apk_file)

    # Unzip
    if args.apk_for_unzip:
        apk_file = os.path.abspath(args.apk_for_unzip)
        unzip_apk(apk_file)

    # dex2jar
    if args.dex_file:
        print('dex hello')
        apk_file = os.path.abspath(args.dex_file)
        dex2jar(apk_file)
