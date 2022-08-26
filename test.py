
class Heap:
    def __init__(self, *__o):
        self.data = list(__o)

    def __len__(self):
        return len(self.data)

    def __repr__(self):
        return f"Heap( {self.data} )"

    def __str__(self):
        return self.__repr__()

    def _is_valid(self, index: int) -> bool:
        return 0 <= index < len(self.data)

    def __getitem__(self, index: int) -> any:
        return self.data[index]

    def __setitem__(self, index: int, __o: any):
        self.data[index] = __o

    def __bool__(self):
        return len(self.data) > 0

    @staticmethod
    def get_parent_index(index: int):
        return (index - 1) // 2

    @staticmethod
    def get_children_indices(index: int):
        _m = index * 2
        return _m + 1, _m + 2

    def get_children(self, index: int):
        index = self.parse_index(index)
        if self._is_valid(index):
            _m = index * 2
            _ch1, _ch2 = _m + 1, _m + 2
            _ch1 = self.data[_ch1] if _ch1 < len(self.data) else None
            _ch2 = self.data[_ch2] if _ch2 < len(self.data) else None
            return _ch1, _ch2
        raise IndexError(f"Index {index} out of range")

    def get_parent(self, index: int):
        if index == 0:
            return None
        index = self.parse_index(index)
        if self._is_valid(index):
            _p_in = (index - 1) // 2
            return self.data[_p_in]
        raise IndexError(f"Index {index} out of range")

    def index(self, __o):
        return self.data.index(__o)

    def append(self, __o: any):
        self.data.append(__o)

    def pop(self, index: int):
        return self.data.pop(index)

    def remove(self, __o: any):
        self.data.remove(__o)

    def insert(self, index: int, __o: any):
        self.data.insert(index, __o)

    def sort(self, key=None, reverse=False):
        self.data.sort(key=key, reverse=reverse)

    def parse_index(self, index):
        return index if index >= 0 else len(self.data) + index

    def sort_tree(self, index, key):
        index = self.parse_index(index)
        _p_in = self.get_parent_index(index)
        _cur = self.data[index]
        while _p_in >= 0 and key(_cur, self.data[_p_in]):
            self.data[index], self.data[_p_in] = self.data[_p_in], _cur
            index, _p_in = _p_in, self.get_parent_index(_p_in)

    def reverse(self):
        self.data.reverse()

    def clear(self):
        self.data.clear()


def is_min(__a, __b):
    return __a < __b


if __name__ == '__main__':
    h = Heap(5, 3, 7, 2, 6, 1, 4)
    print(h)
    h.sort_tree(-1, is_min)
    print(h)

    if h:
        print('yes')
    h.clear()
    if not h:
        print('no')
