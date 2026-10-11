#s005ThreeDimSquash.py
import pj
import pjTkInter as tk
import pjThreeDim as pj3d
import math
import pjSound as sound
from logStdErr import logStdErrClass
lse=logStdErrClass()
lse.errToFile()
####
import random
tk.updateMainLabel("s005ThreeDimSquash")
##tk.title("Squash Game：Start！")
tk.removeAllFromCanvas()
####
pj3d.createCapsule("fox",
  0.25,1.5, ## Radius, Length;
  0,0,0,
  255,0,255,255) ##Magenta;Alpha255;
pj3d.setPosition("fox",5,0.3,38)##39(ListIndexOut);;
#### set Camera Position;;
pj3d.setCameraConstraintLookAt("camera", "fox")
##pj3d.setPosition("camera",4.5,0.53,36) ##
fx,fy,fz=pj3d.getPosition("fox")
pj3d.setPosition("camera",fx,3.8,fz) ##
####
pj3d.createFloor("floor",
   0,-0.01,0, ## 'y' Needs Minus Value;
   0,255,0,123) ##Green;Alpha255;
####
##(1;Hero,2;Floor,4;OtherObject);;
##(1;Hero,2;Friend,4;Enemy),(1;Collectable,2;Floor,4;OtherObject)*256;;
####pj3d.changePivotPosition("fox", 0,0.5,20) ##Line64;;##NoNeed After EmptyTransformLocationYzero;
####pj3d.movePhysicsShape("fox",0,0.5,20);NoNeed After EmptyTransformLocationYzero;
####
##SCNPhysicsBodyTypeStatic; Ceiling;SideWall;is Not InfluencedBy Gravity and Collision, and is Fixed at the Same Position;
##SCNPhysicsBodyTypeDynamic; Ball;is InfluencedBy All the Physical Arithmetic such as Gravity, Friction, Collision. Position;
##SCNPhysicsBodyTypeKinematic; Racket;is Not InfluencedBy All the Physical Arithmetic such as Gravity, Friction, Collision But Can Give Impact to the other Moving Object by moving(Dynamic) in Codes;
####
pj3d.setPhysicsBodyStatic("floor",4,0,0)##Static(catergory,contactTest,collision);
pj3d.setPhysicsBodyStatic("fox",1,2,0)##Static(catergory,contactTest,collision);
pj3d.setPhysicsBodyStatic("sphere",2,1,0)##Static(catergory,contactTest,collision);
#### Light;;
####pj3d.setPosition("directionalLight",0,10,0)
pj3d.setPosition("omniLight",0,4,0)##MakeGreenFloor;
pj3d.setLightIntensity("omniLight",2000)##MakeGreenFloor;
####
pj3d.setPosition("ambientLight",0,-2,0)
pj3d.setLightIntensity("ambientLight",3000)##MakeGreenFloor;
##pj3d.setColor("ambientLight",165,165,0,10) ##Orange
pj3d.setColor("ambientLight",255,77,0,255) ##Yellow
####pj3d.setColor("ambientLight",252,64,0,255) ##Naked Color Matched;;
####pj3d.setColor("ambientLight",255,128,51,255) ##BulbLightColor;
####
##pj.changeTitleLabelToReplMode()
sound.setTouchesEndedOn() ##
##tk.setTitleLabelBgColor(1,2,3,0) ##
##tk.setCanvasColor(1,2,3,0) ##
####tk.setZPosition("Title",65535) ##
pj3d.changePortRaitGamePadToThreeDimMode() ##set PortRaitGamePad To ThreeDim;;
####pj3d.removeCameraConstraintLookAt("camera")
####
class CameraAngle :
  ####
  def __init__(self) :
    self.initGame()
  ####
  def initGame(self) :
    self.speed = 1
    self.cameraRotAngle = 0
    self.blenderAdjust = 90
    ####
    self.cameraDistMax = 8
    self.cameraDistMin = 6
    self.cameraYmax = 3.8
    self.cameraYmin = 0.25
    self.cameraYdiff = 0.04
    ####
    self.diffBase = 0.2 ##To Avoid Passing Through;
    self.angleBase = 5 ##Each Five Degrees;;
    self.diffAngle = 0
    self.beforeFx = 0
    self.beforeFz = 0
    self.contactDx = 0
    self.contactDz = 0
    self.eventX = -1
    self.eventY = -1
    self.evRightX = -1
    self.evRightY = -1
    ####
    self.d = (90/180) * math.pi
    pj3d.rotation("fox",0,0,1,self.d) ##YassunAdd;2026-0214;
    self.rotateCameraAroundFox( self.cameraRotAngle )
    ####
    self.threeDimMap = [ ## 10x13;
      ####[1,1,1,1,1,1,1,1,1,1],
      [2,2,2,2,2,2,2,2,2,2],##Ceiling;
      [1,0,0,0,0,0,0,0,0,1],##SideWall;
      [1,0,0,0,0,0,0,0,0,1],
      [1,0,0,0,0,0,0,0,0,1],
      [1,0,0,0,0,0,0,0,0,1],
      [1,0,0,0,0,0,0,0,0,1],
      [1,0,0,0,0,0,0,0,0,1],
      [1,0,0,0,0,0,0,0,0,1],
      [1,0,0,0,0,0,0,0,0,1],
      [1,0,0,0,0,0,0,0,0,1],
      [1,0,0,0,0,0,0,0,0,1],
      [1,0,0,0,0,0,0,0,0,1],
      [1,0,0,0,0,0,0,0,0,1]
      ####self.threeDimMap = [ ## 11x11;
      ####[1,1,1,1,1,1,1,1,1,1,1],
      ####[1,0,0,0,0,0,0,0,0,0,1],
      ]
    self.boxCenterHeight=-1.0
    for z in range(len(self.threeDimMap)) :
      for x in range(len(self.threeDimMap[z])) :
        if self.threeDimMap[z][x] == 1 :
          self.putSideWall(x,z)
        elif self.threeDimMap[z][x] == 2 :
          self.putCeiling(x,z)
    ##
    self.isGameOver = False
    self.ballPosX = 6.01
    self.ballPosZ = 9.74
    self.ballMoveX = 0.1 ##self.diffBase
    self.ballMoveZ = 0.1 ##self.diffBase
    self.point = 0
    mi1,mi2,mi3,ma1,ma2,ma3 = pj3d.getBoundingBoxMinMax("fox")
    ##lse.print(f"min;{mi1,mi2,mi3},\nmax;{ma1,ma2,ma3}")
    height = ma2 - mi2
    self.racketSizeHalf = ( height / 2 ) ##Half
    self.initBall()
    ##
    tk.title("Squash Game：Start！")
    ####self.showText("Squash Game：Start！")
  ####
  def initBall(self) :
    self.ballPosX = 6.01
    self.ballPosZ = 9.74
    pj3d.createSphere("sphere",
      0.25, ## Radius;
      self.ballPosX,0.3,self.ballPosZ,
      255,255,0,255) ##Yellow;Alpha255;
  ####
  def putSideWall(self,x,z) :
    pj3d.createBox(f"sideWall-z{z:02}-x{x:02}",
      3,3,3,0.0, ## Height(2);
      x * 3 + 1.5, self.boxCenterHeight, z * 3 + 1.5,
      0,0,255,255) ##Blue;Alpha255;
    ###pj3d.setPhysicsBodyStatic(f"sideWall-z{z:02}-x{x:02}",
    ###  4,1,0)##Static(catergory,contactTest,collision);sideWall;Colides;Fox;
    pj3d.setPhysicsBodyStatic(f"sideWall-z{z:02}-x{x:02}",
      4,2,0)##Static(catergory,contactTest,collision);sideWall;Colides;Sphere;
  ####
  def putCeiling(self,x,z) :
    pj3d.createBox(f"ceiling-z{z:02}-x{x:02}",
      3,3,3,0.0, ## Height(2);
      x * 3 + 1.5, self.boxCenterHeight, z * 3 + 1.5,
      128,0,128,255) ##Purple;Alpha255;
      ##255,165,0,255) ##Orange;Alpha255;
    pj3d.setPhysicsBodyStatic(f"ceiling-z{z:02}-x{x:02}",
      4,2,0)##Static(catergory,contactTest,collision);Ceiling;Colides;Sphere;
  ####
  def getFZFXfromZX(self,z, x) : ##YassunAdd;2026-0216;
    import math
    fz = z * 3 + 1.5 ##FromZero;
    fx = x * 3 + 1.5 ##FromZero;
    return fz,fx
  ####
  def getZXfromModel(self,modelName ) :
    import math
    fx, fy, fz = pj3d.getPosition( modelName )
    z = math.floor( fz / 3 ) ##FromZero;
    x = math.floor( fx / 3 ) ##FromZero;
    return z,x
  ####
  def getZXfromFZFX(self,fz,fx) :
    import math
    z = math.floor( fz / 3 ) ##FromZero;
    x = math.floor( fx / 3 ) ##FromZero;
    return z,x
  ####
  def createText(self,modelName,str,x,y,z) :
    pj3d.createText(modelName, 
   str, 
   0.1, #extrusionDepth;
   0.4, #fontSize;
   x,y,z, ##centerPosition;
   255,0,0,255, ##Red;Alpha255;
   0,255,0,255, ##Green;Alpha255;
   0,0,255,255) ##Blue;Alpha255;
  ####
  def showText(self,s) :
    self.createText("text",
    s, ####"All Men Are Created Equal",
    15,1.7,30)
    ####4.7,1.7,0)
    ####4.7,1.7,32.2)
  ####
  def hideText(self) :
    pj3d.removeFromParent("text")
  ####
  def dist(self, fx, fy, fz, cx, cy, cz ) :
      dist = math.sqrt(math.pow(fx - cx,2)+math.pow(fy-cy,2)+math.pow(fz-cz,2))
      if dist < 0.001 :
        dist = 0.001
      return dist
  ####
  def rotateAaroundB(self, nameA, nameB, angle) :
      angle = angle + self.blenderAdjust
      fx,fy,fz = pj3d.getPosition(nameB)
      cx,cy,cz = pj3d.getPosition(nameA)
      dist = self.dist(fx,fy,fz,cx,cy,cz)
      if dist > self.cameraDistMax :
        dist = self.cameraDistMax
      if dist < self.cameraDistMin :
        dist = self.cameraDistMin
      dx = dist * math.cos((math.pi/180)*angle)
      if dx >= self.cameraDistMax :
        dx = self.cameraDistMax
      dz = dist * math.sin((math.pi/180)*angle)
      if dz >= self.cameraDistMax :
        dz = self.cameraDistMax
      cx = fx + dx
      cz = fz + dz
      pj3d.setPosition(nameA,cx, cy, cz ) ##Line85;;
  ####
  def rotateCameraAroundFox(self, angle) :
      self.rotateAaroundB("camera","fox",angle)
  ####
  def showPos(self) :
      fx,fy,fz = pj3d.getPosition("fox")
      cx,cy,cz = pj3d.getPosition("camera")
      z,x = self.getZXfromModel("fox")
      pj3d.setPosition("omniLight",cx,4,cz)##MakeGreenFloor;
      dist = self.dist(fx,fy,fz,cx,cy,cz)
      ####
      ##tk.updateMainLabel(f"(fx,fy,fz);({fx:.2f},{fy:.2f},{fz:.2f})\n" +
      ## f"(x,z);({x:2d},{z:2d})\n" +
      tk.updateMainLabel(f"(fx,fy,fz);({fx:.2f},{fy:.2f},{fz:.2f})\n" +
       f"(cx,cy,cz);({cx:.2f},{cy:.2f},{cz:.2f})\n" +
       f"cameraRotAngle;{self.cameraRotAngle},dist;{dist:.2f}")
  ####
  def keyPress(self, eventKeySym):
      ####tk.updateMainLabel("eventKeySym:" + eventKeySym)
      if eventKeySym == "Up" :##ResetGame;;
        ####self.initBall()
        self.ballPosX = 6.01
        self.ballPosZ = 9.74
        pj3d.setPosition("sphere",
          self.ballPosX,0.3,self.ballPosZ)
        self.resetGame()
        return
      elif eventKeySym == "ControlP" : ##forTestUse;
        pj3d.changePortRaitGamePadToHistoricMode()
        return
      elif eventKeySym == "ControlN" : ##forTestUse;
        pj3d.changePortRaitGamePadToThreeDimMode()
        return
  ####
  def contact(self, contactNodeA, contactNodeB, contactNormalX, contactNormalY, contactNormalZ ):
      ####if ( str(contactNodeA).startswith("fox") and str(contactNodeB).startswith("sideWall") ) ####\
      ####or ( str(contactNodeA).startswith("sideWall") and str(contactNodeB).startswith("fox") ) : ##Line240;;
      if str(contactNodeA) == "fox" or str(contactNodeB) == "fox" :
        self.eventX = -1 ##To Stop Motion;;
        self.eventY = -1 ##To Stop Motion;;
        ####
        fx,fy,fz = pj3d.getPosition("fox")
        ##
        diffFx = fx - self.beforeFx
        diffFz = fz - self.beforeFz
        ####
        if diffFx >= 0 :
          dx =  -math.fabs( contactNormalX )
        else :
          dx = math.fabs( contactNormalX )
        ####fy = fy + contactNormalY
        if diffFz >= 0 :
          dz = -math.fabs( contactNormalZ )
        else :
          dz = math.fabs( contactNormalZ )
        ####tk.updateMainLabel(f"nodeA;{str(contactNodeA)}, nodeB;{str(contactNodeB)}, normal;({contactNormalX:.2f},{contactNormalY:.2f},{contactNormalZ:.2f})")
        self.moveFoxContact(fx,fy,fz,dx,dz)
  #### moves Ball;
  def moveBall(self): ##Line286;
    if self.isGameOver: return
    ####
    bx,by,bz = pj3d.getPosition("sphere")
    z,x = self.getZXfromFZFX(bz+self.ballMoveZ,bx+self.ballMoveX)
    minZ,minX = self.getFZFXfromZX(1,0.5)
    maxZ,maxX = self.getFZFXfromZX(11.9,8.5)
    ##SideWall;
    if ( bx+self.ballMoveX <= minX ) or ( bx+self.ballMoveX >= maxX ) :
      self.ballMoveX *= -1
      sound.midi(0, 64,0.05)
    ##Ceiling;
    if bz+self.ballMoveZ <= minZ  :
      self.ballMoveZ *= -1
      sound.midi(0, 64,0.05)
    rx,ry,rz = pj3d.getPosition("fox") ##RacketPosition;
    aboveRacketZ,aboveRacketX=self.getFZFXfromZX(11.7,1)
    if ( bz+self.ballMoveZ >= aboveRacketZ and bz+self.ballMoveZ < maxZ ) and \
    ( rx - self.racketSizeHalf < bx + self.ballMoveX < rx + self.racketSizeHalf ) : ## RacketHit;
      self.ballMoveZ *= -1
      if random.randint(0, 1) == 0:
        self.ballMoveX *= -1
      sound.midi(0, 71,0.05)
      msgStr = self.getMsgStrGood()
      self.point += 10
      tk.title(msgStr + " Score＝" + str(self.point))
      ####self.showText(msgStr + " Score＝" + str(self.point) )
    #### judges whether Missed
    if bz+self.ballMoveZ >= maxZ :
      msgStr = self.getMsgStrBad()
      tk.title(msgStr + " Score＝" + str(self.point))
      ####self.showText(msgStr + " Score＝" + str(self.point) )
      sound.midi(0, 54,0.8)
      self.isGameOver = True
    if bx+self.ballMoveX >= minX and bx+self.ballMoveX <= maxX :
      bx += self.ballMoveX
    if bz+self.ballMoveZ >= minZ and bz+self.ballMoveZ <= maxZ :
      bz += self.ballMoveZ
    pj3d.setPosition("sphere", bx, by, bz ) ##updateBallposition Only At the Last;
  ####
  def moveFoxContact(self, fx,fy,fz,dx,dz) :
      self.contactDx = dx
      self.contactDz = dz
  ####
  def motion(self, eventX, eventY):
      ####if eventX != -1 and eventY != -1 :
      ####  tk.updateMainLabel("(eventX,eventY):("+ str(eventX) + "," + str(eventY) + ")" )
      self.eventX = eventX
      self.eventY = eventY
      ##stand = pj3d.getNodeStanding("capsule")
      ##lse.print(f"stand;{stand}")
      ##if stand > 0.9 : ##YassunAdd;2026-0214;
      ##  self.d = (90/180) * math.pi
      ##  pj3d.rotation("fox",0,0,1,self.d) ##YassunAdd;2026-0214;
  ####
  def motionRight(self, evRightX, evRightY):
      ####if evRightX != -1 and evRightY != -1 :
      ####  tk.updateMainLabel("(evRightX,evRightY):("+ str(evRightX) + "," + str(evRightY) + ")" )
      self.evRightX = evRightX
      self.evRightY = evRightY
  ####
  def turnFront(self) :
      y = 0 - self.cameraRotAngle/90
      pj3d.eulerAngles("fox",0*self.d,y*self.d,0) ##Front
  ##
  def turnRight(self) :
      y = 1 - self.cameraRotAngle/90
      pj3d.eulerAngles("fox",0*self.d,y*self.d,0) ##Right
  ##
  def turnRear(self) :
      y = 2 - self.cameraRotAngle/90
      pj3d.eulerAngles("fox",0*self.d,y*self.d,0) ##Rear
  ##
  def turnLeft(self) :
      y = 3 - self.cameraRotAngle/90
      pj3d.eulerAngles("fox",0*self.d,y*self.d,0) ##Left
  ####
  def motionFromGameLoop(self) :
      if self.eventX == -1 and self.eventY == -1 :
        return
      ####
      fx,fy,fz = pj3d.getPosition("fox")
      cx,cy,cz = pj3d.getPosition("camera")
      dist = self.dist(fx,fy,fz,cx,cy,cz)
      ####m1 = (fz-cz)/(fx-cx)
      ####m2 = -(fx-cx)/(fz-cz)
      dx = 0
      dy = 0
      if self.eventX  >= 320 + 64 : ##Right
        ##self.turnRight()
        dx =  - (fz-cz)/dist
        dz = (fx-cx)/dist
        self.moveFox(fx,fy,fz,dx,dz)
      elif self.eventX < 320 - 64 : ##Left
        ##self.turnLeft()
        dx =  (fz-cz)/dist
        dz =  - (fx-cx)/dist
        self.moveFox(fx,fy,fz,dx,dz)
      ####
      ##if self.eventY >= 240 + 48 :##Rear
      ##  ##self.turnRear()
      ##  dx =  (fx-cx)/dist
      ##  dz = (fz-cz)/dist
      ##  self.moveFox(fx,fy,fz,dx,dz)
      ##elif self.eventY < 240 - 48 :##Front
      ##  ##self.turnFront()
      ##  dx = - (fx-cx)/dist
      ##  dz = - (fz-cz)/dist
      ##  self.moveFox(fx,fy,fz,dx,dz)
      ####
      self.rotateCameraAroundFox( self.cameraRotAngle )
  ####
  def motionRightFromGameLoop(self) :
      if self.evRightX == -1 and self.evRightY == -1 :
        return
      ####
      fx,fy,fz = pj3d.getPosition("fox")
      cx,cy,cz = pj3d.getPosition("camera")
      dist = self.dist(fx,fy,fz,cx,cy,cz)
      dx = 0
      dy = 0
      if self.evRightY >= 240 + 48 :##Rear
        cy = cy + self.cameraYdiff
        if cy >= self.cameraYmin and cy <= self.cameraYmax :
          pj3d.setPosition("camera",cx, cy, cz)
          return
      elif self.evRightY < 240 - 48 :##Front
        cy = cy - self.cameraYdiff
        if cy >= self.cameraYmin and cy <= self.cameraYmax :
          pj3d.setPosition("camera",cx, cy, cz)
          return
      ####
      if self.evRightX  >= 320 + 64 : ##Right;BackGround Goes Left;
        self.diffAngle = self.angleBase
      elif self.evRightX  < 320 - 64 : ##Left;BackGround Goes Right;
        self.diffAngle = -self.angleBase
  ####
  def motionCanvas(self, evCanvasX, evCanvasY):
      pass ##YassunAdd;2025-0914;
      ####if evCanvasX != -1 and evCanvasY != -1 :
      ####  tk.updateMainLabel("(evCanvasX,evCanvasY):(" + str(evCanvasX) + "," + str(evCanvasY) + ")" )
  ####
  def moveFox(self, fx,fy,fz,dx,dz) :
      self.beforeFx = fx
      self.beforeFz = fz
      fx = fx + dx * self.diffBase
      fz = fz + dz * self.diffBase
      ####
      z,x = self.getZXfromFZFX(fz,fx)
      if self.threeDimMap[z][x] == 1 :
        return
      ####
      pj3d.setPosition("fox", fx, fy, fz)
      ####
      self.turnEulerAngles("text")
      ####
  ####
  def getAngle(self) :
      if self.cameraRotAngle >= 315 or self.cameraRotAngle < 45 :##OR;CameraSeesRear
        angle = 0 ##EnemySeesFront
      elif self.cameraRotAngle >= 45 and self.cameraRotAngle <  135 :##CameraSeesRight
        angle = -1 ##EnemySeesLeft
      elif self.cameraRotAngle >= 135 and self.cameraRotAngle <= 225 :##CameraSeesFront
        angle = 2 ##EnemySeesRear
      elif self.cameraRotAngle >= 225 and self.cameraRotAngle < 315 :##CameraSeesLeft
        angle = 1 ##EnemySeesRight
      return angle
  ####
  def turnEulerAngles(self,modelName) :
      angle = self.getAngle()
      pj3d.eulerAngles(modelName,
          0,self.d*angle,0)
  ####
  def resetGame(self) :
      tk.removeAllFromCanvas()
      ####
      self.initGame()
  ####
  def button(self, eventNum):
    pass
    ####tk.updateMainLabel("eventNum:" + str(eventNum))
  ####
  def gameLoop(self) : ##Line410;
    self.motionFromGameLoop()
    self.motionRightFromGameLoop()
    if self.diffAngle != 0 :
      self.cameraRotAngle = ( self.cameraRotAngle + self.diffAngle ) % 360 ## -90 = (-1)*360 + 270; (-90 % 360)->270, Needs to be Plus Number;
      self.rotateCameraAroundFox( self.cameraRotAngle )
      self.diffAngle = 0
    ####
    fx,fy,fz = pj3d.getPosition("fox")
    if self.contactDx != 0 :
      fx += self.contactDx
      self.contactDx = 0
    if self.contactDz != 0 :
      fz += self.contactDz
      self.contactDz = 0
    ####
    z,x = self.getZXfromFZFX(fz,fx)
    if self.threeDimMap[z][x] == 0 :
      pj3d.setPosition("fox",fx,fy,fz)
    self.showPos()
    self.moveBall()
