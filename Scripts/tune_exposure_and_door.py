import unreal
D='/Game/Art/Doors/AncientDoubleDoor/Materials'
mi=unreal.load_asset(D+'/MI_AncientDoubleDoor_Bright'); mel=unreal.MaterialEditingLibrary
mel.set_material_instance_scalar_parameter_value(mi,'BaseColorBrightness',1.15)
mel.set_material_instance_scalar_parameter_value(mi,'RoughnessMultiplier',1.0)
mel.set_material_instance_scalar_parameter_value(mi,'AOIntensity',.7)
mel.set_material_instance_scalar_parameter_value(mi,'EmissiveDetailIntensity',.02)
mel.set_material_instance_vector_parameter_value(mi,'BaseColorTint',unreal.LinearColor(.62,.56,.48,1))
unreal.EditorAssetLibrary.save_asset(D+'/MI_AncientDoubleDoor_Bright',False)
unreal.EditorLoadingAndSavingUtils.load_map('/Game/Maps/L_RuinsChambers')
for a in unreal.EditorLevelLibrary.get_all_level_actors():
 label=a.get_actor_label()
 if label.startswith('RoomLight_'):
  c=a.get_component_by_class(unreal.PointLightComponent); c.set_editor_property('intensity',700.0)
 if label=='RoomLight_5':
  c=a.get_component_by_class(unreal.PointLightComponent); c.set_editor_property('intensity',250.0); c.set_editor_property('attenuation_radius',650.0)
 if label=='Sun': a.get_component_by_class(unreal.DirectionalLightComponent).set_editor_property('intensity',2.0)
 if label=='Sky_Ambient': a.get_component_by_class(unreal.SkyLightComponent).set_editor_property('intensity',.7)
 if label=='GateExposureControl':
  s=a.get_editor_property('settings'); s.set_editor_property('auto_exposure_bias',-2.0); a.set_editor_property('settings',s)
unreal.EditorLevelLibrary.save_current_level(); unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True,True)
unreal.log('EXPOSURE_AND_DOOR_TUNED bias=-2 lights=700 portal=250')
