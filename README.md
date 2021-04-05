# Inkscape lasercut lattice hinge extension

This is an extension for Inkscape to render Lattice Hinges.

Lattice hinges are patterns that can be laser cut into materials such
as wood and acrylic, allowing them to be bent into surprisingly tight
radii.

This extension is primarily built for Inkscape 1.0 and above.

For version 0.92 there is also a port under `0.92/`, but note that
builtin help is not available.

## Installation

### Inkscape 1.0+

Download the archive and extract it such that all of the files are
contained in a sub-folder of your extensions folder.

### Inkscape 0.92

Download the archive, and from the folder `0.92/` extract the files
`lattice_hinge.inx` and `lattice_hinge.py` into your extensions folder.

## Usage

The extension is found in `Extensions->Laser Tools->Lattice Hinge...`

Choose the type of pattern you'd like by selecting its tab. Adjust the
parameters as needed. Input the width and height of the desired pattern
and then apply (or live preview).

To get a better bounding box by the edge, you can draw a bounding path
around the desired area afterwards, then select `Path->Intersection`
to limit the pattern to exactly that path.

## Contributions

Contributions are welcome, such as for more or improved patterns, etc.

## Licence and contact

Author: Ben Buxton (bbuxton@gmail.com)
Licence: GPLv3
