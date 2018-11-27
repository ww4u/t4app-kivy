from kivy.app import App 

from kivy.uix.behaviors import DragBehavior

from kivy.uix.screenmanager import Screen, ScreenManager

from kivy.uix.widget import Widget 
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.actionbar import ActionBar
from kivy.uix.bubble import Bubble

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.stacklayout import StackLayout

from kivy.uix.actionbar import ActionItem
from kivy.uix.filechooser import FileChooserListView


from kivy.properties import StringProperty
from kivy.properties import ObjectProperty
from kivy.properties import NumericProperty
from kivy.properties import BooleanProperty

from kivy.clock import Clock

from kivy.config import ConfigParser
from kivy.uix.settings import Settings

import os,math,json
from multiprocessing import Process
from threading import Thread

import win32process, win32event
from functools import partial

# complier
from streamcompile import StreamCompile

class SaveLoadDialog( FloatLayout ):
    accept = ObjectProperty(None)
    cancel=ObjectProperty(None)
    text_input=ObjectProperty(None)
    accept_text=StringProperty()

class ProgressDialog( BoxLayout ):
    value = NumericProperty(0)
    cancel = ObjectProperty(None)
    pass 


def obj2dict( obj ):
    d={}
    d['__class__'] = obj.__class__.__name__ 
    d['__module__'] = obj.__module__
    # d.update( obj.__dict__ )
    d['text'] = obj.text 
    d['values'] = obj.values 
    d['para_able'] = obj.paraAble
    d['paras'] = obj.paras 
    d['tab_id'] = obj.tabId
    return d

def dict2obj( d ):    
    # if '__class__' in d:
    #     class_name = d.pop( '__class__' )
    #     module_name = d.pop( '__module__')
    #     module = __import__( module_name )
    #     class_ = getattr( module, class_name )
    #     args = dict( (key.encode('ascii'), value ) for key, value in d.items() )
    #     instance = class_(**args)
    # else:
    #     instance = d
    # return instance 

    item = RoboActionItem()
    item.text = d['text']
    item.values = d['values']
    item.paraAble = d['para_able']
    item.paras = d['paras']
    item.tabId = d['tab_id']
    return item  

class RoboActionItem( DragBehavior, BoxLayout ):
    values = ObjectProperty(None)
    paras = ObjectProperty(None)
    para = StringProperty()
    paraAble = BooleanProperty()
    tabId = NumericProperty(1)

    drag_touch_up = ObjectProperty(None)

    def on_toggle( self, state ):
        print( state )
        if ( 'normal' == state ):
            # self.ids.toggle.window_state = 'hide'
            self.remove_widget( self.textInput )
        else:
            # self.ids.toggle.window_state = 'show'
            self.add_widget( self.textInput )
            # self.ids.toggle.visible = True 

    def serialOut( self, stream ):
        # stream.write

        stream.write( json.dumps(obj2dict(self)) )

        # if ( self.paraAble ):
        #     stream.write( self.text + " " + self.ids.para.text + "\n")
        # else: 
        #     stream.write( self.text )  

    def serialIn( self, stream ):
        pass 

    def on_touch_up(self, touch):
        super( RoboActionItem, self).on_touch_up( touch )
        if self.drag_touch_up:
            self.drag_touch_up( self, touch )

    # def drag_touch_up(self):
    #     print( "touch up" )

def postProcess( args ):
    # print( args )
    os.system( args )

# arg1
# arg2=( on_start, on_end, on_progress )
def testRunProcess( arg1, arg2 ):
    # print('hello*5')
    print( arg1 )

    arg2[0]( )
    arg2[2]( 50 )
    os.system( arg1 )
    arg2[2]( 100 )
    arg2[1]() 

    print("end")

