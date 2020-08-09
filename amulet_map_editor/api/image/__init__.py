import wx
import os
from typing import Type, Union

from amulet_map_editor.api.resources import (
    ResourceItem,
    ResourceDirectory,
    MissingResourceItem,
)


class BitmapResourceItem(ResourceItem):
    def bitmap(self, width=-1, height=-1, quality=wx.IMAGE_QUALITY_HIGH) -> wx.Bitmap:
        bm = wx.Bitmap(self._path)

        if width > 0 or height > 0:
            im: wx.Image = bm.ConvertToImage()
            im = im.Scale(
                width if width > 0 else bm.Width,
                height if height > 0 else bm.Height,
                quality,
            )
            bm = im.ConvertToBitmap()
        return bm

    @classmethod
    def default_object(cls) -> wx.Bitmap:
        bm = wx.Bitmap()
        bm.Create(32, 32)
        return bm


class ImageResourceDirectory(ResourceDirectory):
    ALLOWED_EXTS = (".png",)

    def __init__(
        self, directory_name: str, factory_class: Type[ResourceItem], parent: str
    ):
        super().__init__(directory_name, factory_class, parent)

    def __getattr__(
        self, item
    ) -> Union["ImageResourceDirectory", BitmapResourceItem, MissingResourceItem]:
        return super().__getattr__(item)


_self = ImageResourceDirectory(
    "image", BitmapResourceItem, os.path.dirname(os.path.dirname(__file__))
)


def __getattr__(
    name: str,
) -> Union["ImageResourceDirectory", BitmapResourceItem, MissingResourceItem]:
    return _self.__getattr__(name)


def __dir__():
    return _self.__dir__()
