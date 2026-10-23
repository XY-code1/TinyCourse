import unreal
D='/Game/Art/Doors/AncientDoubleDoor'
M=D+'/Materials'
AT=unreal.AssetToolsHelpers.get_asset_tools(); MEL=unreal.MaterialEditingLibrary
mat=unreal.load_asset(M+'/M_AncientDoubleDoor_Adjustable')
if not mat: mat=AT.create_asset('M_AncientDoubleDoor_Adjustable',M,unreal.Material,unreal.MaterialFactoryNew())
# New asset on this branch: create the adjustable graph once.
def tex(name,x,y,normal=False):
 e=MEL.create_material_expression(mat,unreal.MaterialExpressionTextureSample,x,y); e.texture=unreal.load_asset(D+'/'+name)
 if normal:e.set_editor_property('sampler_type',unreal.MaterialSamplerType.SAMPLERTYPE_NORMAL)
 return e
def scalar(name,default,x,y):
 e=MEL.create_material_expression(mat,unreal.MaterialExpressionScalarParameter,x,y); e.set_editor_property('parameter_name',name); e.set_editor_property('default_value',default); return e
def mult(a,b,x,y):
 e=MEL.create_material_expression(mat,unreal.MaterialExpressionMultiply,x,y); MEL.connect_material_expressions(a,'RGB',e,'A'); MEL.connect_material_expressions(b,'',e,'B'); return e
alb=tex('SM_DoorEntranceCastle_Albedo',-900,-300)
tint=MEL.create_material_expression(mat,unreal.MaterialExpressionVectorParameter,-900,-100); tint.set_editor_property('parameter_name','BaseColorTint'); tint.set_editor_property('default_value',unreal.LinearColor(.78,.70,.60,1))
tinted=mult(alb,tint,-600,-250); bright=scalar('BaseColorBrightness',1.7,-600,-100); base=mult(tinted,bright,-350,-250); MEL.connect_material_property(base,'',unreal.MaterialProperty.MP_BASE_COLOR)
norm=tex('SM_DoorEntranceCastle_Normal',-500,50,True); MEL.connect_material_property(norm,'RGB',unreal.MaterialProperty.MP_NORMAL)
rough=tex('SM_DoorEntranceCastle_Roughness',-900,220); rm=scalar('RoughnessMultiplier',.95,-650,260); rout=mult(rough,rm,-400,220); MEL.connect_material_property(rout,'',unreal.MaterialProperty.MP_ROUGHNESS)
metal=tex('SM_DoorEntranceCastle_Metallic',-500,420); MEL.connect_material_property(metal,'R',unreal.MaterialProperty.MP_METALLIC)
ao=tex('SM_DoorEntranceCastle_AO',-900,600); aoi=scalar('AOIntensity',.65,-650,650); aoout=mult(ao,aoi,-400,600); MEL.connect_material_property(aoout,'',unreal.MaterialProperty.MP_AMBIENT_OCCLUSION)
em=scalar('EmissiveDetailIntensity',.08,-600,820); emout=mult(alb,em,-350,800); MEL.connect_material_property(emout,'',unreal.MaterialProperty.MP_EMISSIVE_COLOR)
MEL.recompile_material(mat); unreal.EditorAssetLibrary.save_asset(M+'/M_AncientDoubleDoor_Adjustable',False)
mi=unreal.load_asset(M+'/MI_AncientDoubleDoor_Bright')
if not mi: mi=AT.create_asset('MI_AncientDoubleDoor_Bright',M,unreal.MaterialInstanceConstant,unreal.MaterialInstanceConstantFactoryNew())
mi.set_editor_property('parent',mat)
for n,v in [('BaseColorBrightness',1.7),('RoughnessMultiplier',.95),('AOIntensity',.65),('EmissiveDetailIntensity',.08)]: MEL.set_material_instance_scalar_parameter_value(mi,n,v)
MEL.set_material_instance_vector_parameter_value(mi,'BaseColorTint',unreal.LinearColor(.78,.70,.60,1))
unreal.EditorAssetLibrary.save_asset(M+'/MI_AncientDoubleDoor_Bright',False)
unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True,True)
unreal.log('ADJUSTABLE_DOOR_MATERIAL_READY')
