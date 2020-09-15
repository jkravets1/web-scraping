#!/usr/bin/python
import json
from peoplelooker import *

if __name__ == "__main__":
    C = Handler()
    cont = C.Execute("John Smith", "", "", "https://lambda.com")
    # cont = C.Execute("aHR0cHM6Ly93d3cucGVvcGxlbG9va2VyLmNvbS9OX01EQXlNell6TlRNNU9UYzFxPT9Kb2huIFNtaXRo", "overview", "", "https://lambda.com")

    try:
        print(json.dumps(cont, indent=2, ensure_ascii=False))
    except Exception as e:
        print(cont)

