import re
import sys
import os
import json
import argparse

def oldExists(functionName, jsonDict):
    if 

parser = argparse.ArgumentParser()
parser.add_argument("dir", help="the project's source directory", type=str)
parser.add_argument("output", help="the name of the json output file", type=str)
parser.add_argument("--old", help="previous version of the snippets, to preserve", type=str)
args = parser.parse_args()

javaFunctions = dict()
jsFunctions = dict()

if args.old:
    try:
        oldFile = open(args.old)
    except IOError:
        print('File not found:', args.old)
        quit()
    try:
        oldSnippets = json.loads(oldFile.read())
    except json.decoder.JSONDecodeError:
        print('Could not decode json from:', args.old)
        quit()


for root, dirs, files in os.walk(args.dir):
    for name in files:
        with open((os.path.join(root, name))) as f:
            contents = f.read()
        items = re.findall("library.put.*$", contents, re.MULTILINE)
        for item in items:
            functionName = re.search('"(.*)"', item).group(1)
            javaResult = re.search(r'new (.*)(\<|\()', item)
            javaFile = javaResult.group(1).replace('<>', '') + '.java'
            javaFunctions[javaFile] = functionName

for root, dirs, files in os.walk(args.dir):
    for name in files:
        if name in javaFunctions:
            with open((os.path.join(root, name))) as f:
                contents = f.read()
            methodSig = re.search('(apply|get|accept|test).*$', contents, re.MULTILINE).group(0)
            parameters = methodSig[methodSig.find("(")+1:methodSig.find(")")]
            jsFunctions[javaFunctions[name]] = parameters.split(',')

