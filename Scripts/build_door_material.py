import unreal, os
SRC=r'D:\Program Files (x86)\xwechat_files\wxid_jl2b2zdteha022_44da\msg\file\2026-10\door_MESH\door_MESH'
DEST='/Game/Art/Doors/AncientDoubleDoor'
# Import the separately supplied AO map.
t=unreal.AssetImportTask(); t.filename=os.path.join(SRC,'SM_DoorEntranceCastle_AO.png'); t.destination_path=DEST; t.automated=True; t.save=True; t.replace_existing=True
unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([t])
ao=unreal.load_asset(DEST+'/SM_DoorEntranceCastle_AO'); ao.set_editor_property('srgb',False)
for n in ['SM_DoorEntranceCastle_Normal','SM_DoorEntranceCastle_Roughness','SM_DoorEntranceCastle_Metallic']:
 tex=unreal.load_asset(DEST+'/'+n); tex.set_editor_property('srgb',False)
asset_tools=unreal.AssetToolsHelpers.get_asset_tools()
mat_path=DEST+'/M_AncientDoubleDoor_PBR'
mat=unreal.load_asset(mat_path)
if not mat: mat=asset_tools.create_asset('M_AncientDoubleDoor_PBR',DEST,unreal.Material,unreal.MaterialFactoryNew())
mel=unreal.MaterialEditingLibrary
def sample(name,x,y,prop,out='RGB',normal=False):
 e=mel.create_material_expression(mat,unreal.MaterialExpressionTextureSample,x,y); e.texture=unreal.load_asset(DEST+'/'+name)
 if normal: e.set_editor_property('sampler_type',unreal.MaterialSamplerType.SAMPLERTYPE_NORMAL)
 mel.connect_material_property(e,out,prop)
sample('SM_DoorEntranceCastle_Albedo',-500,-200,unreal.MaterialProperty.MP_BASE_COLOR)
sample('SM_DoorEntranceCastle_Normal',-500,0,unreal.MaterialProperty.MP_NORMAL,'RGB',True)
sample('SM_DoorEntranceCastle_Roughness',-500,200,unreal.MaterialProperty.MP_ROUGHNESS,'R')
sample('SM_DoorEntranceCastle_Metallic',-500,400,unreal.MaterialProperty.MP_METALLIC,'R')
sample('SM_DoorEntranceCastle_AO',-500,600,unreal.MaterialProperty.MP_AMBIENT_OCCLUSION,'R')
mel.recompile_material(mat); unreal.EditorAssetLibrary.save_asset(mat_path,False); unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True,True)
unreal.log('PBR_MATERIAL_READY '+mat_path)

