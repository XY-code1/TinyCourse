import unreal
for n in ['door_B_01','door_B_02']:
 a=unreal.load_asset('/Game/Art/Doors/AncientDoubleDoor/'+n)
 b=a.get_bounds(); unreal.log('BOUND_DETAIL '+n+' origin='+str(b.origin)+' extent='+str(b.box_extent))
