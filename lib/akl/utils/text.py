# -*- coding: utf-8 -*-
#

import string
import logging
import time
import random
import hashlib
import re
import html

logger = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------
# Strings and text
# -------------------------------------------------------------------------------------------------
# Limits the length of a string for printing. If max_length == -1 do nothing (string has no
# length limit). The string is trimmed by cutting it and adding three dots ... at the end.
# Including these three dots the length of the returned string is max_length or less.
# Example: 'asdfasdfdasf' -> 'asdfsda...'
#
# @param string: [str] String to be trimmed.
# @param max_length: [int] Integer maximum length of the string.
# @return [str] Trimmed string.
def limit_string(string, max_length):
    if max_length > 5 and len(string) > max_length:
        string = string[0:max_length-3] + '...'
    return string

# Some XML encoding of special characters:
#   {'\n': '&#10;', '\r': '&#13;', '\t':'&#9;'}
#
# See http://stackoverflow.com/questions/1091945/what-characters-do-i-need-to-escape-in-xml-documents
# See https://wiki.python.org/moin/EscapingXml
# See https://github.com/python/cpython/blob/master/Lib/xml/sax/saxutils.py
# See http://stackoverflow.com/questions/2265966/xml-carriage-return-encoding
#
def escape_XML(data_str):

    if not isinstance(data_str, str):
        data_str = str(data_str)

    # Ampersand MUST BE replaced FIRST
    data_str = data_str.replace('&', '&amp;')
    data_str = data_str.replace('>', '&gt;')
    data_str = data_str.replace('<', '&lt;')

    data_str = data_str.replace("'", '&apos;')
    data_str = data_str.replace('"', '&quot;')
    
    # --- Unprintable characters ---
    data_str = data_str.replace('\n', '&#10;')
    data_str = data_str.replace('\r', '&#13;')
    data_str = data_str.replace('\t', '&#9;')

    return data_str

def unescape_XML(data_str):
    data_str = data_str.replace('&quot;', '"')
    data_str = data_str.replace('&apos;', "'")

    data_str = data_str.replace('&lt;', '<')
    data_str = data_str.replace('&gt;', '>')
    # Ampersand MUST BE replaced LAST
    data_str = data_str.replace('&amp;', '&')
    
    # --- Unprintable characters ---
    data_str = data_str.replace('&#10;', '\n')
    data_str = data_str.replace('&#13;', '\r')
    data_str = data_str.replace('&#9;', '\t')
    
    return data_str

# See https://www.freeformatter.com/json-escape.html
# The following characters are reserved in JSON and must be properly escaped to be used in strings:
#   Backspace is replaced with \b
#   Form feed is replaced with \f
#   Newline is replaced with \n
#   Carriage return is replaced with \r
#   Tab is replaced with \t
#   Double quote is replaced with \"
#   Backslash is replaced with \\
#
def escape_JSON(s):
    s = s.replace('\\', '\\\\') # >> Must be done first
    #s = s.replace('"', '\\"')

    return s

# Given a text clean it so the cleaned string can be used as a filename.
# 1) Convert any non-printable character into '_'
# 2) Remove special chars
# 3) (DISABLED) Convert spaces ' ' into '_'
def str_to_filename_str(title_str):
    not_valid_chars = '"*/:<>?\\|'
    cleaned_str_1 = ''.join([i if i in string.printable else '_' for i in title_str])
    cleaned_str_2 = ''.join([i if i not in not_valid_chars else '' for i in cleaned_str_1])
    #cleaned_str_3 = cleaned_str_2.replace(' ', '_')
    return cleaned_str_2

#
# Writes a XML text tag line, indented 2 spaces by default.
# Both tag_name and tag_text must be Unicode strings.
# Returns an Unicode string.
#
def XML_line(tag_name, tag_text, num_spaces = 2):
    if tag_text:
        tag_text = escape_XML(tag_text)
        line = '{0}<{1}>{2}</{3}>\n'.format(' ' * num_spaces, tag_name, tag_text, tag_name)
    else:
        # >> Empty tag
        line = '{0}<{1} />\n'.format(' ' * num_spaces, tag_name)

    return line
#
# Decodes HTML <br> tags and HTML entities (&xxx;) into Unicode characters.
# See https://stackoverflow.com/questions/2087370/decode-html-entities-in-python-string
#
def unescape_HTML(s:str) -> str:
    __debug_text_unescape_HTML = False
    if __debug_text_unescape_HTML:
        logger.debug('unescape_HTML() input  "{0}"'.format(s))

    # --- Replace HTML tag characters by their Unicode equivalent ---
    s = s.replace('<br>',   '\n')
    s = s.replace('<br/>',  '\n')
    s = s.replace('<br />', '\n')

    # --- HTML entities ---
    # s = s.replace('&lt;',   '<')
    # s = s.replace('&gt;',   '>')
    # s = s.replace('&quot;', '"')
    # s = s.replace('&nbsp;', ' ')
    # s = s.replace('&copy;', '©')
    # s = s.replace('&amp;',  '&') # >> Must be done last

    # --- HTML Unicode entities ---
    # s = s.replace('&#039;', "'")
    # s = s.replace('&#149;', "•")
    # s = s.replace('&#x22;', '"')
    # s = s.replace('&#x26;', '&')
    # s = s.replace('&#x27;', "'")

    # s = s.replace('&#x101;', "ā")
    # s = s.replace('&#x113;', "ē")
    # s = s.replace('&#x12b;', "ī")
    # s = s.replace('&#x12B;', "ī")
    # s = s.replace('&#x14d;', "ō")
    # s = s.replace('&#x14D;', "ō")
    # s = s.replace('&#x16b;', "ū")
    # s = s.replace('&#x16B;', "ū")

    # >> Use HTMLParser module to decode HTML entities.
    s = html.unescape(s)
    s

    if __debug_text_unescape_HTML:
        logger.debug('nescape_HTML() output "{0}"'.format(s))

    return s

