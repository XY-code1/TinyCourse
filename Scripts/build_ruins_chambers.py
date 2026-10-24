import unreal

MAP = '/Game/Maps/L_RuinsChambers'
DOOR = '/Game/Art/Doors/AncientDoubleDoor'
MATS = DOOR + '/Materials'
MEL = unreal.MaterialEditingLibrary
AT = unreal.AssetToolsHelpers.get_asset_tools()

parent = unreal.load_asset(MATS + '/M_AncientDoubleDoor_Adjustable')
def material_instance(name, brightness, tint, roughness=1.0, ao=.75):
    path = MATS + '/' + name
    mi = unreal.load_asset(path)
    if not mi:
        mi = AT.create_asset(name, MATS, unreal.MaterialInstanceConstant, unreal.MaterialInstanceConstantFactoryNew())
    mi.set_editor_property('parent', parent)
    MEL.set_material_instance_scalar_parameter_value(mi, 'BaseColorBrightness', brightness)
    MEL.set_material_instance_scalar_parameter_value(mi, 'RoughnessMultiplier', roughness)
    MEL.set_material_instance_scalar_parameter_value(mi, 'AOIntensity', ao)
    MEL.set_material_instance_scalar_parameter_value(mi, 'EmissiveDetailIntensity', 0.0)
    MEL.set_material_instance_vector_parameter_value(mi, 'BaseColorTint', unreal.LinearColor(*tint, 1))
    unreal.EditorAssetLibrary.save_asset(path, False)
    return path + '.' + name

MAT_STONE = material_instance('MI_RuinsStone', .72, (.48, .43, .35), 1.15, .82)
MAT_DARK = material_instance('MI_RuinsDarkStone', .55, (.34, .35, .36), 1.2, .82)
material_instance('MI_AncientDoubleDoor_Bright', .62, (.42, .32, .24), 1.08, .80)

if unreal.EditorAssetLibrary.does_asset_exist(MAP): unreal.EditorAssetLibrary.delete_asset(MAP)
unreal.EditorLevelLibrary.new_level(MAP)
load = lambda n: unreal.load_class(None, '/Script/TinyCourse.' + n)
C = {n: load(n) for n in ['CourseBlock', 'Pickup', 'Hazard', 'PressurePlate', 'StoneDoor', 'Checkpoint', 'MovingPlatform']}
spawn, V = unreal.EditorLevelLibrary.spawn_actor_from_class, unreal.Vector
COL = {'blue': unreal.LinearColor(.025,.16,.52,1), 'yellow': unreal.LinearColor(.42,.24,.025,1),
       'red': unreal.LinearColor(.26,.018,.01,1), 'green': unreal.LinearColor(.025,.32,.09,1)}

def block(name, loc, size, look='stone', rot=(0,0,0), collision=True):
    a = spawn(C['CourseBlock'], V(*loc), unreal.Rotator(*rot)); a.set_actor_label(name)
    a.set_actor_scale3d(V(size[0]/100, size[1]/100, size[2]/100))
    if look == 'stone': a.set_editor_property('material_asset_path', MAT_STONE)
    elif look == 'dark': a.set_editor_property('material_asset_path', MAT_DARK)
    else: a.set_editor_property('block_color', COL[look])
    a.set_actor_enable_collision(collision); return a

def actor(kind, name, loc, size=(100,100,100)):
    a = spawn(C[kind], V(*loc)); a.set_actor_label(name); a.set_actor_scale3d(V(size[0]/100,size[1]/100,size[2]/100)); return a

def moving(name, loc, size, travel, speed=140, pause=.75):
    a=actor('MovingPlatform',name,loc,size)
    a.set_editor_property('travel_offset',V(*travel)); a.set_editor_property('move_speed',speed)
    a.set_editor_property('end_pause',pause); a.set_editor_property('material_asset_path',MAT_STONE); return a

def prop(name, shape, loc, size, material=MAT_STONE, rot=(0,0,0)):
    a = spawn(unreal.StaticMeshActor, V(*loc), unreal.Rotator(*rot)); a.set_actor_label(name)
    c = a.get_component_by_class(unreal.StaticMeshComponent)
    c.set_editor_property('static_mesh', unreal.load_asset('/Engine/BasicShapes/' + shape + '.' + shape))
    c.set_world_scale3d(V(size[0]/100,size[1]/100,size[2]/100)); c.set_material(0, unreal.load_asset(material.split('.')[0])); return a

