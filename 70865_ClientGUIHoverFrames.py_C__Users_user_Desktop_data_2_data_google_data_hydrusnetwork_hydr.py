import ClientConstants as CC
import ClientData
import ClientGUICanvas
import ClientGUICommon
import HydrusConstants as HC
import HydrusData
import HydrusGlobals
import os
import wx

class FullscreenHoverFrame( wx.Frame ):
    
    def __init__( self, parent, canvas_key ):
        
        if HC.PLATFORM_WINDOWS:
            
            border_style = wx.BORDER_RAISED
            
        else:
            
            border_style = wx.BORDER_SIMPLE
            
        
        wx.Frame.__init__( self, parent, style = wx.FRAME_TOOL_WINDOW | wx.FRAME_NO_TASKBAR | wx.FRAME_FLOAT_ON_PARENT | border_style )
        
        self._canvas_key = canvas_key
        self._current_media = None
        
        self._last_ideal_position = None
        
        self.SetBackgroundColour( wx.WHITE )
        self.SetCursor( wx.StockCursor( wx.CURSOR_ARROW ) )
        
        self._timer_check_show = wx.Timer( self, id = ClientGUICanvas.ID_TIMER_HOVER_SHOW )
        
        self.Bind( wx.EVT_TIMER, self.TIMEREventCheckIfShouldShow, id = ClientGUICanvas.ID_TIMER_HOVER_SHOW )
        
        self._timer_check_show.Start( 100, wx.TIMER_CONTINUOUS )
        
        HydrusGlobals.client_controller.sub( self, 'SetDisplayMedia', 'canvas_new_display_media' )
        
    
    def _GetIdealSizeAndPosition( self ):
        
        raise NotImplementedError()
        
    
    def _SizeAndPosition( self ):
        
        ( should_resize, my_ideal_size, my_ideal_position ) = self._GetIdealSizeAndPosition()
        
        if should_resize:
            
            self.Fit()
            
            self.SetSize( my_ideal_size )
            
        
        self.SetPosition( my_ideal_position )
        
        
    
    def SetDisplayMedia( self, canvas_key, media ):
        
        if canvas_key == self._canvas_key:
            
            self._current_media = media
            
        
    
    def TIMEREventCheckIfShouldShow( self, event ):
        
        try:
            
            if self._current_media is None:
                
                self.Hide()
                
            else:
                
                ( mouse_x, mouse_y ) = wx.GetMousePosition()
                
                ( my_width, my_height ) = self.GetSize()
                
                ( should_resize, ( my_ideal_width, my_ideal_height ), ( my_ideal_x, my_ideal_y ) ) = self._GetIdealSizeAndPosition()
                
                if my_ideal_width == -1: my_ideal_width = my_width
                if my_ideal_height == -1: my_ideal_height = my_height
                
                in_x = my_ideal_x <= mouse_x and mouse_x <= my_ideal_x + my_ideal_width
                in_y = my_ideal_y <= mouse_y and mouse_y <= my_ideal_y + my_ideal_height
                
                menu_open = HydrusGlobals.client_controller.MenuIsOpen()
                
                dialog_open = False
                
                tlps = wx.GetTopLevelWindows()
                
                for tlp in tlps:
                    
                    if isinstance( tlp, wx.Dialog ):
                        
                        dialog_open = True
                        
                    
                
                mime = self._current_media.GetMime()
                
                in_position = in_x and in_y
                
                mouse_is_over_interactable_media = mime == HC.APPLICATION_FLASH and self.GetParent().MouseIsOverMedia()
                
                mouse_is_near_animation_bar = self.GetParent().MouseIsNearAnimationBar()
                
                mouse_is_over_something_important = mouse_is_over_interactable_media or mouse_is_near_animation_bar
                
                current_focus_tlp = wx.GetTopLevelParent( wx.Window.FindFocus() )
                
                canvas_parent_tlp = wx.GetTopLevelParent( self.GetParent() )
                
                if current_focus_tlp in ( self, canvas_parent_tlp ):
                    
                    focus_is_good = True
                    
                else:
                    
                    focus_is_good = False
                    
                
                ready_to_show = in_position and not mouse_is_over_something_important and focus_is_good and not dialog_open and not menu_open
                ready_to_hide = not menu_open and ( not in_position or dialog_open or not focus_is_good )
                
                if ready_to_show:
                    
                    self._SizeAndPosition()
                    
                    self.Show()
                    
                elif ready_to_hide:
                    
                    self.Hide()
                    
                
            
        except wx.PyDeadObjectError:
            
            self._timer_check_show.Stop()
            
        except:
            
            self._timer_check_show.Stop()
            
            raise
            
        