# class Scripts( BoxLayout ):
class Scripts( GridLayout ):
# class Scripts( FloatLayout ):
    text = StringProperty()
    compileMode = StringProperty()
    script_cancel = ObjectProperty()

    def add_script( self, temp, paras ):
        
        newItem = RoboActionItem()
        newItem.text = temp.name
        newItem.tabId = len( self.children ) + 1

        newItem.paraAble = temp.paraAble
        newItem.values = temp.values

        print( temp.values )

        newItem.drag_touch_up = self.drag_touch_up
        if ( not temp.paraAble ):
            newItem.remove_widget( newItem.ids.para )
            newItem.remove_widget( newItem.ids.toggle )
        else:
            newItem.paras = ( float(paras[0]), float(paras[1]), float(paras[2]), float(paras[3])  )
            # newItem.values = newItem.paras

        # txt input
        print( newItem.ids.toggle.state )
        if ( newItem.ids.toggle.state == 'normal' ):
            newItem.remove_widget( newItem.ids.para )    
        else:
            pass

        self.add_widget( newItem ) 
        # self.mWigList.append( newItem )

        # newItem.fbind( newItem.pos, self._trigger_layout )

    def add_local_script( self, item ):
        item.drag_touch_up = self.drag_touch_up
        if not item.paraAble:
            item.remove_widget( item.ids.para )
        else:
            pass 
        self.add_widget( item )                 

    def drag_touch_up( self, *args ):
        # pass
        # Clock.sch
        Clock.schedule_once(partial(self.reLayout, *args ), .1)

    def export_script( self, path, fileName ):
        self._popup.dismiss()
        abPath = os.path.abspath( path )
        
        sep = fileName.rfind( '\\' )
        self.text = fileName
        if ( sep != -1 ):
            self.text = fileName[sep+1:]  
        with open( os.path.join( abPath, fileName+".json"), 'w' ) as stream:
            if not stream:
                return 
            self.text = fileName    
            for obj in self.children:
                stream.write( json.dumps( obj2dict(obj) ) + "\n" )     

    def import_script( self, path, fileName ):
        self._popup.dismiss()           

        self.clear_widgets()
        abPath = os.path.abspath( path )
        with open( os.path.join( abPath, fileName), 'r' ) as stream:
            if not stream:
                return
            sep = fileName.rfind( '\\' )
            self.text = fileName
            if ( sep != -1 ):
                self.text = fileName[sep+1:] 

            childList = list()                    
            for line in stream:
                item = json.loads( line, object_hook=dict2obj )
                self.add_local_script( item ) 
                childList.append( item )
                # print( item.text )      
            self.children.clear()
            self.children = childList[:]                                 

    def dismiss_popup( self ):
        self._popup.dismiss()
    def on_export( self, btn ):
        # pop up the file name
        #                 
        dlg = SaveLoadDialog( accept=self.export_script, 
                              cancel=self.dismiss_popup,
                              accept_text = 'Save'
                               )
        dlg.ids.fileChooser.rootpath =os.path.abspath( os.curdir )  
                                    
        self._popup = Popup( title="Save file",
                            content=dlg,
                            size_hint=(0.9,0.5), pos_hint={ 'top': 1.0 } ) 
        self._popup.open()                                                                                     

    def on_import( self, btn ):
        # pop up the file name
        #                 
        dlg = SaveLoadDialog( accept=self.import_script, 
                              cancel=self.dismiss_popup,
                              accept_text = 'Load'  )
        dlg.ids.fileChooser.rootpath =os.path.abspath( os.curdir )                                
        self._popup = Popup( title="Load file",
                            content=dlg,
                            size_hint=(0.9,0.5), pos_hint={ 'top': 1.0 } ) 
        self._popup.open()  

    # def run_process( self, args ):
    #     print( "hello" )
    #     pass 

    def on_run( self ):
        
        # compile
        self.compile( )

        # proc = Process( target = postProcess, args=("python " + "G:/study/kivy/_local.py",) )
        # proc = Process( target = testRunProcess, args=('0') )
        # proc.dameon = False

        filePath = os.path.abspath( os.path.curdir ) + "/cache/"
        self._proc = Thread( target = testRunProcess, args=("python " + filePath + "_local.py", 
                                                            ( self.on_start, self.on_end, self.on_progress ) ) )        
        self.createProgress()

        self._proc.start()

    # stop the process
    def on_stop( self ):
        # if ( self._proc ):
            
            # process
            # unschedule the clock

        self.script_cancel( )

        self.on_end()

            # mgr = DevMgr()
            # mgr.terminate()
            # mgr.stop()

        pass 

        # self.compile()

        # self.createProgress()                         

        # with open( "G:/study/kivy/test.json", 'w' ) as stream:
        #     for obj in self.children:
        #         stream.write( json.dumps( obj2dict(obj) ) + "\n" )

        # self.clear_widgets()
        # with open( "G:/study/kivy/test.json", 'r' ) as stream:
        #     for line in stream:
        #         # print( line )
        #         # item = RoboActionItem()
        #         item = json.loads( line, object_hook=dict2obj )
        #         self.add_local_script( item )
        # pass         

        # print( self.compileMode )

    def on_clear( self ):
        self.clear_widgets()

    def on_column( self, col ):
        self.cols = int(col)       

    # crate process
    def createProgress( self ):
        # create the progress
        dlg = ProgressDialog( 
                              cancel=self.on_cancel
                                 )
        self._progress = Popup( title = 'Progress',
                                content=dlg,
                                size_hint=(0.8,0.4), pos_hint={ 'top': 0.8 } )
               

    def on_start( self ):
        self._progress.open()   
        pass 

    def on_end( self ):
        self._proc = None
        self._progress.dismiss()

        pass         
    # cancel
    def on_cancel( self ):
        print('cancel')
        self._progress.dismiss()

        # \todo terminate
        self.on_stop()

        pass 

    # progress
    def on_progress( self, val ):
        if self._progress:
            # self._progress.value = val 
            # self._progress.content.ids.pb.value = val 
            self._progress.content.value = val 
            print( val )
        else:
            print( val, "*"*10 )            

    def compile( self ):
        complier = StreamCompile( 1 if self.compileMode=='down' else 0,
                                  os.path.abspath( os.path.curdir ) + "/cache" )

        # context 
        hand = self.cfg.getfloat( 'config', 'hand' )

        with open( 'cache/_local.py', 'w' ) as stream:
            complier.attachStream( stream )
            complier.genHead()
            complier.genMain()
            
            print( self.autoSpeed )
            for wig in reversed(self.children):
                complier.input( wig.cmd, 
                                self.autoSpeed, 
                                hand, 
                                wig.para )
            complier.genEnd()

    def reLayout( self, *kwargs ):
        # print( kwargs[0] )
        self.sort_the_pos()
        self._trigger_layout()
        # print ( kwargs[1].pos[0], kwargs[1].pos[1] )
        # for obj in self.children:
        #     # if ( obj.collide_point( kwargs[1].pos[0], kwargs[1].pos[1] ) ):
        #     if ( obj.collide_point( *kwargs[1].pos ) ):
        #         print( obj.text, kwargs[0].text )

    def on_test( self, *args ):
        print( 'test' )

        self.compile( )

        # self.sort_the_pos()

        # self._trigger_layout()
        # complier = StreamCompile()

        # with open( '_local.py', 'w' ) as stream:
        #     complier.attachStream( stream )
        #     complier.genHead()
        #     complier.genMain()
        #     for wig in self.mWigList:
                
        #         complier.input( wig.cmd, wig.para )

        #     complier.genEnd()
        # pass 

    def sort_the_pos( self ):
        objList = list()
        for obj in self.children:
            objList.append( ( obj.pos[0], obj.pos[1], obj ) )
        # sort by iter y            
        objList.sort( key=lambda iter:(iter[1]))

        # print("y*"*5)
        # for a in objList:
        #     print( a[2].text )

        # sort by x
        # objList.sort( key=lambda iter:(iter[0]) )
        # print("x*"*5)
        # for a in objList:
        #     print( a[2].text )
        
        norList = objList[:]
        norList.reverse()
        
        orderedList = list()
        split = 0
        gpCnt = int( (len(norList)+self.cols-1)/self.cols )
        for split in range( gpCnt ):
            if ( split == gpCnt-1  ):
                subList = norList[ split * self.cols: ]
            else:
                subList = norList[ split * self.cols: (split+1) * self.cols ]

            subList.sort( key=lambda iter:(iter[0]) )    
            for obj in subList:
                orderedList.append( obj )

        self.children.clear()
        orderedList.reverse()
        # print( len(orderedList) 

        for obj in orderedList:
            self.children.append( obj[2] ) 
            
        #     self.remove_widget( obj[2] )

        # for obj in orderedList:          
        #     self.add_widget( obj[2] )
        #     # print( obj[2].text )

    def on_para_set( self, *vals ):
        print( *vals )
        # the current item
        pass                         

