import yaml
import os
import json
from typing import Union
from io import TextIOWrapper
import importlib

class BasicRick:
    """
        A base class that creates internal structures from embedded structures.

        Args:
            base (str): String (YAML or JSON, file path to YAML/JSON file), text IO stream, dict.
            deep (bool): Internalize dictionary structures in lists.
            args (dict): Intended for extended classes to handle overriden _internalize customisation.

        Raises:
            ValueError: If the given base object can not be handled.
    """
    def _iternalize(self, dictionary : dict, deep : bool, args : dict = None):
        for k, v in dictionary.items():
            if isinstance(v, dict):
                self.__dict__.update({k:BasicRick(v, deep)})
                continue
            if isinstance(v, list) and deep:
                new_list = list()
                for i in v:
                    if isinstance(i, dict):
                        new_list.append(BasicRick(i, deep))
                    else:
                        new_list.append(i)
                self.__dict__.update({k: new_list})
                continue

            self.__dict__.update({k:v})

    def __init__(self, base : Union[dict,str,TextIOWrapper], deep : bool = False, args : dict = None):
        if isinstance(base, dict):
            self._iternalize(base, deep, args)
            return

        if isinstance(base, TextIOWrapper):
            try:
                dict_data = yaml.load(base, Loader=yaml.SafeLoader)
                self._iternalize(dict_data, deep, args)
                return
            except Exception as exc:
                print("Tried: {}".format(exc))
            try:
                dict_data = json.load(base)
                self._iternalize(dict_data, deep, args)
                return
            except Exception as exc:
                print("Tried: {}".format(exc))

        if os.path.isfile(base):
            try:
                dict_data = yaml.load(open(base, 'r'), Loader=yaml.SafeLoader)
                self._iternalize(dict_data, deep, args)
                return
            except Exception as exc:
                print("Tried: {}".format(exc))
            try:
                dict_data = json.load(open(base, 'r'))
                self._iternalize(dict_data, deep, args)
                return
            except Exception as exc:
                print("Tried: {}".format(exc))
        if isinstance(base, str):
            try:
                dict_data = yaml.safe_load(base)
                self._iternalize(dict_data, deep, args)
                return
            except Exception as exc:
                print("Tried: {}".format(exc))
            try:
                dict_data = json.loads(base)
                self._iternalize(dict_data, deep, args)
                return
            except Exception as exc:
                print("Tried: {}".format(exc))

        raise ValueError('Base object could not be internalized, type {} not handled'.format(type(base)))

    def __repr__(self):
        keys = self.__dict__
        items = ("{}={!r}".format(k, self.__dict__[k]) for k in keys if not str(k).__contains__(self.__class__.__name__) and not str(k).endswith('__meta_info') )
        return "{}({})".format(type(self).__name__, ", ".join(items))

    def __eq__(self, other):
        return repr(self) == repr(other)

    def __setitem__(self, key, item):
        self.__dict__.update( {key : item} )

    def __getitem__(self, key):
        return self.__dict__[key]

    def __len__(self):
        return len(self.__dict__)

    def __iter__(self):
        self.__n = 0
        return self

    def __next__(self):
        if self.__n < len(self.__dict__):
            name = list(self.__dict__.keys())[self.__n]
            if str(name).__contains__(self.__class__.__name__) or str(name).endswith('__n'):
                self.__n += 1
            if self.__n < len(self.__dict__):
                obj = self.__dict__[list(self.__dict__.keys())[self.__n]]
                self.__n += 1
                return obj
            else:
                raise StopIteration
        else:
            raise StopIteration

    def _recursive_search(self, dictionary, key):
        if key in dictionary:
            return dictionary[key]
        for k, v in dictionary.items():
            if isinstance(v, BasicRick):
                value = self._recursive_search(v.__dict__, key)
                if value:
                    return value
            if isinstance(v, dict):
                value = self._recursive_search(v, key)
                if value:
                    return value

    def items(self):
        """
        Iterate through all key value pairs.

        Yields:
            tuple: str, object.
        """
        for key in self.__dict__.keys():
            if str(key).__contains__(self.__class__.__name__) or str(key).endswith('__n'):
                continue
            yield key, self.__dict__[key]

    def get(self, key : str, default=None):
        """
        Employs a recursive search of structure and returns the first found key-value pair.
        Searches with normal, upper, and lower case.

        Args:
            key (str): key string being searched.
            default (any): Return value if nothing is found.

        Returns:
            obj: value found, or None for nothing found.
        """
        value = self._recursive_search(self.__dict__, key)
        if not value:
            value = self._recursive_search(self.__dict__, key.lower())
            if not value:
                value = self._recursive_search(self.__dict__, key.upper())
        if not value:
            return default
        return value

    def values(self):
        """
        Gets the higher level values of the current Rick object.

        Returns:
            list: of objects.
        """
        keys = list(self.__dict__.keys())
        objects = [self.__dict__[k] for k in keys if not str(k).__contains__(self.__class__.__name__) and not str(k).endswith('__n')]

        return objects

    def keys(self):
        """
        Gets the higher level keys of the current Rick object.

        Returns:
            list: of keys.
        """
        keys = list(self.__dict__.keys())
        keys = [k for k in keys if not str(k).__contains__(self.__class__.__name__) and not str(k).endswith('__n')]

        return keys

    def dict(self):
        """
        Deconstructs the whole object into a Python dictionary.

        Returns:
            dict: of object.
        """
        d = dict()
        for key, value in self.__dict__.items():
            if str(key).__contains__(self.__class__.__name__) or str(key).endswith('__meta_info'):
                continue
            if isinstance(value, BasicRick) or isinstance(value, PickleRick):
                d[key] = value.dict()
            elif isinstance(value, list):
                new_list = list()
                for element in value:
                    if isinstance(element, BasicRick):
                        new_list.append(element.dict())
                    else:
                        new_list.append(element)
                d[key] = new_list
            else:
                d[key] = value
        return d

    def has(self, key : str, deep=False) -> bool:
        """
        Checks whether the key exists in the object.

        Args:
            key (str): key string being searched.
            deep (bool): whether to search deeply.

        Returns:
            bool: if found.
        """
        if key in self.__dict__:
            return True
        if deep:
            value = self._recursive_search(self.__dict__, key)
            if value:
                return True
        return False

    def to_yaml_file(self, file_path : str):
        """
        Does a self dump to a YAML file.

        Args:
            file_path (str): File path.
        """
        self_as_dict = self.dict()
        with open(file_path, 'w', encoding='utf-8') as fs:
            yaml.safe_dump(self_as_dict, fs)

    def to_yaml_string(self):
        """
        Dumps self to YAML string.

        Returns:
            str: YAML representation.
        """
        self_as_dict = self.dict()
        return yaml.safe_dump(self_as_dict, None)

    def to_json_file(self, file_path: str):
        """
        Does a self dump to a JSON file.

        Args:
            file_path (str): File path.
        """
        self_as_dict = self.dict()
        with open(file_path, 'w', encoding='utf-8') as fs:
            json.dump(self_as_dict, fs)

    def to_json_string(self):
        """
        Dumps self to YAML string.

        Returns:
            str: JSON representation.
        """
        self_as_dict = self.dict()
        return json.dumps(self_as_dict)

    def add_variable(self, name, value):
        """
        Add a new member to Rick.

        Args:
            name (str): Property name.
            value (any): Value of new member.
        """
        self.__dict__.update({name: value})

