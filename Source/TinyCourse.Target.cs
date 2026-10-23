using UnrealBuildTool;

public class TinyCourseTarget : TargetRules
{
    public TinyCourseTarget(TargetInfo Target) : base(Target)
    {
        Type = TargetType.Game;
        DefaultBuildSettings = BuildSettingsVersion.Latest;
        ExtraModuleNames.Add("TinyCourse");
    }
}
