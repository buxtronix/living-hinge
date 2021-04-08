#!/usr/bin/env python

# These two lines are only needed if you don't put the script directly into
# the installation directory
import sys
sys.path.append('/usr/share/inkscape/extensions')

# We will use the inkex module with the predefined Effect base class.
import inkex
# The simplestyle module provides functions for style parsing.
from simplestyle import *


class Generator(object):
    """A generic generator, subclassed for each different lattice style."""
    def __init__(self, x, y, width, height, stroke_width, canvas,
            p_length, p_spacing):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.stroke_width = stroke_width
        self.canvas = canvas
        self.p_length = p_length
        self.p_spacing = p_spacing
        self.fixed_commands = ''
        self.element_width = 20.0

    def draw_one(self, x, y):
        return 'M %f,%f %s' % (x, y, self.fixed_commands)

    def parameter_text(self):
        return 'Lattice Hinge params: length: %f spacing: %f' % (
                self.p_length, self.p_spacing)

    def generate(self):
        style = {'stroke': '#ff0000', 'stroke-width': str(self.stroke_width), 'fill': 'none'}
        path_command = ''
        y = self.y
        while y < self.height:
          x = self.x
          while x < self.width:
            path_command = '%s %s ' % (path_command, self.draw_one(x, y))
            x += self.element_width
          y += self.element_height

        link = self.canvas.add(inkex.PathElement())
        link.update(**{
          'style': style,
          'inkscape:label': 'lattice',
          'd': path_command})
        link.description(self.parameter_text())


class StraightLatticeGenerator(Generator):
    def __init__(self, *args, link_gap=0):
        super(StraightLatticeGenerator, self).__init__(*args)
        self.link_gap = link_gap

        self.element_height = 2*self.p_spacing
        w = self.p_length
        lg = self.link_gap

        if lg < 0.1:
            # Single line for 0 height gap.
            self.fixed_commands = ' m %f,%f h %f m %f,%f h %f m %f,%f h %f' % (
                    w/5, 0,
                    w*3/5,
                    0-w*4/5, self.element_height/2,
                    w*2/5,
                    w/5, 0,
                    w*2/5)
        else:
            self.fixed_commands = (
                    ' m %f,%f h %f v %f h %f'
                    ' m %f,%f h %f v %f h %f v %f'
                    ' m %f,%f h %f v %f h %f ') % (
                            0, self.element_height/2,
                            w*2/5, lg, 0-w*2/5,
                            w/8, 0-lg-self.element_height/2,
                            w*3/4, lg, 0-w*3/4, 0-lg,
                            w*7/8, lg+self.element_height/2,
                            0-w*2/5, 0-lg, w*2/5)
    

    def parameter_text(self):
        text = super(StraightLatticeGenerator, self).parameter_text()
        return '%s link_gap: %f type: straight_lattice' % (text, self.link_gap)


class DiamondLatticeGenerator(Generator):
    def __init__(self, *args, diamond_height=0, diamond_curve=0.5):
        super(DiamondLatticeGenerator, self).__init__(*args)
        self.element_height = self.p_spacing
        self.diamond_curve = diamond_curve
        self.element_width = self.p_length
        h = self.element_height
        w = self.element_width
        dc = diamond_curve *2
        self.fixed_commands = ' m %f,%f c %f,%f %f,%f %f,%f c %f,%f %f,%f %f,%f ' % (
                0, h/4,

                dc*w*0.1, 0,   w*0.4 - dc*w*0.1, h/4,   w*0.4, h/4,
                0-dc*w/10, 0,   0-(w*0.4 - dc*w*0.1),   h/4,   0-w*2/5,  h/4)

        self.fixed_commands = '%s m %f,%f c %f,%f %f,%f %f,%f c %f,%f %f,%f %f,%f ' % (
                self.fixed_commands,
                w, 0-h/2,

                0-dc*w*0.1, 0, 0-(w*0.4 - dc*w*0.1), h/4, 0-w*2/5, h/4,
                dc*w/10, 0, w*0.4 - dc*w*0.1, h/4, w*2/5, h/4)

        self.fixed_commands = '%s m %f,%f c %f,%f %f,%f %f,%f c %f,%f %f,%f %f,%f ' % (
                self.fixed_commands,
                0-w*9/10, h/4,

                dc*w*0.1, 0, w*0.4 - dc*w*0.1, 0-h/4, w*2/5, 0-h/4,
                dc*w/10, 0, w*0.4 - dc*w*0.1, h/4, w*2/5, h/4)

        self.fixed_commands = '%s m %f,%f c %f,%f %f,%f %f,%f c %f,%f %f,%f %f,%f ' % (
                self.fixed_commands,
                0-w*4/5, 0-h,

                dc*w*0.1, 0, w*0.4 - dc*w*0.1, h/4, w*2/5, h/4,
                dc*w/10, 0, w*0.4 - dc*w*0.1, 0-h/4, w*2/5, 0-h/4)


    def draw_one(self, x, y):
        return 'M %f,%f %s' % (x, y, self.fixed_commands)

    def parameter_text(self):
        text = super(DiamondLatticeGenerator, self).parameter_text()
        return '%s height: %f type: diamond_lattice' % (text, self.element_height)


