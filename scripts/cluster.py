from sklearn.cluster import KMeans
from PIL import Image
import numpy as np
import pandas as pd
import sys
from copy import deepcopy
from collections import OrderedDict

def get_image_clusters(image_path, num_clusters: int = 3):
    image = Image.open(image_path)
    image = image.convert("RGBA")
    image_array = np.array(image)
    flattened_array = image_array.reshape(-1, image_array.shape[-1])
    original_colors = pd.DataFrame(flattened_array, columns=['R', 'G', 'B', 'A'])
    unique_colors = pd.DataFrame(np.unique(flattened_array, axis=0), columns=['R', 'G', 'B', 'A'])
    unique_colors = unique_colors[unique_colors['A']>0]
    kmeans = KMeans(n_clusters=num_clusters)
    unique_colors['label'] = kmeans.fit_predict(unique_colors[['R', 'G', 'B']])
    return original_colors, unique_colors, kmeans

def transparify(image_path, output_path, num_clusters = 3):
    img = Image.open(image_path)
    img = img.convert("RGBA")

    oc, uc, kmeans = get_image_clusters(image_path=image_path, num_clusters=num_clusters)
    oc['label'] = kmeans.predict(oc[['R','G','B']])
    for label in uc['label'].unique().tolist():
        oc_t = oc.copy(deep=True)
        oc_t.loc[(oc_t['label']==label),'A'] = 0
        img.putdata(list(oc_t[['R','G','B','A']].itertuples(index=False)))
        img.save(f"{output_path}-{label}-Removed.png", "PNG")

def transparify_with_fill(image_path, background_path, output_path, num_clusters = 3):
    img = Image.open(image_path)
    img = img.convert("RGBA")

    bkrnd = Image.open(background_path)
    bkrnd = bkrnd.resize(img.size)
    bkrnd_array = np.array(bkrnd)
    bkrnd_flattened_array = bkrnd_array.reshape(-1, bkrnd_array.shape[-1])
    bkrnd_df = pd.DataFrame(bkrnd_flattened_array, columns=['R', 'G', 'B', 'A'])
    bkrnd_df['A'] = 255
    
    oc, uc, kmeans = get_image_clusters(image_path=image_path, num_clusters=num_clusters)
    oc['label'] = kmeans.predict(oc[['R','G','B']])

    oc_keep = oc.copy(deep=True)
    oc_keep.loc[(oc_keep['A']>0),['R','G','B','A']] = bkrnd_df
    bkrnd_df = oc_keep

    transparency_gradient = range(255, 20, -int(255/(num_clusters)))

    images = []

    for i, label in enumerate(uc['label'].unique().tolist()):
        oc_t = oc.copy(deep=True)
        bkrnd_df['A'] = transparency_gradient[i]
        oc_t.loc[(oc_t['label']==label),['R','G','B','A']] = bkrnd_df
        img.putdata(list(oc_t[['R','G','B','A']].itertuples(index=False)))
        img.save(f"{output_path}-{label}-T{transparency_gradient[i]}-Replaced.png", "PNG")
        images.append({
            't': transparency_gradient[i],
            'img': deepcopy(img)
        })

    images = sorted(images, key=lambda x:x['t'], reverse=True)

    base_img = None
    for count, image in enumerate(images):
        if count==0:
            base_img=image['img']
            continue
        base_img.paste(image['img'], (0,0))
    base_img.save(f"{output_path}-Combined.png")

if __name__ == "__main__":
    transparify(image_path=sys.argv[1], output_path=sys.argv[2], num_clusters=int(sys.argv[3]))
    #transparify_with_fill(image_path=sys.argv[1], background_path=sys.argv[4], output_path=sys.argv[2], num_clusters=int(sys.argv[3]))