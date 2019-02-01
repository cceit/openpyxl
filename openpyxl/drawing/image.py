from __future__ import absolute_import
# Copyright (c) 2010-2019 openpyxl

from io import BytesIO

try:
    from PIL import Image as PILImage
except ImportError:
    PILImage = False


def _import_image(img):
    if not PILImage:
        raise ImportError('You must install Pillow to fetch image objects')

    if not isinstance(img, PILImage.Image):
        img = PILImage.open(img)

    return img


class Image(object):
    """Image in a spreadsheet"""

    _id = 1
    _path = "/xl/media/image{0}.{1}"
    anchor = "A1"

    def __init__(self, img):

        self.ref = img

        # don't keep the image open
        image = _import_image(img)
        self.width = image.size[0]
        self.height = image.size[1]
        try:
            self.format = image.format.lower()
        except AttributeError:
            self.format = "png"
        image.close()


    def _data(self):
        """
        Open image and write it to a buffer when saving the workbook
        """
        img = _import_image(self.ref)
        fp = None
        # don't convert these file formats
        if self.format in ['gif', 'jpeg', 'png']:
            if img.fp:
                img.fp.seek(0)
                fp = img.fp
        if not fp:
            fp = BytesIO()
            img.save(fp, format=self.format)

        return fp.read()


    @property
    def path(self):
        return self._path.format(self._id, self.format)
