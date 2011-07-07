'''
DrawBook

To do:
Bugs:
'''

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from libavg import avg



class Draw(object):
  '''
  create the draw surface (call DrawNode & create tools)
  left: divNode <- RectNode (background color) & ImageNodes (for tools)
  right: CanvasNode (with RectNode & circleNodes)
  for the beginning: draw only
  '''