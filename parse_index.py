import re
import json


def parse_index(path="./power-broker-index.txt", sort=False):
    data = open(path)
    index = []

    for line in data.readlines():
        first_digit = 0
        for i, c in enumerate(line):
            if c.isdigit():
                first_digit = i
                break
        name_str, pages_str = line[:first_digit], line[first_digit:]
        name_matches = re.match(
            r"^([\w\s\-'.\(\)\-]+), ([\w\s\-'.\-]+)[,\s]+(\([\w\s\-'.\-,]+\))*", name_str)
        last_name = name_matches.group(1)
        first_name = name_matches.group(2)
        parentheses = name_matches.group(
            3) if name_matches.group(3) is not None else ''
        parentheses = parentheses.replace('(', '')
        parentheses = parentheses.replace(')', '')
        page_matches = re.findall(r"(\d+)-*(\d*)", pages_str)
        pages = []
        for m in page_matches:
            pages.append(int(m[0]))
            if len(m[1]) > 0:
                addt = list(m[0])
                start = len(addt) - len(m[1])
                for i in range(len(m[1])):
                    addt[start+i] = m[1][i]
                pages.append(int(''.join(addt)))
        index.append({
            'first': first_name,
            'last': last_name,
            'parentheses': parentheses,
            'pages': pages
        })
    if sort:
        index.sort(key=lambda x: len(x['pages']), reverse=True)
    return index

if __name__ == "__main__":
    index = parse_index(sort=True)
    with open("power-broker-index.json", "w") as f:
        json.dump(index, f, sort_keys=True, indent=2)