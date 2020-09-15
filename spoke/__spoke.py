#!/usr/bin/python
import json
from spoke import *

if __name__ == "__main__":
    C = Handler()
    cont = C.Execute("John", "", "", "https://lambda.com")
    # cont = C.Execute("aHR0cDovL3d3dy5zcG9rZS5jb20vcGVvcGxlL2pvaG4tYS1tYXR0aWFjY2ktanItM2UxNDI5YzA5ZTU5N2MxMDA4OGE0Mjkw", "overview", "", "https://lambda.com")

    try:
        print(json.dumps(cont, indent=2, ensure_ascii=False))
    except Exception as e:
        print(cont)

