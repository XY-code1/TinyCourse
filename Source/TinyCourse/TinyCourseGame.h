#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "GameFramework/Character.h"
#include "GameFramework/GameModeBase.h"
#include "GameFramework/HUD.h"
#include "TinyCourseGame.generated.h"

class ATextRenderActor;

class UCameraComponent;
class USpringArmComponent;
class UStaticMeshComponent;
class USphereComponent;
class UBoxComponent;
class UPointLightComponent;
class USpotLightComponent;

UCLASS()
class TINYCOURSE_API ACourseBlock : public AActor
{
    GENERATED_BODY()
public:
    ACourseBlock();
    virtual void OnConstruction(const FTransform& Transform) override;
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Course") FLinearColor BlockColor = FLinearColor(.35f, .32f, .28f);
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Course") FString MaterialAssetPath;
private:
    UPROPERTY() UStaticMeshComponent* Mesh;
    void ApplyAppearance();
protected:
    virtual void BeginPlay() override;
};

UCLASS()
class TINYCOURSE_API ATinyCharacter : public ACharacter
{
    GENERATED_BODY()
public:
    ATinyCharacter();
    virtual void SetupPlayerInputComponent(UInputComponent* Input) override;
    virtual void Tick(float DeltaSeconds) override;
    virtual void Landed(const FHitResult& Hit) override;
private:
    UPROPERTY() USpringArmComponent* SpringArm;
    UPROPERTY() UCameraComponent* Camera;
    UPROPERTY() UPointLightComponent* CharacterFillLight;
    void Forward(float Value);
    void Right(float Value);
    void JumpPressed();
    void JumpReleased();
    void CrouchPressed();
    void CrouchReleased();
    void RestartRun();
    float CoyoteRemaining = 0.f;
    float JumpBufferRemaining = 0.f;
    bool bMoved = false;
    bool bJumped = false;
};

UCLASS()
class TINYCOURSE_API APickup : public AActor
{
    GENERATED_BODY()
public:
    APickup();
protected:
    virtual void BeginPlay() override;
    virtual void Tick(float DeltaSeconds) override;
private:
    UPROPERTY() UStaticMeshComponent* Mesh;
    UFUNCTION() void Collected(UPrimitiveComponent* OverlappedComponent, AActor* OtherActor,
        UPrimitiveComponent* OtherComponent, int32 OtherBodyIndex, bool bFromSweep,
        const FHitResult& SweepResult);
};

UCLASS()
class TINYCOURSE_API AHazard : public AActor
{
    GENERATED_BODY()
public:
    AHazard();
protected:
    virtual void BeginPlay() override;
private:
    UPROPERTY() UStaticMeshComponent* Mesh;
    UFUNCTION() void Hit(UPrimitiveComponent* OverlappedComponent, AActor* OtherActor,
        UPrimitiveComponent* OtherComponent, int32 OtherBodyIndex, bool bFromSweep,
        const FHitResult& SweepResult);
};

UCLASS()
class TINYCOURSE_API ATimedHazard : public AActor
{
    GENERATED_BODY()
public:
    ATimedHazard();
    virtual void BeginPlay() override;
    virtual void Tick(float DeltaSeconds) override;
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Hazard") float PhaseOffset = 0.f;
    void ForceSafe();
    void SetAuditWarning();
    void SetAuditActive();
private:
    UPROPERTY() UStaticMeshComponent* Mesh;
    float Elapsed = 0.f;
    bool bActive = false;
    bool bSafe = false;
    bool bWarnedOnce = false;
    UFUNCTION() void Hit(UPrimitiveComponent* Overlapped, AActor* Other, UPrimitiveComponent* OtherComponent, int32 BodyIndex, bool bFromSweep, const FHitResult& Sweep);
};

UCLASS()
class TINYCOURSE_API ASweepingHazard : public AActor
{
    GENERATED_BODY()
public:
    ASweepingHazard();
    virtual void BeginPlay() override;
    virtual void Tick(float DeltaSeconds) override;
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Hazard") FVector TravelOffset = FVector(700.f,0,0);
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Hazard") float SweepSpeed = .75f;
    void ForceSafe();
private:
    UPROPERTY() UStaticMeshComponent* Mesh;
    FVector Origin;
    float Elapsed = 0.f;
    bool bSafe = false;
    UFUNCTION() void Hit(UPrimitiveComponent* Overlapped, AActor* Other, UPrimitiveComponent* OtherComponent, int32 BodyIndex, bool bFromSweep, const FHitResult& Sweep);
};

UCLASS()
class TINYCOURSE_API AMovingPlatform : public AActor
{
    GENERATED_BODY()
public:
    AMovingPlatform();
    virtual void BeginPlay() override;
    virtual void Tick(float DeltaSeconds) override;
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Movement") FVector TravelOffset = FVector(400.f, 0.f, 0.f);
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Movement") float MoveSpeed = 140.f;
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Movement") float EndPause = .75f;
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Visual") FString MaterialAssetPath;
private:
    UPROPERTY() UStaticMeshComponent* Mesh;
    UPROPERTY() UStaticMeshComponent* EdgeN;
    UPROPERTY() UStaticMeshComponent* EdgeS;
    UPROPERTY() UStaticMeshComponent* EdgeE;
    UPROPERTY() UStaticMeshComponent* EdgeW;
    FVector Origin;
    float Distance = 0.f;
    float HoldRemaining = 0.f;
    int32 Direction = 1;
};

