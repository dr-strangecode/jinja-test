# -*- coding: utf-8 -*-
# tags_list.py - filters from saltstack.salt.salt.utils.jinja.py

def list_with_tag(dct,tag):
    '''
    creates a list from a dict with each element having a tag

    .. code-block:: yaml

    items:
      item1:
        - tag1
        - tag2
      item2:
        - tag1
    
    .. code-block:: jinja

    {{ items | list_on_tag(tag1) }}

    .. code-block:: text

    [item1, item2]
    '''
    if isinstance(dct, dict) and isinstance(tag,str):
        return [k for k,v in dct.iteritems() if tag in v]
    return dct

def install(env):
    env.filters['list_with_tag'] = list_with_tag
