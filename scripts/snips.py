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
parser.add_argument("-s", "--snips", default=None, help="Generate VS Code snippets", action="store_true")
parser.add_argument("-d", "--docs", default=None, help="Generate documentation", action="store_true")

args = parser.parse_args()

if not (args.docs or args.snips):
    print("Choose either documentation or snippets to generate.")
    quit()

if args.snips and args.docs:
    print("Cannot generate both documentation and snippets at once.")
    quit()

if args.old and not (args.snips or args.docs):
    print("Cannot use old file if not generating documentation or snippets.")
    quit()

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
            method = util.getMethod(contents, path)
            if method is not None:
                jsFunctions[javaFunctions[name]] = util.getMethod(contents, path)

if args.snips:
    jsonOut = open(args.output + '.json', 'w')
    snippets = dict()

    for name, method in jsFunctions.items():
        snippets[name] = (util.toJson(name, method['parameters'])) 
    jsonOut.write(json.dumps(snippets, indent=3))
    jsonOut.close()

if args.docs:
    modules = util.getModules(jsFunctions)
    moduleFiles = dict()
    if os.path.exists('docs'):
        shutil.rmtree('docs')
    os.mkdir('docs') 
    moduleFiles = dict()
    if args.old:
        try:
            oldDocs = list()
            oldModules = set()
            for file in glob.glob(os.path.join(args.old, "*.md")):
                fileContent = open(file).read()
                result = re.findall("module:.*", fileContent, re.IGNORECASE)
                if len(result) > 0:
                    module = result[0].split(' ')[1]
                    print(module)
                else:
                    continue
                oldDocs.append(file)
                oldModules.add(module)
                print(modules)
                if module in modules:
                    print(file)
                    shutil.copy(file, 'docs/' + module + '-functions.md')
                    moduleFiles[module] = open('docs/' + module + '-functions.md', 'a')
                for method in re.findall("^## .*", fileContent, re.MULTILINE):
                    if method.split(' ')[1] in jsFunctions:
                        del jsFunctions[method.split(' ')[1]]
                
        except IOError:
            print('File not found: ', args.old)
            quit()

        conModules = oldModules.intersection(modules)
    for module in modules:
        if module not in conModules:
           moduleFiles[module] = open('docs/' + module + '-functions.md', 'w') 
    for name, method in jsFunctions.items(): 
        out = moduleFiles[method['module']]
        out.write('## ' + name + '\n\n')
        out.write('### Signature:\n')
        out.write('```javascript\n ' + method['returnType'] + ' ' + name + '(')
        i = 1
        for parameter in method['parameters']:
            out.write(parameter)
            if i < len(method['parameters']):
                out.write(', ')
        out.write(')\n')
        out.write('```\n\n')
    for file in moduleFiles:
        moduleFiles[file].close()
