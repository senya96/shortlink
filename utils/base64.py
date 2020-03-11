import random

base64_chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'


def get_base64_string(l=6):
    arr = list()
    for i in range(l):
        arr.append(random.choice(base64_chars))
    return ''.join(arr)
