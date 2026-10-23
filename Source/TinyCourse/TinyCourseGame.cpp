#include "TinyCourseGame.h"
#include "Camera/CameraComponent.h"
#include "Components/BoxComponent.h"
#include "Components/CapsuleComponent.h"
#include "Components/StaticMeshComponent.h"
#include "Components/SkeletalMeshComponent.h"
#include "Engine/Canvas.h"
#include "Engine/Engine.h"
#include "Engine/StaticMesh.h"
#include "Materials/MaterialInstanceDynamic.h"
#include "Materials/MaterialInterface.h"
#include "Engine/DirectionalLight.h"
#include "Engine/SkyLight.h"
#include "Engine/PointLight.h"
#include "Components/DirectionalLightComponent.h"
#include "Components/SkyLightComponent.h"
#include "Components/PointLightComponent.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "GameFramework/PlayerController.h"
#include "GameFramework/PlayerStart.h"
#include "GameFramework/SpringArmComponent.h"
#include "Kismet/GameplayStatics.h"
#include "EngineUtils.h"
#include "Misc/CommandLine.h"
#include "Misc/FileHelper.h"
#include "Misc/Paths.h"
#include "HAL/FileManager.h"
#include "UnrealClient.h"

static UStaticMesh* CubeMesh()
{
    static UStaticMesh* Mesh = LoadObject<UStaticMesh>(nullptr, TEXT("/Engine/BasicShapes/Cube.Cube"));
    return Mesh;
}

static UStaticMesh* SphereMesh()
{
    static UStaticMesh* Mesh = LoadObject<UStaticMesh>(nullptr, TEXT("/Engine/BasicShapes/Sphere.Sphere"));
    return Mesh;
}

static void Paint(UStaticMeshComponent* Mesh, const FLinearColor& Color)
{
    if (!Mesh || !Mesh->GetWorld() || !Mesh->GetWorld()->IsGameWorld()) return;
    auto* Base = LoadObject<UMaterialInterface>(nullptr,
        TEXT("/Engine/BasicShapes/BasicShapeMaterial.BasicShapeMaterial"));
    auto* Material = UMaterialInstanceDynamic::Create(Base, Mesh);
    Material->SetVectorParameterValue(TEXT("Color"), Color);
    Mesh->SetMaterial(0, Material);
}

ACourseBlock::ACourseBlock()
{
    Mesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("CourseMesh"));
    RootComponent = Mesh;
    Mesh->SetStaticMesh(CubeMesh());
}
void ACourseBlock::OnConstruction(const FTransform& Transform)
{
    Super::OnConstruction(Transform);
    Paint(Mesh, BlockColor);
}
void ACourseBlock::BeginPlay() { Super::BeginPlay(); Paint(Mesh, BlockColor); }

ATinyCharacter::ATinyCharacter()
{
    PrimaryActorTick.bCanEverTick = true;
    GetCapsuleComponent()->SetCapsuleHalfHeight(88.f);
    GetCharacterMovement()->MaxWalkSpeed = 450.f;
    GetCharacterMovement()->JumpZVelocity = 520.f;
    GetCharacterMovement()->GravityScale = 1.35f;
    GetCharacterMovement()->AirControl = .35f;
    GetCharacterMovement()->MaxAcceleration = 1800.f;
    GetCharacterMovement()->BrakingDecelerationWalking = 1800.f;
    bUseControllerRotationYaw = false;
    GetCharacterMovement()->bOrientRotationToMovement = true;

    if (auto* Manny = LoadObject<USkeletalMesh>(nullptr, TEXT("/Game/Characters/Mannequins/Meshes/SKM_Manny_Simple.SKM_Manny_Simple")))
    {
        GetMesh()->SetSkeletalMesh(Manny);
        GetMesh()->SetRelativeLocation(FVector(0, 0, -88.f));
        GetMesh()->SetRelativeRotation(FRotator(0, -90.f, 0));
        if (auto* Anim = LoadClass<UAnimInstance>(nullptr, TEXT("/Game/Characters/Mannequins/Anims/Unarmed/ABP_Unarmed.ABP_Unarmed_C")))
            GetMesh()->SetAnimInstanceClass(Anim);
    }

    SpringArm = CreateDefaultSubobject<USpringArmComponent>(TEXT("SpringArm"));
    SpringArm->SetupAttachment(RootComponent);
    SpringArm->TargetArmLength = 350.f;
    SpringArm->SetRelativeRotation(FRotator(-20.f, 0.f, 0.f));
    SpringArm->bUsePawnControlRotation = true;
    SpringArm->bEnableCameraLag = true;
    SpringArm->CameraLagSpeed = 10.f;
    SpringArm->bDoCollisionTest = true;
    Camera = CreateDefaultSubobject<UCameraComponent>(TEXT("Camera"));
    Camera->SetupAttachment(SpringArm);
}

