import unreal, os
src=r"D:\UnrealProjects\TinyCourse\Resources\Audio"
tasks=[]
for name in sorted(os.listdir(src)):
    if not name.lower().endswith('.wav'): continue
    t=unreal.AssetImportTask(); t.filename=os.path.join(src,name); t.destination_path='/Game/Audio'; t.automated=True; t.replace_existing=True; t.save=True; tasks.append(t)
unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks(tasks)
unreal.EditorAssetLibrary.save_directory('/Game/Audio',only_if_is_dirty=False,recursive=True)
for t in tasks: unreal.log('RC_AUDIO_IMPORTED '+','.join(t.imported_object_paths))
