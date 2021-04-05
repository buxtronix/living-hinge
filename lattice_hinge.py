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
    def __init__(self, width, height, offset, stroke_width, canvas,
            p_length, p_interval, p_spacing, p_offset):
        self.width = width
        self.height = height
        self.offset = offset
        self.stroke_width = stroke_width
        self.canvas = canvas
        self.p_length = p_length
        self.p_interval = p_interval
        self.p_spacing = p_spacing
        self.p_offset = p_offset

    def generate(self):
        style = {'stroke': '#ff0000', 'stroke-width': str(self.stroke_width), 'fill': 'none'}
        path_command = ''
        offs = 0
        y = 0
        while y < self.height:
          x = offs
          while x < self.width:
            path_command = '%s %s' % (path_command, self.draw_one(x, y))
            x += self.p_interval
          offs += self.p_offset
          offs = offs % self.p_interval
          y += self.p_spacing

        attrs = {
          'style': formatStyle(style),
          inkex.addNS('label', 'inkscape'): 'lattice',
          'd': path_command}
        inkex.etree.SubElement(self.canvas, inkex.addNS('path', 'svg'), attrs)


class StraightLatticeGenerator(Generator):
    def __init__(self, *args, **kwargs):
        super(StraightLatticeGenerator, self).__init__(*args)
        self.link_gap = kwargs['link_gap']
        if self.link_gap == 0:
            # Single line for 0 height gap.
            self.fixed_commands = ' h %f ' % self.p_length
        else:
            self.fixed_commands = 'l %f,%f l %f,%f l %f,%f l %f,%f ' % (
              self.p_length, 0,
              0, self.link_gap,
              0-self.p_length, 0,
              0, 0-self.link_gap)

    def draw_one(self, x, y):
        return 'M %f,%f %s' % (x, y, self.fixed_commands)


class DiamondLatticeGenerator(Generator):
    def __init__(self, *args, **kwargs):
        super(DiamondLatticeGenerator, self).__init__(*args)
        self.diamond_height = kwargs['diamond_height']
        self.fixed_commands = 'l %f,%f l %f,%f l %f,%f l %f,%f ' % (
                self.p_length/2, 0-self.diamond_height/2,
                self.p_length/2, self.diamond_height/2,
                0-self.p_length/2, self.diamond_height/2,
                0-self.p_length/2, 0-self.diamond_height/2)

    def draw_one(self, x, y):
        return 'M %f,%f %s' % (x, y+self.diamond_height/2, self.fixed_commands)


class HoneycombLatticeGenerator(Generator):
    def __init__(self, *args, **kwargs):
        super(HoneycombLatticeGenerator, self).__init__(*args)
        self.comb_height = kwargs['comb_height']
        line_length = self.p_length * kwargs['comb_ratio']
        arrow_length = self.p_length * (1-kwargs['comb_ratio']) * 0.5
        self.fixed_commands = (
                'l %f,%f l %f,%f l %f,%f l %f,%f l %f,%f '
                'l %f,%f l %f,%f') % (
                        arrow_length, self.comb_height/2,
                        0-arrow_length, self.comb_height/2,
                        arrow_length, 0-self.comb_height/2,
                        line_length, 0,
                        arrow_length, 0-self.comb_height/2,
                        0-arrow_length, self.comb_height/2,
                        arrow_length, self.comb_height/2)

    def draw_one(self, x, y):
        return 'M %f,%f %s' % (x, y, self.fixed_commands)


class WavyLatticeGenerator(Generator):
    def __init__(self, *args, **kwargs):
        super(WavyLatticeGenerator, self).__init__(*args)
        self.wave_height = kwargs['wave_height']
        self.fixed_commands = ' h %f c 4,0 3,4 %f,%f h %f c 2,0 1.5,-2 %f,%f h %f' % (
                self.p_length*0.2,
            self.p_length*0.25, self.wave_height,
            self.p_length*0.3,
            self.p_length*0.2, 0-self.wave_height/2,
            self.p_length*0.175)

    def draw_one(self, x, y):
        return 'M %f,%f %s' % (x, y, self.fixed_commands)


