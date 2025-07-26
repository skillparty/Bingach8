# Design Document

## Overview

This design document outlines the implementation approach for minor UI positioning refinements in the Bingacho game. The changes focus on improving visual balance through precise positioning adjustments and interface cleanup by removing redundant text elements.

## Architecture

### Component Structure
The changes affect two main UI rendering functions:
- `draw_current_number()` - Renders the current number display
- `draw_number_history()` - Renders the history panel  
- `draw_board()` - Renders the game board with title

### Positioning System
The current positioning system uses:
- `scale_value()` function for responsive scaling
- Fixed pixel offsets for element positioning
- Alignment coordination between related elements

## Components and Interfaces

### 1. Current Number Display Component
**Location:** `main.py` - `draw_current_number()` function
**Current Implementation:**
```python
container_y = scale_value(24, False, min_value=16, max_value=48)
```
**Required Change:**
```python
container_y = scale_value(25, False, min_value=17, max_value=49)  # +1px adjustment
```

### 2. History Panel Component  
**Location:** `main.py` - `draw_number_history()` function
**Current Implementation:**
```python
panel_y = scale_value(24, False, min_value=16, max_value=48)
```
**Required Change:**
```python
panel_y = scale_value(25, False, min_value=17, max_value=49)  # +1px adjustment
```

### 3. Board Title Component
**Location:** `main.py` - `draw_board()` function
**Current Implementation:**
```python
# Subtítulo con información del modo
mode_text = f"Modo: {cfg.BOARD_ROWS}×{cfg.BOARD_COLS} | Números 1-{cfg.TOTAL_NUMBERS}"
subtitle_font = fonts["number_small"]
subtitle_surface = subtitle_font.render(mode_text, True, cfg.GRAY)
subtitle_rect = subtitle_surface.get_rect(center=(container_rect.centerx, title_y + scale_value(35, False, min_value=25, max_value=45)))
screen.blit(subtitle_surface, subtitle_rect)
```
**Required Change:** Complete removal of this code block

## Data Models

### Positioning Coordinates
- **Y-coordinate adjustment:** +1 pixel for both number display and history panel
- **Alignment maintenance:** Both elements must have identical Y coordinates
- **Scaling preservation:** Adjustments must work with the existing `scale_value()` system

### UI Element Removal
- **Subtitle text removal:** Complete elimination of mode information display
- **Spacing preservation:** Maintain existing visual hierarchy without the removed element

## Error Handling

### Positioning Validation
- Ensure adjusted positions don't cause element overlap
- Verify minimum and maximum value constraints are updated consistently
- Maintain responsive behavior across different screen resolutions

### Visual Regression Prevention
- Confirm title text remains properly positioned after subtitle removal
- Verify board layout isn't affected by subtitle removal
- Ensure no visual artifacts remain from removed elements

## Testing Strategy

### Unit Testing
1. **Position Verification Test**
   - Verify current number Y position is exactly 1px lower
   - Verify history panel Y position is exactly 1px lower
   - Confirm both elements maintain identical Y coordinates

2. **Element Removal Test**
   - Confirm subtitle text is not rendered
   - Verify no empty space remains where subtitle was
   - Check that board title positioning is unaffected

### Visual Testing
1. **Cross-Resolution Testing**
   - Test positioning adjustments on 4K, 2K, 1080p, and 720p
   - Verify scaling behavior with new position values
   - Confirm alignment is maintained across all resolutions

2. **Interface Cleanup Testing**
   - Verify clean appearance without subtitle text
   - Check visual balance after text removal
   - Confirm no layout disruption in both game modes

### Integration Testing
1. **Game Mode Testing**
   - Test normal mode (9×10) without subtitle
   - Test alternate mode (7×11) without subtitle
   - Verify consistent behavior across both modes

2. **Element Interaction Testing**
   - Confirm repositioned elements don't interfere with board
   - Verify proper spacing between all UI components
   - Test hover effects and interactions remain functional

## Implementation Approach

### Phase 1: Position Adjustments
1. Update `draw_current_number()` Y coordinate calculation
2. Update `draw_number_history()` Y coordinate calculation  
3. Update corresponding min/max value constraints
4. Test alignment between both elements

### Phase 2: Subtitle Removal
1. Locate and remove subtitle rendering code in `draw_board()`
2. Remove related variables and calculations
3. Verify title positioning remains correct
4. Test visual appearance without subtitle

### Phase 3: Validation
1. Run positioning tests to verify 1px adjustment
2. Visual inspection across multiple resolutions
3. Confirm no regressions in existing functionality
4. Update any related documentation or test scripts