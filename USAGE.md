# Pomodoro Timer - User Guide

## Overview
A desktop Pomodoro Timer application implementing a state machine for productivity management with visual and audible feedback.

## Features

### Core Functionality
- **Three States with Fixed Durations:**
  - Focus: 25 minutes (Green background)
  - Short Break: 5 minutes (Yellow background)
  - Long Break: 15 minutes (Red background)

- **Automatic Cycle Management:**
  - Tracks completed Focus sessions
  - After 4 Focus sessions, automatically triggers a Long Break
  - Resets cycle counter after Long Break

- **Automatic Transitions:**
  - Timer automatically advances to the next state when reaching 0:00
  - Continues running without manual intervention

### User Interface

#### Main Display
- **Large Timer Display:** Shows time remaining in MM:SS format
- **State Label:** Displays current state (Focus/Short Break/Long Break)
- **Color-Coded Background:** 
  - Green = Focus
  - Yellow = Short Break
  - Red = Long Break

#### Cycle Indicator
- Four circles at the center of the window
- Filled white circles = completed Focus sessions
- Empty circles = remaining Focus sessions in current cycle

#### Control Buttons
1. **Start:** Begin the countdown timer
2. **Pause:** Temporarily halt the timer
3. **Reset/Skip:** 
   - Stops current timer
   - Resets to Focus state
   - Advances the cycle appropriately

### Audio Feedback
- Plays a distinct beep sound (1000 Hz, 500ms) when timer reaches 0:00
- Alerts you to state changes

## How to Use

1. **Start a Focus Session:**
   - Click "Start" to begin the 25-minute Focus timer
   - The background will be green

2. **Take a Break:**
   - When the Focus timer reaches 0:00, you'll hear a beep
   - The timer automatically switches to Short Break (or Long Break after 4 Focus sessions)
   - Background changes to yellow (Short Break) or red (Long Break)

3. **Resume Work:**
   - After a break completes, the timer automatically returns to Focus state
   - Click "Start" to begin your next Focus session

4. **Pause if Needed:**
   - Click "Pause" to temporarily stop the timer
   - Click "Start" to resume from where you left off

5. **Skip/Reset:**
   - Click "Reset/Skip" to stop the current session
   - Returns to Focus state
   - Useful if you need to skip a break or restart

## Running the Application

```bash
python pomodoro_timer.py
```

## Requirements
- Python 3.x
- tkinter (included with Python)
- winsound (Windows only, included with Python on Windows)

## Technical Details

### State Machine Logic
- **State Enum:** Defines three states (FOCUS, SHORT_BREAK, LONG_BREAK)
- **Cycle Counter:** Tracks 0-3 completed Focus sessions
- **Automatic Transitions:** Implements deterministic state transitions

### Architecture
- **PomodoroTimer Class:** Core state machine logic
- **PomodoroGUI Class:** User interface implementation
- **Thread-based Audio:** Sound alerts play asynchronously to avoid UI blocking

## Troubleshooting

**No sound playing:**
- Ensure your system volume is not muted
- On non-Windows systems, you may need to implement alternative audio playback

**Window doesn't appear:**
- Ensure tkinter is properly installed
- Try running: `python -m tkinter` to test tkinter installation

**Timer not counting down:**
- Click the "Start" button to begin the countdown
- Ensure the button is enabled (not grayed out)
