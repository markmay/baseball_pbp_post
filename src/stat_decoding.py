import base64

def recode(data):
    result = []
    i = len(data)

    for i in range(len(data)):
        c = data[i]
        if c >= ord('a') and c <= ord('z'):
            result.append(lower_char_change(c))
        elif c >= ord('A') and c <= ord('Z'):
            result.append(upper_char_Change(c))
        else:
            result.append(chr(c))
    return "".join(result)

def lower_char_change(ch):
    return char_change(ch, ord('a'))

def upper_char_Change(ch):
    return char_change(ch, ord('A'))

def char_change(ch, base_ch):
    return chr((ch - base_ch + 13) % 26 + base_ch)

def decode_response(data):
    return base64.b64decode(recode(data)).decode('utf-8')