def dd_json_loads(json_str: str) -> dict or list:
    if type(json_str) != str:
        raise Exception('The passed argument is not a string')
    json_str = json_str.strip()
    if len(json_str) == 0 or json_str[0] not in ['{', '['] or json_str[-1] not in ['}', ']']:
        raise Exception('The string is not format json')

    def get_elements(str_elements: str) -> list:
        """The function splits the string into elements and returns a list of elements"""
        count_brackets1, count_brackets2 = 0, 0
        str_elements = str_elements.strip('{').strip('}').strip('[').strip(']')
        object_list, obj = [], ''
        comma_ignore = False
        for elem in str_elements:
            if comma_ignore:
                if elem != ',':
                    continue
                comma_ignore = False
                continue
            if count_brackets1:
                if elem == '{':
                    count_brackets1 += 1
                    obj += elem
                elif elem == '}':
                    count_brackets1 -= 1
                    obj += elem
                    if not count_brackets1:
                        object_list.append(obj.strip())
                        obj = ''
                        comma_ignore = True
                        count_brackets1 = 0
                else:
                    obj += elem
            elif count_brackets2:
                if elem == '[':
                    count_brackets2 += 1
                    obj += elem
                elif elem == ']':
                    count_brackets2 -= 1
                    obj += elem
                    if not count_brackets2:
                        object_list.append(obj.strip())
                        obj = ''
                        comma_ignore = True
                        count_brackets2 = 0
                else:
                    obj += elem
            elif elem == '{':
                count_brackets1 += 1
                obj += elem
            elif elem == '[':
                count_brackets2 += 1
                obj += elem
            elif elem == ',':
                object_list.append(obj.strip())
                obj = ''
            else:
                obj += elem
        else:
            object_list.append(obj.strip())
        return object_list

    def is_dict(str_dict: str) -> dict:
        out_json = {}
        object_list = get_elements(str_dict)
        for item in object_list:
            key, value = '', ''
            key_flag = True
            quotation_mark = True
            value_flag = False
            value_type = None
            for i, a in enumerate(item):
                if key_flag:
                    if a == '"':
                        if quotation_mark:
                            quotation_mark = False
                        else:
                            quotation_mark = True
                            key_flag = False
                    else:
                        key += a
                else:
                    if not value_flag:
                        if a in [' ', ':', '\n']:
                            continue
                        else:
                            value_flag = True
                    if a == '{':
                        value = is_dict(item[i:].strip())
                        break
                    if a == '[':
                        value = is_list(item[i:].strip())
                        break
                    if not value_type:
                        if a == '"':
                            value_type = 'string'
                        else:
                            value_type = 'numb'
                            value += a
                    else:
                        if a != '"':
                            value += a
            if value_type == 'numb':
                if '.' in value:
                    value = float(value)
                else:
                    value = int(value)
            out_json[key] = value
        return out_json

    def is_list(str_list: str) -> list:
        out_json = []
        elements = get_elements(str_list)
        for ss in elements:
            if len(ss) < 1:
                out_json.append('')
            elif ss[0] == '{':
                out_json.append(is_dict(ss))
            elif ss[0] == '[':
                out_json.append(is_list(ss))
            elif ss[0] == '"':
                out_json.append(ss.strip('"'))
            else:
                if '.' in ss:
                    out_json.append(float(ss))
                else:
                    out_json.append(int(ss))
        return out_json

    if json_str[0] == '{':
        return is_dict(json_str)
    else:
        return is_list(json_str)
