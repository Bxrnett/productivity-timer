"""
Pomodoro Timer Desktop Application
A state machine-based timer application for productivity management
"""
import tkinter as tk
from tkinter import font
from enum import Enum
import winsound
from threading import Thread


class State(Enum):
    """Timer states for the Pomodoro technique"""
    FOCUS = "Focus"
    SHORT_BREAK = "Short Break"
    LONG_BREAK = "Long Break"


class PomodoroTimer:
    """State machine implementation for Pomodoro Timer"""
    
    # State durations in seconds
    DURATIONS = {
        State.FOCUS: 25 * 60,        # 25 minutes
        State.SHORT_BREAK: 5 * 60,   # 5 minutes
        State.LONG_BREAK: 15 * 60    # 15 minutes
    }
    
    # State colors
    COLORS = {
        State.FOCUS: "#4CAF50",        # Green
        State.SHORT_BREAK: "#FFEB3B",  # Yellow
        State.LONG_BREAK: "#F44336"    # Red
    }
    
    def __init__(self):
        self.current_state = State.FOCUS
        self.time_remaining = self.DURATIONS[State.FOCUS]
        self.is_running = False
        self.focus_count = 0  # Tracks completed focus sessions (0-3)
        self.timer_id = None
        
    def get_next_state(self):
        """Determine the next state based on current state and focus count"""
        if self.current_state == State.FOCUS:
            # After a focus session, check if we should take a long break
            if self.focus_count >= 3:  # 4th focus session completed
                return State.LONG_BREAK
            else:
                return State.SHORT_BREAK
        else:
            # After any break, return to focus
            return State.FOCUS
    
    def transition_to_next_state(self):
        """Transition to the next state in the cycle"""
        if self.current_state == State.FOCUS:
            self.focus_count += 1
            if self.focus_count >= 4:
                self.focus_count = 0  # Reset after long break
        
        self.current_state = self.get_next_state()
        self.time_remaining = self.DURATIONS[self.current_state]
    
    def reset_to_focus(self):
        """Reset to focus state and advance the cycle"""
        if self.current_state == State.FOCUS:
            # If already in focus, just reset the timer
            self.time_remaining = self.DURATIONS[State.FOCUS]
        else:
            # Skip current break and go to next focus
            self.current_state = State.FOCUS
            self.time_remaining = self.DURATIONS[State.FOCUS]
    
    def tick(self):
        """Decrement timer by one second, return True if timer reached zero"""
        if self.time_remaining > 0:
            self.time_remaining -= 1
            return self.time_remaining == 0
        return False
    
    def format_time(self):
        """Format time remaining as MM:SS"""
        minutes = self.time_remaining // 60
        seconds = self.time_remaining % 60
        return f"{minutes:02d}:{seconds:02d}"
    
    def get_energy_drink_display(self):
        """Generate energy drink visual based on time remaining"""
        total_time = self.DURATIONS[self.current_state]
        percent_remaining = self.time_remaining / total_time
        
        # Calculate fill level (0-10)
        fill_level = int(percent_remaining * 10)
        
        # Energy drink can ASCII art
        can_top = "  ___________  "
        can_pull_tab = " |  _____  |  "
        can_opening = " | |_____| |  "
        can_neck = " |           |  "
        
        # Build the can body with fill levels
        lines = [can_top, can_pull_tab, can_opening, can_neck]
        
        # 10 levels of liquid
        for i in range(10):
            if i < (10 - fill_level):
                # Empty part
                lines.append(" |           |  ")
            else:
                # Filled part with liquid
                lines.append(" | ▓▓▓▓▓▓▓ |  ")
        
        can_bottom = " |___________|  "
        lines.append(can_bottom)
        
        return "\n".join(lines)


