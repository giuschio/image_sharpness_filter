import re
import shutil

from os.path import basename as basename

from pathlib import Path

def natural_sort(l): 
    # from here https://stackoverflow.com/questions/4836710/is-there-a-built-in-function-for-string-natural-sort
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(l, key=alphanum_key)


def import_images(fpath: str) -> list:
    images = list(Path(fpath).glob("*.jpg"))
    images += list(Path(fpath).glob("*.png"))
    images_s = [str(p) for p in images]
    return natural_sort(images_s)


def export_images(images_out, fpath):
    path = Path(fpath)
    path.mkdir(parents=True, exist_ok=True)
    for img in images_out:
        shutil.copy2(img, fpath)