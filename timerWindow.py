import tkinter as tk


class TimerApp:
    """
    A simple timer display using Tkinter. Tracks elapsed time in seconds,
    converting to MM:SS format, and updates every second when running.
    """

    def __init__(self, root):
        # Reference to the parent Tk or Toplevel window for the timer
        self.root = root
        self.root.title("Game Timer")

        # Internal counter of elapsed seconds
        self.seconds = 0
        # Flag indicating whether the timer is actively counting
        self.timer_running = False

        # Label widget that displays the time in "MM:SS" format
        self.timer_label = tk.Label(
            root,
            text="00:00",
            font=("Helvetica", 48)
        )
        self.timer_label.pack(pady=20)

        # Immediately update the timer label (shows "00:00" initially)
        self.update_timer()

    def start_timer(self):
        """
        Begin counting time if the timer is not already running.
        Sets the flag and triggers update_timer() to start the loop.
        """
        if not self.timer_running:
            self.timer_running = True
            self.update_timer()

    def stop_timer(self):
        """
        Pause the timer by clearing the running flag.
        The next scheduled update_timer call will see this flag is False
        and will not increment further.
        """
        self.timer_running = False

    def update_timer(self):
        """
        If the timer is running, increment the seconds counter by one,
        compute minutes/seconds, format as MM:SS, and update the label.
        Then schedule another call to update_timer() after 1000ms (1 second).
        If the timer is not running, simply ensure the current display remains.
        """
        if self.timer_running:
            # Increment the internal seconds counter
            self.seconds += 1

            # Convert total seconds into minutes and seconds
            minutes = self.seconds // 60
            seconds = self.seconds % 60
            # Format as two-digit MM:SS
            time_str = f"{minutes:02}:{seconds:02}"
            # Update the label to show the new time
            self.timer_label.config(text=time_str)

            # Schedule this method to be called again after 1 second
            self.root.after(1000, self.update_timer)
        else:
            # If timer is not running, still schedule update to keep display synced
            self.root.after(1000, self.update_timer)
