import sys
sys.path.append('../')
from common import utils
import pytest
from PIL import Image, ImageChops
import numpy as np

CHANNEL_COLUMNS = ['R', 'G', 'B', 'A']

def generate_random_test_image() -> Image:
    imarray = np.random.rand(100,100,3) * 255
    im = Image.fromarray(imarray.astype('uint8')).convert('RGBA')
    return im

def dataframe_to_image(image_df) -> Image:
    df = image_df[CHANNEL_COLUMNS]
    im = Image.new("RGBA", df.size)
    im.putdata(list(df.itertuples(index=False)))
    return im

def are_images_equal(im1: Image, im2: Image) -> bool:
    diff = ImageChops.difference(im1, im2)
    return True if not diff.getbbox else False
    
class TestImageUtils:
    def test_image_to_dataframe(self):
        initial_image = generate_random_test_image()
        transformed_image_df = utils.image_to_dataframe(
            in_image=initial_image,
            positional=False
        )
        transformed_image = dataframe_to_image(transformed_image_df)
        assert are_images_equal(initial_image, transformed_image) is True

    def test_image_to_dataframe_positional(self):
        initial_image = generate_random_test_image()
        transformed_image_df = utils.image_to_dataframe(in_image=initial_image)
        transformed_image = dataframe_to_image(transformed_image_df)
        assert are_images_equal(initial_image, transformed_image) is True