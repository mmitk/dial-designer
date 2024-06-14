from PIL import Image
from sklearn.cluster import KMeans
from . import utils
from typing import List

CHANNEL_COLUMNS = ['R', 'G', 'B', 'A']

class QImage:

    def __init__(self, image_path: str) -> None:
        self.img = Image.open(image_path).convert("RGBA")
        self.img_data = utils.image_to_dataframe(self.img)

class DesignImage(QImage):
    def __init__(self, image_path: str, fill_image_path: str = None, num_color_groups: int = None) -> None:
        super(image_path=image_path)
        if fill_image_path:
            self.fill_image = QImage(fill_image_path)
        else:
            self.fill_image = None
        self._num_clusters = num_color_groups
        if self._num_clusters: 
            self.fit_clusters(self._num_clusters)
        else:
            self._model = None
        self.layers = []

    def fit_clusters(self, num_clusters: int = 2, **kwargs) -> None:
        self._model = KMeans(n_clusters=num_clusters).fit(self.img_data)

    def predict_clusters(self) -> None:
        self.img_data['labels'] = self._model.predict(self.img_data)
        self.labels = self.img_data['labels'].tolist()

    def transparify(self) -> list:
        for label in self.labels:
            layer_image = Image.new("RGBA", self.img.size)
            layer_image_data = self.img_data.copy(deep=True)
            layer_image_data.loc[(layer_image_data['labels']==label), 'A'] = 0
            layer_image.putdata(list(layer_image_data[[CHANNEL_COLUMNS]].itertuples(index=False)))
            self.layers.append(layer_image)
        return self.layers
    
    def fit_transparify(self, num_clusters: int = 2, **kwargs) -> list:
        self.fit_clusters(
            num_clusters=num_clusters,
            **kwargs
        )
        self.predict_clusters()
        return self.transparify()