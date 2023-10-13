import re

regexes = [r'[\s\-_,]', r'[\W]', r'[aieouäöü]', r'[a-z]', r'[AIEOUÄÖÜ]', r'[A-Z0-9]']
digraphs = ["ch", "gh", "gn", "kn", "ph", "qu", "sh", "th", "wh", "wr"]
diblends = ["bl", "br", "cl", "cr", "fl", "fr", "gl", "gr", "pl", "pr", "sc", "sl", "sm", "sn", "sp", "st"]
trigraphs = ["chr", "sch"]
triblends = ["shr", "spl", "spr", "squ", "str", "thr"]


def process_string(str, length=3, keep_separators=False, strict=True):
    if strict and length <= 0:
        return ""

    str = re.sub(r'^[\s\-_,]+', '', str)
    str = re.sub(r'[\s\-_,]+$', '', str)

    if length >= len(str):
        return str

    chars = list(str)
    pos = 1
    order = [pos]
    ordered_count = 1
    word = 1
    words = [1]
    sep = 0
    new_word = False
    found = False
    i = 1

    while i < len(chars):
        order.append(0)

        if re.search(regexes[0], chars[i]):
            words.append(0)
            new_word = True
            sep += 1
        else:
            if new_word:
                new_word = False
                word += 1
                pos += 1
                order[i] = pos
                ordered_count += 1

                if i < len(chars) + 2:
                    for tri in trigraphs + triblends:
                        if (
                                tri[0] == chars[i].lower()
                                and tri[1] == chars[i + 1].lower()
                                and tri[2] == chars[i + 2].lower()
                        ):
                            found = True
                            break

                if found:
                    found = False
                    pos += 1
                    order.append(pos)
                    ordered_count += 1
                    pos += 1
                    order.append(pos)
                    ordered_count += 1
                    words.extend([word, word])
                    i += 2
                elif i < len(chars) + 1:
                    for di in digraphs + diblends:
                        if (
                                di[0] == chars[i].lower()
                                and di[1] == chars[i + 1].lower()
                        ):
                            found = True
                            break

                    if found:
                        found = False
                        pos += 1
                        order.append(pos)
                        ordered_count += 1
                        words.append(word)
                        i += 1

            words.append(word)

        i += 1

    if not strict:
        should = word
        if keep_separators:
            should += sep
        if length < should:
            length = should

    if keep_separators:
        i = 0
        while i < len(chars):
            if words[i] == 0:
                order[i] = pos
                ordered_count += 1
                pos += 1
            i += 1
        pos = len(chars)
    else:
        pos = len(chars)
        i = len(chars)
        while i > 0:
            i -= 1
            if words[i] == 0:
                order[i] = pos
                ordered_count += 1
                pos -= 1

    j = 1
    unfinished = True

    while j < len(regexes) and unfinished:
        i = len(chars)
        while i > 0:
            i -= 1
            if order[i] <= 0:
                if re.search(regexes[j], chars[i]):
                    order[i] = pos
                    ordered_count += 1
                    pos -= 1
                    if ordered_count == len(chars):
                        unfinished = False
                        break
        j += 1

    chars = [val if order[i] <= length else "" for i, val in enumerate(chars)]
    return "".join(chars)