void ATinyCharacter::SetupPlayerInputComponent(UInputComponent* Input)
{
    Input->BindAxis("MoveForward", this, &ATinyCharacter::Forward);
    Input->BindAxis("MoveRight", this, &ATinyCharacter::Right);
    Input->BindAxis("Turn", this, &APawn::AddControllerYawInput);
    Input->BindAxis("LookUp", this, &APawn::AddControllerPitchInput);
    Input->BindAction("Jump", IE_Pressed, this, &ATinyCharacter::JumpPressed);
    Input->BindAction("Jump", IE_Released, this, &ATinyCharacter::JumpReleased);
    Input->BindAction("Restart", IE_Pressed, this, &ATinyCharacter::RestartRun);
}

void ATinyCharacter::Forward(float V) { if (Controller && V) { AddMovementInput(FRotationMatrix(FRotator(0, Controller->GetControlRotation().Yaw, 0)).GetUnitAxis(EAxis::X), V); bMoved = true; } }
void ATinyCharacter::Right(float V) { if (Controller && V) { AddMovementInput(FRotationMatrix(FRotator(0, Controller->GetControlRotation().Yaw, 0)).GetUnitAxis(EAxis::Y), V); bMoved = true; } }
void ATinyCharacter::JumpPressed() { JumpBufferRemaining = .12f; }
void ATinyCharacter::JumpReleased() { StopJumping(); }
void ATinyCharacter::Landed(const FHitResult& Hit) { Super::Landed(Hit); CoyoteRemaining = .12f; }
void ATinyCharacter::Tick(float Dt)
{
    Super::Tick(Dt);
    CoyoteRemaining = GetCharacterMovement()->IsMovingOnGround() ? .12f : FMath::Max(0.f, CoyoteRemaining - Dt);
    JumpBufferRemaining = FMath::Max(0.f, JumpBufferRemaining - Dt);
    if (JumpBufferRemaining > 0.f && CoyoteRemaining > 0.f) { Jump(); JumpBufferRemaining = 0.f; CoyoteRemaining = 0.f; bJumped = true; }
    if (auto* GM = GetWorld()->GetAuthGameMode<ATinyCourseGameMode>())
    {
        if (bMoved && !GM->bMovementTutorialDone) { GM->bMovementTutorialDone = true; GM->Objective = TEXT("SPACE  Jump"); }
        if (bJumped && !GM->bJumpTutorialDone) { GM->bJumpTutorialDone = true; GM->Objective = TEXT("Complete three trials and collect energy cores"); }
    }
}
void ATinyCharacter::RestartRun() { if (auto* GM = GetWorld()->GetAuthGameMode<ATinyCourseGameMode>()) GM->RestartRun(); }

