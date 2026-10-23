import unreal
MAP='/Game/Maps/L_RuinsChambers'
unreal.EditorLoadingAndSavingUtils.load_map(MAP)
door_class=unreal.load_class(None,'/Script/TinyCourse.StoneDoor')
count=0
for actor in unreal.EditorLevelLibrary.get_all_level_actors():
    if actor.get_class()==door_class:
        actor.set_actor_scale3d(unreal.Vector(1,1,1))
        actor.set_actor_label('Final_DoubleRuinsDoor')
        count+=1
unreal.EditorLevelLibrary.save_current_level()
unreal.log('DOUBLE_DOOR_MAP_UPDATED count='+str(count))
