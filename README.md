# Inkscape lasercut living hinge extension

[Link to releases](https://github.com/buxtronix/living-hinge/releases)

This is an extension for Inkscape to render Living Hinges.

Living hinges are patterns that can be laser cut into materials such
as wood and acrylic, allowing them to be bent into surprisingly tight
radii.

![Samples](images/hinges.png "Sample swatches")

This extension is primarily built for Inkscape 1.0 and above, but there
is also a 0.92+ release.

![Screenshot](images/living_hinge.png "Screenshot of extension")

## Installation

For details see the [wiki.](https://github.com/buxtronix/living-hinge/wiki)

### Inkscape 1.0+

Download the release archive and extract it such that all of the files are
contained in a *sub-folder* of your extensions folder.

Your extensions folder can be found at `Edit->Preferences->System->User Extensions`

On Linux, this is usually:

`~/.config/inkscape/extensions`

On windows it's usually:

`c:\Users\<username>\AppData\Roaming\inkscape\extensions`

### Inkscape 0.92

Download the 0.92 release archive, and extract the files `living_hinge.inx` and
`living_hinge.py` into your extensions folder (see above for the location). Do not
put them in a subfolder.
The 0.92 release is functionally identical, however the extension dialog does not
display some elements such as sliders and images.

## Usage

The extension is found in `Extensions->Render->Living Hinge...`

Input the width and height of the desired pattern and then apply (or
live preview).  
If an object is currently selected, the extension will fill the object's
bounding box instead of using the size inputs.

Choose the type of pattern you'd like by selecting its tab. Adjust the
parameters as needed. Play with the sliders in Live Preview mode
to find the optimal values and click Apply to use it.

The extension will round some of the parameters up or down in order to
fill the desired area evenly.

To get a better bounding box by the edge, you can draw a bounding path
around the desired area afterwards, then select `Path->Intersection`
to limit the pattern to exactly that path.

Selecting *Draw Swatch Card* will render a complete sample swatch ready
for cutting.

## Patterns

The currently supported patterns are:

Straight lattice:
![Straight Lattice](images/straight-lattice.png "Straight Lattice")

Diamond lattice:
![Diamond Lattice](images/diamond-lattice.png "Diamond Lattice")

Cross lattice:
![Cross Lattice](images/cross-lattice.png "Cross Lattice")

Wavy Lattice:
![Wavy Lattice](images/wavy-lattice.png "Wavy Lattice")

## Contributions

Contributions are welcome, such as for more or improved patterns, etc.

## Licence and contact

Author: Ben Buxton (bbuxton@gmail.com)
Licence: GPLv3
