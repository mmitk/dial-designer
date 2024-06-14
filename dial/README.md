Flow:

### 1. Ingest

- accept photo and params from user
    - number of layers
    - etching config per color
    - load in allowed colors from user config
    - layer etch order (i.e. Blue -> Red -> Black, or Green -> Blue -> Purple)
- Filter photo
    For each pixel:
        - calculate distance from each allowed color
        - choose color with minimum distance
        - change pixel to chosen color

###  Transform - layer and mask

- Seperate image by color into layers
    - for each layer, keep all pixels in layer, make all others transparent
- Calculate mask
    Going down the layer etch order:
        - if first layer, leave as is
        - all pixels in layer that are present in any previous layer should be made transparent for that layer
        
