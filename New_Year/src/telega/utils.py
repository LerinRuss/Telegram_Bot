class LoadCache:
    _LOAD_STORAGE = {}

    @staticmethod
    def load(path: str):
        if path in LoadCache._LOAD_STORAGE:
            return LoadCache._LOAD_STORAGE[path]

        with open(path, 'rb') as f:
            body = f.read()
            LoadCache._LOAD_STORAGE[path] = body

            return body
