import unreal, os
SRC=r'D:\Program Files (x86)\xwechat_files\wxid_jl2b2zdteha022_44da\msg\file\2026-10\door_MESH\door_MESH'
DEST='/Game/Art/Doors/AncientDoubleDoor'
files=['door_A.fbx','door_B_01.fbx','door_B_02.fbx','door_C.fbx','door_D.fbx']
tasks=[]
for name in files:
 t=unreal.AssetImportTask(); t.filename=os.path.join(SRC,name); t.destination_path=DEST; t.automated=True; t.save=True; t.replace_existing=True
 ui=unreal.FbxImportUI(); ui.import_as_skeletal=False; ui.import_mesh=True; ui.import_materials=True; ui.import_textures=True
 ui.static_mesh_import_data.combine_meshes=False
 ui.static_mesh_import_data.normal_import_method=unreal.FBXNormalImportMethod.FBXNIM_IMPORT_NORMALS_AND_TANGENTS
 ui.static_mesh_import_data.generate_lightmap_u_vs=True
 t.options=ui; tasks.append(t)
unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks(tasks)
for t in tasks:
 unreal.log('DOOR_IMPORT '+t.filename+' => '+','.join(t.imported_object_paths))
for path in unreal.EditorAssetLibrary.list_assets(DEST,recursive=True,include_folder=False):
 asset=unreal.EditorAssetLibrary.load_asset(path)
 if isinstance(asset,unreal.Texture2D) and ('Normal' in path or '_AO' in path or 'Metallic' in path or 'Roughness' in path):
  asset.set_editor_property('srgb',False); unreal.EditorAssetLibrary.save_asset(path,only_if_is_dirty=False)
 if isinstance(asset,unreal.StaticMesh):
  b=asset.get_bounds(); unreal.log('DOOR_BOUNDS '+path+' size='+str(b.box_extent*2.0))
unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True,True)