class FullscreenHoverFrameCommands( FullscreenHoverFrame ):
    
    def __init__( self, parent, canvas_key ):
        
        FullscreenHoverFrame.__init__( self, parent, canvas_key )
        
        self._always_archive = False
        self._current_zoom = 1.0
        self._current_index_string = ''
        
        vbox = wx.BoxSizer( wx.VERTICAL )
        
        self._first_button = wx.BitmapButton( self, bitmap = CC.GlobalBMPs.first )
        self._first_button.Bind( wx.EVT_BUTTON, lambda event: HydrusGlobals.client_controller.pub( 'canvas_show_first', self._canvas_key ) )
        self._first_button.SetToolTipString( 'first' )
        
        self._previous_button = wx.BitmapButton( self, bitmap = CC.GlobalBMPs.previous )
        self._previous_button.Bind( wx.EVT_BUTTON, lambda event: HydrusGlobals.client_controller.pub( 'canvas_show_previous', self._canvas_key ) )
        self._previous_button.SetToolTipString( 'previous' )
        
        self._index_text = wx.StaticText( self, label = 'index' )
        
        self._next_button = wx.BitmapButton( self, bitmap = CC.GlobalBMPs.next )
        self._next_button.Bind( wx.EVT_BUTTON, lambda event: HydrusGlobals.client_controller.pub( 'canvas_show_next', self._canvas_key ) )
        self._next_button.SetToolTipString( 'next' )
        
        self._last_button = wx.BitmapButton( self, bitmap = CC.GlobalBMPs.last )
        self._last_button.Bind( wx.EVT_BUTTON, lambda event: HydrusGlobals.client_controller.pub( 'canvas_show_last', self._canvas_key ) )
        self._last_button.SetToolTipString( 'last' )
        
        self._archive_button = wx.BitmapButton( self, bitmap = CC.GlobalBMPs.archive )
        self._archive_button.Bind( wx.EVT_BUTTON, self.EventArchiveButton )
        
        self._trash_button = wx.BitmapButton( self, bitmap = CC.GlobalBMPs.delete )
        self._trash_button.Bind( wx.EVT_BUTTON, lambda event: HydrusGlobals.client_controller.pub( 'canvas_delete', self._canvas_key ) )
        self._trash_button.SetToolTipString( 'send to trash' )
        
        self._delete_button = wx.BitmapButton( self, bitmap = CC.GlobalBMPs.trash_delete )
        self._delete_button.Bind( wx.EVT_BUTTON, lambda event: HydrusGlobals.client_controller.pub( 'canvas_delete', self._canvas_key ) )
        self._delete_button.SetToolTipString( 'delete completely' )
        
        self._undelete_button = wx.BitmapButton( self, bitmap = CC.GlobalBMPs.undelete )
        self._undelete_button.Bind( wx.EVT_BUTTON, lambda event: HydrusGlobals.client_controller.pub( 'canvas_undelete', self._canvas_key ) )
        self._undelete_button.SetToolTipString( 'undelete' )
        
        self._zoom_text = wx.StaticText( self, label = 'zoom' )
        
        zoom_in = wx.BitmapButton( self, bitmap = CC.GlobalBMPs.zoom_in )
        zoom_in.Bind( wx.EVT_BUTTON, lambda event: HydrusGlobals.client_controller.pub( 'canvas_zoom_in', self._canvas_key ) )
        zoom_in.SetToolTipString( 'zoom in' )
        
        zoom_out = wx.BitmapButton( self, bitmap = CC.GlobalBMPs.zoom_out )
        zoom_out.Bind( wx.EVT_BUTTON, lambda event: HydrusGlobals.client_controller.pub( 'canvas_zoom_out', self._canvas_key ) )
        zoom_out.SetToolTipString( 'zoom out' )
        
        zoom_switch = wx.BitmapButton( self, bitmap = CC.GlobalBMPs.zoom_switch )
        zoom_switch.Bind( wx.EVT_BUTTON, lambda event: HydrusGlobals.client_controller.pub( 'canvas_zoom_switch', self._canvas_key ) )
        zoom_switch.SetToolTipString( 'zoom switch' )
        
        fullscreen_switch = wx.BitmapButton( self, bitmap = CC.GlobalBMPs.fullscreen_switch )
        fullscreen_switch.Bind( wx.EVT_BUTTON, lambda event: HydrusGlobals.client_controller.pub( 'canvas_fullscreen_switch', self._canvas_key ) )
        fullscreen_switch.SetToolTipString( 'fullscreen switch' )
        
        open_externally = wx.BitmapButton( self, bitmap = CC.GlobalBMPs.open_externally )
        open_externally.Bind( wx.EVT_BUTTON, lambda event: HydrusGlobals.client_controller.pub( 'canvas_open_externally', self._canvas_key ) )
        open_externally.SetToolTipString( 'open externally' )
        
        close = wx.Button( self, label = 'X', style = wx.BU_EXACTFIT )
        close.Bind( wx.EVT_BUTTON, lambda event: HydrusGlobals.client_controller.pub( 'canvas_close', self._canvas_key ) )
        close.SetToolTipString( 'close' )
        
        self._top_hbox = wx.BoxSizer( wx.HORIZONTAL )
        self._title_text = wx.StaticText( self, label = 'title' )
        self._info_text = wx.StaticText( self, label = 'info' )
        self._button_hbox = wx.BoxSizer( wx.HORIZONTAL )
        
        self._top_hbox.AddF( self._first_button, CC.FLAGS_MIXED )
        self._top_hbox.AddF( self._previous_button, CC.FLAGS_MIXED )
        self._top_hbox.AddF( self._index_text, CC.FLAGS_MIXED )
        self._top_hbox.AddF( self._next_button, CC.FLAGS_MIXED )
        self._top_hbox.AddF( self._last_button, CC.FLAGS_MIXED )
        self._top_hbox.AddF( ( 20, 20 ), CC.FLAGS_EXPAND_BOTH_WAYS )
        self._top_hbox.AddF( self._archive_button, CC.FLAGS_MIXED )
        self._top_hbox.AddF( self._trash_button, CC.FLAGS_MIXED )
        self._top_hbox.AddF( self._delete_button, CC.FLAGS_MIXED )
        self._top_hbox.AddF( self._undelete_button, CC.FLAGS_MIXED )
        self._top_hbox.AddF( ( 20, 20 ), CC.FLAGS_EXPAND_BOTH_WAYS )
        self._top_hbox.AddF( self._zoom_text, CC.FLAGS_MIXED )
        self._top_hbox.AddF( zoom_in, CC.FLAGS_MIXED )
        self._top_hbox.AddF( zoom_out, CC.FLAGS_MIXED )
        self._top_hbox.AddF( zoom_switch, CC.FLAGS_MIXED )
        self._top_hbox.AddF( fullscreen_switch, CC.FLAGS_MIXED )
        self._top_hbox.AddF( open_externally, CC.FLAGS_MIXED )
        self._top_hbox.AddF( close, CC.FLAGS_MIXED )
        
        vbox.AddF( self._top_hbox, CC.FLAGS_EXPAND_PERPENDICULAR )
        vbox.AddF( self._title_text, CC.FLAGS_CENTER )
        vbox.AddF( self._info_text, CC.FLAGS_CENTER )
        vbox.AddF( self._button_hbox, CC.FLAGS_CENTER )
        
        self.SetSizer( vbox )
        
        HydrusGlobals.client_controller.sub( self, 'SetCurrentZoom', 'canvas_new_zoom' )
        HydrusGlobals.client_controller.sub( self, 'SetIndexString', 'canvas_new_index_string' )
        HydrusGlobals.client_controller.sub( self, 'ProcessContentUpdates', 'content_updates_gui' )
        
        self.Bind( wx.EVT_MOUSEWHEEL, self.EventMouseWheel )
        
    
    def _GetIdealSizeAndPosition( self ):
        
        parent = self.GetParent()
        
        ( parent_width, parent_height ) = parent.GetClientSize()
        
        ( my_width, my_height ) = self.GetSize()
        
        my_ideal_width = int( parent_width * 0.6 )
        
        should_resize = my_ideal_width != my_width
        
        ideal_size = ( my_ideal_width, -1 )
        ideal_position = parent.ClientToScreenXY( int( parent_width * 0.2 ), 0 )
        
        return ( should_resize, ideal_size, ideal_position )
        
    
    def _ResetButtons( self ):
        
        if self._current_media is not None:
            
            if self._always_archive or self._current_media.HasInbox():
                
                self._archive_button.SetBitmapLabel( CC.GlobalBMPs.archive )
                self._archive_button.SetToolTipString( 'archive' )
                
            else:
                
                self._archive_button.SetBitmapLabel( CC.GlobalBMPs.to_inbox )
                self._archive_button.SetToolTipString( 'return to inbox' )
                
            
            current_locations = self._current_media.GetLocationsManager().GetCurrent()
            
            if CC.LOCAL_FILE_SERVICE_KEY in current_locations:
                
                self._trash_button.Show()
                self._delete_button.Hide()
                self._undelete_button.Hide()
                
            elif CC.TRASH_SERVICE_KEY in current_locations:
                
                self._trash_button.Hide()
                self._delete_button.Show()
                self._undelete_button.Show()
                
            
        
    
    def _ResetText( self ):
        
        if self._current_media is None:
            
            self._title_text.Hide()
            self._info_text.Hide()
            
        else:
            
            label = self._current_media.GetTitleString()
            
            if len( label ) > 0:
                
                self._title_text.SetLabelText( label )
                
                self._title_text.Show()
                
            else: self._title_text.Hide()
            
            lines = self._current_media.GetPrettyInfoLines()
            
            label = ' | '.join( lines )
            
            self._info_text.SetLabelText( label )
            
            self._info_text.Show()
            
        
    
    def AddCommand( self, label, callback ):
        
        command = wx.Button( self, label = label, style = wx.BU_EXACTFIT )
        command.Bind( wx.EVT_BUTTON, callback )
        
        self._button_hbox.AddF( command, CC.FLAGS_MIXED )
        
    
    def EventArchiveButton( self, event ):
        
        if self._always_archive or self._current_media.HasInbox():
            
            HydrusGlobals.client_controller.pub( 'canvas_archive', self._canvas_key )
            
        else:
            
            HydrusGlobals.client_controller.pub( 'canvas_inbox', self._canvas_key )
            
        
    
    def EventMouseWheel( self, event ):
        
        event.ResumePropagation( 1 )
        event.Skip()
        
    
    def ProcessContentUpdates( self, service_keys_to_content_updates ):
        
        if self._current_media is not None:
            
            my_hash = self._current_media.GetHash()
            
            do_redraw = False
            
            for ( service_key, content_updates ) in service_keys_to_content_updates.items():
                
                if True in ( my_hash in content_update.GetHashes() for content_update in content_updates ):
                    
                    do_redraw = True
                    
                    break
                    
                
            
            if do_redraw:
                
                self._ResetButtons()
                
                self.Fit()
                
                self._SizeAndPosition()
                
            
        
    
    def SetAlwaysArchive( self, value ):
        
        self._always_archive = value
        
        self._ResetButtons()
        
    
    def SetCurrentZoom( self, canvas_key, zoom ):
        
        if canvas_key == self._canvas_key:
            
            self._current_zoom = zoom
            
            label = ClientData.ConvertZoomToPercentage( self._current_zoom )
            
            self._zoom_text.SetLabelText( label )
            
            self._top_hbox.Layout()
            
        
    
    def SetDisplayMedia( self, canvas_key, media ):
        
        if canvas_key == self._canvas_key:
            
            FullscreenHoverFrame.SetDisplayMedia( self, canvas_key, media )
            
            self._ResetButtons()
            
            self._ResetText()
            
            self.Fit()
            
            self._SizeAndPosition()
            
        
    
    def SetIndexString( self, canvas_key, text ):
        
        if canvas_key == self._canvas_key:
            
            self._current_index_string = text
            
            self._index_text.SetLabelText( self._current_index_string )
            
            self._top_hbox.Layout()
            
        
    
    def SetNavigable( self, value ):
        
        if value:
            
            self._first_button.Show()
            self._last_button.Show()
            
            self._previous_button.SetToolTipString( 'previous' )
            self._next_button.SetToolTipString( 'next' )
            
        else:
            
            self._first_button.Hide()
            self._last_button.Hide()
            
            self._previous_button.SetToolTipString( 'back' )
            self._next_button.SetToolTipString( 'skip' )

