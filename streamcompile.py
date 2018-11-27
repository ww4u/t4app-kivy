
import math
import time
import os 

class CompilerAssist():
    @staticmethod
    def euclidDistance( posA, posB ):
        # return ( math.pow( posA[0]-posB[0] ) )
        sum = 0
        for i in range( 3 ):
            sum += math.pow( posA[i] - posB[i], 2 )
        return math.sqrt( sum )

    @staticmethod        
    def euclidDt( posA, posB, speed ):
        if ( speed == 0.0 ):
            raise Exception("Invlaid speed")
        return CompilerAssist.euclidDistance( posA, posB ) / math.fabs( speed )           

class RoutePoint(  ):
    def __init__( self, pos=(0,0,0,0), dt=1, step=0 ):
        self.mPos = pos
        self.mDt = dt
        self.mStep = step

    def __repr__( self ):
        return "{4},({0},{1},{2},{3}),{5}".format( self.mPos[0], self.mPos[1], self.mPos[2], self.mPos[3], 
                                                   self.mDt,
                                                   self.mStep )

class RouteTrace( list ):
    
    def append( self, obj ):
        if ( obj.mDt <= 0 and len(self) > 0 ):
            pass 
        else:
            super( RouteTrace, self ).append( obj )            

    def exportTraceData( self, fileName ):

        dt = 0
        with open(fileName,'w') as stream:             
            if  not stream:
                raise Exception("Open fail")

            stream.write('[MRX-T4]\n')
            stream.write('[t,x,y,z,terminal,mode]\n')

            # sum the dt
            for pt in self:
                # print( pt )     
                fmtStr = "{0},{1},{2},{3},{4},{5}\n"
                dt += pt.mDt
                stream.write( fmtStr.format( dt, pt.mPos[0], pt.mPos[1], pt.mPos[2], pt.mPos[3], pt.mStep ) )

        self.clear()
        return dt

class CompilerContext( ):

    def __init__( self, homePos=(0,0,0,0) ):
        self._homePos = homePos

        self.mPosNow = [0,0,0,0]     # current pos

        self.mTrace = RouteTrace()

    def setPos( self, pos ):
        self.mPosNow[0:3] = pos[0:3] 

    def setHand( self, h ):
        self.mPosNow[3] = h

    def accHand( self, h ):
        self.mPosNow[3] += h         

    def homePos( self ):
        self.mPosNow[:] = self._homePos[:]