class CrossLatticeGenerator(Generator):
    def __init__(self, *args):
        super(CrossLatticeGenerator, self).__init__(*args)
        self.element_height = self.p_spacing
        self.element_width = self.p_length
        self.fixed_commands = 'm %f,%f l %f,%f l %f,%f l %f,%f   m %f,%f l %f,%f l %f,%f l %f,%f  m %f,%f l %f,%f l %f,%f m %f,%f l %f,%f m %f,%f l %f,%f l %f,%f m %f,%f l %f,%f'  % (
                    # Top
                    self.element_width/10, self.element_height*3/10,
                    self.element_width/5, 0-self.element_height*3/10,
                    self.element_width*2/5, 0,
                    self.element_width/5, self.element_height*3/10,
                    # Bottom
                    0, self.element_height*4/10,
                    0-self.element_width/5, self.element_height*3/10,
                    0-self.element_width*2/5, 0,
                    0-self.element_width/5, 0-self.element_height*3/10,
                    # Left
                    0-self.element_width/10, 0-self.element_height*2/10,
                    self.element_width/5, 0,
                    self.element_width/5, 0-self.element_height*3/10,
                    0-self.element_width/5, self.element_height*3/10,
                    self.element_width/5, self.element_height*3/10,
                    # Right
                    self.element_width/5, 0,
                    self.element_width/5, 0-self.element_height*3/10,
                    0-self.element_width/5, 0-self.element_height*3/10,
                    self.element_width/5, self.element_height*3/10,
                    self.element_width/5, 0)

    def parameter_text(self):
        text = super(CrossLatticeGenerator, self).parameter_text()
        return '%s height: %f type: cross_lattice' % (text, self.element_height)


class WavyLatticeGenerator(Generator):
    def __init__(self, *args, **kwargs):
        super(WavyLatticeGenerator, self).__init__(*args)
        self.element_height = self.p_spacing
        h = self.element_height
        w = self.p_length
        self.element_width = self.p_length
        self.fixed_commands = ' m %f,%f h %f c %f,%f %f,%f %f,%f h %f m %f,%f h %f c %f,%f %f,%f %f,%f h %f ' % (
            0, h,      # Start of element (left)
            w*0.1,          # Short horiz line.
            w*0.1, 0,       # Control 1
            w*3/40, 0-h/2,  # Control 2
            w*0.2, 0-h/2,   # Curve top.
            w*0.175,        # Top horiz line.
            0-w*0.1, 0-h/2, # Move to higher line.
            w*0.3,          # Long higher horiz line.
            w/5, 0,         # Control 1
            w/10, h,       # Control 2
            w*0.25, h,      # Curve down.
            w*0.1)          # End horiz line.

    def parameter_text(self):
        text = super(WavyLatticeGenerator, self).parameter_text()
        return '%s height: %f type: wavy_lattice' % (text, self.element_height)


class LatticeHingeEffect(inkex.EffectExtension):
    """
    Extension to create laser cut bend lattices.
    """
    def add_arguments(self, pars):
      pars.add_argument("--tab", help="Bend pattern to generate")

      pars.add_argument("--width", type=float, default=300, help="Width of pattern")
      pars.add_argument("--height", type=float, default=100, help="Height of pattern")

      pars.add_argument("--sl_length", type=int, default=20, help="Length of links")
      pars.add_argument("--sl_gap", type=float, default=0.5, help="Gap between links")
      pars.add_argument("--sl_spacing", type=float, default=20, help="Spacing of links")

      pars.add_argument("--dl_curve", type=float, default=0.5, help="Curve of diamonds")
      pars.add_argument("--dl_length", type=float, default=24, help="Length of diamonds")
      pars.add_argument("--dl_spacing", type=float, default=4, help="Spacing of diamonds")

      pars.add_argument("--cl_length", type=float, default=24, help="Length of combs")
      pars.add_argument("--cl_spacing", type=float, default=4, help="Spacing of combs")

      pars.add_argument("--wl_length", type=int, default=20, help="Length of links")
      pars.add_argument("--wl_interval", type=int, default=30, help="Interval between links")
      pars.add_argument("--wl_spacing", type=float, default=0.5, help="Spacing between links")

    def effect(self):
        """
        Effect behaviour.
        """
        canvas = self.svg.get_current_layer()
        stroke_width = self.svg.unittouu('0.2mm')
        if len(self.svg.selected) > 1:
            raise inkex.AbortExtension('Select at most one object')
        x = 0
        y = 0
        for elem in self.svg.selected.values():
            bbox = elem.bounding_box()
            self.options.width = bbox.width
            self.options.height = bbox.height
#            x = bbox.x
#            y = bbox.y
            break

        if self.options.tab == 'straight_lattice':
          generator = StraightLatticeGenerator(
                  x, y, self.options.width, self.options.height,
                  stroke_width, canvas, self.options.sl_length,
                  self.options.sl_spacing,
                  link_gap=self.options.sl_gap)
        elif self.options.tab == 'diamond_lattice':
          generator = DiamondLatticeGenerator(
                  x, y, self.options.width, self.options.height,
                  stroke_width, canvas, self.options.dl_length,
                  self.options.dl_spacing,
                  diamond_curve=self.options.dl_curve)
        elif self.options.tab == 'cross_lattice':
          generator = CrossLatticeGenerator(
                  x, y, self.options.width, self.options.height,
                  stroke_width, canvas, self.options.cl_length,
                  self.options.cl_spacing)
        elif self.options.tab == 'wavy_lattice':
          generator = WavyLatticeGenerator(
                  x, y, self.options.width, self.options.height,
                  stroke_width, canvas, self.options.wl_length,
                  self.options.wl_spacing)
        else:
          inkex.errormsg(_("Select a valid pattern tab before rendering."))
          return

        generator.generate()

# Create effect instance and apply it.
LatticeHingeEffect().run()