class PickleRick(BasicRick):
    """
        An extended version of the BasePickleRick that can load OS environ variables and Python Lambda functions.

        Args:
            base (str): String (YAML or JSON, file path to YAML/JSON file), text IO stream, dict.
            deep (bool): Internalize dictionary structures in lists.
            load_lambda (bool): Load lambda as code or strings.
    """

    def _iternalize(self, dictionary : dict, deep : bool, args : dict = None):
        for k, v in dictionary.items():
            if isinstance(v, dict):
                if 'type' in v.keys() and v['type'] == 'env':
                    self.add_env_variable(k, v['load'], v.get('default', None))
                    continue
                if 'type' in v.keys() and v['type'] == 'lambda':
                    load = v['load']
                    imports = v.get('import', None)
                    if args and args['load_lambda']:
                        self.add_lambda(k, load, imports)
                    else:
                        self.__dict__.update({k: v})
                    continue
                if 'type' in v.keys() and v['type'] == 'function':
                    name = v.get('name', k)
                    load = v['load']
                    args_dict = v.get('args', None)
                    imports = v.get('import', None)

                    if args and args['load_lambda']:
                        self.add_function(name, load, args_dict, imports)
                    else:
                        self.__dict__.update({k: v})
                    continue
                self.__dict__.update({k:PickleRick(v, deep, args['load_lambda'])})
                continue
            if isinstance(v, list) and deep:
                new_list = list()
                for i in v:
                    if isinstance(i, dict):
                        new_list.append(PickleRick(i, deep, args['load_lambda']))
                    else:
                        new_list.append(i)
                self.__dict__.update({k: new_list})
                continue
            self.__dict__.update({k: v})

    def __init__(self, base: Union[dict, str] , deep : bool = False, load_lambda : bool = False):
        self.__meta_info = dict()
        super().__init__(base, deep, {'load_lambda' : load_lambda})

    def dict(self):
        """
        Deconstructs the whole object into a Python dictionary.

        Returns:
            dict: of object.
        """
        d = dict()
        for key, value in self.__dict__.items():
            if str(key).__contains__(self.__class__.__name__):
                continue
            if key in self.__meta_info.keys():
                d[key] = self.__meta_info[key]
            elif isinstance(value, BasicRick):
                d[key] = value.dict()
            elif isinstance(value, list):
                new_list = list()
                for element in value:
                    if isinstance(element, BasicRick):
                        new_list.append(element.dict())
                    else:
                        new_list.append(element)
                d[key] = new_list
            else:
                d[key] = value
        return d

    def add_function(self, name, load, args : dict = None, imports : list = None ):
        """
        Add a new function to Rick.

        Args:
            name (str): Property name.
            load (str): Python code containing the function.
            args (dict): Key-value pairs of arguments with default values.
            imports (list): Python modules to import.
        """
        if imports and isinstance(imports, list):
            for i in imports:
                if 'import' in i:
                    exec(i, globals())
                else:
                    exec('import {}'.format(i), globals())
        exec(load, globals())
        if args and isinstance(args, dict):
            arg_list = list()
            arg_list_defaults = list()
            for arg in args.keys():
                default_value = args[arg]
                if isinstance(default_value, str):
                    arg_list_defaults.append("{a}='{d}'".format(a=arg, d=default_value))
                else:
                    arg_list_defaults.append("{a}={d}".format(a=arg, d=default_value))
                arg_list.append('{a}={a}'.format(a=arg))

            func_string = 'lambda {args_default}: {name}({args})'.format(
                args_default=','.join(arg_list_defaults),
                args=','.join(arg_list),
                name=name)
        else:
            func_string = 'lambda: {name}()'.format(name=name)
        self.__dict__.update({name: eval(func_string)})
        self.__meta_info[name] = {'type' : 'function', 'name' : name, 'args' : args, 'import' : imports, 'load' : load}

    def add_lambda(self, name, load, imports : list = None ):
        """
        Add a Python lambda to Rick.

        Args:
            name (str): Property name.
            load (str): Python code containing the lambda.
            imports (list): Python modules to import.
        """
        if imports and isinstance(imports, list):
            for i in imports:
                if 'import' in i:
                    exec(i, globals())
                else:
                    exec('import {}'.format(i), globals())
        self.__dict__.update({name: eval(load)})
        self.__meta_info[name] = {'type' : 'lambda', 'import' : imports, 'load' : load}

    def add_env_variable(self, name, load, default = None):
        """
        Add a new OS ENVIRONMENT VARIABLE to Rick.

        Args:
            name (str): Property name.
            load (str): ENV var name.
            default (any): Default to value.
        """
        self.__dict__.update({name: os.getenv(load, default)})
        self.__meta_info[name] = {'type' : 'env', 'load' : load, 'default' : default}
