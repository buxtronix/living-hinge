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
    def __init__(self, width, height, stroke_width, canvas,
            p_length, p_interval, p_spacing, p_offset):
        self.width = width
        self.height = height
        self.stroke_width = stroke_width
        self.canvas = canvas
        self.p_length = p_length
        self.p_interval = p_interval
        self.p_spacing = p_spacing
        self.p_offset = p_offset
        self.fixed_commands = ''
        self.start_commands = ''
        self.end_commands = ''

    def element_height(self):
        return 0

    def draw_one(self, x, y):
        return 'M %f,%f %s' % (x, y, self.fixed_commands)

    def draw_start(self, x, y):
        return 'M %f,%f %s' % (x, y, self.start_commands)

    def draw_end(self, x, y):
        return 'M %f,%f %s' % (x, y, self.end_commands)

    def parameter_text(self):
        return 'Lattice Hinge params: length: %f interval: %f spacing: %f' % (
                self.p_length, self.p_interval, self.p_spacing)

    def generate(self):
        style = {'stroke': '#ff0000', 'stroke-width': str(self.stroke_width), 'fill': 'none'}
        path_command = ''
        offs = 0
        y = 0
        row = 0
        while y < self.height - self.element_height():
          column = 0
          x = offs
          while x < self.width:
            if column == 0 and row % 2:
                path_command = '%s %s ' % (path_command, self.draw_start(0, y))
            if x + self.p_length/2 > self.width:
                path_command = '%s %s ' % (path_command, self.draw_end(x, y))
            else:
                path_command = '%s %s ' % (path_command, self.draw_one(x, y))
            x += self.p_interval
            column += 1
          offs += self.p_offset
          offs = offs % self.p_interval
          y += self.p_spacing
          row += 1

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
        start_end = self.p_offset - (self.p_interval - self.p_length)
        if self.link_gap < 0.1:
            # Single line for 0 height gap.
            self.fixed_commands = ' h %f ' % self.p_length
            self.start_commands = ' h %f ' % start_end
            self.end_commands = ' h %f ' % (0-start_end)
        else:
            self.fixed_commands = 'l %f,%f l %f,%f l %f,%f l %f,%f ' % (
              self.p_length, 0,
              0, self.link_gap,
              0-self.p_length, 0,
              0, 0-self.link_gap)
            self.start_commands = 'l %f,%f l %f,%f l %f,%f l %f,%f ' % (
              start_end, 0,
              0, self.link_gap,
              0-start_end, 0,
              0, 0-self.link_gap)
            self.end_commands = 'l %f,%f l %f,%f l %f,%f l %f,%f ' % (
              start_end, 0,
              0, self.link_gap,
              0-start_end, 0,
              0, 0-self.link_gap)

    def element_height(self):
        return self.link_gap

    def parameter_text(self):
        text = super(StraightLatticeGenerator, self).parameter_text()
        return '%s link_gap: %f type: straight_lattice' % (text, self.link_gap)


class DiamondLatticeGenerator(Generator):
    def __init__(self, *args, diamond_height=0):
        super(DiamondLatticeGenerator, self).__init__(*args)
        self.diamond_height = diamond_height
        self.fixed_commands = 'l %f,%f l %f,%f l %f,%f l %f,%f ' % (
                self.p_length/2, 0-self.diamond_height/2,
                self.p_length/2, self.diamond_height/2,
                0-self.p_length/2, self.diamond_height/2,
                0-self.p_length/2, 0-self.diamond_height/2)
        start_end = self.p_offset - (self.p_interval - self.p_length)
        self.start_commands = 'm %f,%f l %f,%f l %f,%f l %f,%f ' % (
                0, self.diamond_height/5,
                start_end, self.diamond_height/3,
                0-start_end, self.diamond_height/3,
                0, 0-self.diamond_height*2/3)
        self.end_commands = 'm %f,%f l %f,%f l %f,%f l %f,%f ' % (
                0, self.diamond_height/2,
                start_end, 0-self.diamond_height/3,
                0, self.diamond_height*2/3,
                0-start_end, 0-self.diamond_height/3)

    def element_height(self):
        return self.diamond_height

    def draw_one(self, x, y):
        return 'M %f,%f %s' % (x, y+self.diamond_height/2, self.fixed_commands)

    def parameter_text(self):
        text = super(DiamondLatticeGenerator, self).parameter_text()
        return '%s height: %f type: diamond_lattice' % (text, self.diamond_height)


