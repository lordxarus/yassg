#!/usr/bin/env python
import sys
if "src/" not in sys.path:
    sys.path += ["src/"]
run_module("unittest discover -s test")