# Remove HTML tags from string.
def remove_HTML_tags(s):
    p = re.compile(r'<.*?>')
    s = p.sub('', s)

    return s

def unescape_and_untag_HTML(s):
    s = unescape_HTML(s)
    s = remove_HTML_tags(s)

    return s

def str_2_Uni(string):
    # print(type(string))
    if type(string).__name__ == 'unicode':
        unicode_str = string
    elif type(string).__name__ == 'str':
        unicode_str = string.decode('utf-8', errors = 'replace')
    else:
        print('TypeError: ' + type(string).__name__)
        raise TypeError
    # print(type(unicode_str))

    return unicode_str

def remove_Kodi_color_tags(s):
    s = re.sub(r'\[COLOR \S+?\]', '', s)
    s = re.sub(r'\[color \S+?\]', '', s)
    s = s.replace('[/color]', '')
    s = s.replace('[/COLOR]', '')

    return s

#
# Generates a random an unique MD5 hash and returns a string with the hash
#
def misc_generate_random_SID() -> str:
    t1 = time.time()
    t2 = t1 + random.getrandbits(32)
    base = hashlib.md5(str(t1 + t2).encode('utf-8'))
    sid = base.hexdigest()

    return sid

# -------------------------------------------------------------------------------------------------
# ROM name cleaning and formatting
# -------------------------------------------------------------------------------------------------
#
# This function is used to clean the ROM name to be used as search string for the scraper.
#
# 1) Cleans ROM tags: [BIOS], (Europe), (Rev A), ...
# 2) Substitutes some characters by spaces
#
def format_ROM_name_for_scraping(title):
    title = re.sub(r'\[.*?\]', '', title)
    title = re.sub(r'\(.*?\)', '', title)
    title = re.sub(r'\{.*?\}', '', title)
    
    title = title.replace('_', ' ')
    title = title.replace('-', ' ')
    title = title.replace(':', '')
    title = title.replace('.', ' ')
    title = title.strip()

    return title

#
# Format ROM file name when scraping is disabled.
# 1) Remove No-Intro/TOSEC tags (), [], {} at the end of the file
#
# title      -> Unicode string
# clean_tags -> bool
#
# Returns a Unicode string.
#
def  format_ROM_title(title, clean_tags):
    #
    # Regexp to decompose a string in tokens
    #
    if clean_tags:
        reg_exp = r'\[.+?\]\s?|\(.+?\)\s?|\{.+?\}|[^\[\(\{]+'
        tokens = re.findall(reg_exp, title)
        str_list = []
        for token in tokens:
            stripped_token = token.strip()
            if (stripped_token[0] == '[' or stripped_token[0] == '(' or stripped_token[0] == '{') and \
               stripped_token != '[BIOS]':
                continue
            str_list.append(stripped_token)
        cleaned_title = ' '.join(str_list)
    else:
        cleaned_title = title

    # if format_title:
    #     if (title.startswith("The ")): new_title = title.replace("The ","", 1)+", The"
    #     if (title.startswith("A ")): new_title = title.replace("A ","", 1)+", A"
    #     if (title.startswith("An ")): new_title = title.replace("An ","", 1)+", An"
    # else:
    #     if (title.endswith(", The")): new_title = "The "+"".join(title.rsplit(", The", 1))
    #     if (title.endswith(", A")): new_title = "A "+"".join(title.rsplit(", A", 1))
    #     if (title.endswith(", An")): new_title = "An "+"".join(title.rsplit(", An", 1))

    return cleaned_title

# -------------------------------------------------------------------------------------------------
# Multidisc ROM support
# -------------------------------------------------------------------------------------------------
def get_ROM_basename_tokens(basename_str):
    DEBUG_TOKEN_PARSER = False

    # --- Parse ROM base_noext/basename_str into tokens ---
    reg_exp = r'\[.+?\]|\(.+?\)|\{.+?\}|[^\[\(\{]+'
    tokens_raw = re.findall(reg_exp, basename_str)
    if DEBUG_TOKEN_PARSER:
        logger.debug('get_ROM_basename_tokens() tokens_raw   {0}'.format(tokens_raw))

    # >> Strip tokens
    tokens_strip = list()
    for token in tokens_raw: tokens_strip.append(token.strip())
    if DEBUG_TOKEN_PARSER:
        logger.debug('get_ROM_basename_tokens() tokens_strip {0}'.format(tokens_strip))

    # >> Remove empty tokens ''
    tokens_clean = list()
    for token in tokens_strip: 
        if token: tokens_clean.append(token)
    if DEBUG_TOKEN_PARSER:        
        logger.debug('get_ROM_basename_tokens() tokens_clean {0}'.format(tokens_clean))

    # >> Remove '-' tokens from Trurip multidisc names
    tokens = list()
    for token in tokens_clean:
        if token == '-': continue
        tokens.append(token)
    if DEBUG_TOKEN_PARSER:
        logger.debug('get_ROM_basename_tokens() tokens       {0}'.format(tokens))

    return tokens
