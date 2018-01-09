# -*- coding: utf-8 -*-
import string
import sys

def get_content_level(strip_line):
    head, sep, tail = strip_line.partition(' ')
    num_of_sharp = len(head)  # count how many '#' there are
    section_title = tail.strip()
    return section_title, num_of_sharp - 1

def retrieve_headers(input_fn):
    headers = header('', -1, True) # the virtual root
    with open(input_fn, encoding='utf-8', mode = 'r') as md_f:
        for line in md_f:
            # print(repr(line))
            strip_line = line.strip()

            if not (len(strip_line) > 0 and strip_line[0] == '#'):
                continue

            section_title, level = get_content_level(strip_line)
            # print("print while reading the file. Section title: {}, "
            #   "level: {}".format(section_title, level))
            new_header = header(section_title, level)

            headers.absorb(new_header)

    return headers

class header():
    def __init__(self, content='', level=-1, is_virtual=False):
        # vritual header is used for the section title which
        #  directly starts from higher levels.
        self.header_title = content
        self.my_level = level  # level starts from 0.

        if level == -1:
            self.is_virtual = True
        else:
            self.is_virtual = is_virtual

        self.my_sec_num = 0
        self.child_headers = []

    def absorb(self, new_header):
        if new_header.my_level <= self.my_level:
            raise ValueError("The new header has a higher level ({}) than the"
                             " current level({}).".format(new_header.my_level,
                                                          self.my_level))

        if new_header.my_level == self.my_level + 1:
            self.child_headers.append(new_header)
        else:
            if len(self.child_headers) == 0:
                self.child_headers.append(header('', self.my_level + 1, True))

            self.child_headers[-1].absorb(new_header)

    def assign_child_sec_num(self, parent_sec_num=''):
        sec_num = 1
        for header in self.child_headers:
            if len(parent_sec_num) == 0:
                header.my_sec_num = "{:d}".format(sec_num)
            else:
                header.my_sec_num = "{:s}.{:d}".format(parent_sec_num, sec_num)

            sec_num = sec_num + 1
            header.assign_child_sec_num(header.my_sec_num)

    def get_level_symbol(self, sym):
        if not isinstance(sym, str):
            raise ValueError("Given symbol format ({}) not correct, which "
                             "must be a string.".format(sym))

        return sym * self.my_level

    def conv_title(self, header):
        if not isinstance(header, str):
            raise ValueError("Given header has type ({}). But a string is "
                             "required.".format(type(header)))

        # Lower case the string
        header = header.lower()
        # remove any punction other than hypen
        header = header.strip(string.punctuation.translate({ord('-'): None}))
        # change any space into a hypen
        header = ' '.join(header.split()).replace(' ', '-')

        return header

    def get_anchor_link(self, header, existing_anchor_links):
        new_anchor_link = self.conv_title(header)
        num_appearance = existing_anchor_links.count(new_anchor_link)
        existing_anchor_links.append(new_anchor_link)

        if num_appearance > 0:
            new_anchor_link = "{}-{}".format(new_anchor_link,
                                             str(num_appearance))

        # print("new_anchor_link: ", new_anchor_link)
        return new_anchor_link

    def gen_gfm_anchor(self, existing_anchor_links=[]):
        if self.is_virtual:
            self.anchor = None
        else:
            # Generate the link to the current header
            anchor_link = self.get_anchor_link(self.header_title,
                                               existing_anchor_links)

            # print("header_title: {}, anchor_link: {}\n".format(
            #        self.header_title, anchor_link))
            self.anchor = "[{:s}](#{:s})".format(self.header_title,
                                                 anchor_link)

        # generate the link to the child headers
        for child_header in self.child_headers:
            child_header.gen_gfm_anchor(existing_anchor_links)

    def gen_gfm_toc(self, add_sec_num=False):
        toc = []
        if not self.is_virtual and self.my_level != -1:
            if add_sec_num:
                toc.append("{} - {} {}".format(self.get_level_symbol(' '),
                                      self.my_sec_num, self.anchor))
            else:
                toc.append("{} - {}".format(self.get_level_symbol(' '),
                                            self.anchor))

        for child_header in self.child_headers:
            toc.extend(child_header.gen_gfm_toc(add_sec_num))

        return toc

    def print_headers(self, add_sec_num=False):
        if not self.is_virtual and self.my_level != -1:
            if add_sec_num:
                print("{} {} {}".format(self.get_level_symbol(
                    ' '), self.my_sec_num, self.header_title))
            else:
                print("{} {}".format(self.get_level_symbol(
                    ' '), self.header_title))

        for child_header in self.child_headers:
            child_header.print_headers(add_sec_num)

input_fn = sys.argv[1]
print("The file name read from the argument is:", input_fn)
try:
    headers = retrieve_headers(input_fn)
    headers.assign_child_sec_num()
    headers.gen_gfm_anchor()
    toc = headers.gen_gfm_toc(False)
except:
    raise Error("Something wrong heppend.")
print("Processing finished successfully with Generated title: \n")
for item in toc:
    print(item)
