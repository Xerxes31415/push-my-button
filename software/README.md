# Push My Button Software

This is the code written for the Push My Button.  It's written in CircuitPython 9.x.  

## General design

This is a simple while loop that looks for changes in button state and keeps track of time.  When it sees a button press, it will enqueue random values for intensity and duration.  It will also flash the LED and start a cooldown timer.  The queue will
