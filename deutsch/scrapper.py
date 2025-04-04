import time

import requests
from bs4 import BeautifulSoup


def func(n, o=0):
    with open("./d", "r", encoding="utf-8") as f:
        r = f.read().split("\n")

    with open(f"./x{n}", "r", encoding="utf-8") as f:
        d = eval(f.read() or '{}')

    for i in r[n:]:
        n += 1
        try:
            res = requests.get(f"https://context.reverso.net/traduction/allemand-francais/{i}",
                               headers={"Connection": "keep-alive",
                                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0"})
            if res.status_code != 200:
                print(i, res.status_code)
                continue
            soup = BeautifulSoup(res.text, "html.parser")
            r2 = []
            r3 = []
            for val in soup.select("a.translation.ltr:not(.translation-hidden)"):
                r2.append(val.attrs["data-term"])
            for val in soup.select("div.example"):
                r3.append([
                    val.select_one(" span.text[lang=de]").text.replace("\n", "").replace("\r", "").strip(),
                    val.select_one(" span.text:not([lang=de])").text.replace("\n", "").replace("\r", "").strip()
                ])
            d[i] = {"translations": r2, "context": r3}
            print(f"[{n} / {len(r)}]", i, "ok")
        except Exception as e:
            break

    with open(f"./x{n}", "w+", encoding="utf-8") as f:
        f.write(str(d))

    if n < len(r):
        time.sleep(100)
        func(n)


def func2():
    with open("x2015", "r", encoding="utf-8") as f:
        d = eval(f.read())

    r = d.copy()
    for k, v in d.items():
        if not v['translations']:
            r.pop(k)
    with open("x_final", "w+", encoding="utf-8") as f:
        f.write(str(r))


func2()
