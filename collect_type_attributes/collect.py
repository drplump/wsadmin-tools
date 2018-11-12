# -*- coding: utf-8 -*-

'''
The code below looks terrible
Need to use Python 2.1 impose its own limitations.
'''

import re
import os

global AdminConfig

def write_csv(target, body):
    ''' Write attributes to formatted .csv file '''
    if '.csv' != target.lower()[len(target)-4:]:
        target += '.csv'
    f = open(target, 'w')
    try:
        template = '"%(name)s"; "%(type)s"; "%(islist)s"; "%(isreference)s"; "%(isrequired)s"; "%(isbase)s"; "%(default_value)s"; "%(variants)s"; "%(position)s"\n'
        f.write('"name"; "type"; "list"; "reference"; "required"; "base"; "default-value"; "variants"; "position"\n')
        for a in body:
            f.write(template % a)
    finally:
        f.close()


def write_json(target, body):
    ''' Write attributes to formatted .json file '''
    if '.json' != target.lower()[len(target)-5:]:
        target += '.json'
    f = open(target, 'w')
    try:
        template = '    "name": "%(name)s",\n' \
                   '    "type": "%(type)s",\n' \
                   '    "list": %(islist)s,\n' \
                   '    "reference": %(isreference)s,\n' \
                   '    "required": %(isrequired)s,\n' \
                   '    "base": %(isbase)s,\n' \
                   '    "default-value": "%(default_value)s",\n' \
                   '    "variants": "%(variants)s",\n' \
                   '    "position": %(position)s\n'
        f.write('[\n')
        for a in body:
            f.write('  {\n')
            f.write(template % a)
            if body.index(a) < len(body) - 1:
                f.write('  },\n')
            else:
                f.write('  }\n')
        f.write(']\n')
    finally:
        f.close()


def generate_attributes(type_list, dest_path):
    '''
    Collect type attributes and store it
    :param type_list: list of configuration object types
    :param dest_path: path to store attribute collection
    '''
    for type_name in type_list:
        attributes = []
        required = [re.compile('\s+').split(a) for a in AdminConfig.required(type_name).splitlines() if a.find('WASX7361I') < 0]
        defaults = [re.compile('\s+').split(a) for a in AdminConfig.defaults(type_name).splitlines()]
        for string in AdminConfig.attributes(type_name).splitlines():
            attribute_name = string[:string.find(' ')]
            attribute_desc = string[len(attribute_name):].strip()
            ## conditional expression added in python 2.5 .. sadly
            if attribute_desc.find('(') >= 0:
                attribute_type = attribute_desc[:attribute_desc.find('(')]
            else:
                attribute_type = attribute_desc
            attribute_type = attribute_type.replace('*', '').replace('@','').strip()
            if attribute_desc.find('(') >= 0:
                attribute_variants = attribute_desc[attribute_desc.find('(')+1:attribute_desc.find(')')].replace(' ', '').split(',')
            else:
                attribute_variants = []
            if attribute_desc.find('*') < 0:
                attribute_list = 'false'
            else:
                attribute_list = 'true'
            if attribute_desc.find('@') < 0:
                attribute_ref = 'false'
            else:
                attribute_ref = 'true'

            attribute_required = 'false'
            for r in required:
                if r[0] == attribute_name:
                    attribute_required = 'true'
            attribute_default_value = ''
            attribute_position = -1
            pos = 0
            for d in defaults:
                if d[0] == attribute_name:
                    attribute_default_value = d[2]
                    attribute_position = pos
                pos += 1
            if attribute_type in type_list:
                attribute_base = 'true'
            else:
                attribute_base = 'false'
            attributes.append(
                {
                    'name': attribute_name,                     # attribute name
                    'type': attribute_type,                     # attribute type
                    'islist': attribute_list,                   # attribute represents a collection of objects
                    'isreference': attribute_ref,               # attribute represents a reference to another object
                    'isrequired': attribute_required,           # attribute is required
                    'isbase': attribute_base,                   # attribute type represents a base type
                    'default_value': attribute_default_value,   # default value for attribute (can by empty)
                    'variants': ','.join(attribute_variants),   # attribute possible values
                    'position': attribute_position              # attribute sort position (-1 fro unknown position)
                }
            )
            write_csv('%s/%s' % (dest_path, type_name), attributes)
            write_json('%s/%s' % (dest_path, type_name), attributes)


if __name__ == "__main__":
    type_list = [t for t in AdminConfig.types().splitlines() if t.find('.') < 0]
    dest_path = './out'

    ## prepare workspace
    if os.path.isdir(dest_path):
        for c in os.listdir(dest_path):
            os.unlink('%s/%s' % (dest_path, c))
    else:
        os.mkdir(dest_path)

    ## write attributes to files
    generate_attributes(type_list, dest_path)
