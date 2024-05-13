#!/usr/bin/env python3

key = [99, 9, 61, 110, 94, 114, 119, 194, 42, 163, 63, 8, 97, 114, 131, 41]
with open("enc.key", "wb") as f:
    f.write(bytes(key))
