import unreal
MAP='/Game/Maps/L_RuinsChambers'
unreal.EditorLoadingAndSavingUtils.load_map(MAP)
actors=unreal.EditorLevelLibrary.get_all_level_actors()
for a in actors:
 label=a.get_actor_label()
 if label=='RoomLight_5':
  c=a.get_component_by_class(unreal.PointLightComponent); c.set_editor_property('intensity',650.0); c.set_editor_property('attenuation_radius',850.0); c.set_editor_property('cast_shadows',True); unreal.log('GATE_BACKLIGHT_REDUCED')
 if label.startswith('FinalGateFrame_'):
  try: a.set_editor_property('block_color',unreal.LinearColor(.58,.52,.44,1))
  except: pass
# Replace only our named exposure volume if this script is rerun.
pp=None
for a in actors:
 if a.get_actor_label()=='GateExposureControl': pp=a
if not pp:
 pp=unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.PostProcessVolume,unreal.Vector(-900,500,150)); pp.set_actor_label('GateExposureControl')
pp.set_editor_property('unbound',True)
s=pp.get_editor_property('settings')
for name,val in [('override_auto_exposure_min_brightness',True),('override_auto_exposure_max_brightness',True),('auto_exposure_min_brightness',1.0),('auto_exposure_max_brightness',1.0),('override_auto_exposure_bias',True),('auto_exposure_bias',0.0)]:
 try: s.set_editor_property(name,val); unreal.log('PP_SET '+name)
 except Exception as e: unreal.log_warning('PP_SKIP '+name+' '+str(e))
pp.set_editor_property('settings',s)
unreal.EditorLevelLibrary.save_current_level(); unreal.log('GATE_LIGHTING_EXPOSURE_SAVED')