#
# Version helper class
#
class VersionNumber(object):
    def __init__(self, versionString):
        self.versionNumber = versionString.split('.')

    def getFullString(self):
        return '.'.join(self.versionNumber)

    def getMajor(self):
        return int(self.versionNumber[0])

    def getMinor(self):
        return int(self.versionNumber[1])

    def getBuild(self):
        return int(self.versionNumber[2])
    
##################################################################################
# Tables & CSV
##################################################################################
# Renders a list of list of strings table into a CSV list of strings.
# The list of strings must be joined with '\n'.join()
def render_table_CSV_slist(table_str):
    rows = len(table_str)
    cols = len(table_str[0])
    table_str_list = []
    for i in range(1, rows):
        row_str = ''
        for j in range(cols):
            if j < cols - 1:
                row_str += '{},'.format(table_str[i][j])
            else:
                row_str += '{}'.format(table_str[i][j])
        table_str_list.append(row_str)

    return table_str_list

#
# First row            column aligment 'right' or 'left'
# Second row           column titles
# Third and next rows  table data
#
# Returns a list of strings that must be joined with '\n'.join()
#
def render_table_str(table_str:list):
    rows = len(table_str)
    cols = len(table_str[0])
    table_str_list = []
    col_sizes = get_table_str_col_sizes(table_str, rows, cols)
    col_padding = table_str[0]

    # --- Table header ---
    row_str = ''
    for j in range(cols):
        if j < cols - 1:
            row_str += print_padded_left(table_str[1][j], col_sizes[j]) + '  '
        else:
            row_str += print_padded_left(table_str[1][j], col_sizes[j])
    table_str_list.append(row_str)
    # >> Table -----
    total_size = sum(col_sizes) + 2*(cols-1)
    table_str_list.append('{0}'.format('-' * total_size))

    # --- Data rows ---
    for i in range(2, rows):
        row_str = ''
        for j in range(cols):
            if j < cols - 1:
                if col_padding[j] == 'right':
                    row_str += print_padded_right(table_str[i][j], col_sizes[j]) + '  '
                else:
                    row_str += print_padded_left(table_str[i][j], col_sizes[j]) + '  '
            else:
                if col_padding[j] == 'right':
                    row_str += print_padded_right(table_str[i][j], col_sizes[j])
                else:
                    row_str += print_padded_left(table_str[i][j], col_sizes[j])
        table_str_list.append(row_str)

    return table_str_list

#
# First row             column aligment 'right' or 'left'
# Second and next rows  table data
#
def render_table_str_NO_HEADER(table_str):
    rows = len(table_str)
    cols = len(table_str[0])
    table_str_list = []
    # >> Ignore row 0 when computing sizes.
    col_sizes = get_table_str_col_sizes(table_str, rows, cols)
    col_padding = table_str[0]

    # --- Data rows ---
    for i in range(1, rows):
        row_str = ''
        for j in range(cols):
            if j < cols - 1:
                if col_padding[j] == 'right':
                    row_str += print_padded_right(table_str[i][j], col_sizes[j]) + '  '
                else:
                    row_str += print_padded_left(table_str[i][j], col_sizes[j]) + '  '
            else:
                if col_padding[j] == 'right':
                    row_str += print_padded_right(table_str[i][j], col_sizes[j])
                else:
                    row_str += print_padded_left(table_str[i][j], col_sizes[j])
        table_str_list.append(row_str)

    return table_str_list

def print_padded_left(str, str_max_size):
    formatted_str = '{0}'.format(str)
    padded_str =  formatted_str + ' ' * (str_max_size - len(formatted_str))

    return padded_str

def print_padded_right(str, str_max_size):
    formatted_str = '{0}'.format(str)
    padded_str = ' ' * (str_max_size - len(formatted_str)) + formatted_str

    return padded_str

#
# Removed Kodi colour tags before computing size (substitute by ''):
#   A) [COLOR skyblue]
#   B) [/COLOR]
#
def get_table_str_col_sizes(table_str, rows, cols):
    col_sizes = [0] * cols
    for j in range(cols):
        col_max_size = 0
        for i in range(1, rows):
            cell_str = re.sub(r'\[COLOR \w+?\]', '', table_str[i][j])
            cell_str = re.sub(r'\[/COLOR\]', '', cell_str)
            str_size = len('{0}'.format(cell_str))
            if str_size > col_max_size: col_max_size = str_size
        col_sizes[j] = col_max_size

    return col_sizes
    