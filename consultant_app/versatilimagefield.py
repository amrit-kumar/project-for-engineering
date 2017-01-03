import io
from io import StringIO
from PIL import Image
# from StringIO import StringIO

from .views import *
from versatileimagefield.datastructures import SizedImage
from django.utils.datastructures import *

from versatileimagefield.fields import VersatileImageField
from versatileimagefield.registry import versatileimagefield_registry

# Unregistering the 'crop' Sizer
# versatileimagefield_registry.unregister_sizer('crop')
# Registering a custom 'crop' Sizer
# versatileimagefield_registry.register_sizer('crop', SomeCustomSizedImageCls)


class ThumbnailImage(SizedImage):
    """
    Sizes an image down to fit within a bounding box

    See the `process_image()` method for more information
    """

    filename_key = 'thumbnail'

    def process_image(self, image, image_format, save_kwargs,
                      width=400, height=400):


        """
        Returns a StringIO instance of `image` that will fit
        within a bounding box as specified by `width`x`height`
        """
        imagefile = io.BytesIO()

        image.thumbnail(
            (width, height),
            Image.ANTIALIAS
        )
        image.save(
            imagefile,
            **save_kwargs
        )
        return imagefile

# Registering the ThumbnailSizer to be available on VersatileImageField
# via the `thumbnail` attribute
versatileimagefield_registry.unregister_sizer('thumbnail')
versatileimagefield_registry.register_sizer('thumbnail', ThumbnailImage)
