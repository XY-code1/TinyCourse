# TinyCourse — Floating Ruins Stage A

Unreal Engine 5.7 third-person course prototype on the `revamp/experience-pass` branch.

## Current playable loop

1. Start on the central safe island.
2. Complete Route A (blue jumps) and collect core 1.
3. Complete Route B (yellow mandatory moving platform) and collect core 2.
4. Activate the Route C checkpoint, cross the red-orange hazards, and collect core 3.
5. Return to the central pressure plate.
6. Open the locked gate and enter the purple goal portal.

Controls: `WASD`, mouse, `Space`, `R`.

## Map

The project-owned default map is `/Game/Maps/L_FloatingRuins`.
It contains saved level actors and no longer depends on `BuildCourse()` for the formal course.

The editor-generation source is `Scripts/build_floating_ruins.py`.

## Stage A scope

Included: formal saved map, three spatially distinct routes, three cores, mandatory moving platform, hazard/checkpoint route, locked gate, pressure plate, goal and in-engine audit captures.

Deferred: final skeletal character and animations, production UI, audio, particles, final art and Windows packaging.