class LeftBorder( BoxLayout ):
    pass

class RightBorder( BoxLayout ):
    pass

class OpsBar( BoxLayout ):
    pass 

class CoordButton( BoxLayout ):
    pass

# class ImageButton(Button):
#     pass     

class ToolButtons( BoxLayout ):
    # pass 
    def show_bubble( self ):
        # if not hasattr( self, 'bubble' ):
        #     self.bubble = OpsBubble()
        #     # self.add_widget( self.bubble )
        #     self.bubble.arrow_pos='top_mid'  
        # else:
        #     self.bubble.arrow_pos='top_mid'            

        pop = OpsPopup()
        
        popup = Popup( content = pop, title='ops', size_hint=(0.5,0.5) )

        pop.dismiss_pop = partial( self.dismiss_bubble, popup )

        popup.open()

    def dismiss_bubble(self, bubble ):
        bubble.dismiss()

    def on_release( self, btn ):
        print( btn )        

class InfoPanel( BoxLayout ):
    pass 

class SpeedPanel( BoxLayout ):
    pass 

class JointsButton( BoxLayout ):
    pass 
    # text = StringProperty()
    # pass 
    # def __init__( self, **kwargs ):
    #     super( joints_button, self ).__init__( **kwargs )     

class OpsPopup( BoxLayout ):
# class OpsPopup( Popup ):
    # on_dismiss = ObjectProperty(None)
    pass 
    # pass 

