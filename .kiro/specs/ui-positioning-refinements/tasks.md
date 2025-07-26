# Implementation Plan

- [x] 1. Update current number display positioning
  - Modify the Y coordinate calculation in `draw_current_number()` function
  - Change from `scale_value(24, False, min_value=16, max_value=48)` to `scale_value(25, False, min_value=17, max_value=49)`
  - Ensure the 1 pixel downward adjustment is applied consistently
  - _Requirements: 1.1, 1.3_

- [x] 2. Update history panel positioning  
  - Modify the Y coordinate calculation in `draw_number_history()` function
  - Change from `scale_value(24, False, min_value=16, max_value=48)` to `scale_value(25, False, min_value=17, max_value=49)`
  - Maintain perfect alignment with the current number display
  - _Requirements: 1.2, 1.3_

- [x] 3. Remove board subtitle text
  - Locate the subtitle rendering code in `draw_board()` function
  - Remove the mode text generation: `mode_text = f"Modo: {cfg.BOARD_ROWS}×{cfg.BOARD_COLS} | Números 1-{cfg.TOTAL_NUMBERS}"`
  - Remove the subtitle font, surface, and rect creation code
  - Remove the `screen.blit(subtitle_surface, subtitle_rect)` call
  - _Requirements: 2.1, 2.5_

- [x] 4. Verify positioning alignment
  - Test that both current number display and history panel have identical Y coordinates
  - Confirm the 1 pixel adjustment is correctly applied
  - Ensure no interference with other UI elements
  - _Requirements: 1.3, 1.4_

- [x] 5. Test visual appearance
  - Verify the board title "TABLERO DE NÚMEROS" remains properly positioned
  - Confirm no empty space or artifacts remain where subtitle was removed
  - Test appearance in both normal and alternate game modes
  - _Requirements: 2.2, 2.3, 2.4, 2.5_

- [x] 6. Update test scripts
  - Modify `test_positioning.py` to reflect the new Y coordinate values
  - Update position calculations to use the new base value of 25 instead of 24
  - Verify test script accurately reports the positioning changes
  - _Requirements: 1.1, 1.2_