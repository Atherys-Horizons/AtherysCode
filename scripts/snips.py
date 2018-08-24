import re
import os
import sys
import util
import json
import argparse 

parser = argparse.ArgumentParser(description='''Tool for generating VS Code snippets and markdown documentation for AtherysScript. 
                                              By default will generate the json information for every function from the given directory.''')
parser.add_argument("dir", help="the project's source directory", type=str)
parser.add_argument("output", help="the name of the json output file", type=str)
parser.add_argument("-o", "--old", help="previous version of the snippets, to preserve", type=str)
parser.add_argument("-s", "--snips", help="Generate VS Code snippets", action='store_true')
parser.add_argument("-d", "--docs", help="Generate documentation", action='store_true')

args = parser.parse_args()

javaFunctions = dict()
jsFunctions = dict()

if args.old and args.snips:
    try:
        oldFile = open(args.old)
    except IOError:
        print('File not found:', args.old)
        quit()

    try:
        snippets = json.loads(oldFile.read())
        oldFile.close()
        os.rename(args.old, args.output + '.json')
        jsonOut = open(args.output + '.json', 'w')
    except json.decoder.JSONDecodeError:
        print('Could not decode json from:', args.old)
        quit()
else:
    jsonOut = open(args.output + '.json', 'w')
    snippets = dict()

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
            if functionName in snippets:
                continue

            javaFileName = util.getJavaFile(line)
            if "Event" in javaFileName:
                jsFunctions[functionName] = {
                    'parameters': 'function',
                    'returnType': 'null',
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
            jsFunctions[javaFunctions[name]] = util.getMethod(contents, path)

out = open('directory.json', 'w')
out.write(json.dumps(jsFunctions, indent=3)) 
out.close()

if args.snips:
    for name, method in jsFunctions.items():
        snippets[name] = (util.toJson(name, method['parameters'])) 

    jsonOut.write(json.dumps(snippets, indent=3))
    jsonOut.close()