class FileMgr(BoxLayout):
    pass 

class ActionMgr(BoxLayout):
    pass 

class ScriptMgr(BoxLayout):
    manualSpeed = NumericProperty(10)
    autoSpeed = NumericProperty(50)
    compileMode = StringProperty()
    pass         

class LeftBar(BoxLayout):
    pass      

class RightBar(BoxLayout):
    pass           

class MActionButton( Button, ActionItem ):
    pass 

class MActionBar( ActionBar ):
    pass 

class MainScreen(Screen):
    pass 
    # def on_test( self ):
    #     print('test')

class SettingScreen(Screen):
    pass 
    
class MainFrame(BoxLayout):
    pass 
    # def on_test( self ):
    #     print('test')
        # ids.sm.on_test()
        # print( self.ids.sm.screens[0].ids )

from mrq.MRQ import MRQ 
from mrq.sinanju import Sinanju 
from mrq.mgr import DevMgr 

config_json="""
[
{
"type": "title",
"title": "windows",
"text": "Config"
},

{
"type": "numeric",
"title": "Step",
"desc": "The step of x/y/z in mm",
"section": "config",
"key": "step"
},

{
"type": "numeric",
"title": "Hand",
"desc": "The hand expand angle",
"section": "config",
"key": "hand"
},

{
"type": "numeric",
"title": "max speed",
"desc": "The max speed in mm/s",
"section": "config",
"key": "max_speed"
}

]
"""

