# coding: utf-8

import unicodedata
from xml.etree import cElementTree
from collections import defaultdict


def xml_to_dict(xml):
    def etree_to_dict(t):
        d = {t.tag: {} if t.attrib else None}
        children = list(t)
        if children:
            dd = defaultdict(list)
            for dc in map(etree_to_dict, children):
                for k, v in dc.items():
                    dd[k].append(v)
            d = {t.tag: {k:v[0] if len(v) == 1 else v for k, v in dd.items()}}
        if t.attrib:
            d[t.tag].update(('@' + k, v) for k, v in t.attrib.items())
        if t.text:
            text = t.text.strip()
            if children or t.attrib:
                if text:
                  d[t.tag]['#text'] = text
            else:
                d[t.tag] = text
        return d
    return etree_to_dict(cElementTree.XML(xml))


def format_text(text):
    text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('ascii')
    return text.replace(' ', '').lower()