class FullscreenHoverFrameRatings( FullscreenHoverFrame ):
    
    def __init__( self, parent, canvas_key ):
        
        FullscreenHoverFrame.__init__( self, parent, canvas_key )
        
        vbox = wx.BoxSizer( wx.VERTICAL )
        
        self._icon_panel = wx.Panel( self )
        
        self._icon_panel.SetBackgroundColour( wx.WHITE )
        
        self._trash_icon = ClientGUICommon.BufferedWindowIcon( self._icon_panel, CC.GlobalBMPs.trash )
        self._inbox_icon = ClientGUICommon.BufferedWindowIcon( self._icon_panel, CC.GlobalBMPs.inbox )
        
        icon_hbox = wx.BoxSizer( wx.HORIZONTAL )
        
        icon_hbox.AddF( ( 16, 16 ), CC.FLAGS_EXPAND_SIZER_BOTH_WAYS )
        icon_hbox.AddF( self._trash_icon, CC.FLAGS_MIXED )
        icon_hbox.AddF( self._inbox_icon, CC.FLAGS_MIXED )
        
        self._icon_panel.SetSizer( icon_hbox )
        
        # repo strings
        
        self._file_repos = wx.StaticText( self, label = '', style = wx.ALIGN_RIGHT )
        
        # likes
        
        like_hbox = wx.BoxSizer( wx.HORIZONTAL )
        
        like_hbox.AddF( ( 16, 16 ), CC.FLAGS_EXPAND_BOTH_WAYS )
        
        like_services = HydrusGlobals.client_controller.GetServicesManager().GetServices( ( HC.LOCAL_RATING_LIKE, ), randomised = False )
        
        for service in like_services:
            
            service_key = service.GetServiceKey()
            
            control = ClientGUICommon.RatingLikeCanvas( self, service_key, canvas_key )
            
            like_hbox.AddF( control, CC.FLAGS_NONE )
            
        
        # each numerical one in turn
        
        vbox.AddF( self._icon_panel, CC.FLAGS_EXPAND_SIZER_BOTH_WAYS )
        vbox.AddF( self._file_repos, CC.FLAGS_EXPAND_BOTH_WAYS )
        vbox.AddF( like_hbox, CC.FLAGS_EXPAND_SIZER_BOTH_WAYS )
        
        numerical_services = HydrusGlobals.client_controller.GetServicesManager().GetServices( ( HC.LOCAL_RATING_NUMERICAL, ), randomised = False )
        
        for service in numerical_services:
            
            service_key = service.GetServiceKey()
            
            control = ClientGUICommon.RatingNumericalCanvas( self, service_key, canvas_key )
            
            hbox = wx.BoxSizer( wx.HORIZONTAL )
            
            hbox.AddF( ( 16, 16 ), CC.FLAGS_EXPAND_SIZER_BOTH_WAYS )
            hbox.AddF( control, CC.FLAGS_NONE )
            
            vbox.AddF( hbox, CC.FLAGS_EXPAND_SIZER_BOTH_WAYS )
            
        
        self.SetSizer( vbox )
        
        self._ResetData()
        
        HydrusGlobals.client_controller.sub( self, 'ProcessContentUpdates', 'content_updates_gui' )
        
        self.Bind( wx.EVT_MOUSEWHEEL, self.EventMouseWheel )
        
    
    def _GetIdealSizeAndPosition( self ):
        
        parent = self.GetParent()
        
        ( parent_width, parent_height ) = parent.GetClientSize()
        
        ( my_width, my_height ) = self.GetSize()
        
        my_ideal_width = int( parent_width * 0.2 )
        
        should_resize = my_ideal_width != my_width
        
        ideal_size = ( my_ideal_width, -1 )
        ideal_position = parent.ClientToScreenXY( int( parent_width * 0.8 ), 0 )
        
        return ( should_resize, ideal_size, ideal_position )
        
    
    def _ResetData( self ):
        
        if self._current_media is not None:
            
            has_inbox = self._current_media.HasInbox()
            has_trash = CC.TRASH_SERVICE_KEY in self._current_media.GetLocationsManager().GetCurrent()
            
            if has_inbox or has_trash:
                
                self._icon_panel.Show()
                
                if has_inbox:
                    
                    self._inbox_icon.Show()
                    
                else:
                    
                    self._inbox_icon.Hide()
                    
                
                if has_trash:
                    
                    self._trash_icon.Show()
                    
                else:
                    
                    self._trash_icon.Hide()
                    
                
            else:
                
                self._icon_panel.Hide()
                
            
            remote_strings = self._current_media.GetLocationsManager().GetRemoteLocationStrings()
            
            if len( remote_strings ) == 0:
                
                self._file_repos.Hide()
                
            else:
                
                remote_string = os.linesep.join( remote_strings )
                
                self._file_repos.SetLabelText( remote_string )
                
                self._file_repos.Show()
                
            
            self.Fit()
            
        
        self._SizeAndPosition()
        
    
    def EventMouseWheel( self, event ):
        
        event.ResumePropagation( 1 )
        event.Skip()
        
    
    def ProcessContentUpdates( self, service_keys_to_content_updates ):
        
        if self._current_media is not None:
            
            my_hash = self._current_media.GetHash()
            
            do_redraw = False
            
            for ( service_key, content_updates ) in service_keys_to_content_updates.items():
                
                if True in ( my_hash in content_update.GetHashes() for content_update in content_updates ):
                    
                    if True in ( content_update.IsInboxRelated() for content_update in content_updates ):
                        
                        do_redraw = True
                        
                        break
                        
                    
                
            
            if do_redraw:
                
                self._ResetData()
                
            
        
    
    def SetDisplayMedia( self, canvas_key, media ):
        
        if canvas_key == self._canvas_key:
            
            FullscreenHoverFrame.SetDisplayMedia( self, canvas_key, media )
            
            self._ResetData()
            
        

