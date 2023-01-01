from typing import IO, Any


class ImageSource:
    def __init__(self, source: IO[Any], file_name: str):
        self.source = source
        self.file_name = file_name


class Scene:
    def __init__(self, image_source: ImageSource, caption: str):
        self.image_source = image_source
        self.caption = caption


introduction = Scene(ImageSource(open('res/Introduction.png', 'rb'), 'Introduction'), 'Introduction caption.')
story = [Scene(ImageSource(open('res/Scene_1.png', 'rb'), 'Scene_1'), 'Scene 1 caption.'),
         Scene(ImageSource(open('res/Scene_2.png', 'rb'), 'Scene_2'), 'Scene 2 caption.'),
         Scene(ImageSource(open('res/Scene_3.png', 'rb'), 'Scene_3'), 'Scene 3 caption.')]
