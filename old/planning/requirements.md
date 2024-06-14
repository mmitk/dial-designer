# Requirements

The following is the necessary behavior for the dial designer for various use cases

## Laser Etching Paint

### Process

    - Blank or sterile dial is painted with layers of enamel paint (with clear layers in between)
    - An image is chosen/provide by user to the DialDesigner
    - DialDesigner takes the colors in the image and maps them all to the closest color that matches the paint
        - e.g. The dial is painted with Green, Blue, and Black colors, the closest matching code for those colors is stored and mapped in a full color space, and the light green in the image gets converted to the green that matches the color of the green paint
    - DialDesigner seperates the image into layers grouped by color (potentially lumped with above step)
    - Each layer is then converted into White (the are that will be etched by the laser) and Black (parts that won't be lasered)
        - A mask must be applied so laser doesn't etch in the same place as a previous layer has already been etched
    - The layers are output in the correct order they should be printed, along with the settings necessary to etch into that layer
        - a map of EtchSettings->PaintColor is created before hand manually and provided as a config
  
### Requirements

#### Color Mapping
Because we are limited by the colors provided by the paints, we need to be able to map colors from an input image to one of the paint colors.

<ins>Plan to achieve this:<ins> 

Given an input image represented as a set of RGB of pixels _I<sub>RGB</sub>_ and the user provided list of hex colors that represent the paint set _P<sub>RGB</sub>_ perform a mapping on the input image by calculating the mininmum distance between RGB values for each pixel in the image and each color in the user provided list, then transforming the input pixel to the color of the minimum distance:

for all pixels _p<sub>RGB</sub>_ in _P<sub>RGB</sub>_:

An Image (_I<sub>inp</sub>_) is passed into DialDesigner. The Image is filtered through the map in previous step (i.e. _M<sub>c</sub>_):  

_I<sub>out</sub> = M<sub>c</sub>(I<sub>inp</sub>)_

Image is 
