#!/usr/bin/python3
import os
import sys
import glob
import shutil


from tools import routine_cmd, simplify


def main():
    destdir = os.getenv('DEPLOYDIR').strip().rstrip('/')
    fconfig = os.getenv('FILE').strip()
    fclone = fconfig.split('.')[0] + '.clone.sh'
    if not os.path.exists(fc1 := f'{destdir}/{fclone}'):
        fc1 = f'{destdir}/1.clone.sh'
    with open(fc2 := f'{destdir}/{fconfig}') as f:
        text1 = f.readlines()
    i = 0
    for t in text1:
        if 'CONFIG_TARGET_' in t and 'DEVICE' in t:
            s = i + 1
        elif '# Applications' in t:
            e = i
            break
        i += 1
    for t in text1[s:e]:
        if t.strip():
            break
        else:
            s += 1
    for t in reversed(text1[s:e]):
        if t.strip():
            break
        else:
            e -= 1
    if s == e:
        extra_t = None
    else:
        extra_t = text1[s:e]
    routine_cmd.gen_dot_config(fc1, fc2)
    simplify.simplify_config(fc2, remain_text=extra_t)
    # 移动.fullbak到backups目录
    if not os.path.exists(d1 := f'{destdir}/backups'):
        os.makedirs(d1)
    shutil.move(f'{fc2}.fullbak', f'{d1}/{fconfig}.fullbak')
    # 仅保留本次刷新的.config和.config.fullbak
    for item in glob.glob(f'{destdir}/**', recursive=True):
        if not os.path.isdir(item) and fconfig not in item:
            os.remove(item)


if __name__ == '__main__':
    main()