APickup::APickup()
{
    PrimaryActorTick.bCanEverTick = true;
    Mesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("Pickup"));
    RootComponent = Mesh;
    Mesh->SetStaticMesh(SphereMesh());
    Mesh->SetWorldScale3D(FVector(.35f));
    Mesh->SetCollisionProfileName(TEXT("OverlapAllDynamic"));
    Mesh->SetGenerateOverlapEvents(true);
    Paint(Mesh, FLinearColor(0.f, .8f, 1.f));
    Mesh->OnComponentBeginOverlap.AddDynamic(this, &APickup::Collected);
}
void APickup::BeginPlay() { Super::BeginPlay(); Paint(Mesh, FLinearColor(0.f, .8f, 1.f)); }
void APickup::Tick(float Dt) { Super::Tick(Dt); AddActorLocalRotation(FRotator(0, 100.f * Dt, 0)); }
void APickup::Collected(UPrimitiveComponent*, AActor* Other, UPrimitiveComponent*, int32, bool, const FHitResult&) { if (Cast<ATinyCharacter>(Other)) { GetWorld()->GetAuthGameMode<ATinyCourseGameMode>()->TakePickup(); Destroy(); } }

AHazard::AHazard()
{
    Mesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("Hazard"));
    RootComponent = Mesh;
    Mesh->SetStaticMesh(CubeMesh());
    Mesh->SetCollisionProfileName(TEXT("OverlapAllDynamic"));
    Mesh->SetGenerateOverlapEvents(true);
    Paint(Mesh, FLinearColor(.9f, .03f, .02f));
    Mesh->OnComponentBeginOverlap.AddDynamic(this, &AHazard::Hit);
}
void AHazard::BeginPlay() { Super::BeginPlay(); Paint(Mesh, FLinearColor(.9f, .03f, .02f)); }
void AHazard::Hit(UPrimitiveComponent*, AActor* Other, UPrimitiveComponent*, int32, bool, const FHitResult&) { if (Cast<ATinyCharacter>(Other)) GetWorld()->GetAuthGameMode<ATinyCourseGameMode>()->Fail(); }

AMovingPlatform::AMovingPlatform()
{
    PrimaryActorTick.bCanEverTick = true;
    Mesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("Platform"));
    RootComponent = Mesh;
    Mesh->SetStaticMesh(CubeMesh());
    Mesh->SetMobility(EComponentMobility::Movable);
    Paint(Mesh, FLinearColor(1.f, .35f, .03f));
}
void AMovingPlatform::BeginPlay() { Super::BeginPlay(); Origin = GetActorLocation(); Paint(Mesh, FLinearColor(1.f, .55f, .03f)); }
void AMovingPlatform::Tick(float Dt) { Super::Tick(Dt); SetActorLocation(Origin + FVector(0, FMath::Sin(GetWorld()->TimeSeconds * 1.2f) * 260.f, 0)); }

AStoneDoor::AStoneDoor()
{
    PrimaryActorTick.bCanEverTick = true;
    Mesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("Door"));
    RootComponent = Mesh;
    Mesh->SetStaticMesh(CubeMesh());
    Paint(Mesh, FLinearColor(.8f, .04f, .03f));
}
void AStoneDoor::BeginPlay() { Super::BeginPlay(); Paint(Mesh, FLinearColor(.8f, .04f, .03f)); }
void AStoneDoor::Open() { ClosedLocation = GetActorLocation(); Paint(Mesh, FLinearColor(.05f, 1.f, .25f)); bOpening = true; }
void AStoneDoor::Tick(float Dt)
{
    Super::Tick(Dt);
    if (!bOpening) return;
    const FVector Target = ClosedLocation + FVector(0, 0, 500);
    SetActorLocation(FMath::VInterpConstantTo(GetActorLocation(), Target, Dt, 260.f));
    if (FVector::DistSquared(GetActorLocation(), Target) < 4.f)
    {
        bOpening = false;
        Mesh->SetCollisionEnabled(ECollisionEnabled::NoCollision);
    }
}

