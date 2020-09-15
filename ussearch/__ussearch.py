#!/usr/bin/python
import json
from ussearch import *

if __name__ == "__main__":
    C = Handler()
    cont = C.Execute("John smith", "", "", "https://lambda.com")
    # cont = C.Execute("aHR0cHM6Ly93d3cudXNzZWFyY2guY29tL2V5SnhiMmxrSWpvaU1URTJUVFJZUmtoVU9FSWlMQ0p4WmlJNklrcHZhRzRpTENKeGJpSTZJbk50YVhSb0lpd2lZWFZuYldWdWRITndJam9pY1c5cFpEMHhNVFpOTkZoR1NGUTRRaVp4WmoxS2IyaHVKbkZ1UFZOdGFYUm9KbkZ0YVQxWEpuRmpQVTV2Y20xaGJpWnhjejFQU3laeGVqMDNNekEzTVMwek1EVTJJbjA9P0pvaG4gc21pdGg=", "overview", "", "https://lambda.com")

    try:
        print(json.dumps(cont, indent=2, ensure_ascii=False))
    except Exception as e:
        print(cont)