## in order to make the function moveBall() Short.
## Added getMsgStrGood() and getMsgStrBad().
  ####
  def getMsgStrGood(self):
    msgInt = random.randint(0, 4)
    if msgInt == 0:
      msgStr = "You are Good at！"
    elif msgInt == 1:
      msgStr = "That's Good！"
    elif msgInt == 2:
      msgStr = "That's Nice！"
    elif msgInt == 3:
      msgStr = "It's Good！"
    elif msgInt == 4:
      msgStr = "Awesome！"
    return msgStr
  ####
  def getMsgStrBad(self):
    msgInt = random.randint(0, 2)
    if msgInt == 0:
      msgStr = "You are Bad at！"
    elif msgInt == 1:
      msgStr = "You missed it！"
    elif msgInt == 2:
      msgStr = "I can't see it！"
    return msgStr
  ####
####
ca = CameraAngle()
ca.speed = 0.05

tk.bindKeyPressFunction("s005ThreeDimSquash:s005ThreeDimSquash.ca.keyPress")

tk.bindButtonFunction("s005ThreeDimSquash:s005ThreeDimSquash.ca.button")

tk.bindMotionFunction("s005ThreeDimSquash:s005ThreeDimSquash.ca.motion")

tk.bindMotionRightFunction("s005ThreeDimSquash:s005ThreeDimSquash.ca.motionRight")

tk.bindMotionCanvasFunction("s005ThreeDimSquash:s005ThreeDimSquash.ca.motionCanvas")

tk.startTimerFunctionAfter("s005ThreeDimSquash:s005ThreeDimSquash.ca.gameLoop", ca.speed)

pj3d.bindContactFunction("s005ThreeDimSquash:s005ThreeDimSquash.ca.contact")