APressurePlate::APressurePlate()
{
    Mesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("PressurePlate"));
    RootComponent = Mesh;
    Mesh->SetStaticMesh(CubeMesh());
    Mesh->SetCollisionProfileName(TEXT("OverlapAllDynamic"));
    Mesh->SetGenerateOverlapEvents(true);
    Paint(Mesh, FLinearColor(.1f, .45f, 1.f));
    Mesh->OnComponentBeginOverlap.AddDynamic(this, &APressurePlate::Pressed);
}
void APressurePlate::BeginPlay() { Super::BeginPlay(); Paint(Mesh, FLinearColor(.1f, .45f, 1.f)); }
void APressurePlate::Pressed(UPrimitiveComponent*, AActor* Other, UPrimitiveComponent*, int32, bool, const FHitResult&)
{
    if (Cast<ATinyCharacter>(Other)) GetWorld()->GetAuthGameMode<ATinyCourseGameMode>()->PressPlate();
}
void APressurePlate::SetActivated()
{
    Paint(Mesh, FLinearColor(.05f, 1.f, .25f));
    SetActorScale3D(FVector(GetActorScale3D().X, GetActorScale3D().Y, .06f));
}

ACheckpoint::ACheckpoint()
{
    Mesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("Checkpoint"));
    RootComponent = Mesh;
    Mesh->SetStaticMesh(CubeMesh());
    Mesh->SetCollisionProfileName(TEXT("OverlapAllDynamic"));
    Mesh->SetGenerateOverlapEvents(true);
    Paint(Mesh, FLinearColor(.1f, 1.f, .45f));
    Mesh->OnComponentBeginOverlap.AddDynamic(this, &ACheckpoint::Activated);
}
void ACheckpoint::BeginPlay() { Super::BeginPlay(); Paint(Mesh, FLinearColor(.05f, .8f, .25f)); }
void ACheckpoint::Activated(UPrimitiveComponent*, AActor* Other, UPrimitiveComponent*, int32, bool, const FHitResult&)
{
    if (Cast<ATinyCharacter>(Other))
        GetWorld()->GetAuthGameMode<ATinyCourseGameMode>()->ActivateCheckpoint(GetActorLocation() + FVector(0,0,140));
}

AGoal::AGoal()
{
    Mesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("Goal"));
    RootComponent = Mesh;
    Mesh->SetStaticMesh(CubeMesh());
    Mesh->SetCollisionProfileName(TEXT("OverlapAllDynamic"));
    Mesh->SetGenerateOverlapEvents(true);
    Paint(Mesh, FLinearColor(.65f, .05f, 1.f));
    Mesh->OnComponentBeginOverlap.AddDynamic(this, &AGoal::Reached);
}
void AGoal::BeginPlay() { Super::BeginPlay(); Paint(Mesh, FLinearColor(.65f, .05f, 1.f)); }
void AGoal::Reached(UPrimitiveComponent*, AActor* Other, UPrimitiveComponent*, int32, bool, const FHitResult&) { if (Cast<ATinyCharacter>(Other)) GetWorld()->GetAuthGameMode<ATinyCourseGameMode>()->TryFinish(); }

void ATinyHUD::DrawHUD()
{
    Super::DrawHUD();
    auto* GM = GetWorld()->GetAuthGameMode<ATinyCourseGameMode>();
    if (!GM || !Canvas) return;
    DrawText(FString::Printf(TEXT("CORE %d/%d"), GM->Collected, GM->Total), FLinearColor::White, 45, 35, GEngine->GetLargeFont(), 1.1f, false);
    if (!GM->Objective.IsEmpty()) DrawText(GM->Objective, FLinearColor(.75f,.88f,1), 45, 82, GEngine->GetLargeFont(), 1.f, false);
    if (!GM->Message.IsEmpty()) DrawText(GM->Message, GM->Finished ? FLinearColor::Green : FLinearColor::Yellow, 45, 128, GEngine->GetLargeFont(), 1.f, false);
}

ATinyCourseGameMode::ATinyCourseGameMode()
{
    PrimaryActorTick.bCanEverTick = true;
    DefaultPawnClass = ATinyCharacter::StaticClass();
    HUDClass = ATinyHUD::StaticClass();
}

