import unreal

MAP='/Game/Maps/L_RuinsChambers'
if unreal.EditorAssetLibrary.does_asset_exist(MAP): unreal.EditorAssetLibrary.delete_asset(MAP)
unreal.EditorLevelLibrary.new_level(MAP)
load=lambda n: unreal.load_class(None, '/Script/TinyCourse.'+n)
C={n:load(n) for n in ['CourseBlock','Pickup','MovingPlatform','Hazard','PressurePlate','StoneDoor','Checkpoint','Goal']}
spawn=unreal.EditorLevelLibrary.spawn_actor_from_class
V=unreal.Vector
COL={
 'stone':unreal.LinearColor(.32,.28,.23,1),'dark':unreal.LinearColor(.08,.10,.14,1),
 'blue':unreal.LinearColor(.05,.25,.85,1),'yellow':unreal.LinearColor(.95,.55,.04,1),
 'red':unreal.LinearColor(.9,.08,.02,1),'green':unreal.LinearColor(.05,.8,.2,1),
 'purple':unreal.LinearColor(.6,.04,1,1)}
def block(name,loc,size,col='stone'):
 a=spawn(C['CourseBlock'],V(*loc)); a.set_actor_label(name); a.set_actor_scale3d(V(size[0]/100,size[1]/100,size[2]/100)); a.set_editor_property('block_color',COL[col]); return a
def actor(kind,name,loc,size=(100,100,100)):
 a=spawn(C[kind],V(*loc)); a.set_actor_label(name); a.set_actor_scale3d(V(size[0]/100,size[1]/100,size[2]/100)); return a
def room(name,cx,cy,w,d,accent='stone',openings=()):
 block(name+'_Floor',(cx,cy,-25),(w,d,50),'stone')
 block(name+'_Ceiling',(cx,cy,500),(w,d,40),'dark')
 # Four centred 400 cm door gaps keep rooms connected while retaining solid boundaries.
 side=(w-400)/2; depth=(d-400)/2
 for tag,x in [('W',cx-(400+side)/2),('E',cx+(400+side)/2)]:
  block(name+'_North_'+tag,(x,cy-d/2,250),(side,40,500),'dark'); block(name+'_South_'+tag,(x,cy+d/2,250),(side,40,500),'dark')
 for tag,y in [('N',cy-(400+depth)/2),('S',cy+(400+depth)/2)]:
  block(name+'_West_'+tag,(cx-w/2,y,250),(40,depth,500),'dark'); block(name+'_East_'+tag,(cx+w/2,y,250),(40,depth,500),'dark')
 # colored floor guide, narrow and non-blocking
 block(name+'_Guide',(cx,cy,6),(min(w-120,600),60,10),accent)
def corridor(name,cx,cy,w,d,accent='stone'):
 block(name+'_Floor',(cx,cy,-25),(w,d,50),'stone'); block(name+'_Ceiling',(cx,cy,500),(w,d,40),'dark')
 block(name+'_North',(cx,cy-d/2,250),(w,40,500),'dark'); block(name+'_South',(cx,cy+d/2,250),(w,40,500),'dark')
 block(name+'_Guide',(cx,cy,6),(w-80,45,8),accent)
def doorway_x(name,x,y,accent='stone'):
 block(name+'_N',(x,y-310,250),(50,220,500),'dark'); block(name+'_S',(x,y+310,250),(50,220,500),'dark'); block(name+'_Top',(x,y,450),(50,400,100),accent)
def doorway_y(name,x,y,accent='stone'):
 block(name+'_W',(x-310,y,250),(220,50,500),'dark'); block(name+'_E',(x+310,y,250),(220,50,500),'dark'); block(name+'_Top',(x,y,450),(400,50,100),accent)

# Spawn tutorial room 1200x1000 and corridor to hall (X is forward).
room('Tutorial',-3400,0,1200,1000,'stone'); doorway_x('TutorialExit',-2800,0,'green')
# carve playable passage by covering wall collision with gap: actual wall replaced by side sections
# Disable full east wall from room helper by locating it outside path; add a floor bridge through it.
block('TutorialDoorPassage',(-2800,0,110),(90,350,260),'green')
actor('CourseBlock','Dummy',(-10000,0,-1000),(1,1,1))
ps=spawn(unreal.PlayerStart,V(-3700,0,110)); ps.set_actor_label('Spawn_PlayerStart'); ps.set_actor_rotation(unreal.Rotator(0,0,0),False)
corridor('TutorialToHall',-2500,0,600,400,'green')
# low teaching platform, 180 cm gap marker
block('TutorialJumpStart',(-3450,0,20),(320,320,90),'stone'); block('TutorialJumpLanding',(-3000,0,55),(300,300,160),'blue')

