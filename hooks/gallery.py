import glob
import os
import pprint
import json

import requests
import Image

from config import imgur_client_id


pp = pprint.PrettyPrinter(indent=4)

FILE_TYPES = ['jpg', 'JPG', 'jpeg', 'JPEG', 'png', 'PNG', 'gif', 'GIF']
GALLERY_DIR = os.path.abspath('./media/img/gallery/') + '/'
REL_GALLERY_DIR = '/img/gallery/'
PREVIEW_IMGS_NUM = 3
THUMB_PREFIX = 'THUMB_'

IMGUR_HEADERS = {'Authorization': 'Client-ID {0}'.format(imgur_client_id)}
IMGUR_ALBUM_URL = "https://api.imgur.com/3/album/{0}/"
IMGUR_ALBUM_CACHE = {}

# THUMB_SIZE_LETTER  (see http://api.imgur.com/models/image)
TS = 'm'

MAX_WIDTH = 400
MAX_HEIGHT = 600


class Gallery(object):
    """Gallery and album pages."""

    def __init__(self):
        self.albums = {}

    def get_albums(self, page, templ_vars):
        """
        Wok page.template.pre hook
        Load several preview images into each album.
        """
        if 'type' in page.meta and page.meta['type'] == 'index':
            album_pages = sorted(
                templ_vars['site']['categories']['gallery'],
                key=lambda album: album['datetime'],
            )
            albums = {}
            for album_page in album_pages:
                image_list = []
                images = map(
                    lambda i: i['thumb_src'],
                    self.albums[album_page['slug']]
                )
                image_list += images[:PREVIEW_IMGS_NUM]
                albums[album_page['slug']] = image_list
            templ_vars['site']['albums'] = albums

    def get_images(self, page):
        """
        Wok page.template.pre hook
        Get all images in the album as relative paths.
        Binds srcs and thumb_srcs to template.
        """
        is_imgur = page.meta.get('source') == 'imgur'

        if 'type' in page.meta and page.meta['type'] == 'album':
            album = page.meta

            # Route to the correct image host based on source attribute.
            Klass = Local
            if is_imgur:
                Klass = Imgur
            self.albums[album['slug']] = Klass().get_images(page)

    def set_images(self, page, templ_vars):
        """
        Wok page.template.pre hook
        Inserts a single JSON blob containing all images into the page.
        """
        album = page.meta
        if 'type' in page.meta and page.meta['type'] == 'album':
            templ_vars['site']['images'] = json.dumps(
                self.albums[album['slug']]
            )


class Local(object):
    """Filesystem images."""

    def get_images(self, page):
        """Get paths of all of the images in the album."""
        album = page.meta
        srcs = []
        # Get absolute paths of images in album for each file type.
        for file_type in FILE_TYPES:
            imgs = glob.glob(
                GALLERY_DIR + album['slug'] + '/*.' + file_type
            )

            for img in imgs:
                img_rel_path = (
                    REL_GALLERY_DIR +
                    album['slug'] + '/' + img.split('/')[-1]
                )
                srcs.append(img_rel_path)

        # Split full srcs and thumb srcs from srcs into two lists
        images = []
        thumb_srcs = filter(
            lambda src: src.split('/')[-1].startswith(THUMB_PREFIX),
            srcs
        )
        for thumb_src in thumb_srcs:
            src = thumb_src.replace(THUMB_PREFIX, '')
            thumb_width, thumb_height = calc_img_hw(thumb_src)
            width, height = calc_img_hw(src)
            images.append({
                'thumb_src': thumb_src,
                'thumb_width': thumb_width,
                'thumb_height': thumb_height,

                'src': src,
                'width': width,
                'height': height,
            })
        return images


class Imgur(object):
    """Imgur-hosted images."""

    def get_images(self, page):
        if 'album-id' not in page.meta:
            raise Exception("No album id for {0}".format(page.meta['title']))
        return map(
            make_image,
            sorted(
                self._get_imgur_album(page.meta['album-id'])['data']['images'],
                key=lambda img: img['datetime'],
                reverse=True
            )
        )

    def _get_imgur_album(self, album_id):
        global IMGUR_ALBUM_CACHE
        if album_id not in IMGUR_ALBUM_CACHE:
            response = requests.get(
                IMGUR_ALBUM_URL.format(album_id), headers=IMGUR_HEADERS
            )
            IMGUR_ALBUM_CACHE[album_id] = json.loads(response.content)
        return IMGUR_ALBUM_CACHE[album_id]


def calc_img_hw(path):
    image = Image.open(path.replace(REL_GALLERY_DIR, GALLERY_DIR))
    return image.size[0], image.size[1]


def calc_thumb(self, src):
    for ft in FILE_TYPES:
        if src.endswith(ft):
            return src.replace('.' + ft, TS + '.' + ft)
    raise Exception("Unknown filetype for {0}".format(src))


def calc_thumb_xy(*args):
    def refactor(*args):
        return map(lambda d: int(d * 0.9), args)

    def within_max(width, height):
        if width > MAX_WIDTH:
            return False
        if height > MAX_HEIGHT:
            return False
        return True

    while not within_max(*args):
        args = refactor(*args)

    return args


def make_image(image):
    width = image['width']
    height = image['height']
    thumb_width, thumb_height = calc_thumb_xy(width, height)
    return {
        'thumb_src': calc_thumb(image['link']),
        'thumb_width': thumb_width,
        'thumb_height': thumb_height,

        'src': image['link'],
        'width': width,
        'height': height,
    }