class HoneycombLatticeGenerator(Generator):
    def __init__(self, *args, comb_height=0, comb_ratio=0):
        super(HoneycombLatticeGenerator, self).__init__(*args)
        self.comb_height = comb_height
        self.comb_ratio = comb_ratio
        line_length = self.p_length * comb_ratio
        arrow_length = self.p_length * (1-comb_ratio) * 0.5
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

        start_end = self.p_offset - (self.p_interval - self.p_length) - arrow_length
        self.start_commands = (
                'm %f,%f l %f,%f l %f,%f l %f,%f l %f,%f ') % (
                        0, self.comb_height/2,
                        start_end, 0,
                        arrow_length, 0-self.comb_height/2,
                        0-arrow_length, self.comb_height/2,
                        arrow_length, self.comb_height/2)
        self.end_commands = ('l %f,%f l %f,%f l %f,%f l %f,%f ') % (
                        arrow_length, self.comb_height/2,
                        0-arrow_length, self.comb_height/2,
                        arrow_length, 0-self.comb_height/2,
                        line_length/4, 0)

    def element_height(self):
        return self.comb_height

    def parameter_text(self):
        text = super(HoneycombLatticeGenerator, self).parameter_text()
        return '%s height: %f ratio: %f type: honeycomb_lattice' % (text, self.comb_height, self.comb_ratio)


class WavyLatticeGenerator(Generator):
    def __init__(self, *args, **kwargs):
        super(WavyLatticeGenerator, self).__init__(*args)
        self.wave_height = kwargs['wave_height']
        self.fixed_commands = ' h %f c 4,0 3,4 %f,%f h %f c 2,0 1.5,-2 %f,%f h %f' % (
            self.p_length*0.2,
            self.p_length*0.25, self.wave_height,
            self.p_length*0.2,
            self.p_length*0.2, 0-self.wave_height/2,
            self.p_length*0.175)

    def element_height(self):
        return self.wave_height

    def parameter_text(self):
        text = super(WavyLatticeGenerator, self).parameter_text()
        return '%s height: %f type: wavy_lattice' % (text, self.wave_height)


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
      pars.add_argument("--sl_interval", type=int, default=30, help="Interval between links")
      pars.add_argument("--sl_spacing", type=float, default=20, help="Spacing of links")

      pars.add_argument("--dl_length", type=float, default=24, help="Length of diamonds")
      pars.add_argument("--dl_height", type=float, default=4, help="Height of diamonds")
      pars.add_argument("--dl_interval", type=float, default=28, help="Interval between diamonds")
      pars.add_argument("--dl_spacing", type=float, default=4, help="Spacing of diamonds")

      pars.add_argument("--hl_length", type=float, default=24, help="Length of combs")
      pars.add_argument("--hl_height", type=float, default=4, help="Height of combs")
      pars.add_argument("--hl_interval", type=float, default=28, help="Interval between combs")
      pars.add_argument("--hl_spacing", type=float, default=4, help="Spacing of combs")
      pars.add_argument("--hl_ratio", type=float, default=0.5, help="Element arrow ratio")

      pars.add_argument("--wl_length", type=int, default=20, help="Length of links")
      pars.add_argument("--wl_interval", type=int, default=30, help="Interval between links")
      pars.add_argument("--wl_spacing", type=float, default=20, help="Spacing of links")
      pars.add_argument("--wl_height", type=float, default=0.5, help="Height of links")

    def effect(self):
        """
        Effect behaviour.
        """
        canvas = self.svg.get_current_layer()
        stroke_width = self.svg.unittouu('2px')
        if len(self.svg.selected) > 1:
            raise inkex.AbortExtension('Select at most one object')
        for elem in self.svg.selected.values():
            self.options.width = elem.width
            self.options.height = elem.height

        if self.options.tab == 'straight_lattice':
          generator = StraightLatticeGenerator(
                  self.options.width, self.options.height,
                  stroke_width, canvas, self.options.sl_length,
                  self.options.sl_interval, self.options.sl_spacing,
                  self.options.sl_interval/2,
                  link_gap=self.options.sl_gap)
        elif self.options.tab == 'diamond_lattice':
          generator = DiamondLatticeGenerator(
                  self.options.width, self.options.height,
                  stroke_width, canvas, self.options.dl_length,
                  self.options.dl_interval, self.options.dl_spacing,
                  self.options.dl_interval/2,
                  diamond_height=self.options.dl_height)
        elif self.options.tab == 'honeycomb_lattice':
          generator = HoneycombLatticeGenerator(
                  self.options.width, self.options.height,
                  stroke_width, canvas, self.options.hl_length,
                  self.options.hl_interval, self.options.hl_spacing,
                  self.options.hl_interval/2,
                  comb_height=self.options.hl_height,
                  comb_ratio=self.options.hl_ratio)
        elif self.options.tab == 'wavy_lattice':
          generator = WavyLatticeGenerator(
                  self.options.width, self.options.height,
                  stroke_width, canvas, self.options.wl_length,
                  self.options.wl_interval, self.options.wl_spacing,
                  self.options.wl_interval,
                  wave_height=self.options.wl_height)
        else:
          inkex.errormsg(_("Select a valid pattern tab before rendering."))
          return

        generator.generate()

# Create effect instance and apply it.
LatticeHingeEffect().run()
