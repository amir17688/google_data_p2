"""
This file is part of the "Sylphis" 3D engine
Copyright (c) 2002 - 2007 by Harry Kalogirou

	Copyright (c) 2013 Charilaos Kalogirou.
	All rights reserved.

	Redistribution and use in source and binary forms are permitted
	provided that the above copyright notice and this paragraph are
	duplicated in all such forms and that any documentation,
	advertising materials, and other materials related to such
	distribution and use acknowledge that the software was developed
	by Charilaos Kalogirou. The name of the
	Charilaos Kalogirou may not be used to endorse or promote products derived
	from this software without specific prior written permission.
	THIS SOFTWARE IS PROVIDED ``AS IS'' AND WITHOUT ANY EXPRESS OR
	IMPLIED WARRANTIES, INCLUDING, WITHOUT LIMITATION, THE IMPLIED
	WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
"""

import sys, sylphis, math
from string import *
from CJoint import *
from util import manage

class CJointBall(CJoint):
    __classname__ = 'joint_ball'
    __desc__ = 'A ball<->socket joint'
    def __init__(self, *args):
        CSimpleActor.__init__(self, *args)
      
    def join(self, ent):
        CJoint.join(self, ent)
        self.joint = manage(sylphis.CJointBall, 0, 0)
        

