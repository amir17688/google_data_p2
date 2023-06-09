##########################################################################
#
#  Copyright (c) 2014, Image Engine Design Inc. All rights reserved.
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are
#  met:
#
#      * Redistributions of source code must retain the above
#        copyright notice, this list of conditions and the following
#        disclaimer.
#
#      * Redistributions in binary form must reproduce the above
#        copyright notice, this list of conditions and the following
#        disclaimer in the documentation and/or other materials provided with
#        the distribution.
#
#      * Neither the name of John Haddon nor the names of
#        any other contributors to this software may be used to endorse or
#        promote products derived from this software without specific prior
#        written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
#  IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
#  THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
#  PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
#  CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
#  EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#  PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
#  PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
#  LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
#  NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#  SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
##########################################################################

import functools

import IECore

import Gaffer
import GafferUI

class PresetsPlugValueWidget( GafferUI.PlugValueWidget ) :

	def __init__( self, plug, parenting = None ) :

		self.__menuButton = GafferUI.MenuButton( "", menu = GafferUI.Menu( Gaffer.WeakMethod( self.__menuDefinition ) ) )
		GafferUI.PlugValueWidget.__init__( self, self.__menuButton, plug, parenting = parenting )

		self.__plugMetadataChangedConnection = Gaffer.Metadata.plugValueChangedSignal().connect( Gaffer.WeakMethod( self.__plugMetadataChanged ) )

		self._addPopupMenu( self.__menuButton )
		self._updateFromPlug()

	def _updateFromPlug( self ) :

		self.__menuButton.setEnabled( self._editable() )

		text = ""
		if self.getPlug() is not None :
			with self.getContext() :
				text = Gaffer.NodeAlgo.currentPreset( self.getPlug() ) or "Invalid"

		self.__menuButton.setText( text )

	def __menuDefinition( self ) :

		result = IECore.MenuDefinition()
		if self.getPlug() is None :
			return result

		currentPreset = Gaffer.NodeAlgo.currentPreset( self.getPlug() )
		for n in Gaffer.NodeAlgo.presets( self.getPlug() ) :
			result.append(
				"/" + n,
				{
					"command" : functools.partial( Gaffer.WeakMethod( self.__applyPreset ), preset = n ),
					"checkBox" : n == currentPreset,
				}
			)

		return result

	def __applyPreset( self, unused, preset ) :

		with Gaffer.UndoContext( self.getPlug().ancestor( Gaffer.ScriptNode ) ) :
			Gaffer.NodeAlgo.applyPreset( self.getPlug(), preset )

	def __plugMetadataChanged( self, nodeTypeId, plugPath, key, plug ) :

		if self.getPlug() is None :
			return

		if plug is not None and not plug.isSame( self.getPlug() ) :
			return

		if not self.getPlug().node().isInstanceOf( nodeTypeId ) :
			return

		if key.startswith( "preset:" ) :
			self._updateFromPlug()
