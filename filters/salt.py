# -*- coding: utf-8 -*-
# salt.py - filters from saltstack.salt.salt.utils.jinja.py

import re
import uuid

def skip_filter(data):
    '''
    Suppress data output

    .. code-balock:: yaml

        {% my_string = "foo" %}

        {{ my_string|skip }}

    will be rendered as empty string,

    '''
    return ''

def ensure_sequence_filter(data):
    '''
    Ensure sequenced data.

    **sequence**

        ensure that parsed data is a sequence

    .. code-block:: jinja

        {% set my_string = "foo" %}
        {% set my_list = ["bar", ] %}
        {% set my_dict = {"baz": "qux"} %}

        {{ my_string|sequence|first }}
        {{ my_list|sequence|first }}
        {{ my_dict|sequence|first }}


    will be rendered as:

    .. code-block:: yaml

        foo
        bar
        baz
    '''
    if not isinstance(data, (list, tuple, set, dict)):
        return [data]
    return data

def to_bool(val):
    '''
    Returns the logical value.

    .. code-block:: jinja

        {{ 'yes' | to_bool }}

    will be rendered as:

    .. code-block:: text

        True
    '''
    if val is None:
        return False
    if isinstance(val, bool):
        return val
    if isinstance(val, (six.text_type, six.string_types)):
        return val.lower() in ('yes', '1', 'true')
    if isinstance(val, six.integer_types):
        return val > 0
    if not isinstance(val, collections.Hashable):
        return len(val) > 0
    return False

def quote(txt):
    '''
    Wraps a text around quotes.

    .. code-block:: jinja

        {% set my_text = 'my_text' %}
        {{ my_text | quote }}

    will be rendered as:

    .. code-block:: text

        'my_text'
    '''
    return pipes.quote(txt)

def regex_escape(value):
    return re.escape(value)

def regex_search(txt, rgx, ignorecase=False, multiline=False):
    '''
    Searches for a pattern in the text.

    .. code-block:: jinja

        {% set my_text = 'abcd' %}
        {{ my_text | regex_search('^(.*)BC(.*)$', ignorecase=True) }}

    will be rendered as:

    .. code-block:: text

        ('a', 'd')
    '''
    flag = 0
    if ignorecase:
        flag |= re.I
    if multiline:
        flag |= re.M
    obj = re.search(rgx, txt, flag)
    if not obj:
        return
    return obj.groups()

def regex_match(txt, rgx, ignorecase=False, multiline=False):
    '''
    Searches for a pattern in the text.

    .. code-block:: jinja

        {% set my_text = 'abcd' %}
        {{ my_text | regex_match('^(.*)BC(.*)$', ignorecase=True) }}

    will be rendered as:

    .. code-block:: text

        ('a', 'd')
    '''
    flag = 0
    if ignorecase:
        flag |= re.I
    if multiline:
        flag |= re.M
    obj = re.match(rgx, txt, flag)
    if not obj:
        return
    return obj.groups()

def regex_replace(txt, rgx, val, ignorecase=False, multiline=False):
    r'''
    Searches for a pattern and replaces with a sequence of characters.

    .. code-block:: jinja

        {% set my_text = 'lets replace spaces' %}
        {{ my_text | regex_replace('\s+', '__') }}

    will be rendered as:

    .. code-block:: text

        lets__replace__spaces
    '''
    flag = 0
    if ignorecase:
        flag |= re.I
    if multiline:
        flag |= re.M
    compiled_rgx = re.compile(rgx, flag)
    return compiled_rgx.sub(val, txt)

def uuid_(val):
    '''
    Returns a UUID corresponding to the value passed as argument.

    .. code-block:: jinja

        {{ 'example' | uuid }}

    will be rendered as:

    .. code-block:: text

        f4efeff8-c219-578a-bad7-3dc280612ec8
    '''
    return six.text_type(
        uuid.uuid5(
            GLOBAL_UUID,
            salt.utils.stringutils.to_str(val)
        )
    )