class StreamCompile( ):
    def __init__( self, opt=0, path = os.path.abspath(os.curdir)):
        
        # arch
        self._stream = None 
        self._level = 1
        self._optimize = 0

        # context 
        self._zero_pos = (250,0,512,0)   
        self._context = CompilerContext( self._zero_pos )
        self._context.setPos( self._zero_pos )

        self._optimize = opt
        self._path = path 

    def attachStream( self, stream ):
        self._stream = stream 

    def genBegin( self ):
        self.genHead()
        self.genMain()

    def genEnd( self ):
        if ( len( self._context.mTrace ) > 1 ):
            # pass 
            fileName = '%s/_%f.mrp' % ( self._path, time.time() )
            sumTime = self._context.mTrace.exportTraceData( fileName )
            
            self.genExec( fileName, sumTime )

        else:
            pass             

    def genHead( self ):
        template="""
from mrq.sinanju import Sinanju       
"""        
        self._stream.write( template )

    def genMain( self ):
        template = """
if __name__=="__main__": 
    # create obj
    this_robo = Sinanju("MRX-T4")
"""                
        self._stream.write( template )

    def genPre( self ):
        self._stream.write( "    " * self._level )

    # fileName, runtime
    def genExec( self, *para ):
        template = ("""this_robo.program( 0,0,r'{0}' )        
""",
        """this_robo.waitEnd( 0,0, {1}*5 )
""",
        """this_robo.call( 0,0 )
""",
        """this_robo.waitIdle(0,0, {1}*2 )
""",
)
        if self._optimize != 0:
            for subt in template:
                fmtRaw = subt.format( *para )
                self.genPre()
                self._stream.write( fmtRaw )

    def genCenter( self, cmd, speed, *para ):
        template = ("""this_robo.center( 0,1)        
""",
        """this_robo.waitIdle(0,1)
""")
        # inited
        if self._optimize == 0  or  len( self._context.mTrace ) < 1:      
            for subt in template:
                fmtRaw = subt.format( *para )
                self.genPre()
                self._stream.write( fmtRaw )

        # export
        if ( len( self._context.mTrace ) > 0 ):
            # add zero
            # self._context.homePos()
            self._context.mTrace.append(  
                                            RoutePoint(  self._context._homePos,
                                                            CompilerAssist.euclidDt( self._context._homePos, 
                                                                                     self._context.mPosNow, speed ) 
                                                        ) )
            # export
            fileName = '%s/_%f.mrp' % (self._path, time.time() )
            sumTime= self._context.mTrace.exportTraceData( fileName )

            self.genExec( fileName, sumTime )

            self._context.mTrace.clear()
                          
        # rezero
        self._context.homePos()
        self._context.mTrace.append(  RoutePoint(  ( self._context.mPosNow[0], 
                                                    self._context.mPosNow[1],
                                                    self._context.mPosNow[2], 
                                                    0),
                                                    0 ) )            

    def genHand( self, cmd, speed, handAngle ):
        template = ("""this_robo.move( 0,0,(250,0,512,0 ),(250,0,512, {0} ), {1}  )        
""",
        """this_robo.waitIdle(0,0)
""")
        if self._optimize == 0 :
            for subt in template:
                paraList = ( handAngle, math.fabs( handAngle/speed ) )
                fmtRaw = subt.format( *paraList )
                self.genPre()
                self._stream.write( fmtRaw )

        # log the point
        self._context.mTrace.append(  RoutePoint(  ( self._context.mPosNow[0], 
                                                     self._context.mPosNow[1],
                                                     self._context.mPosNow[2], 
                                                     self._context.mPosNow[3] + handAngle ),
                                                     math.fabs( handAngle/speed ) ) )
        self._context.accHand( handAngle )                                             

    def genMove( self, cmd, speed, step, *para ):
        template = ("""this_robo.routeTo( ({0}, {1}, {2}), {4}, step={5} )        
""",
        """this_robo.waitIdle(0,0)
""")
        if self._optimize == 0 :
            for subt in template:
                coord = tuple( para[0].split(',') )
                paraList = list( coord )
                paraList.append( speed )
                paraList.append( step )
                # print( paraList )
                fmtRaw = subt.format( *paraList )
                # fmtRaw = subt % para[0].split(',')
                # print( para[0].split(',') )
                self.genPre()
                self._stream.write( fmtRaw )

        # pos now
        coord = para[0].split(',')
        
        # keep the hand
        pos = ( float(coord[0]), float(coord[1]), float(coord[2]), self._context.mPosNow[3], )

        self._context.mTrace[-1].mStep = step
        self._context.mTrace.append( RoutePoint( 
                                                    pos,
                                                    CompilerAssist.euclidDt( pos, self._context.mPosNow, speed ), 
                                                    0     
                                                ) )  
        self._context.setPos( pos )                                                          

    def genLoop( self, cmd, para ):
        pass 

    def input( self, cmd, speed, hand, *para ):
        if ( cmd == 'loop' ):
            self.genLoop( cmd, *para )
        elif( 'movej' in cmd ):
            self.genMove( cmd, speed, 0, *para ) 
        elif( 'movel' in cmd ):
            self.genMove( cmd, speed, 5, *para )  
        elif( 'expand' in cmd ):
            self.genHand( cmd, speed, hand  ) 
        elif( 'subtract' in cmd ):
            self.genHand( cmd, speed, -hand  ) 
        elif( 'center' in cmd ):
            self.genCenter( cmd, speed, *para ) 
        else:
            pass                        

if __name__=="__main__":
    
    # print(  CompilerAssist.euclidDistance( (0,0,0,0), (1,1,1,1) ) )
    print( os.path.abspath( os.curdir ) )
    compiler = StreamCompile( 1 )
    
    with open("a.txt", 'w') as stream: 
        compiler.attachStream( stream )

        compiler.genBegin()

        compiler.input( 'center', 10,0 )
        compiler.input( 'movej', 10, 0, "1,2,3,4" )
        compiler.input( 'movel', 10, 0, "2,3,4,5" )
        compiler.input( 'center', 10,0 )

        compiler.genEnd()

    # for obj in compiler._context.mTrace:
    #     print ( obj )            