class FullscreenHoverFrameTags( FullscreenHoverFrame ):
    
    def __init__( self, parent, canvas_key ):
        
        FullscreenHoverFrame.__init__( self, parent, canvas_key )
        
        vbox = wx.BoxSizer( wx.VERTICAL )
        
        self._tags = ClientGUICommon.ListBoxTagsSelectionHoverFrame( self, self._canvas_key )
        
        vbox.AddF( self._tags, CC.FLAGS_EXPAND_SIZER_BOTH_WAYS )
        
        self.SetSizer( vbox )
        
        HydrusGlobals.client_controller.sub( self, 'ProcessContentUpdates', 'content_updates_gui' )
        
    
    def _GetIdealSizeAndPosition( self ):
        
        parent = self.GetParent()
        
        ( parent_width, parent_height ) = parent.GetClientSize()
        
        ( my_width, my_height ) = self.GetSize()
        
        my_ideal_width = int( parent_width * 0.2 )
        
        my_ideal_height = parent_height
        
        should_resize = my_ideal_width != my_width or my_ideal_height != my_height
        
        ideal_size = ( my_ideal_width, my_ideal_height )
        ideal_position = parent.ClientToScreenXY( 0, 0 )
        
        return ( should_resize, ideal_size, ideal_position )
        
    
    def _ResetTags( self ):
        
        if self._current_media is not None:
            
            self._tags.SetTagsByMedia( [ self._current_media ], force_reload = True )
            
        
    
    def ProcessContentUpdates( self, service_keys_to_content_updates ):
        
        if self._current_media is not None:
            
            my_hash = self._current_media.GetHash()
            
            do_redraw = False
            
            for ( service_key, content_updates ) in service_keys_to_content_updates.items():
                
                if True in ( my_hash in content_update.GetHashes() for content_update in content_updates ):
                    
                    do_redraw = True
                    
                    break
                    
                
            
            if do_redraw:
                
                self._ResetTags()
                
            
        
    
    def SetDisplayMedia( self, canvas_key, media ):
        
        if canvas_key == self._canvas_key:
            
            FullscreenHoverFrame.SetDisplayMedia( self, canvas_key, media )
            
            self._ResetTags()
            
        
    