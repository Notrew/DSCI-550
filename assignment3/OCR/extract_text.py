import functools as fc
import json
from time import sleep
from PIL import Image
import pytesseract
import os
from typing import Tuple
import multiprocessing as mp


class GetText():
    pic_path = "./data/"

    def __init__(self) -> None:
        self.args = []
        pass

    def split_file_name(self, file_name: str) -> Tuple[str,str]:
        base, ext = file_name.split(".")
        return base, ext

    def dir_func(self, dir:str):
        print(f"[INFO] Processing dir:{dir}")

        file_names = os.listdir(f"./data/{dir}")
        for i in range(len(file_names)):
            name = file_names[i]
            print(f"\r---->Processing {i+1}/{len(file_names)} -> {(i+1)/len(file_names)*100:.2f}%", end="")
            self.args.append((name, dir))
        print("   √ done.")
        return 0

def get_text(self , file_name, dir, result, lock):
        date, ext = self.split_file_name(file_name)
        part_string = []
        image= Image.open(f"./data/{dir}/{file_name}")
        num = image.height//3000
        for i in range(num):
            part = image.crop((0,3000*(i),1000,3000*(i+1) if (i+1)!=num else image.height ))
            vcode=pytesseract.image_to_string(part)
            part_string.append(vcode)
        lock.acquire()
        if "dir" in result: tmp = result[dir]
        else: tmp = {}
        tmp[date] = fc.reduce(lambda x,y:x+y,part_string,"")
        result[dir] = tmp
        lock.release()
        return

def save_result(path: str, result: dict) -> None:
    print("[INFO] Saving results...", end="")
    with open(path, "w") as f:
        json.dump(result, f)
    print("   √ done.")

def main() ->None:
    a = GetText()
    manager = mp.Manager()
    pool = mp.Pool(8)
    result = manager.dict()
    lock = manager.Lock()

    dirs = os.listdir("./data/")
    list( map(a.dir_func, dirs) )
    ags = tuple(map(lambda x: (a, x[0], x[1], result, lock), a.args))
    progress = []
    for args in ags:
        progress.append(pool.apply_async(func= get_text, args=args))
    pool.close()
    while (len(progress)):
        finished = len(ags)-len(progress)
        print(f"\r[INFO] Retrieving Text...{(finished+1)/len(ags)*100:.2f}% ({finished+1}/{len(ags)})", end="")
        for i in progress:
            if i.ready():
                progress.remove(i)
        sleep(5)
    pool.join()
    print("   √ done.")
    save_result("./result.json", dict(result))
    print("[INFO] All finished.")

if __name__ == "__main__":
    main()



