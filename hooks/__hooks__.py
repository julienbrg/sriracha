from hooks import compile_sass
from gallery import Gallery
import thumbnail


gallery = Gallery()

hooks = {
    'site.start': [thumbnail.create_thumbnails],
    'page.meta.post': [gallery.get_images],
    'page.template.pre': [gallery.get_albums, gallery.set_images],
    'site.output.post': [compile_sass],
}
