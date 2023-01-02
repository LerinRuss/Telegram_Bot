from typing import IO, Any
from utils import LoadCache


class ImageSource:
    def __init__(self, source: IO[Any], file_name: str):
        self.source = source
        self.file_name = file_name


class Scene:
    def __init__(self, image_source: ImageSource, caption: str):
        self.image_source = image_source
        self.caption = caption


introduction = Scene(ImageSource(LoadCache.load('res/Introduction.png'), 'Introduction'), 'Introduction caption.')
story = [Scene(ImageSource(LoadCache.load('res/Scene_1.png'), 'Scene_1'), 'Scene 1 caption.'),
         Scene(ImageSource(LoadCache.load('res/Scene_2.png'), 'Scene_2'), 'Scene 2 caption.'),
         Scene(ImageSource(LoadCache.load('res/Scene_3.png'), 'Scene_3'), 'Scene 3 caption.')]
