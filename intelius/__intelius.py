#!/usr/bin/python
import json
from intelius import *

if __name__ == "__main__":
    C = Handler()
    cont = C.Execute("John", "", "", "https://lambda.com")
    # cont = C.Execute("aHR0cHM6Ly9pbnRlbGl1cy5jb20vJTJGYnV5JTJGcGVvcGxlLXNlYXJjaCUyRjA2MDFOMlZUUVRXJTNGbGFzdG5hbWUlM0RKb2huJTI2c2VsZWN0ZWQtZmlyc3RuYW1lJTNESm9obiUyNnNlbGVjdGVkLWxhc3RuYW1lJTNESm9obiUyNnNlbGVjdGVkLW5hbWUlM0RKb2huLUpvaG4/Sm9obg==", "overview", "", "https://lambda.com")

    try:
        print(json.dumps(cont, indent=2, ensure_ascii=False))
    except Exception as e:
        print(cont)

