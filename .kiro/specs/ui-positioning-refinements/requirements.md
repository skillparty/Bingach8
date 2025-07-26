# Requirements Document

## Introduction

This specification addresses minor UI positioning refinements for the Bingacho game interface. The goal is to improve the visual balance by making small adjustments to element positioning and removing unnecessary text labels that clutter the interface.

## Requirements

### Requirement 1

**User Story:** As a player, I want the number display and history panel to be positioned slightly lower so that the visual balance is improved and there's better spacing from the top edge.

#### Acceptance Criteria

1. WHEN the game interface loads THEN the current number display SHALL be positioned 1 pixel lower than its current position
2. WHEN the game interface loads THEN the history panel SHALL be positioned 1 pixel lower than its current position  
3. WHEN both elements are repositioned THEN they SHALL maintain perfect horizontal alignment with each other
4. WHEN the repositioning is applied THEN there SHALL be no interference with the game board or other UI elements

### Requirement 2

**User Story:** As a player, I want a cleaner interface without redundant text labels so that I can focus on the game content without visual clutter.

#### Acceptance Criteria

1. WHEN the game board is displayed THEN the subtitle text "Modo: 9×10 | Números 1-90" SHALL be removed completely
2. WHEN the subtitle is removed THEN the board title "TABLERO DE NÚMEROS" SHALL remain visible and properly positioned
3. WHEN the subtitle is removed THEN the visual spacing around the board SHALL be maintained appropriately
4. WHEN playing in alternate mode THEN the corresponding subtitle text SHALL also be removed
5. WHEN the subtitle is removed THEN no empty space or visual artifacts SHALL remain where the text was previously displayed