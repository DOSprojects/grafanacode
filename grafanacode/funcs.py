# funcs.py
# V0.5.0 LDO 19/10/2022: initial version
# V0.5.1 LDO 12/11/2022: refactor modules
# V0.6.1 LDO 17/12/2022: release candidate 1
'''
    grafanacode: utility functions
'''

#******************************************************************************
# EXTERNAL MODULE REFERENCES
#******************************************************************************
import os
import importlib
import math
import requests

#******************************************************************************
# GENERAL HELPER FUNCTIONS
#******************************************************************************
def generateUID(alphabet=None, size=None):
    '''
    Get an UID; credits: https://github.com/puyuan/py-nanoid

    Parameters:
        alphabet (string): a string of characters allowed in the UID, defaults to '_-0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        size (int): the length of the UIT to generate, defaults to 9
    Returns:
        string: generated UID
    '''
    if alphabet is None:
        alphabet = '_-0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    alphabet_len = len(alphabet)
    if size is None:
        size = 9
    uid = ''
    mask = 1
    if alphabet_len > 1:
        mask = (2 << int(math.log(alphabet_len - 1) / math.log(2))) - 1
    steps = int(math.ceil(1.6 * mask * size / alphabet_len))
    while True:
        random_bytes = bytearray(os.urandom(steps))
        for step in range(steps):
            random_byte = random_bytes[step] & mask
            if random_byte < alphabet_len:
                if alphabet[random_byte]:
                    uid += alphabet[random_byte]
                    if len(id) >= size:
                        return uid
#******************************************************************************
def getJsonKey(jsondict):
    '''
    Get the key from a JSON dict if it exists, otherwise None

    Parameters:
        jsondict (dict): json source
    Returns:
        string: dict key or None
    '''
    if type(jsondict) != dict:
        return None
    if jsondict == {}:
        return None
    return list(jsondict.keys())[0]
#******************************************************************************
def addJsonItem(jsondict, keylist, value):
    '''
    Add an element to a JSON, eventually create parent levels

    Parameters:
        jsondict (dict): json where to add to (will be modified by function
        keylist (list): list with keys on subsequent levels
        value (any): value to add, can be bool, str, int, float, list, dict, obj, ...
    Returns:
        nothing
    '''
    if type(jsondict) is not dict:
        raise Exception(f'json is not a dict but:{type(jsondict)}')
    elif type(keylist) is not list:
        raise Exception(f'keylist is not a list but:{type(keylist)}')
    elif len(keylist) == 0:
        raise Exception(f'keylist empty; keylist:{keylist}')
    else:
        if len(keylist) == 1:
            jsondict[keylist[0]] = value
        else:
            hjson = jsondict
            for key in keylist[:-1]:
                if key not in hjson:
                    hjson[key] = {}
                hjson = hjson[key]
            hjson[keylist[-1]] = value
#******************************************************************************
def getJsonItem(jsondict, keylist, default='KEYERROR'):
    '''
    Get an element from a JSON if it exists, otherwise None

    Parameters:
        jsondict (dict): json source
        keylist (list): list with keys on subsequent levels
        default (any): KEYERROR raises exception, else default if not found
    Returns:
        any: found value or default value
    '''
    if len(keylist) == 0:
        if default == 'KEYERROR':
            raise Exception(f'key not found; keylist:{keylist}')
        return default
    else:
        if type(jsondict) != dict:
            raise Exception(f'json is not a dict; json:{jsondict}')
        if keylist[0] in jsondict:
            if len(keylist) == 1:
                return jsondict[keylist[0]]
            else:
                return getJsonItem(jsondict[keylist[0]], keylist[1:], default)
        else:
            if default == 'KEYERROR':
                raise Exception(f'key not found; keylist:{keylist}')
            return default
#******************************************************************************
def cutJsonItem(jsondict, keylist, default='KEYERROR'):
    '''
    Get an element from a JSON if it exists and delete it , otherwise None

    Parameters:
        jsondict (dict): json source; the found value will be removed
        keylist (list): list with keys on subsequent levels
        default (any): KEYERROR raises exception, else default if not found
    Returns:
        any: found value or default value
    '''
    if len(keylist) == 0:
        if default == 'KEYERROR':
            raise Exception(f'key not found; keylist:{keylist}')
        return default
    else:
        if keylist[0] in jsondict:
            if len(keylist) == 1:
                return jsondict.pop(keylist[0], default)
            else:
                return cutJsonItem(jsondict[keylist[0]], keylist[1:], default)
        else:
            if default == 'KEYERROR':
                raise Exception(f'key not found; keylist:{keylist}')
            return default
#******************************************************************************
def filterByProperty(inlist, propertyname, value):
    '''
    Filter from list by property; return a new list with the items where named property has requested value. E.g. ::

        filterByProperty([{'propX': value_1, 'a': 1}, {'propY': value_2, 'a': 2}, {'propX': value_1, 'a': 3}, {'propX': value_2, 'a': 4}], 'propX', value_1}
    
        returns: [{'propX': value_1, 'a': 1}, {'propX': value_1, 'a': 3}]

    Parameters:
        inlist (list): source list
        propertyname (str): property name
        value (any): value to compare with
    Returns:
        string: dict key or None
    '''
    retval = []
    for item in inlist:
        if propertyname in item:
            if item[propertyname]==value:
                retval.append(item)
    return retval