def lamp(name, loc, color, intensity=250, radius=900, shadows=False):
    a = spawn(unreal.PointLight, V(*loc)); a.set_actor_label(name); c = a.get_component_by_class(unreal.PointLightComponent)
    c.set_editor_property('intensity', intensity); c.set_editor_property('attenuation_radius', radius)
    c.set_editor_property('light_color', color); c.set_editor_property('cast_shadows', shadows); return a

def edge(name, loc, size, color='blue'):
    return block(name, loc, size, color, collision=False)

def sign(name, value, loc, yaw, color):
    a=spawn(unreal.TextRenderActor,V(*loc),unreal.Rotator(0,yaw,0)); a.set_actor_label(name)
    c=a.get_component_by_class(unreal.TextRenderComponent); c.set_editor_property('text',value)
    c.set_editor_property('world_size',42); c.set_editor_property('text_render_color',color); return a

# Compact tutorial threshold opening directly onto the gate sightline.
block('EntryFloor', (-2700,0,-25), (700,900,50)); block('EntryCeiling', (-2700,0,520), (700,900,45),'dark')
block('EntryNorthWall', (-2700,-450,260), (700,50,520),'dark'); block('EntrySouthWall', (-2700,450,260),(700,50,520),'dark')
block('EntryWestWall', (-3050,0,260),(50,900,520),'dark')
ps=spawn(unreal.PlayerStart,V(-1800,250,110)); ps.set_actor_label('Spawn_PlayerStart'); ps.set_actor_rotation(unreal.Rotator(0,-9,0),False)

# Central hall shell: warm stone, framed gate, six columns, steps, inlay and rubble.
block('HallFloor',(-1550,0,-30),(2400,1800,60)); block('HallCeiling',(-1550,0,650),(2400,1800,55),'dark')
block('HallNorthA',(-2350,-900,300),(800,70,600),'dark'); block('HallNorthB',(-650,-900,300),(800,70,600),'dark')
block('HallSouthA',(-2175,900,300),(1150,70,600),'dark')
block('HallSouthGateDivider',(-975,900,300),(190,70,600),'dark'); block('HallSouthEdge',(-385,900,300),(70,70,600),'dark')
block('GateWallN',(-350,-600,300),(90,600,600),'dark'); block('GateWallS',(-350,600,300),(90,600,600),'dark')
block('GateLintel',(-350,0,555),(100,650,150)); block('GateFrameN',(-400,-380,265),(150,110,530)); block('GateFrameS',(-400,380,265),(150,110,530))
for i,(x,y) in enumerate([(-2250,-690),(-2250,690),(-1550,-690),(-1550,690),(-850,-690),(-850,690)]):
    prop('RuinsColumn_%02d'%i,'Cylinder',(x,y,220),(145,145,440),MAT_STONE)
    prop('ColumnBase_%02d'%i,'Cylinder',(x,y,28),(205,205,56),MAT_DARK)
for i,(x,z,w) in enumerate([(-760,12,900),(-640,32,700),(-520,52,500)]): block('GateStep_%d'%i,(x,0,z),(120,w,28))
for i,x in enumerate((-1950,-1600,-1250,-900)):
    edge('HallInlay_%02d'%i,(x,0,4),(170,18,8),'blue')
for i,(x,y,s,r) in enumerate([(-520,-600,90,18),(-470,-670,65,-12),(-900,560,75,25),(-1020,610,55,-30)]):
    block('BrokenStone_%02d'%i,(x,y,s/3),(s,s*.65,s*.5),'stone',(r,r*.4,r*.2))

# Three doorways: color only at trim and signage. Yellow/red are physically sealed.
block('BlueFrameL',(-1800,-900,250),(120,100,500)); block('BlueFrameR',(-1200,-900,250),(120,100,500)); block('BlueFrameTop',(-1500,-900,520),(720,100,100))
edge('BlueTrim',(-1500,-835,430),(420,12,18),'blue')
sign('BlueTrialSign','蓝色跳跃试炼',(-1630,-824,470),90,unreal.Color(100,170,255,255))
for name,x,color in [('Yellow',-1300,'yellow'),('Red',-650,'red')]:
    block(name+'FrameL',(x-230,900,250),(90,100,500)); block(name+'FrameR',(x+230,900,250),(90,100,500)); block(name+'FrameTop',(x,900,520),(550,100,100))
    sealed=block(name+'SealedDoor',(x,855,230),(370,70,460),'dark'); edge(name+'Trim',(x,810,430),(310,12,18),color)
    label=sign(name+'TrialSign',('黄色 尚未开放' if name=='Yellow' else '红色 尚未开放'),(x-150,800,470),-90,unreal.Color(220,200,155,255))
    if name=='Yellow':
        sealed.set_editor_property('tags',[unreal.Name('YellowGate')]); label.set_editor_property('tags',[unreal.Name('YellowSign')])
    else: sealed.set_editor_property('tags',[unreal.Name('RedGate')])