class PomodoroGUI:
    """GUI implementation for Pomodoro Timer"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Pomodoro Timer")
        self.root.geometry("600x400")
        self.root.resizable(False, False)
        
        # Initialize timer state machine
        self.timer = PomodoroTimer()
        
        # Create UI components
        self.create_widgets()
        self.update_display()
        
    def create_widgets(self):
        """Create all GUI components"""
        # Main container with colored background
        self.main_frame = tk.Frame(self.root, bg=PomodoroTimer.COLORS[State.FOCUS])
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # State label
        state_font = font.Font(family="Helvetica", size=24, weight="bold")
        self.state_label = tk.Label(
            self.main_frame,
            text=self.timer.current_state.value,
            font=state_font,
            bg=PomodoroTimer.COLORS[State.FOCUS],
            fg="white"
        )
        self.state_label.pack(pady=(20, 10))
        
        # Energy drink display
        drink_font = font.Font(family="Courier", size=16, weight="bold")
        self.drink_label = tk.Label(
            self.main_frame,
            text=self.timer.get_energy_drink_display(),
            font=drink_font,
            bg=PomodoroTimer.COLORS[State.FOCUS],
            fg="white",
            justify=tk.LEFT
        )
        self.drink_label.pack(pady=20)
        
        # Cycle indicator (focus session tracker)
        self.cycle_frame = tk.Frame(self.main_frame, bg=PomodoroTimer.COLORS[State.FOCUS])
        self.cycle_frame.pack(pady=10)
        
        self.cycle_indicators = []
        for i in range(4):
            indicator = tk.Canvas(
                self.cycle_frame,
                width=30,
                height=30,
                bg=PomodoroTimer.COLORS[State.FOCUS],
                highlightthickness=0
            )
            indicator.pack(side=tk.LEFT, padx=5)
            # Draw circle
            circle = indicator.create_oval(5, 5, 25, 25, outline="white", width=2)
            self.cycle_indicators.append((indicator, circle))
        
        # Control buttons
        button_frame = tk.Frame(self.main_frame, bg=PomodoroTimer.COLORS[State.FOCUS])
        button_frame.pack(pady=20)
        
        button_font = font.Font(family="Helvetica", size=12, weight="bold")
        
        self.start_button = tk.Button(
            button_frame,
            text="Start",
            font=button_font,
            bg="white",
            fg="black",
            width=8,
            height=2,
            command=self.start_timer
        )
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.pause_button = tk.Button(
            button_frame,
            text="Pause",
            font=button_font,
            bg="white",
            fg="black",
            width=8,
            height=2,
            command=self.pause_timer,
            state=tk.DISABLED
        )
        self.pause_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = tk.Button(
            button_frame,
            text="Stop",
            font=button_font,
            bg="white",
            fg="black",
            width=8,
            height=2,
            command=self.stop_timer,
            state=tk.DISABLED
        )
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        self.reset_button = tk.Button(
            button_frame,
            text="Reset/Skip",
            font=button_font,
            bg="white",
            fg="black",
            width=8,
            height=2,
            command=self.reset_timer
        )
        self.reset_button.pack(side=tk.LEFT, padx=5)
    
    def update_display(self):
        """Update all display elements to reflect current state"""
        # Update colors
        bg_color = PomodoroTimer.COLORS[self.timer.current_state]
        self.main_frame.config(bg=bg_color)
        self.state_label.config(bg=bg_color, text=self.timer.current_state.value)
        self.drink_label.config(bg=bg_color, text=self.timer.get_energy_drink_display())
        self.cycle_frame.config(bg=bg_color)
        
        # Update cycle indicators
        for i, (indicator, circle) in enumerate(self.cycle_indicators):
            indicator.config(bg=bg_color)
            if i < self.timer.focus_count:
                # Filled circle for completed focus sessions
                indicator.itemconfig(circle, fill="white", outline="white")
            else:
                # Empty circle for remaining sessions
                indicator.itemconfig(circle, fill="", outline="white")
    
    def start_timer(self):
        """Start the countdown timer"""
        if not self.timer.is_running:
            self.timer.is_running = True
            self.start_button.config(state=tk.DISABLED)
            self.pause_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.NORMAL)
            self.countdown()
    
    def pause_timer(self):
        """Pause the countdown timer"""
        self.timer.is_running = False
        self.start_button.config(state=tk.NORMAL)
        self.pause_button.config(state=tk.DISABLED)
        if self.timer.timer_id:
            self.root.after_cancel(self.timer.timer_id)
    
    def stop_timer(self):
        """Stop the timer and reset to current state duration"""
        # Stop the timer
        self.timer.is_running = False
        if self.timer.timer_id:
            self.root.after_cancel(self.timer.timer_id)
        
        # Reset time to current state's full duration
        self.timer.time_remaining = self.timer.DURATIONS[self.timer.current_state]
        
        # Update UI
        self.start_button.config(state=tk.NORMAL)
        self.pause_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.DISABLED)
        self.update_display()
    
    def reset_timer(self):
        """Reset/Skip to next focus session"""
        # Stop the timer
        self.timer.is_running = False
        if self.timer.timer_id:
            self.root.after_cancel(self.timer.timer_id)
        
        # Reset to focus state and advance cycle
        self.timer.reset_to_focus()
        
        # Update UI
        self.start_button.config(state=tk.NORMAL)
        self.pause_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.DISABLED)
        self.update_display()
    
    def countdown(self):
        """Main countdown loop"""
        if self.timer.is_running:
            timer_complete = self.timer.tick()
            self.update_display()
            
            if timer_complete:
                # Play alert sound
                self.play_alert()
                
                # Transition to next state
                self.timer.transition_to_next_state()
                self.update_display()
                
                # Continue running automatically
                self.timer.timer_id = self.root.after(1000, self.countdown)
            else:
                # Schedule next tick
                self.timer.timer_id = self.root.after(1000, self.countdown)
    
    def play_alert(self):
        """Play an audible alert sound"""
        def play_sound():
            # Play Windows default beep (frequency, duration in ms)
            winsound.Beep(1000, 500)  # 1000 Hz for 500ms
        
        # Play sound in separate thread to avoid blocking
        Thread(target=play_sound, daemon=True).start()


def main():
    """Main entry point for the application"""
    root = tk.Tk()
    app = PomodoroGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