UCLASS()
class TINYCOURSE_API AStoneDoor : public AActor
{
    GENERATED_BODY()
public:
    AStoneDoor();
    virtual void BeginPlay() override;
    virtual void Tick(float DeltaSeconds) override;
    void Open();
private:
    UPROPERTY() USceneComponent* Root;
    UPROPERTY() USceneComponent* LeftHinge;
    UPROPERTY() USceneComponent* RightHinge;
    UPROPERTY() UStaticMeshComponent* LeftLeaf;
    UPROPERTY() UStaticMeshComponent* RightLeaf;
    UPROPERTY() UPointLightComponent* LockLight;
    UPROPERTY() USpotLightComponent* FrontFillLight;
    UPROPERTY() UPointLightComponent* LeftRimLight;
    UPROPERTY() UPointLightComponent* RightRimLight;
    float OpenElapsed = 0.f;
    bool bOpening = false;
    bool bOpened = false;
};

UCLASS()
class TINYCOURSE_API APressurePlate : public AActor
{
    GENERATED_BODY()
public:
    APressurePlate();
    void SetActivated();
protected:
    virtual void BeginPlay() override;
private:
    UPROPERTY() UStaticMeshComponent* Mesh;
    UFUNCTION() void Pressed(UPrimitiveComponent* OverlappedComponent, AActor* OtherActor,
        UPrimitiveComponent* OtherComponent, int32 OtherBodyIndex, bool bFromSweep,
        const FHitResult& SweepResult);
};

UCLASS()
class TINYCOURSE_API ACheckpoint : public AActor
{
    GENERATED_BODY()
public:
    ACheckpoint();
protected:
    virtual void BeginPlay() override;
private:
    UPROPERTY() UStaticMeshComponent* Mesh;
    bool bActivated = false;
    UFUNCTION() void Activated(UPrimitiveComponent* OverlappedComponent, AActor* OtherActor,
        UPrimitiveComponent* OtherComponent, int32 OtherBodyIndex, bool bFromSweep,
        const FHitResult& SweepResult);
};

UCLASS()
class TINYCOURSE_API AGoal : public AActor
{
    GENERATED_BODY()
public:
    AGoal();
protected:
    virtual void BeginPlay() override;
private:
    UPROPERTY() UStaticMeshComponent* Mesh;
    UFUNCTION() void Reached(UPrimitiveComponent* OverlappedComponent, AActor* OtherActor,
        UPrimitiveComponent* OtherComponent, int32 OtherBodyIndex, bool bFromSweep,
        const FHitResult& SweepResult);
};

UCLASS()
class TINYCOURSE_API ATinyHUD : public AHUD
{
    GENERATED_BODY()
public:
    virtual void DrawHUD() override;
};

UCLASS()
class TINYCOURSE_API ATinyCourseGameMode : public AGameModeBase
{
    GENERATED_BODY()
public:
    ATinyCourseGameMode();
    virtual void BeginPlay() override;
    virtual void Tick(float DeltaSeconds) override;
    void TakePickup();
    void Fail();
    void PressPlate();
    void ActivateCheckpoint(const FVector& Location);
    void TryFinish();
    void RestartRun();
    void ShowMessage(const FString& Text, float Seconds = 2.5f);
    int32 Collected = 0;
    int32 Total = 3;
    int32 Deaths = 0;
    float Time = 0.f;
    bool Finished = false;
    bool PlateActivated = false;
    FString Message;
    FString Objective = TEXT("完成三项试炼，收集能量核心并开启遗迹大门");
    bool bMovementTutorialDone = false;
    bool bJumpTutorialDone = false;
private:
    FVector Start = FVector(-900, 0, 120);
    FVector RespawnPoint = Start;
    UPROPERTY() AStoneDoor* Door = nullptr;
    UPROPERTY() APressurePlate* Plate = nullptr;
    TArray<TWeakObjectPtr<APickup>> Pickups;
    bool bAuditCapture = false;
    float AuditElapsed = 0.f;
    float AuditNextStep = 1.f;
    int32 AuditStep = 0;
    float MessageUntil = 0.f;
    bool bNearBlueEntrance = false;
    bool bNearYellowEntrance = false;
    bool bNearMovingPlatform = false;
    bool bNearCrouchTunnel = false;
    bool bNearLockedEntrance = false;
    bool bNearRedTrial = false;
    UPROPERTY() AActor* YellowGate = nullptr;
    UPROPERTY() ATextRenderActor* YellowSign = nullptr;
    UPROPERTY() AActor* RedGate = nullptr;
    UPROPERTY() ATextRenderActor* RedSign = nullptr;
    void UnlockYellowTrial();
    void UnlockRedTrial();
    void DisableRedHazards();
    void BuildCourse();
    void SpawnPlayer();
    void RunAuditStep();
    AActor* Block(FVector Location, FVector Scale, FColor Color);
};
