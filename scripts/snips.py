#!/usr/bin/env python3

import re
import os
import sys
import util
import glob
import json
import shutil
import argparse 
from datetime import datetime

parser = argparse.ArgumentParser(description='Tool for generating VS Code snippets and markdown documentation for AtherysScript.')
parser.add_argument("dir", help="the project's source directory", type=str)
parser.add_argument("output", help="the name of the json output file", type=str)
parser.add_argument("-o", "--old", help="previous version of the snippets or docs, to preserve", type=str)

args = parser.parse_args()

javaFunctions = dict()
jsFunctions = dict()

for root, dirs, files in os.walk(args.dir):
    for name in files:
        if name == 'DialogMsg.java':
            continue
        path = os.path.join(root, name)
        with open(path) as f:
            contents = f.read()
        lines = util.findFunctions(contents)
        for line in lines:
            if not '"' in line:
                continue
            functionName = util.getName(line)

            javaFileName = util.getJavaFile(line)
            if "Event" in javaFileName:
                jsFunctions[functionName] = {
                    'parameters': 'Consumer',
                    'returnType': 'boolean',
                    'module': 'event'
                }
            else:
                javaFunctions[util.getJavaFile(line)] = functionName

for root, dirs, files in os.walk(args.dir):
    for name in files:
        if name in javaFunctions:
            path = os.path.join(root, name)
            with open(path) as javaFile:
                contents = javaFile.read()
            method = util.getMethod(contents, path)
            if method is not None:
                jsFunctions[javaFunctions[name]] = util.getMethod(contents, path)

jsonOut = open(args.output + '.json', 'w')
snippets = dict()

for name, method in jsFunctions.items():
    snippets[name] = (util.toJson(name, method['parameters'])) 
jsonOut.write(json.dumps(snippets, indent=3))
jsonOut.close()

print("Functions found:", len(jsFunctions))
