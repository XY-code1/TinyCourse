import unreal

MAP = '/Game/Maps/L_RuinsChambers'
if unreal.EditorAssetLibrary.does_asset_exist(MAP):
    unreal.EditorAssetLibrary.delete_asset(MAP)
unreal.EditorLevelLibrary.new_level(MAP)

load = lambda n: unreal.load_class(None, '/Script/TinyCourse.' + n)
C = {n: load(n) for n in ['CourseBlock', 'Pickup', 'Hazard', 'PressurePlate', 'StoneDoor', 'Checkpoint']}
spawn, V = unreal.EditorLevelLibrary.spawn_actor_from_class, unreal.Vector
COL = {
    'stone': unreal.LinearColor(.24, .22, .19, 1), 'stone2': unreal.LinearColor(.38, .34, .28, 1),
    'dark': unreal.LinearColor(.055, .07, .10, 1), 'blue': unreal.LinearColor(.03, .28, .85, 1),
    'yellow': unreal.LinearColor(.8, .45, .03, 1), 'red': unreal.LinearColor(.72, .055, .025, 1),
    'green': unreal.LinearColor(.03, .65, .18, 1), 'purple': unreal.LinearColor(.42, .04, .75, 1)
}

def block(name, loc, size, color='stone'):
    a = spawn(C['CourseBlock'], V(*loc)); a.set_actor_label(name)
    a.set_actor_scale3d(V(size[0] / 100, size[1] / 100, size[2] / 100))
    a.set_editor_property('block_color', COL[color]); return a

def actor(kind, name, loc, size=(100, 100, 100)):
    a = spawn(C[kind], V(*loc)); a.set_actor_label(name)
    a.set_actor_scale3d(V(size[0] / 100, size[1] / 100, size[2] / 100)); return a

def text(name, value, loc, color, size=55, rotation=(0, 0, 0)):
    a = spawn(unreal.TextRenderActor, V(*loc), unreal.Rotator(*rotation)); a.set_actor_label(name)
    c = a.get_component_by_class(unreal.TextRenderComponent)
    c.set_editor_property('text', value)
    c.set_editor_property('world_size', size); c.set_editor_property('text_render_color', color); return a

def lamp(name, loc, color, intensity=850, radius=900):
    a = spawn(unreal.PointLight, V(*loc)); a.set_actor_label(name)
    c = a.get_component_by_class(unreal.PointLightComponent)
    c.set_editor_property('intensity', intensity); c.set_editor_property('attenuation_radius', radius)
    c.set_editor_property('light_color', color); c.set_editor_property('cast_shadows', False); return a

# Tutorial room and short threshold into the hall. The player looks directly at the gate.
block('TutorialFloor', (-3000, 0, -25), (1000, 900, 50), 'stone')
block('TutorialCeiling', (-3000, 0, 500), (1000, 900, 40), 'dark')
block('TutorialNorthWall', (-3000, -450, 250), (1000, 40, 500), 'dark')
block('TutorialSouthWall', (-3000, 450, 250), (1000, 40, 500), 'dark')
block('TutorialWestWall', (-3500, 0, 250), (40, 900, 500), 'dark')
block('TutorialExitN', (-2500, -325, 250), (40, 250, 500), 'dark')
block('TutorialExitS', (-2500, 325, 250), (40, 250, 500), 'dark')
block('TutorialExitTop', (-2500, 0, 455), (40, 400, 90), 'stone2')
ps = spawn(unreal.PlayerStart, V(-3220, 0, 110)); ps.set_actor_label('Spawn_PlayerStart'); ps.set_actor_rotation(unreal.Rotator(0, 0, 0), False)

# Central hall: compact, layered with steps and pillars; final gate is dead ahead.
block('HallFloor', (-1400, 0, -25), (2200, 1600, 50), 'stone')
block('HallCeiling', (-1400, 0, 600), (2200, 1600, 40), 'dark')
block('HallNorthWall_W', (-2050, -800, 300), (900, 40, 600), 'dark')
block('HallNorthWall_E', (-650, -800, 300), (900, 40, 600), 'dark')
block('HallSouthWall', (-1400, 800, 300), (2200, 40, 600), 'dark')
block('HallWestWallN', (-2500, -600, 300), (40, 400, 600), 'dark')
block('HallWestWallS', (-2500, 600, 300), (40, 400, 600), 'dark')
block('GateSideN', (-300, -575, 300), (80, 450, 600), 'dark')
block('GateSideS', (-300, 575, 300), (80, 450, 600), 'dark')
block('GateHeader', (-300, 0, 520), (80, 700, 160), 'stone2')
for y in (-620, 620): block('HallPillar_%d' % y, (-850, y, 220), (130, 130, 440), 'stone2')
for x, z, w in [(-720, 15, 800), (-610, 35, 620), (-500, 55, 460)]: block('GateStep_%d' % x, (x, 0, z), (110, w, 30), 'stone2')
block('BlueGuide', (-1500, -735, 4), (650, 45, 8), 'blue')
block('YellowGuide', (-1150, 735, 4), (420, 45, 8), 'yellow')
block('RedGuide', (-650, 735, 4), (420, 45, 8), 'red')

