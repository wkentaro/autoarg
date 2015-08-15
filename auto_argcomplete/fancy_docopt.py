#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from docopt import parse_section, Option


def parse_defaults(doc, section_name=None):
    if section_name is None:
        section_name = 'options:'

    defaults = []
    for s in parse_section(section_name, doc):
        _, _, s = s.partition(':')
        split = re.split('\n[ \t]*(-\S+?)', '\n' + s)[1:]
        split = [s1 + s2 for s1, s2 in zip(split[::2], split[1::2])]
        options = [OptionWithDesc.parse(s) for s in split if s.startswith('-')]
        defaults += options
    return defaults


class OptionWithDesc(Option):
    def __init__(self, short=None, long=None,
                 argcount=0, value=False, description=None):
        assert argcount in (0, 1)
        if description is None:
            description = ''
        self.description = description
        self.short, self.long, self.argcount = short, long, argcount
        self.value = None if value is False and argcount else value

    @classmethod
    def parse(class_, option_description):
        short, long, argcount, value = None, None, 0, False
        options, _, description = option_description.strip().partition('  ')
        options = options.replace(',', ' ').replace('=', ' ')
        for s in options.split():
            if s.startswith('--'):
                long = s
            elif s.startswith('-'):
                short = s
            else:
                argcount = 1
        if argcount:
            matched = re.findall('\[default: (.*)\]', description, flags=re.I)
            value = matched[0] if matched else None
        description = description.strip()
        return class_(short, long, argcount, value, description)

    def __repr__(self):
        return 'Option(%r, %r, %r, %r, %r)' % (self.short, self.long,
                                               self.argcount, self.value,
                                               self.description)
