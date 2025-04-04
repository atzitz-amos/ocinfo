with open("x_final", "r", encoding="utf-8") as f:
    d = eval(f.read())

csv = ""

for k, v in d.items():
    csv += "; ".join(v['translations']) + "\t"
    if len(v['context']) == 0:
        csv += " \t \t"
    elif len(v['context']) == 1:
        csv += v['context'][0][1].replace("\n", " ") + "\t \t"
    else:
        csv += v['context'][0][1].replace("\n", " ") + "\t" + v['context'][1][1].replace("\n", " ") + "\t"
    csv += k + "\t"

    if len(v['context']) == 0:
        csv += " \t \t"
    elif len(v['context']) == 1:
        csv += v['context'][0][0].replace("\n", " ") + "\t \t"
    else:
        csv += v['context'][0][0].replace("\n", " ") + "\t" + v['context'][1][0].replace("\n", " ") + "\t"

    csv += "\n"

with open("x2_final.tsv", "w+", encoding="utf-8") as f:
    f.write(csv)
