import unreal

MAP = '/Game/Maps/L_FloatingRuins'

# Replace only the generated map; source logic is preserved.
if unreal.EditorAssetLibrary.does_asset_exist(MAP):
    unreal.EditorAssetLibrary.delete_asset(MAP)
unreal.EditorLevelLibrary.new_level(MAP)

block_cls = unreal.load_class(None, '/Script/TinyCourse.CourseBlock')
pickup_cls = unreal.load_class(None, '/Script/TinyCourse.Pickup')
platform_cls = unreal.load_class(None, '/Script/TinyCourse.MovingPlatform')
hazard_cls = unreal.load_class(None, '/Script/TinyCourse.Hazard')
plate_cls = unreal.load_class(None, '/Script/TinyCourse.PressurePlate')
door_cls = unreal.load_class(None, '/Script/TinyCourse.StoneDoor')
checkpoint_cls = unreal.load_class(None, '/Script/TinyCourse.Checkpoint')
goal_cls = unreal.load_class(None, '/Script/TinyCourse.Goal')

spawn = unreal.EditorLevelLibrary.spawn_actor_from_class

def vec(x, y, z): return unreal.Vector(x, y, z)
def color(r, g, b): return unreal.LinearColor(r, g, b, 1.0)

def block(name, loc, scale, tint):
    a = spawn(block_cls, vec(*loc))
    a.set_actor_label(name)
    a.set_actor_scale3d(vec(*scale))
    a.set_editor_property('block_color', tint)
    return a

def actor(cls, name, loc, scale=(1,1,1)):
    a = spawn(cls, vec(*loc))
    a.set_actor_label(name)
    a.set_actor_scale3d(vec(*scale))
    return a

warm = color(.42, .34, .25)
blue = color(.06, .28, .85)
yellow = color(.9, .55, .05)
red = color(.85, .08, .025)
dark = color(.16, .14, .18)

# Spawn and central hub.
actor(unreal.PlayerStart, 'Spawn_PlayerStart', (-420, 0, 150))
block('Hub_Main', (0, 0, 0), (12, 12, 1), warm)
block('Spawn_Backdrop', (-620, 0, 220), (.5, 12, 5), dark)
block('Hub_Pillar_N', (520, -430, 180), (1.2, 1.2, 4), warm)
block('Hub_Pillar_S', (520, 430, 180), (1.2, 1.2, 4), warm)

# Route A (north): three mandatory jumps and core 1.
for i, y in enumerate((-760, -1030, -1300)):
    block(f'RouteA_Jump_{i+1}', (0, y, 70 + i*35), (3.0, 1.7, .45), blue)
actor(pickup_cls, 'Core_A', (0, -1300, 190), (.38,.38,.38))

# Route B (south): only the moving platform bridges the void.
block('RouteB_Landing', (220, 1320, 90), (4.0, 3.0, .55), yellow)
actor(platform_cls, 'RouteB_MandatoryMovingPlatform', (220, 860, 75), (2.2, 2.2, .3))
actor(pickup_cls, 'Core_B', (220, 1320, 190), (.38,.38,.38))

# Route C (west): checkpoint, narrow bridge, unavoidable jump-over hazards.
block('RouteC_Bridge', (-950, 260, 35), (7.0, 3.0, .5), red)
block('RouteC_End', (-1420, 260, 70), (3.0, 4.0, .55), warm)
actor(checkpoint_cls, 'Checkpoint_C', (-690, 260, 100), (.7, 1.35, .1))
actor(hazard_cls, 'Hazard_C_1', (-900, 260, 95), (.55, 3.4, .22))
actor(hazard_cls, 'Hazard_C_2', (-1120, 260, 110), (.55, 3.4, .22))
actor(pickup_cls, 'Core_C', (-1420, 260, 185), (.38,.38,.38))

# Locked landmark gate. The only bridge to the goal passes through this door.
block('GateBridge', (780, 0, 45), (4.0, 4.0, .55), warm)
block('GateWall_N', (680, -430, 220), (1.0, 4.6, 5.0), dark)
block('GateWall_S', (680, 430, 220), (1.0, 4.6, 5.0), dark)
block('GateLintel', (680, 0, 500), (1.0, 4.0, 1.0), warm)
actor(plate_cls, 'Central_PressurePlate', (470, 0, 80), (1.25,1.25,.12))
actor(door_cls, 'Central_StoneDoor', (680, 0, 250), (.55,4.0,4.0))

# Goal island and a portal visible from spawn above the door line.
block('GoalIsland', (1250, 0, 80), (8.0, 8.0, 1.0), warm)
block('GoalMonolith_L', (1480, -230, 300), (.8,.8,5.5), dark)
block('GoalMonolith_R', (1480, 230, 300), (.8,.8,5.5), dark)
actor(goal_cls, 'Goal_Portal', (1500, 0, 330), (.35,2.6,3.8))

# Lighting and atmosphere saved in the map.
sun = actor(unreal.DirectionalLight, 'Sun_KeyLight', (0,0,900))
sun.set_actor_rotation(unreal.Rotator(-45,-30,0), False)
sun.get_component_by_class(unreal.DirectionalLightComponent).set_editor_property('intensity', 7.0)
sky = actor(unreal.SkyLight, 'Sky_Ambient', (0,0,700))
sky.get_component_by_class(unreal.SkyLightComponent).set_editor_property('intensity', 1.5)
actor(unreal.SkyAtmosphere, 'SkyAtmosphere', (0,0,0))
fog = actor(unreal.ExponentialHeightFog, 'CloudMist', (0,0,-350))
fog_comp = fog.get_component_by_class(unreal.ExponentialHeightFogComponent)
fog_comp.set_editor_property('fog_density', .012)
fog_comp.set_editor_property('fog_height_falloff', .12)

unreal.EditorLevelLibrary.save_current_level()
unreal.log('FLOATING_RUINS_MAP_SAVED:' + MAP)