# Trial portals: blue open; yellow and red visibly sealed for this vertical slice.
block('BlueDoorLeft', (-1850, -800, 250), (300, 45, 500), 'dark')
block('BlueDoorRight', (-1150, -800, 250), (300, 45, 500), 'dark')
block('BlueDoorTop', (-1500, -800, 520), (400, 45, 80), 'blue')
text('BlueTrialSign', '蓝色试炼：掌握跳跃', (-1500, -775, 430), unreal.Color(80, 150, 255, 255), 45, (0, 90, 90))
for name, x, col in [('Yellow', -1150, 'yellow'), ('Red', -650, 'red')]:
    block(name + 'LockedDoor', (x, 785, 210), (360, 55, 420), 'dark')
    block(name + 'Header', (x, 750, 500), (430, 70, 90), col)
    text(name + 'LockedSign', '尚未开放', (x, 715, 300), unreal.Color(210, 210, 210, 255), 48, (0, -90, 90))

actor('PressurePlate', 'CentralPressurePlate', (-820, 0, 34), (170, 170, 12))
actor('StoneDoor', 'FinalStoneDoor', (-245, 0, 215), (100, 100, 100))
text('FinalGateTitle', '三核遗迹大门', (-330, 0, 500), unreal.Color(230, 205, 150, 255), 52, (0, 0, 0))

# Five 250 cm platforms, measured edge gaps 150/200/230/260 cm.
block('BlueRoomBottom', (-1500, -2250, -260), (1500, 2500, 50), 'dark')
block('BlueRoomWestWall', (-2250, -2250, 250), (40, 2500, 1000), 'dark')
block('BlueRoomEastWall', (-750, -2250, 250), (40, 2500, 1000), 'dark')
block('BlueRoomNorthWall', (-1500, -3500, 250), (1500, 40, 1000), 'dark')
block('BlueRoomCeiling', (-1500, -2250, 750), (1500, 2500, 40), 'dark')
actor('Checkpoint', 'Checkpoint_BlueEntrance', (-1500, -1030, 20), (260, 200, 12))
actor('Hazard', 'BlueFallReset', (-1500, -2250, -205), (1420, 2380, 40))
gaps = [150, 200, 230, 260]; y = -1175
zs = [20, 60, 105, 150, 195]; xs = [-1500, -1380, -1600, -1370, -1580]
for i in range(5):
    block('BluePlatform_%d' % (i + 1), (xs[i], y, zs[i]), (250, 250, 60), 'blue')
    if i < 4: y -= 250 + gaps[i]
actor('Pickup', 'Core_Blue', (xs[-1], y, zs[-1] + 145), (42, 42, 42))
block('BlueReturnLedge', (-910, -2350, 210), (180, 1900, 60), 'green')
block('BlueReturnLanding', (-1120, -1170, 75), (420, 320, 80), 'green')
text('BlueDistanceScale', '150  >  200  >  230  >  260 cm', (-2200, -2250, 420), unreal.Color(100, 170, 255, 255), 38, (0, 90, 90))

# Soft room lighting with fixed exposure; gate is brightest object, not an overexposed wall.
sun = spawn(unreal.DirectionalLight, V(0, 0, 900)); sun.set_actor_label('Sun'); sun.set_actor_rotation(unreal.Rotator(-50, -25, 0), False)
sun.get_component_by_class(unreal.DirectionalLightComponent).set_editor_property('intensity', .7)
sky = spawn(unreal.SkyLight, V(0, 0, 700)); sky.set_actor_label('Sky_Ambient'); sky.get_component_by_class(unreal.SkyLightComponent).set_editor_property('intensity', .35)
lamp('TutorialLight', (-3000, 0, 340), unreal.Color(180, 205, 255), 180, 850)
lamp('HallWarmLight', (-1450, 0, 430), unreal.Color(255, 210, 160), 320, 1250)
lamp('GateKeyLight', (-620, 0, 330), unreal.Color(255, 195, 130), 450, 700)
lamp('BlueRoomLight', (-1500, -2250, 500), unreal.Color(75, 135, 255), 420, 1450)

unreal.EditorLevelLibrary.save_current_level()
unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
unreal.log('BLUE_VERTICAL_SLICE_SAVED:' + MAP)
unreal.log('JUMP_GAPS_CM:150,200,230,260 MAX=260 PLATFORM=250x250')
