import json
prefixForm = 'prefix: {prefix}'
paramForm = '${{{index}:{name}}}'
bodyForm = '{name}({params})'

def formatNormal(name, parameters):
    params = '' 
    index = 1
    for t, param in parameters.items():
        params += paramForm.format(index=index, name=param)
        index += 1
    function = dict()
    function['prefix'] = name
    function['body'] = bodyForm.format(name=name, params=params)
    function['description'] = ""
    return json.dumps({name: function})
    
def formatListener(name):
    function = dict()
    function['prefix'] = name
    function['body'] = (name + '(function(event) {', '    $0', '}')
    function['description'] = ''
    return json.dumps({name: function})
