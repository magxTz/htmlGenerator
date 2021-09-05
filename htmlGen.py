class htmlGenerator:
    tags = ['head', 'body', 'button', 'canvas', 'span', 'img', 'br', 'empty',
            'div', 'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'input', 'table']

    def __init__(self, string='example'):
        self.inputString = string
        self.lists = []

    @staticmethod
    def detect_indent_level(listOfString):
        tab_len = 4
        indents = []
        for item in listOfString:
            whitespace = len(item) - len(item.lstrip())
            level = int(whitespace / tab_len)
            indents.append(level)
        return indents

    def convert2list(self):
        str_list = self.inputString.split('\n')
        for ls in str_list:
            if ls == '':
                str_list.remove(ls)
        return str_list

    @staticmethod
    def removeIndents(lst):
        for _ in lst:
            __ = _.strip()
            lst[lst.index(_)] = __
        return lst

    @staticmethod
    def normalize(ll):
        for _ in ll:
            __ = _.lower()
            ll[ll.index(_)] = __

    def tag_indices(self, lst):
        sls = self.removeIndents(lst)
        tag_indices_arr = []
        x = 0
        while x < len(sls):
            _ls = sls[x]
            ls = _ls[:-1]
            if ls in self.tags:
                index = lst.index(_ls)
                tag_indices_arr.append(index)
                sls.remove(_ls)
                sls.insert(index, _ls.upper())

            x += 1
        self.normalize(sls)
        return tag_indices_arr

    def get_tagList(self, tg_ind, indent, text):
        i = 0
        while i < len(tg_ind):
            try:
                if indent[tg_ind[i]] == indent[tg_ind[i + 1]]:
                    self.lists.append(text[tg_ind[i]:tg_ind[i + 1]])
                elif indent[tg_ind[i]] not in indent[tg_ind[i + 1]:]:
                    self.lists.append(text[tg_ind[i]:len(indent)])
            except IndexError:
                self.lists.append(text[tg_ind[i]:len(indent)])

            i += 1

        return self.lists

    def tagList2dict(self, tags_dict_Array):
        m_tagName = ''
        content = ''
        style = ''
        incompleteTag = False
        x = 0
        while x < len(self.lists):
            for ls in self.lists[x]:
                if ls.__contains__(':'):
                    tg = ls[:-1]
                    if not incompleteTag and tg in self.tags:
                        incompleteTag = True
                        m_tagName = tg

                if incompleteTag and ls.__contains__('='):
                    attribute, value = ls.split('=')
                    if attribute == 'text':
                        content += value + " "
                    else:
                        style += f'{attribute}:{value};'

            tags_dict_Array[x]['name'] = m_tagName
            tags_dict_Array[x]['content'] = content
            tags_dict_Array[x]['style'] = style
            incompleteTag = False
            style = ''
            content = ''
            x += 1
        return tags_dict_Array

    @staticmethod
    def listToString(s):
        str1 = ''
        for _ in s:
            str1 += _
        return str1

    def finalize(self, tags_dict_Array, tags_indices_len, indents, text):
        def generate(tgs):
            try:
                tab_space = '   '
                tg_name = tgs['name']
                tg_content = tgs['content']
                tg_style = tgs['style']
                indent = indents[text.index(tg_name + ':')]
                if tg_name == 'img':
                    src_link = ''
                    take_src = tg_style.split(';')
                    for attrb in take_src:
                        _attr = attrb.split(':')
                        for _ in _attr:
                            if _ == 'src':
                                src_link = self.listToString(_attr[_attr.index(_) + 1:])
                    tg_style = tg_style.replace(f'src:{src_link};', '')
                    s_output = f'<{tg_name} src="{src_link}" style="{tg_style}">\n   {tg_content}\n{tab_space * indent}</{tg_name}>\n'
                else:
                    s_output = f'<{tg_name} style="{tg_style}">\n   {tg_content}\n{tab_space * indent}</{tg_name}>\n'
                return tab_space * indent + s_output
            except ValueError:
                pass

        result = ''
        tg = 0
        while tg < len(tags_dict_Array):
            if tags_dict_Array[tg]['name'] == 'body':
                cont = ''
                for i in range(tg + 1, tags_indices_len):
                    if tags_dict_Array[i]['name'] == 'div':
                        style = tags_dict_Array[i]['style']
                        _cont = ''
                        garbage_tags = []
                        for ii in range(i + 1, tags_indices_len):
                            _cont += generate(tags_dict_Array[ii])
                            garbage_tags.append(tags_dict_Array[ii])
                        template = {'name': 'empty', 'content': 'empty', 'style': 'empty'}
                        for k in garbage_tags:
                            if k in tags_dict_Array:
                                index = tags_dict_Array.index(k)
                                tags_dict_Array.remove(k)
                                tags_dict_Array.insert(index, template)
                        tags_dict_Array[i]['name'] = 'div'
                        tags_dict_Array[i]['content'] = _cont
                        tags_dict_Array[i]['style'] = style
                        div_tag = generate(tags_dict_Array[i])
                        cont += div_tag
                    else:
                        try:
                            cont += generate(tags_dict_Array[i])
                        except TypeError:
                            pass
                tags_dict_Array[tg]['name'] = 'body'
                tags_dict_Array[tg]['content'] = cont
                tags_dict_Array[tg]['style'] = ''
                result += generate(tags_dict_Array[tg])
            elif tags_dict_Array[tg]['name'] in self.tags:
                try:
                    tag_name = tags_dict_Array[tg]['name']
                    if indents[text.index(f'{tag_name}:')] <= indents[text.index('body:')]:
                        result += generate(tags_dict_Array[tg])
                except ValueError:
                    pass
            tg += 1
        return result


class magx_HTML(htmlGenerator):
    def __init__(self, ht_string):
        self.ht_str = ht_string
        super().__init__()

    def getHTML(self):
        return self.generateHTML(self.ht_str)

    @staticmethod
    def generateHTML(_ht):
        ht_gen = htmlGenerator(_ht)
        lst = ht_gen.convert2list()
        indents = ht_gen.detect_indent_level(lst)
        tag_indices = ht_gen.tag_indices(lst)
        tag_indices_len = len(tag_indices)
        tag_list = ht_gen.get_tagList(tag_indices, indents, lst)

        tags_dict_Array = []
        for x in range(len(tag_indices)):
            tags_dict_Array.append(dict())
        tags_dict_Array = ht_gen.tagList2dict(tags_dict_Array)
        output = ht_gen.finalize(tags_dict_Array, tag_indices_len, indents, lst)
        return output
