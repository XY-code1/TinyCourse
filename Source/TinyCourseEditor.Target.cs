using UnrealBuildTool;

public class TinyCourseEditorTarget : TargetRules
{
    public TinyCourseEditorTarget(TargetInfo Target) : base(Target)
    {
        Type = TargetType.Editor;
        DefaultBuildSettings = BuildSettingsVersion.Latest;
        ExtraModuleNames.Add("TinyCourse");
    }
}
