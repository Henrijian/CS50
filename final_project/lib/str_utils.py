def remain_letter(in_str, ignore=[]):
    out_str = ""
    for char in in_str:
        if (char.isalpha()) or (char in ignore):
            out_str += char
    return out_str
