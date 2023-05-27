#===========================================================================
#
# Copyright (c) 2014, California Institute of Technology.
# U.S. Government Sponsorship under NASA Contract NAS7-03001 is
# acknowledged.  All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
# 
# 1. Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution.
# 
# 3. Neither the name of the copyright holder nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
#===========================================================================

""": A class for managing styles."""

__version__ = "$Revision: #1 $"

#===========================================================================
import os
import os.path
from . import types as S
from .MplStyle import MplStyle
import matplotlib as MPL
#===========================================================================

__all__ = [ 'MplStyleManager' ]

# Some global variables
MPLSTYLE_CLASS = MplStyle
MPLSTYLE_EXTENSION = "mplstyle"
MPLSTYLE_PREFIX = "MPL"

MPLSTYLE_CUSTOM_FUNC = "applyStyle"

MPLSTYLE_HEADER = """
#======================================================================
#
#   matplotlib style file
#
#   This file is automatically generated by mplStyle.MplStyleManager
#   additional python code that is not directly setting properties on the
#   style in this file will be lost the next time this file is written.
#
#======================================================================
"""

#===========================================================================
class MplStyleManager( S.StyleManager ):
   """: An object used to manage one or more Style classes.

   """
   #-----------------------------------------------------------------------
   def __init__( self ):
      """: Create a new MplStyleManager object.
      """
      S.StyleManager.__init__( self, MPLSTYLE_CLASS,
                                     MPLSTYLE_EXTENSION,
                                     MPLSTYLE_PREFIX )

   #-----------------------------------------------------------------------
   def _loadFromFile( self, fname ):
      """: Load the specified style file.

      = INPUT VARIABLES
      - fname    The path of the file to load.

      = RETURN VALUE
      - Returns the new style that results from loading from the specified file.
      """
      # Allow style files to use some variables.
      createData = lambda : {
         'MplStyle' : MplStyle,
         }

      data = createData()
      try:
         execfile( fname, data )
      except Exception, e:
         msg = "MplStyleManager had an error loading the file '%s'" % fname
         raise S.util.mergeExceptions( e, msg )

      if 'style' in data:
         style = data['style']
      else:
         msg = "MplStyleManager is unable to load the style file '%s' " \
               "because there was no value named 'style' of type 'MplStyle' " \
               "found." % (fname,)
         raise Exception( msg )

      if not isinstance( style, MplStyle ):
         msg = "MplStyleManager is unable to load the style file '%s' " \
               "because the value named 'style' was expected to be of type " \
               "'MplStyle', but was instead of type '%s'" % \
               (fname, style.__class__.__name__)
         raise Exception( msg )

      # Load the custom file
      custom = os.path.dirname( fname )
      customBase, customExt = os.path.splitext( fname )
      custom = os.path.join( custom, ( "%s_custom%s" % (customBase,
                                                        customExt) ) )

      if os.path.exists( custom ):
         customData = createData()
         execfile( custom, customData )

         if MPLSTYLE_CUSTOM_FUNC in customData:
            style.custom = customData[MPLSTYLE_CUSTOM_FUNC]
         else:
            msg = "MplStyleManager encountered an error while loading the " \
                  "style '%s'.  A custom script was found, but the expected " \
                  "entry point '%s' was not found in the file.\nCustom File: " \
                  "'%s'" % (style.name, MPLSTYLE_CUSTOM_FUNC, custom)
            raise Exception( msg )

      return style

   #-----------------------------------------------------------------------
   def _writeSubStyle( self, fout, style, prefix ):
      """: Write the style to the file

      = INPUT VARIABLES
      - fout     The output file we are writing to
      - style    The sub-style to write.
      - prefix   The prefix to add to the beginning of each line.
      """
      propertyNames = style.propertyNames()

      for name in propertyNames:
         value = getattr( style, name )

         if value is None:
            continue

         if isinstance( value, str ) or isinstance( value, unicode ):
            value = "'%s'" % value

         if isinstance( value, S.SubStyle ):
            self._writeSubStyle( fout, value, "%s.%s" % (prefix, name) )
         else:
            fout.write( "%s.%s = %s\n" % (prefix, name, value) )

   #-----------------------------------------------------------------------
   def _saveToFile( self, style, fname ):
      """: Save the style to persistent file.

      This will write the given style to the named file overwriting the file if
      it already exists.

      = INPUT VARIABLES
      - style     The style to save to a file.
      - fname     The name of the file to save the style to.
      """
      with open( fname, 'w' ) as fout:
         fout.write( MPLSTYLE_HEADER )
         fout.write( "style = MplStyle( '%s' )\n" % (style.name,) )
         self._writeSubStyle( fout, style, 'style' )

   #-----------------------------------------------------------------------
   def _deleteStyleFile( self, fname ):
      """: Delete the persistent files for a style.

      = INPUT VARIABLES
      - fname    The name of the style file to delete.
      """
      # Remove the file
      os.remove( fname )

      # Check for a custom script file and remove it.
      custom = os.path.dirname( fname )
      customBase, customExt = os.path.splitext( fname )
      custom = os.path.join( custom, ( "%s_custom%s" % (customBase,
                                                        customExt) ) )

      if os.path.exists( custom ):
         os.remove( custom )

   #-----------------------------------------------------------------------
   def _create( self, name, properties, parent, custom, **kwargs ):
      """: Create a new style with the given name.

      = INPUT VARIABLES
      - name        The name to give to the newly created style.
      - properties  Initial property values to set in the newly created style.
      - parent      The name of an existing style to use as the parent of the
                    newly created style.
      - custom      A callable object or function that will be passed the object
                    that needs styling.
      - kwargs      Any extra keyword arguments are passed into the style
                    constructor.
      """
      return MplStyle( name, properties, parent, custom )

#-----------------------------------------------------------------------

