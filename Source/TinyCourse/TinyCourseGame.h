#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "GameFramework/Character.h"
#include "GameFramework/GameModeBase.h"
#include "GameFramework/HUD.h"
#include "TinyCourseGame.generated.h"

class UCameraComponent;
class USpringArmComponent;
class UStaticMeshComponent;
class USphereComponent;
class UBoxComponent;

UCLASS()
class TINYCOURSE_API ACourseBlock : public AActor
{
    GENERATED_BODY()
public:
    ACourseBlock();
    virtual void OnConstruction(const FTransform& Transform) override;
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Course") FLinearColor BlockColor = FLinearColor(.35f, .32f, .28f);
private:
    UPROPERTY() UStaticMeshComponent* Mesh;
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
class TINYCOURSE_API AMovingPlatform : public AActor
{
    GENERATED_BODY()
public:
    AMovingPlatform();
    virtual void BeginPlay() override;
    virtual void Tick(float DeltaSeconds) override;
private:
    UPROPERTY() UStaticMeshComponent* Mesh;
    FVector Origin;
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
    UPROPERTY() UStaticMeshComponent* Mesh;
    FVector ClosedLocation;
    bool bOpening = false;
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
    int32 Collected = 0;
    int32 Total = 3;
    int32 Deaths = 0;
    float Time = 0.f;
    bool Finished = false;
    bool PlateActivated = false;
    FString Message;
    FString Objective = TEXT("WASD 绉诲姩");
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
    void BuildCourse();
    void SpawnPlayer();
    void RunAuditStep();
    AActor* Block(FVector Location, FVector Scale, FColor Color);
};
