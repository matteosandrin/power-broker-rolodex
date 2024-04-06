import json

FULL_TEXT = open("./power-broker-full-text.txt").read()
METADATA = json.load(open("./power-broker-metadata.json"))


def get_pages(page_nums, expand=False):
    if expand:
        page_nums = expand_page_nums(page_nums, 2)
    page_ranges = page_nums_to_page_ranges(page_nums)
    exceprts = []
    for start, end in page_ranges:
        text = get_page_range(start, end)
        exceprts.append(text)
    return exceprts


def get_page_range(start, end):
    start_loc = find_page_location(start)
    end_loc = find_page_location(end)
    return FULL_TEXT[start_loc:end_loc]


def find_page_location(page_num):
    chapter, next_chapter = None, None
    for i, c in enumerate(METADATA["chapters"]):
        if c["page"] <= page_num:
            chapter = c
            next_chapter = METADATA["chapters"][i+1]
    chapter_start, chapter_end = \
        find_chapter_location(chapter), find_chapter_location(next_chapter)
    page_count = next_chapter["page"] - chapter["page"]
    char_count = chapter_end - chapter_start
    avg_char_per_page = char_count / page_count
    if chapter["page"] == page_num:
        return chapter_start
    else:
        # the first page of each chapter has less words because of the chapter
        # title. Therefore, we need to subtract that offset from the number
        # of pages.
        return int(chapter_start + float(page_num - chapter["page"] - chapter["offset"]) * avg_char_per_page)


def find_chapter_location(chapter):
    return FULL_TEXT.find("\n\n\n\n\n" + chapter["name"])

def expand_page_nums(page_nums, expand_amount):
    expanded_page_nums = []
    for p in page_nums:
        expanded_page_nums.append(p)
        for i in range(1, expand_amount+1):
            expanded_page_nums.append(p + i)
            expanded_page_nums.append(p - i)
    expanded_page_nums = list(set(expanded_page_nums))
    return sorted(expanded_page_nums)


def page_nums_to_page_ranges(page_nums):
    page_ranges = []
    i = 0
    while i < len(page_nums):
        page_ranges.append([page_nums[i], page_nums[i]+1])
        adv = 1
        for k in range(i+1, len(page_nums)):
            if page_nums[k] == page_nums[k-1] + 1:
                page_ranges[-1][1] = page_nums[k] + 1
                adv += 1
            else:
                break
        i += adv
    return [tuple(pr) for pr in page_ranges]
