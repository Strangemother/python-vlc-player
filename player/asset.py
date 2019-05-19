import os

from PyQt5.QtGui import QPainter, QColor, QPixmap, QIcon
from PyQt5.QtCore import Qt
from settings import resolve_in

def png_asset(filename, set_to=None, size=32, color=(255, 255,255), mask_color=(0,0,0,), **kw):

    fp = os.path.abspath(filename)
    if os.path.exists(fp):
        raise FileNotFoundError(fp)

    icon = QPixmap(fp)
    #icon.setStyleSheet("text-color: red")
    # scaled_icon = icon.scaled(30, 30, Qt.KeepAspectRatio & Qt.SmoothTransformation)
    mask = icon.createMaskFromColor(QColor(*mask_color), Qt.MaskOutColor)

    p = QPainter()
    p.begin(icon)
    p.setPen(QColor(*color))
    p.drawPixmap(icon.rect(), mask, mask.rect())
    p.end()

    scaled_icon = icon.scaledToHeight(size, Qt.SmoothTransformation)
    #scaled_icon.drawPixmap(pix.rect(), mask, mask.rect())

    if set_to is not None:
        set_to.setPixmap(scaled_icon)

    return scaled_icon


def get_image_path(config, name='teapot'):
    image_path = resolve_in(config, 'images')
    player_root = resolve_in(config, 'root')
    icon_path = os.path.join(player_root, image_path, name)
    return icon_path


def resolve_png_asset(config, **kw):
    icon_path = get_image_path(config, kw.get('name', None))
    return png_asset(icon_path, **kw)


def resolve_as_icon(config, **kw):
    png_asset = resolve_png_asset(config, **kw)

    app_icon = QIcon()
    app_icon.addPixmap(png_asset)
    return app_icon