void ATinyCourseGameMode::BeginPlay()
{
    Super::BeginPlay();
    if (GetWorld()->GetMapName().Contains(TEXT("L_FloatingRuins")) || GetWorld()->GetMapName().Contains(TEXT("L_RuinsChambers")))
    {
        for (TActorIterator<AStoneDoor> It(GetWorld()); It; ++It) { Door = *It; break; }
        for (TActorIterator<APressurePlate> It(GetWorld()); It; ++It) { Plate = *It; break; }
    }
    SpawnPlayer();
    bAuditCapture = FParse::Param(FCommandLine::Get(), TEXT("CourseAuditCapture"));
    if (bAuditCapture) IFileManager::Get().MakeDirectory(*(FPaths::ProjectSavedDir() / TEXT("Screenshots/Audit")), true);
}
void ATinyCourseGameMode::Tick(float Dt)
{
    Super::Tick(Dt);
    if (!Finished) Time += Dt;
    if (auto* P = UGameplayStatics::GetPlayerPawn(this, 0); P && P->GetActorLocation().Z < -500.f) Fail();
    if (bAuditCapture)
    {
        AuditElapsed += Dt;
        if (AuditElapsed >= AuditNextStep) { RunAuditStep(); AuditNextStep += 1.25f; }
    }
}

void ATinyCourseGameMode::RunAuditStep()
{
    auto* P = UGameplayStatics::GetPlayerPawn(this, 0);
    if (!P) return;
    auto Move = [P](const FVector& L) { P->SetActorLocation(L, false, nullptr, ETeleportType::TeleportPhysics); };
    auto Shot = [](const TCHAR* Name)
    {
        FScreenshotRequest::RequestScreenshot(FPaths::ProjectSavedDir() / TEXT("Screenshots/Audit") / Name, false, false);
    };
    switch (AuditStep++)
    {
    case 0: Shot(TEXT("01_spawn.png")); break;
    case 1: Move(FVector(0,-1300,190)); break;
    case 2: Shot(TEXT("02_route_a_core1.png")); break;
    case 3: Move(FVector(220,1320,190)); break;
    case 4: Shot(TEXT("03_route_b_core2.png")); break;
    case 5: Move(FVector(-690,260,170)); break;
    case 6: Move(FVector(-900,260,140)); break;
    case 7: Shot(TEXT("04_hazard_checkpoint_respawn.png")); break;
    case 8: Move(FVector(-1420,260,185)); break;
    case 9: Shot(TEXT("05_route_c_core3.png")); break;
    case 10: Move(FVector(300,0,160)); break;
    case 11: Shot(TEXT("06_return_central.png")); break;
    case 12: Move(FVector(470,0,160)); break;
    case 13: Shot(TEXT("07_plate_gate_opening.png")); break;
    case 14: Shot(TEXT("08_gate_open.png")); break;
    case 15: Move(FVector(1500,0,350)); break;
    case 16: Shot(TEXT("09_goal_complete.png")); bAuditCapture = false; break;
    default: bAuditCapture = false; break;
    }
}

AActor* ATinyCourseGameMode::Block(FVector L, FVector S, FColor Color)
{
    AActor* A = GetWorld()->SpawnActor<AActor>(AActor::StaticClass(), L, FRotator::ZeroRotator);
    auto* M = NewObject<UStaticMeshComponent>(A, TEXT("Block"));
    A->SetRootComponent(M); M->RegisterComponent(); M->SetStaticMesh(CubeMesh()); M->SetWorldScale3D(S);
    Paint(M, FLinearColor(Color));
    return A;
}

