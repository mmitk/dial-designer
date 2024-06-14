import numpy as np
from PIL import Image
import pandas as pd

def flatten_array(in_array: np.array) -> np.array:
    return in_array.reshape(-1, in_array.shape[-1])

def image_to_dataframe(in_image: Image.Image, positional: bool = True) -> pd.DataFrame:
    image_array = np.array(in_image)
    
    if not positional: 
        return pd.DataFrame(flatten_array(image_array), columns=['R','G','B','A'])
    
    height, width, channels = image_array.shape
    reshaped_array = image_array.reshape(-1, channels)

    X_coordinates, Y_coordinates = np.meshgrid(range(width), range(height))
    X_coordinates = X_coordinates.flatten()
    Y_coordinates = Y_coordinates.flatten()

    df = pd.DataFrame(reshaped_array, columns=['R','G','B','A'])
    df['X'] = X_coordinates
    df['Y'] = Y_coordinates

    return df