#**********************************************************
def deepMerge(destination, dict2add):
    '''
    Recursive merge the additional dictionary in the destination dictionary, overwrite if key exists.

    Parameters:
        destination (dict): dictionary, will be modified
        dict2add (dict): dictionary to merge, also on sublevels.
    Returns:
        nothing
    '''
    # pylint: disable=too-many-branches
    if dict2add is None:                                            # nothing to dict2add
        return
    if destination is None:                                         # no destination, so simply replace
        destination = dict2add
        return
    if isinstance(destination, (bool, int, float, str)):            # destination is simple type: replace
        destination = dict2add
        return
    if isinstance (destination, list):                              # destination is list: can dict2add to list
        if isinstance (dict2add, list):                             #   check if we want to merge lists
            if dict2add != []:                                      #     then list to merge can't be empty
                destination += dict2add
        else:                                                       #   we want to append another type to list
            destination[key].append(dict2add[key])                  # TODO: Using variable 'key' before assignment (used-before-assignment)
        return
    if isinstance (destination, dict):                              # destination is dict: can dict2add to dict
        if isinstance (dict2add, dict):                             #   check if we want to merge dicts
            if dict2add != {}:                                      #     then dict to merge can't be empty
                for key in dict2add:                                #       iterate over all items in dict2add
                    if key not in destination:                      #         if key doesn't exist in destination then simply dict2add
                        destination[key] = dict2add[key]
                        destination[key] = dict2add[key]
                    else:                                           #         if key does exist in destination then merge (iterate)
                        deepMerge(destination[key], dict2add[key])
        else:                                                       #   we can only merge dicts
            raise Exception(f'{dict2add} is not a dict but a {type(dict2add)}')

#**********************************************************
def cleanFilename(source):
    '''
    Remove invalid characters ' %:/,.\\[]<>*?' from filename

    Parameters:
        source (str): input name
    Returns:
        string: source converted to valid filename
    '''
    remove = ' %:/,.\\[]<>*?'
    return ''.join([c for c in source if c not in remove])

#******************************************************************************
# AUX FUNCTIONS
#******************************************************************************
def getPlugins():
    '''
    Get all plugins available in the /plugins map

    Parameters:
        nothing
    Returns:
        dict: dict with all available plugins
    '''
    # pylint: disable=import-outside-toplevel
    path  = os.path.dirname(__file__) + '/plugins'
    files = os.listdir(path)
    plugins = {'targets': [], 'dashboards': [], 'panels': [],}
    from inspect import getmembers, isfunction
    for fname in files:
        if len(fname)<8:
            continue
        if fname == '__init__.py' or fname[-3:]!='.py':
            continue
        name = fname[:-3]
        if len(name)>7 and name[:7] == 'target_':
            plugins['targets'].append(name)
        elif len(name)>10 and name[:10] == 'dashboard_':
            plugins['dashboards'].append(name)
        elif len(name)>6 and name[:6] == 'panel_':
            plugins['panels'].append(name)
    return plugins

#**********************************************************
def getPluginsExtract():
    '''
    Get all extract functions from the plugins available in the /plugins map

    Parameters:
        nothing
    Returns:
        dict: dict with all available extract functions
    '''
    # pylint: disable=import-outside-toplevel, too-many-nested-blocks
    path  = os.path.dirname(__file__) + '/plugins'
    files = os.listdir(path)
    plugins = {}
    from inspect import getmembers, isfunction
    for fname in files:
        if len(fname)<8:
            continue
        if fname == '__init__.py' or fname[-3:]!='.py':
            continue
        name = fname[:-3]
        if len(name)>6 and name[:6] == 'panel_':
            try:
                mod = importlib.import_module(f'grafanacode.plugins.{name}')
                funs = dir(mod)
                if 'EXTRACTCHILDCLASS' not in funs:
                    for fun in funs:
                        if len(fun)>13 and fun[:13] == 'extractPanel_':
                            plugins[fun[13:]]=name
            except ImportError as error:
                print('Error funs.getPluginsExtract: ', error)
    return plugins

#**********************************************************
def printPlugins():
    '''
    Get and print all plugins available in the /plugins map
    '''
    plugins = getPlugins()
    print('\n available plugins:')
    print('-------------------')
    print(' Targets:')
    for item in plugins['targets']:
        print(f'  {item}')
    print('-------------------')
    print(' Dashboards:')
    for item in plugins['dashboards']:
        print(f'  {item}')
    print('-------------------')
    print(' Panels:')
    for item in plugins['panels']:
        print(f'  {item}')
    print('-------------------')

#**********************************************************
# Print all plugins
def printPluginsExtract():
    '''
    Get and print all extract functions from the plugins available in the /plugins map
    '''
    plugins = getPluginsExtract()
    print('\n available extract plugins:')
    print('-------------------')
    for key, value in plugins.items():
        print(f'  {key} : {value}')
    print('-------------------')