class JointBtnApp( App ):
    this_device = None
    this_robo = None
    this_clock_event = None
    _cfg = ObjectProperty(None)

    icon = 'image/m.png'

    def build(self):
        
        self.frame = MainFrame()

        parser = ConfigParser()
        parser.read("jointbtn.ini")
        
        # parser.

        self._cfg = parser

        s = Settings()
        s.add_json_panel( 'config', parser, data=config_json) 
 
        self.frame.ids.sm.screens[1].add_widget( s )

        self.coord = 'Both'

        return self.frame     

        # parser = ConfigParser()
        # parser.read("config.ini")
        
        # s = Settings()
        # s.add_json_panel( 'config', parser, data=config_json) 
        # return s

        # self.sm = ScreenManager()

        # ms = MainScreen()
        # ss = SettingScreen()

        # self.sm.add_widget( ms )
        # self.sm.add_widget( ss )

        # parser = ConfigParser()
        # parser.read("config.ini")
        
        # s = Settings()
        # s.add_json_panel( 'config', parser, data=config_json) 
        # ss.add_widget( s )

        # frame  = Scripts()
        # self.frame = frame
        
        # return self.sm

    # def build_config( self, config ):
        
    #     pass 

    def on_screen_n(self, txt, index ):
        # print( txt ) 
        # self.frame.ids.sm.switch_to(  self.frame.ids.sm.screens[ index ] )
        # self.frame.ids.sm.current = self.frame.ids.sm.screens[ index ]
        # print( self.frame.ids.sm.screens_name[ index ] )
        self.frame.ids.sm.current = self.frame.ids.sm.screens_name[ index ]
        # print ( self.frame.ids.sm )
            
    def on_home( self ):
        if ( self.this_device == None ):
            return 
        else:
            pass 

        self.this_robo.center( )            


    def on_fold( self ):
        if ( self.this_device == None ):
            return 
        else:
            pass 

        self.this_robo.fold( )             

    # force stop
    def on_fstop( self ):
        # print( self._cfg.getfloat('graphics', 'step' ) )

        # print( self.guessManualTime( 10 ) )
        # print( self.guessAutoTime( 10 ) )

        # force stop

        # cancel the connect
        if ( self.this_clock_event ):
            self.this_clock_event.cancel()

        if ( self.this_device ):
            connectBtn = self.frame.ids.sm.screens[0].ids.rightbar.ids.tools.ids.connect
            self.on_connect( connectBtn )
            connectBtn.state = 'normal'

        mgr = DevMgr()
        mgr.terminate()
        pass 

    def on_script_cancel( self ):
        # print( "script stop" )
        self.on_fstop()
        pass         

    def on_connect( self, btn ):
        if ( self.this_device == None ):
            self.this_device =  MRQ("device1")
            self.this_robo = Sinanju("MRX-T4")

            self.this_clock_event = Clock.schedule_interval( self.on_interval, 1 )

            btn.text = "Disconnect"
        else:
            self.this_device.close()
            self.this_robo.close()
            self.this_device = None
            self.this_robo = None

            self.this_clock_event.cancel()

            btn.text = "Connect"
        pass                         

    def on_coord( self, txt ):
        
        # pre preoc
        if ( self.coord == 'Both' ):            
            lb = self.frame.ids.sm.screens[0].ids.leftborder
            lb.remove_widget( lb.joint )
            lb.remove_widget( lb.world )

            rb = self.frame.ids.sm.screens[0].ids.rightborder 
            rb.remove_widget( rb.joint )
            rb.remove_widget( rb.world )

        elif ( self.coord == 'Joint' ):    
            lb = self.frame.ids.sm.screens[0].ids.leftborder
            lb.remove_widget( lb.joint )

            rb = self.frame.ids.sm.screens[0].ids.rightborder 
            rb.remove_widget( rb.joint )
        elif ( self.coord == 'World' ):                  
            lb = self.frame.ids.sm.screens[0].ids.leftborder
            lb.remove_widget( lb.world )

            rb = self.frame.ids.sm.screens[0].ids.rightborder 
            rb.remove_widget( rb.world ) 
        else:
            raise Exception("Invalid coord")            

        self.coord = txt 
        # add again
        if ( txt=='Both' ):
            lb = self.frame.ids.sm.screens[0].ids.leftborder
            lb.add_widget( lb.world )
            lb.add_widget( lb.joint )
            

            rb = self.frame.ids.sm.screens[0].ids.rightborder 
            rb.add_widget( rb.world )
            rb.add_widget( rb.joint )
            
        elif( txt == 'Joint' ):
            lb = self.frame.ids.sm.screens[0].ids.leftborder
            lb.add_widget( lb.joint )

            rb = self.frame.ids.sm.screens[0].ids.rightborder 
            rb.add_widget( rb.joint )    
            pass
        elif( txt == 'World' ):
            lb = self.frame.ids.sm.screens[0].ids.leftborder
            lb.add_widget( lb.world )

            rb = self.frame.ids.sm.screens[0].ids.rightborder 
            rb.add_widget( rb.world )
        else:
            pass                                    

    def on_joint_press( self, btn, id, txt ):
        print( id, txt )
        if ( self.this_device == None ):
            return 

        if ( txt == '-' ):
            self.this_device.move( id, 0, -self.manualSpeed(),1,-self.manualSpeed() )
        else:
            self.this_device.move( id, 0, self.manualSpeed(),1, self.manualSpeed() )                        
        pass 

    def on_joint_release( self, btn, id, txt ):
        print( id, txt )
        if ( self.this_device == None ):
            return 

        self.this_device.stop( id, 0 )

    def on_coord_release( self, btn, id, sign  ):
        print( id, sign )
        if ( self.this_device == None ):
            return 

        dir = 1
        if '-' in sign:
            dir = -1
        else:
            dir = 1            

        step = math.fabs( self._cfg.getfloat('config','step') )
        if ( id == 0 ):
            self.this_robo.stepX( 0,0, step * dir, step/self.manualSpeed() )
        elif id == 1:
            self.this_robo.stepY( 0,0, step * dir, step/self.manualSpeed() )
        elif id == 2:
            self.this_robo.stepZ( 0,0, step * dir, step/self.manualSpeed() )
        else:
            pass                                    

    def on_align( self ):
        if ( self.this_robo == None ):
            return 

        self.this_robo.align()            
        pass 

    def on_interval( self, dt ):
        # update pos
        poses = self.this_robo.pose()
        self.frame.ids.sm.screens[0].ids.leftbar.ids.info.values = poses

        return True

    def guess_time( self, dist, speed ):
        if ( math.fabs( speed ) < 0.001  ):
            raise Exception("Invalid speed")

        return math.fabs( dist ) / math.fabs(speed)               

    def manualSpeed( self ):
        maxSpeed = self._cfg.getfloat( 'config', 'max_speed' )
        slider = self.frame.ids.sm.screens[0].ids.rightbar.ids.manual
        
        return math.fabs( maxSpeed * slider.value / 100.0 )

    def autoSpeed( self ):
        maxSpeed = self._cfg.getfloat( 'config', 'max_speed' )
        slider = self.frame.ids.sm.screens[0].ids.rightbar.ids.auto
        
        return math.fabs( maxSpeed * slider.value / 100.0 )         

    def guessManualTime( self, dist ):
        return self.guess_time( dist, self.manualSpeed() )

    def guessAutoTime( self, dist ):
        return self.guess_time( dist, self.autoSpeed() )

if __name__=='__main__':
    JointBtnApp().run()        