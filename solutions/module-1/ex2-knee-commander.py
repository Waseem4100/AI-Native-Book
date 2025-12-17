#!/usr/bin/env python3
"""
Exercise 2 Solution (Part 2): Knee Commander Node

This is a complete solution for the knee commander (publisher) part of
Exercise 2: Publisher-Subscriber System. This node:
- Publishes knee joint commands in a sequence
- Sends one command every 2 seconds
- Cycles through a predefined motion sequence

Author: Physical AI Textbook
License: MIT
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64


class KneeCommander(Node):
    """
    Publishes knee joint commands in a sequence.

    Demonstrates sending a series of target positions to
    simulate knee bending motion.

    This demonstrates:
    - Creating a publisher
    - Using a timer for periodic publishing
    - Publishing Float64 messages
    - Sequencing through a list of commands
    """

    def __init__(self):
        """Initialize the knee commander node."""
        super().__init__('knee_commander')

        # Create publisher
        self.command_pub = self.create_publisher(
            Float64,
            '/humanoid/knee/command',
            10  # Queue size
        )

        # Define motion sequence (angle in radians, description)
        self.motion_sequence = [
            (0.0, "Straight leg (0°)"),
            (0.785, "Slight bend (45°)"),
            (1.571, "Right angle (90°)"),
            (0.785, "Return to 45°"),
            (0.0, "Straight leg (0°)")
        ]

        # Track current step in sequence
        self.current_step = 0

        # Create timer (2.0 seconds interval)
        self.timer = self.create_timer(2.0, self.publish_next_command)

        self.get_logger().info('Knee commander started')
        self.get_logger().info(f'Motion sequence has {len(self.motion_sequence)} steps')
        self.get_logger().info('Publishing every 2 seconds')

    def publish_next_command(self):
        """
        Publish the next command in the sequence.

        Sends the command, logs it, and advances to the next step
        (wrapping around to the beginning when reaching the end).
        """
        # Get current step from motion_sequence
        target_position, description = self.motion_sequence[self.current_step]

        # Create Float64 message
        msg = Float64()
        msg.data = target_position

        # Publish message
        self.command_pub.publish(msg)

        # Log the command (radians and degrees)
        position_deg = target_position * 57.2958
        self.get_logger().info(
            f'Step {self.current_step + 1}/{len(self.motion_sequence)}: '
            f'{description} → {target_position:.3f} rad ({position_deg:.1f}°)'
        )

        # Increment current_step (wrap around to 0 at end)
        self.current_step = (self.current_step + 1) % len(self.motion_sequence)

        # Log when sequence repeats
        if self.current_step == 0:
            self.get_logger().info('--- Sequence complete, restarting ---')


def main(args=None):
    """Main function for the knee commander node."""
    rclpy.init(args=args)
    node = KneeCommander()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Shutting down knee commander...')

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()


"""
=== GRADING RUBRIC ===

Full Credit (100 points):
- [20 pts] Node initializes with correct name 'knee_commander'
- [20 pts] Publisher created with correct topic '/humanoid/knee/command'
- [20 pts] Timer created with 2.0 second interval
- [20 pts] Motion sequence defined with 5 steps
- [15 pts] Sequence cycles correctly (wraps around)
- [5 pts] Logging shows clear information

Partial Credit:
- [-10 pts] Incorrect topic name
- [-15 pts] Incorrect timer interval
- [-10 pts] Sequence doesn't wrap around (stops after first cycle)
- [-5 pts] Missing or poor logging
- [-10 pts] Wrong message type

Testing Commands:
```bash
# Terminal 1: Run controller (must be running first)
python3 ex2-knee-controller.py

# Terminal 2: Run commander
python3 ex2-knee-commander.py

# Terminal 3: Monitor commands
ros2 topic echo /humanoid/knee/command
ros2 topic hz /humanoid/knee/command  # Should be ~0.5 Hz

# Check both nodes are running
ros2 node list  # Should show both knee_controller and knee_commander

# View topic info
ros2 topic info /humanoid/knee/command --verbose
# Should show:
#   Publisher count: 1
#   Subscriber count: 1
```

Expected Output:
```
[INFO] [knee_commander]: Knee commander started
[INFO] [knee_commander]: Motion sequence has 5 steps
[INFO] [knee_commander]: Publishing every 2 seconds
[INFO] [knee_commander]: Step 1/5: Straight leg (0°) → 0.000 rad (0.0°)
[INFO] [knee_commander]: Step 2/5: Slight bend (45°) → 0.785 rad (45.0°)
[INFO] [knee_commander]: Step 3/5: Right angle (90°) → 1.571 rad (90.0°)
[INFO] [knee_commander]: Step 4/5: Return to 45° → 0.785 rad (45.0°)
[INFO] [knee_commander]: Step 5/5: Straight leg (0°) → 0.000 rad (0.0°)
[INFO] [knee_commander]: --- Sequence complete, restarting ---
[INFO] [knee_commander]: Step 1/5: Straight leg (0°) → 0.000 rad (0.0°)
...
```

Key Implementation Details:
1. Motion sequence is a list of tuples (angle, description)
2. current_step tracks position in sequence
3. Modulo operator (%) wraps around: (4 + 1) % 5 = 0
4. Each command published immediately when timer fires
5. No delay or waiting for confirmation (open-loop control)

Common Mistakes:
1. Not using modulo → Index out of bounds after first cycle
2. Publishing inside __init__() → Only publishes once
3. Using while loop instead of timer → Blocking behavior
4. Hardcoding sequence length → Breaks if sequence changes

Extensions:
1. Add parameter for custom sequence:
   ```python
   self.declare_parameter('sequence', [0.0, 1.57, 0.0])
   sequence = self.get_parameter('sequence').value
   ```

2. Add pause between cycles:
   ```python
   if self.current_step == 0:
       self.get_logger().info('Pausing for 5 seconds...')
       # Would need to modify timer logic or add state machine
   ```

3. Read sequence from YAML file:
   ```python
   import yaml
   with open('knee_sequence.yaml') as f:
       self.motion_sequence = yaml.safe_load(f)['sequence']
   ```
"""