def unique(values):
    '''
    Removes duplicates from a list.

    .. code-block:: jinja

        {% set my_list = ['a', 'b', 'c', 'a', 'b'] -%}
        {{ my_list | unique }}

    will be rendered as:

    .. code-block:: text

        ['a', 'b', 'c']
    '''
    ret = None
    if isinstance(values, collections.Hashable):
        ret = set(values)
    else:
        ret = []
        for value in values:
            if value not in ret:
                ret.append(value)
    return ret

def lst_min(obj):
    '''
    Returns the min value.

    .. code-block:: jinja

        {% set my_list = [1,2,3,4] -%}
        {{ my_list | min }}

    will be rendered as:

    .. code-block:: text

        1
    '''
    return min(obj)

def lst_max(obj):
    '''
    Returns the max value.

    .. code-block:: jinja

        {% my_list = [1,2,3,4] -%}
        {{ set my_list | max }}

    will be rendered as:

    .. code-block:: text

        4
    '''
    return max(obj)

def lst_avg(lst):
    '''
    Returns the average value of a list.

    .. code-block:: jinja

        {% my_list = [1,2,3,4] -%}
        {{ set my_list | avg }}

    will be rendered as:

    .. code-block:: yaml

        2.5
    '''
    if not isinstance(lst, collections.Hashable):
        return float(sum(lst)/len(lst))
    return float(lst)

def union(lst1, lst2):
    '''
    Returns the union of two lists.

    .. code-block:: jinja

        {% my_list = [1,2,3,4] -%}
        {{ set my_list | union([2, 4, 6]) }}

    will be rendered as:

    .. code-block:: text

        [1, 2, 3, 4, 6]
    '''
    if isinstance(lst1, collections.Hashable) and isinstance(lst2, collections.Hashable):
        return set(lst1) | set(lst2)
    return unique(lst1 + lst2)

def intersect(lst1, lst2):
    '''
    Returns the intersection of two lists.

    .. code-block:: jinja

        {% my_list = [1,2,3,4] -%}
        {{ set my_list | intersect([2, 4, 6]) }}

    will be rendered as:

    .. code-block:: text

        [2, 4]
    '''
    if isinstance(lst1, collections.Hashable) and isinstance(lst2, collections.Hashable):
        return set(lst1) & set(lst2)
    return unique([ele for ele in lst1 if ele in lst2])

def difference(lst1, lst2):
    '''
    Returns the difference of two lists.

    .. code-block:: jinja

        {% my_list = [1,2,3,4] -%}
        {{ set my_list | difference([2, 4, 6]) }}

    will be rendered as:

    .. code-block:: text

        [1, 3, 6]
    '''
    if isinstance(lst1, collections.Hashable) and isinstance(lst2, collections.Hashable):
        return set(lst1) - set(lst2)
    return unique([ele for ele in lst1 if ele not in lst2])

def symmetric_difference(lst1, lst2):
    '''
    Returns the symmetric difference of two lists.

    .. code-block:: jinja

        {% my_list = [1,2,3,4] -%}
        {{ set my_list | symmetric_difference([2, 4, 6]) }}

    will be rendered as:

    .. code-block:: text

        [1, 3]
    '''
    if isinstance(lst1, collections.Hashable) and isinstance(lst2, collections.Hashable):
        return set(lst1) ^ set(lst2)
    return unique([ele for ele in union(lst1, lst2) if ele not in intersect(lst1, lst2)])

def install(env):
    env.filters['skip_filter'] = skip_filter
    env.filters['ensure_sequence_filter'] = ensure_sequence_filter
    env.filters['to_bool'] = to_bool
    env.filters['quote'] = quote
    env.filters['regex_escape'] = regex_escape
    env.filters['regex_search'] = regex_search
    env.filters['regex_match'] = regex_match
    env.filters['regex_replace'] = regex_replace
    env.filters['uuid_'] = uuid_
    env.filters['unique'] = unique
    env.filters['lst_min'] = lst_min
    env.filters['lst_max'] = lst_max
    env.filters['lst_avg'] = lst_avg
    env.filters['union'] = union
    env.filters['intersect'] = intersect
    env.filters['difference'] = difference
    env.filters['symmetric_difference'] = symmetric_difference