plate=actor('PressurePlate','CentralPressurePlate',(-1030,0,30),(175,175,12))
actor('StoneDoor','FinalStoneDoor',(-310,0,215),(120,120,120))
sign('FinalGateSign','三核遗迹大门',(-410,-170,520),0,unreal.Color(220,190,140,255))

# Blue room: stone platforms with thin blue energy edging, dark-red reset floor and multi-point fill.
block('BlueRoomFloor',(-1500,-2250,-260),(1600,2500,55),'dark')
block('BlueWestWall',(-2300,-2250,280),(60,2500,1080),'dark'); block('BlueEastWall',(-700,-2250,280),(60,2500,1080),'dark')
block('BlueEndWall',(-1500,-3500,280),(1600,60,1080),'dark'); block('BlueCeiling',(-1500,-2250,780),(1600,2500,50),'dark')
actor('Checkpoint','Checkpoint_BlueEntrance',(-1500,-1040,20),(140,90,10))
actor('Hazard','BlueFallReset',(-1500,-2250,-205),(1500,2380,40))
gaps=[150,200,230,260]; y=-1180; zs=[20,60,105,150,195]; xs=[-1500,-1380,-1600,-1370,-1580]
for i in range(5):
    block('BlueStonePlatform_%d'%(i+1),(xs[i],y,zs[i]),(250,250,64),'stone')
    edge('BlueEdgeN_%d'%i,(xs[i],y-118,zs[i]+34),(230,10,8),'blue')
    edge('BlueEdgeS_%d'%i,(xs[i],y+118,zs[i]+34),(230,10,8),'blue')
    edge('BlueEdgeW_%d'%i,(xs[i]-118,y,zs[i]+34),(10,230,8),'blue')
    edge('BlueEdgeE_%d'%i,(xs[i]+118,y,zs[i]+34),(10,230,8),'blue')
    if i<4: y -= 250+gaps[i]
actor('Pickup','Core_Blue',(xs[-1],y,zs[-1]+145),(42,42,42))
block('BlueReturnLedge',(-910,-2350,210),(180,1900,65),'stone'); edge('ReturnEdge',(-995,-2350,246),(12,1850,10),'green')
block('BlueReturnLanding',(-1120,-1170,75),(420,320,80),'stone')

# Yellow trial: timing, moving-platform riding and a mandatory crouch tunnel.
# The room is narrow and readable; yellow is limited to trims and machinery edges.
block('YellowRoomFloor',(-1300,2450,-235),(1700,3100,50),'dark')
block('YellowWestWall',(-2150,2450,285),(60,3100,1040),'dark')
block('YellowEastWall',(-450,2450,285),(60,3100,1040),'dark')
block('YellowEndWall',(-1300,4000,285),(1700,60,1040),'dark')
block('YellowCeiling',(-1300,2450,780),(1700,3100,50),'dark')
block('YellowEntrySafe',(-1300,1120,20),(520,400,80),'stone')
edge('YellowEntryLine',(-1300,940,65),(380,14,12),'yellow')
actor('Checkpoint','Checkpoint_YellowEntrance',(-1300,1080,72),(150,100,10))

# A dark reset floor covers every gap without becoming a dominant red surface.
actor('Hazard','YellowFallReset',(-1300,2480,-185),(1600,2920,35))

# First timing section: lateral platform and offset landing.
moving('YellowMover_Horizontal1',(-1570,1570,80),(300,300,32),(540,0,0),145,.7)
block('YellowLanding1',(-760,1780,90),(330,360,70),'stone')
edge('YellowLanding1Trim',(-760,1610,128),(300,10,9),'yellow')
moving('YellowMover_Horizontal2',(-800,2100,125),(280,280,32),(-500,0,0),130,.6)
block('YellowTunnelApproach',(-1300,2260,85),(420,300,80),'stone')

