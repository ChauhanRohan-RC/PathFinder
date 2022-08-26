def remove_all_whitespaces(_str: str) -> str:
    return ''.join(_str.split())


def load_map(file_path: str, key_value_delimiter: str = '=', comment_token='#',
             remove_whitespaces: bool = True, key_filter=None, value_filter=None) -> dict:
    """
    Load key-value pairs from a given file

    :param file_path: path of input file
    :param key_value_delimiter: delimiter for each entry, line format = key{delimiter}value
    :param comment_token: signifies starting of a comment
    :param remove_whitespaces: whether to remove whitespaces from each line
    :param key_filter: a predicate to decide whether an entry corresponding to key must be included
    :param value_filter: a predicate to decide whether an entry corresponding to value must be included

    :return: dict containing key-value pairs (all as strings)
    """
    _map = {}

    try:
        with open(file_path, "r+") as f:
            for line in f.readlines():
                if comment_token:
                    comment_token_index = line.find(comment_token)
                    if comment_token_index >= 0:
                        line = line[:comment_token_index]
                if remove_whitespaces:
                    line = remove_all_whitespaces(line)
                line = line.replace('\n', '')
                if line:
                    _dat = line.split(key_value_delimiter)
                    if len(_dat) == 2:
                        k, v = _dat[0], _dat[1]
                        if k and (not key_filter or key_filter(k)) and (not value_filter or value_filter(v)):
                            _map[_dat[0]] = _dat[1]
    except Exception as e:
        print(f"Error while loading data from file {file_path}: {e}")

    return _map
