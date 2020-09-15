#!/usr/bin/python
import json
from www_1881 import *

if __name__ == "__main__":
    C = Handler()
    cont = C.Execute("John", "", "", "https://lambda.com")
    # cont = C.Execute("aHR0cHM6Ly93d3cuMTg4MS5uby9lbnRyZXByZW5vZXIvZW50cmVwcmVub2VyLXJvZ2FsYW5kL2VudHJlcHJlbm9lci1uZWRyZS12YXRzL2pvaG4tZWlrYW5lc18zMDUxNTQzNVMxLz9xdWVyeT1qb2hu", "overview", "", "https://lambda.com")

    try:
        print(json.dumps(cont, indent=2, ensure_ascii=False))
    except Exception as e:
        print(cont)