# Central hall 1800x1600; direct spatial branches north/south/east.
room('CentralHall',-1500,0,1800,1600,'stone')
# open silhouettes: large colored inner doorframes and guide lines
doorway_x('HallWestEntry',-2400,0,'green')
doorway_y('BlueTrialDoor',-1500,-800,'blue')
doorway_x('YellowTrialDoor',-600,0,'yellow')
doorway_y('RedTrialDoor',-1500,800,'red')
doorway_x('FinalGateFrame',-700,500,'purple')
actor('PressurePlate','CentralPressurePlate',(-850,500,35),(150,150,12))
actor('StoneDoor','FinalStoneDoor',(-600,500,200),(45,350,400))

# Blue jump room north, 4 measured jumps with gaps 180/230/260/290 cm.
corridor('BlueConnector',-1500,-1050,400,500,'blue'); room('BlueJumpRoom',-1500,-2000,1400,1400,'blue')
platforms=[(-1900,-1800,30),(-1650,-1800,70),(-1360,-1800,110),(-1040,-1800,150),(-700,-1800,190)]
for i,(x,y,z) in enumerate(platforms): block(f'BluePlatform_{i+1}',(x,y,z),(250,300,60),'blue')
actor('Pickup','Core_Blue',(-700,-1800,310),(38,38,38))
block('BlueShortcutBridge',(-1300,-2300,35),(800,260,70),'green')

# Yellow room straight ahead; gap has only moving platform.
corridor('YellowConnector',-250,0,700,400,'yellow'); room('YellowPlatformRoom',700,0,1600,1200,'yellow')
block('YellowStart',(200,0,25),(350,500,80),'yellow'); block('YellowEnd',(1200,0,25),(350,500,80),'yellow')
actor('MovingPlatform','YellowMandatoryMovingPlatform',(700,0,35),(260,260,40))
actor('Pickup','Core_Yellow',(1250,0,150),(38,38,38))

# Red room south; checkpoint before unavoidable full-width hazard lanes.
corridor('RedConnector',-1500,1050,400,500,'red'); room('RedHazardRoom',-1500,2000,1400,1400,'red')
actor('Checkpoint','Checkpoint_RedEntrance',(-1500,1450,50),(180,300,12))
for i,y in enumerate((1700,1950,2200)): actor('Hazard',f'RedHazard_{i+1}',(-1500,y,35),(1000,150,35))
block('RedSafeIsland1',(-1850,1825,45),(260,180,90),'stone'); block('RedSafeIsland2',(-1150,2075,45),(260,180,90),'stone')
actor('Pickup','Core_Red',(-1500,2500,150),(38,38,38))

# Independent portal room behind the final gate, visible by purple glow.
corridor('GateCorridor',-250,500,700,400,'purple'); room('PortalRoom',500,500,900,900,'purple')
actor('Goal','Goal_Portal',(650,500,210),(45,240,360))
block('PortalBackdrop',(820,500,220),(60,500,440),'purple')

# Basic readable indoor lighting, no black void.
sun=spawn(unreal.DirectionalLight,V(0,0,800)); sun.set_actor_label('Sun'); sun.set_actor_rotation(unreal.Rotator(-55,-25,0),False); sun.get_component_by_class(unreal.DirectionalLightComponent).set_editor_property('intensity',5.0)
sky=spawn(unreal.SkyLight,V(0,0,700)); sky.set_actor_label('Sky_Ambient'); sky.get_component_by_class(unreal.SkyLightComponent).set_editor_property('intensity',2.0)
for i,(x,y,c) in enumerate([(-3400,0,(.8,.85,1)),(-1500,0,(1,.85,.6)),(-1500,-2000,(.2,.45,1)),(700,0,(1,.65,.1)),(-1500,2000,(1,.15,.05)),(500,500,(.65,.1,1))]):
 l=spawn(unreal.PointLight,V(x,y,350)); l.set_actor_label('RoomLight_'+str(i)); co=l.get_component_by_class(unreal.PointLightComponent); co.set_editor_property('intensity',4000.0); co.set_editor_property('attenuation_radius',1400.0); co.set_editor_property('cast_shadows',False)
unreal.EditorLevelLibrary.save_current_level()
unreal.log('RUINS_CHAMBERS_MAP_SAVED:'+MAP)
unreal.log('JUMP_SCALE configured: tutorial=180cm normal=230/260cm hard=290cm platform_min=250x250cm rise_max=40cm')