void ATinyCourseGameMode::BuildCourse()
{
    // The engine Entry map contains no lights. Add a simple daylight rig so the
    // generated character, platforms and gameplay objects are actually visible.
    auto* Sun = GetWorld()->SpawnActor<ADirectionalLight>(
        ADirectionalLight::StaticClass(), FVector::ZeroVector, FRotator(-50.f, -35.f, 0.f));
    Sun->GetLightComponent()->SetIntensity(8.f);
    Sun->GetLightComponent()->SetLightColor(FLinearColor(1.f, .92f, .8f));

    auto* Sky = GetWorld()->SpawnActor<ASkyLight>(
        ASkyLight::StaticClass(), FVector::ZeroVector, FRotator::ZeroRotator);
    Sky->GetLightComponent()->SetMobility(EComponentMobility::Movable);
    Sky->GetLightComponent()->SetIntensity(2.f);
    Sky->GetLightComponent()->RecaptureSky();

    // Keep every gameplay section readable even when it is enclosed by walls.
    const float LightPositions[] = { -850.f, -250.f, 400.f, 1050.f, 1600.f };
    for (const float X : LightPositions)
    {
        auto* Lamp = GetWorld()->SpawnActor<APointLight>(
            APointLight::StaticClass(), FVector(X, 0, 520), FRotator::ZeroRotator);
        auto* Light = Cast<UPointLightComponent>(Lamp->GetLightComponent());
        Light->SetIntensity(6500.f);
        Light->SetAttenuationRadius(1250.f);
        Light->SetLightColor(FLinearColor(.65f, .8f, 1.f));
        Light->SetCastShadows(false);
    }

    const FColor Floor(55, 65, 82);
    const FColor Platform(100, 120, 150);
    const FColor Wall(26, 34, 50);
    Block(FVector(0,0,-70), FVector(22,8,1), Floor);
    Block(FVector(0,-850,260), FVector(22,1,7), Wall);
    Block(FVector(0, 850,260), FVector(22,1,7), Wall);
    Block(FVector(-2150,0,260), FVector(1,8,7), Wall);
    Block(FVector(400,0,70), FVector(2.2f,2,0.4f), Platform);
    Block(FVector(760,0,150), FVector(2,2,0.4f), Platform);
    Block(FVector(1120,0,240), FVector(2,2,0.4f), Platform);
    Block(FVector(1500,0,330), FVector(3,2.5f,0.4f), Platform);
    // Lab-style gateway and cover pieces similar to an editor-built course.
    Block(FVector(-250,-330,90), FVector(.45f,1.2f,2.2f), Wall);
    Block(FVector(-250, 330,90), FVector(.45f,1.2f,2.2f), Wall);
    Block(FVector(-250,0,290), FVector(.45f,2.2f,.35f), Platform);
    Block(FVector(1250,-520,40), FVector(1.4f,.5f,1.2f), Wall);
    Block(FVector(1250, 520,40), FVector(1.4f,.5f,1.2f), Wall);

    const FVector PickupLocations[] = { {-550,0,35}, {-100,250,35}, {400,0,150} };
    for (const FVector& L : PickupLocations) Pickups.Add(GetWorld()->SpawnActor<APickup>(APickup::StaticClass(), L, FRotator::ZeroRotator));

    auto* H1 = GetWorld()->SpawnActor<AHazard>(AHazard::StaticClass(), FVector(100,0,-10), FRotator::ZeroRotator); H1->SetActorScale3D(FVector(2.5f,.7f,.2f));
    auto* H2 = GetWorld()->SpawnActor<AHazard>(AHazard::StaticClass(), FVector(850,0,20), FRotator::ZeroRotator); H2->SetActorScale3D(FVector(2,.7f,.2f));
    auto* MP = GetWorld()->SpawnActor<AMovingPlatform>(AMovingPlatform::StaticClass(), FVector(760,0,60), FRotator::ZeroRotator); MP->SetActorScale3D(FVector(1.5f,1.5f,.25f));
    Plate = GetWorld()->SpawnActor<APressurePlate>(APressurePlate::StaticClass(), FVector(1120,0,295), FRotator::ZeroRotator); Plate->SetActorScale3D(FVector(1.1f,1.1f,.12f));
    Door = GetWorld()->SpawnActor<AStoneDoor>(AStoneDoor::StaticClass(), FVector(1370,0,250), FRotator::ZeroRotator); Door->SetActorScale3D(FVector(.35f,3.f,3.f));
    auto* Checkpoint = GetWorld()->SpawnActor<ACheckpoint>(ACheckpoint::StaticClass(), FVector(1450,0,410), FRotator::ZeroRotator); Checkpoint->SetActorScale3D(FVector(.5f,1.5f,.08f));
    auto* Goal = GetWorld()->SpawnActor<AGoal>(AGoal::StaticClass(), FVector(1700,0,460), FRotator::ZeroRotator); Goal->SetActorScale3D(FVector(.25f,2.f,1.5f));
}