class LatticeHingeEffect(inkex.Effect):
    """
    Extension to create laser cut bend lattices.
    """
    def __init__(self):
        inkex.Effect.__init__(self)
        self.OptionParser.add_option("--tab", type="string", dest="tab", help="Bend pattern to generate")

        self.OptionParser.add_option("--width", type=float, default=300, help="Width of pattern")
        self.OptionParser.add_option("--height", type=float, default=100, help="Height of pattern")

        self.OptionParser.add_option("--sl_length", type=int, default=20, help="Length of links")
        self.OptionParser.add_option("--sl_gap", type=float, default=0.5, help="Gap between links")
        self.OptionParser.add_option("--sl_interval", type=int, default=30, help="Interval between links")
        self.OptionParser.add_option("--sl_spacing", type=int, default=20, help="Spacing of links")
        self.OptionParser.add_option("--sl_offset", type=int, default=15, help="Offset of rows")

        self.OptionParser.add_option("--dl_length", type=int, default=24, help="Length of diamonds")
        self.OptionParser.add_option("--dl_height", type=float, default=4, help="Height of diamonds")
        self.OptionParser.add_option("--dl_interval", type=int, default=28, help="Interval between diamonds")
        self.OptionParser.add_option("--dl_spacing", type=int, default=4, help="Spacing of diamonds")
        self.OptionParser.add_option("--dl_offset", type=int, default=14, help="Offset of rows")

        self.OptionParser.add_option("--hl_length", type=int, default=24, help="Length of combs")
        self.OptionParser.add_option("--hl_height", type=float, default=4, help="Height of combs")
        self.OptionParser.add_option("--hl_interval", type=int, default=28, help="Interval between combs")
        self.OptionParser.add_option("--hl_spacing", type=int, default=4, help="Spacing of combs")
        self.OptionParser.add_option("--hl_offset", type=int, default=14, help="Offset of rows")
        self.OptionParser.add_option("--hl_ratio", type=float, default=0.5, help="Element arrow ratio")

        self.OptionParser.add_option("--wl_length", type=int, default=20, help="Length of links")
        self.OptionParser.add_option("--wl_height", type=float, default=0.5, help="Height of links")
        self.OptionParser.add_option("--wl_interval", type=int, default=30, help="Interval between links")
        self.OptionParser.add_option("--wl_spacing", type=float, default=20, help="Spacing of links")
        self.OptionParser.add_option("--wl_offset", type=int, default=15, help="Offset of rows")

    def effect(self):
        """
        Effect behaviour.
        """
        self.svg = self.document.getroot()
        print 'Selected: %s\nSelection: %s\n', self.svg.selected, self.svg.selection)
        if self.svg.selection:
            node = self.svg.selection.values()[0]
            print 'Select node: %s' % node
            self.options.width = node.width
            self.options.height = node.height
        else:
            canvas = self.current_layer
        offset = 0
        stroke_width = self.unittouu('2px')

        if self.options.tab == '"straight_lattice"':
          generator = StraightLatticeGenerator(
                  self.options.width, self.options.height, offset,
                  stroke_width, canvas, self.options.sl_length,
                  self.options.sl_interval, self.options.sl_spacing,
                  self.options.sl_offset,
                  link_gap=self.options.sl_gap)
        elif self.options.tab == '"diamond_lattice"':
          generator = DiamondLatticeGenerator(
                  self.options.width, self.options.height, offset,
                  stroke_width, canvas, self.options.dl_length,
                  self.options.dl_interval, self.options.dl_spacing,
                  self.options.dl_offset,
                  diamond_height=self.options.dl_height)
        elif self.options.tab == '"honeycomb_lattice"':
          generator = HoneycombLatticeGenerator(
                  self.options.width, self.options.height, offset,
                  stroke_width, canvas, self.options.hl_length,
                  self.options.hl_interval, self.options.hl_spacing,
                  self.options.hl_offset,
                  comb_height=self.options.hl_height,
                  comb_ratio=self.options.hl_ratio)
        elif self.options.tab == '"wavy_lattice"':
          generator = WavyLatticeGenerator(
                  self.options.width, self.options.height, offset,
                  stroke_width, canvas, self.options.wl_length,
                  self.options.wl_interval, self.options.wl_spacing,
                  self.options.wl_offset,
                  wave_height=self.options.wl_height)
        else:
          inkex.errormsg(_("Select a valid pattern tab before rendering."))
          return

        generator.generate()

# Create effect instance and apply it.
LatticeHingeEffect().affect()
