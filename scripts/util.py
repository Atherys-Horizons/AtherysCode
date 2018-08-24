import json
prefixForm = 'prefix: {prefix}'
paramForm = '${{{index}:{name}}}'
bodyForm = '{name}({params})'

def toJson(name, parameters):
    if name.startswith('on'):
        return listenerToJson(name)
    else:
        return normalToJson(name, parameters)

def normalToJson(name, parameters):
    params = '' 
    if len(parameters[0]) > 0:
        index = 1
        for param in parameters:
            params += paramForm.format(index=index, name=param.split(' ', 1)[1])
            if index < len(parameters):
                params += ', '
            index += 1

    function = {
        'prefix': name,
        'body': bodyForm.format(name=name, params=params),
        'description': ''
    }
    return function
    
def listenerToJson(name):
    function = {
        'prefix': name,
        'body': (name + '(function(event) {', '    $0', '}'),
        'description': ''
    }
    return function

def getJavaFile(line):
    javaResult = re.search(r'new (.*)(\<|\()', line)
    javaFile = javaResult.group(1).replace('<>', '') + '.java'
    return javaFile

def getMethod(javaContents, path):
    methodSig = re.search('p.*( apply| get| accept| test).*$', javaContents, re.MULTILINE).group(0)
    parameters = methodSig[methodSig.find("(")+1:methodSig.find(")")]
    path = path.replace('\\', '/')
    method = {
        'parameters': parameters.split(', '),
        'returnType': methodSig.split(' ')[1],
        'module': path.split('/')[-2]
    }
    return method

def findFunctions(fileContent):
    return re.findall("library.put.*$", contents, flags=re.MULTILINE|re.IGNORECASE)

def getName(line):
    return re.search('"(.*)"', line).group(1)

