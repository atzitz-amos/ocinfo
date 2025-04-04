# Script to iterate through all subfolders of this directory beginning with the letter m
DIR_PATH = r"C:\Users\amosa\OneDrive\IdeaProjects\ocinfo"

import os

dirs = []

for root, x, files in os.walk(DIR_PATH):
    for dr in x:
        if dr.startswith("m"):
            dirs.append((dr, os.path.join(root, dr)))

_g = "const MODULES = ["

names = [
    [
        "poulpes",
        "voyage d'étude"
    ],
    [],
    [],
    [],
    [
        "boucles",
        "saisie nombre",
        "for & while",
        "multiples",
        "livrets",
        "n!",
        "xoxo",
        "jeu de cartes"
    ],
    [
        "trouver élément",
        "racine cubique",
        "reunion",
        "tableaux 2D",
        "nombres pairs",
        "random",
        "corbeau",
        "corbeau stats"
    ]
]

i = 0


def do(name, path):
    global _g
    _g += f"{{name: '{name}', id: {int(name[1:])}, exercises: ["
    j = 0
    for r, _, f in os.walk(path):
        for file in f:
            if file.endswith(".html") and file not in ["edinburgh.html", "madrid.html"]:
                _g += "{id: '" + file.split("_")[1][:-5]
                try:
                    _g += f'''', name: "{names[i][j]}"}},'''
                except:
                    _g += f"', name: ''}},"
                j += 1
    _g = _g[:-1] + "]},"


for d in dirs:
    do(*d)
    i += 1

print(_g[:-1] + "]")