void ATinyCourseGameMode::SpawnPlayer()
{
    APlayerController* PC = UGameplayStatics::GetPlayerController(this, 0);
    if (!PC) return;
    if (auto* PS = UGameplayStatics::GetActorOfClass(this, APlayerStart::StaticClass())) Start = PS->GetActorLocation();
    RespawnPoint = Start;
    if (APawn* P = PC->GetPawn()) P->SetActorLocation(Start);
    else { auto* NewPawn = GetWorld()->SpawnActor<ATinyCharacter>(ATinyCharacter::StaticClass(), Start, FRotator::ZeroRotator); PC->Possess(NewPawn); }
}

void ATinyCourseGameMode::TakePickup() { ++Collected; Message = FString::Printf(TEXT("Energy Core %d/%d"), Collected, Total); Objective = Collected == Total ? TEXT("All cores collected - return to the central hall") : TEXT("Complete three trials and collect energy cores"); UE_LOG(LogTemp, Display, TEXT("COURSE_EVENT CoreCollected %d/%d"), Collected, Total); }
void ATinyCourseGameMode::PressPlate()
{
    if (PlateActivated) return;
    if (Collected < Total) { Message = FString::Printf(TEXT("Plate needs %d more energy cores"), Total-Collected); return; }
    PlateActivated = true;
    Message = TEXT("Pressure plate activated"); Objective = TEXT("Enter the portal to complete the trial"); UE_LOG(LogTemp, Display, TEXT("COURSE_EVENT PlateActivated DoorOpening"));
    if (Plate) Plate->SetActivated();
    if (Door) Door->Open();
}
void ATinyCourseGameMode::ActivateCheckpoint(const FVector& Location)
{
    RespawnPoint = Location;
    Message = TEXT("Checkpoint activated"); UE_LOG(LogTemp, Display, TEXT("COURSE_EVENT CheckpointActivated %s"), *Location.ToCompactString());
}
void ATinyCourseGameMode::Fail() { ++Deaths; Message = TEXT("Trial failed - respawned at checkpoint"); UE_LOG(LogTemp, Display, TEXT("COURSE_EVENT FailRespawn deaths=%d point=%s"), Deaths, *RespawnPoint.ToCompactString()); if (auto* P = UGameplayStatics::GetPlayerPawn(this,0)) { P->SetActorLocation(RespawnPoint); if (auto* C=Cast<ACharacter>(P)) C->GetCharacterMovement()->StopMovementImmediately(); } }
void ATinyCourseGameMode::TryFinish() { if (Collected < Total || !PlateActivated) { Message = TEXT("Collect all cores and activate the pressure plate"); return; } Finished = true; Objective = TEXT("Trial complete"); Message = FString::Printf(TEXT("RUINS TRIAL COMPLETE  %.1f seconds  Press R to restart"), Time); UE_LOG(LogTemp, Display, TEXT("COURSE_EVENT GoalComplete time=%.1f deaths=%d"), Time, Deaths); }
void ATinyCourseGameMode::RestartRun() { UGameplayStatics::OpenLevel(this, FName(*GetWorld()->GetName()), false); }

