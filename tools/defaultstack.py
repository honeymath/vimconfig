class DefaultStack:
    def __init__(self, default_factory):
        self._data = []
        self._history = []
        self.default_factory = default_factory

    def push(self, value):
        self._data.append(value)

    def pop(self):
        if not self._data:
            self.generate()
        return self._data.pop()
    def generate(self):
        new_value = self.default_factory()
        self._history.append(new_value)
        self._data.prepend(new_value)
    def __getitem__(self, index):
        if index >= 0:
            raise IndexError("Index must be negative for DefaultStack.")
        if index < -1000:
            raise IndexError("Index too negative, please use a reasonable negative index.")
        while -index > len(self._data):
            self.generate()
        return self._data[index]

    def len(self):
        return len(self._data) - len(self._history)
    def negative_len(self):
        return len(self._history) > len(self._data)
    def __len__(self):
        truelen = len(self._data) - len(self._history)
        if truelen < 0:
            print(f"[WARNING]Due to the annoying python restriction, the actual length {truelen} can not returned, return the absolute value instead. Please use .length() to get the actual length.")
            return -truelen
        else:
            return truelen
        return len(self._data) - len(self._history)

    def __repr__(self):
        return f"DefaultStack({self._data} - {self._history})"