# 135 cm clearance: the 176 cm standing capsule is blocked, crouched capsule passes.
block('CrouchTunnelFloor',(-1300,2520,20),(430,560,70),'stone')
block('CrouchTunnelRoof',(-1300,2520,205),(430,560,100),'dark')
block('CrouchTunnelLeft',(-1510,2520,105),(25,560,270),'dark')
block('CrouchTunnelRight',(-1090,2520,105),(25,560,270),'dark')
sign('CrouchInstruction','按住 C 或左 Ctrl 蹲伏通过',(-1490,2240,255),90,unreal.Color(255,210,80,255))
block('YellowMidSafe',(-1300,2860,15),(520,360,80),'stone')
actor('Checkpoint','Checkpoint_YellowMid',(-1300,2840,58),(150,100,10))

# Vertical lift rises 250 cm to the core landing.
moving('YellowLift_Vertical',(-1300,3190,55),(300,300,34),(0,0,250),135,.8)
block('YellowCoreLanding',(-1300,3590,330),(520,480,80),'stone')
edge('YellowCoreLandingTrim',(-1300,3370,373),(430,12,10),'yellow')
yellow_core=actor('Pickup','Core_Yellow',(-1300,3590,475),(42,42,42)); yellow_core.set_editor_property('tags',[unreal.Name('YellowCore')])
sign('YellowReturnSign','黄色核心 / 返回中央大厅',(-1520,3860,470),-90,unreal.Color(255,210,80,255))

# Safe return balcony along the east wall; it reconnects to the hall without teleporting.
block('YellowReturnTop',(-720,3590,330),(620,300,70),'stone')
block('YellowReturnWalk',(-570,2420,220),(240,2050,65),'stone')
block('YellowReturnRamp',(-760,1330,110),(620,700,70),'stone',(0,-12,0))
for yy in (1450,2050,2650,3250): edge('YellowGuide_%d'%yy,(-560,yy,255),(12,150,10),'yellow')

lamp('YellowEntryFill',(-1300,1200,360),unreal.Color(230,185,105),280,800)
lamp('YellowTimingFill',(-1300,1900,420),unreal.Color(225,180,100),320,950)
lamp('YellowTunnelFill',(-1300,2520,115),unreal.Color(205,165,95),180,520)
lamp('YellowLiftFill',(-1300,3300,480),unreal.Color(235,190,105),330,950)
lamp('YellowCoreGuide',(-1300,3590,560),unreal.Color(255,175,45),360,600)

# Fixed, deliberately modest illumination. No white emissive architecture.
sun=spawn(unreal.DirectionalLight,V(0,0,900)); sun.set_actor_label('Sun'); sun.set_actor_rotation(unreal.Rotator(-50,-25,0),False)
sun.get_component_by_class(unreal.DirectionalLightComponent).set_editor_property('intensity',.55)
sky=spawn(unreal.SkyLight,V(0,0,700)); sky.set_actor_label('Sky_Ambient'); sky.get_component_by_class(unreal.SkyLightComponent).set_editor_property('intensity',.55)
lamp('EntryFill',(-2600,0,350),unreal.Color(190,205,220),180,850)
lamp('HallAmbient',(-1500,0,470),unreal.Color(205,215,225),240,1400)
lamp('GateWarmKey',(-680,0,330),unreal.Color(255,190,125),450,820)
lamp('MannyHallFill',(-2050,180,230),unreal.Color(255,215,175),150,700)
lamp('BlueEntryFill',(-1500,-1250,330),unreal.Color(120,160,230),190,800)
lamp('BlueMidFill',(-1500,-2200,390),unreal.Color(120,150,205),210,1050)
lamp('BlueEndFill',(-1500,-3050,430),unreal.Color(130,170,235),230,850)
lamp('CoreGuideLight',(xs[-1],y,zs[-1]+220),unreal.Color(50,130,255),260,520)

unreal.EditorLevelLibrary.save_current_level(); unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True,True)
unreal.log('PHASE1_VISUAL_MAP_SAVED:'+MAP)
unreal.log('USED_ASSETS '+MAT_STONE+' '+MAT_DARK+' '+DOOR+'/door_B_01 '+DOOR+'/door_B_02')
unreal.log('JUMP_GAPS_CM 150,200,230,260')
