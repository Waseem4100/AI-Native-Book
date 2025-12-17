#!/usr/bin/env python3
"""
Exercise 2 Solution (Part 1): Knee Controller Node

This is a complete solution for the knee controller (subscriber) part of
Exercise 2: Publisher-Subscriber System. This node:
- Subscribes to command topic
- Simulates smooth knee movement
- Publishes current state

Author: Physical AI Textbook
License: MIT
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64


class KneeController(Node):
    """
    Simulates a knee joint controller.

    Subscribes to command topic, simulates movement toward target,
    and publishes current state at 100 Hz.

    This demonstrates:
    - Creating a subscriber
    - Creating a publisher
    - Implementing a control loop
    - Simulating smooth joint movement
    """

    def __init__(self):
        """Initialize the knee controller node."""
        super().__init__('knee_controller')

        # Create subscriber for command topic
        self.command_sub = self.create_subscription(
            Float64,
            '/humanoid/knee/command',
            self.command_callback,
            10  # Queue size
        )

        # Create publisher for state topic
        self.state_pub = self.create_publisher(
            Float64,
            '/humanoid/knee/state',
            10  # Queue size
        )

        # Controller state
        self.current_position = 0.0  # radians
        self.target_position = 0.0   # radians
        self.velocity = 0.1          # rad/s (speed of movement)

        # Control loop timer (100 Hz = 0.01 seconds)
        self.timer = self.create_timer(0.01, self.control_loop)

        # Counter for periodic logging (log every 50 iterations = 0.5 seconds)
        self.loop_counter = 0

        self.get_logger().info('Knee controller started')
        self.get_logger().info(f'Movement velocity: {self.velocity} rad/s')

    def command_callback(self, msg):
        """
        Called when a command message arrives.

        Args:
            msg: Float64 message containing target position in radians
        """
        # Extract target position from message
        self.target_position = msg.data

        # Log the received command in radians and degrees
        position_deg = self.target_position * 57.2958  # Convert rad to deg
        self.get_logger().info(
            f'Received command: {self.target_position:.3f} rad '
            f'({position_deg:.1f}°)'
        )

    def control_loop(self):
        """
        Control loop running at 100 Hz.

        Simulates smooth movement toward target position and
        publishes current state.
        """
        # Compute position error
        error = self.target_position - self.current_position

        # Compute time step (0.01 seconds)
        dt = 0.01

        # If error is small (< 0.01 rad ≈ 0.6°), stop moving
        if abs(error) < 0.01:
            # Already at target, do nothing
            velocity_command = 0.0
        else:
            # Move toward target at constant velocity
            if error > 0:
                # Target is ahead, move forward
                velocity_command = self.velocity
            else:
                # Target is behind, move backward
                velocity_command = -self.velocity

            # Update position based on velocity
            # Don't overshoot the target
            delta = velocity_command * dt
            if abs(delta) > abs(error):
                # Would overshoot, just go to target
                self.current_position = self.target_position
            else:
                self.current_position += delta

        # Publish current position to state topic
        state_msg = Float64()
        state_msg.data = self.current_position
        self.state_pub.publish(state_msg)

        # Log position periodically (every 50 iterations = 0.5 seconds)
        self.loop_counter += 1
        if self.loop_counter >= 50:
            self.loop_counter = 0
            position_deg = self.current_position * 57.2958
            self.get_logger().info(
                f'Current position: {self.current_position:.3f} rad '
                f'({position_deg:.1f}°)'
            )

            # Check if we've reached the target
            if abs(error) < 0.01:
                self.get_logger().info('✓ Target reached')


def main(args=None):
    """Main function for the knee controller node."""
    rclpy.init(args=args)
    node = KneeController()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Shutting down knee controller...')

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()


"""
=== GRADING RUBRIC ===

Full Credit (100 points):
- [15 pts] Node initializes with correct name 'knee_controller'
- [15 pts] Subscriber created with correct topic and message type
- [15 pts] Publisher created for state topic
- [15 pts] Timer created with 0.01 second interval (100 Hz)
- [20 pts] Control loop implements smooth movement toward target
- [10 pts] Movement doesn't overshoot target
- [5 pts] State published at 100 Hz
- [5 pts] Logging implemented correctly

Partial Credit:
- [-10 pts] Incorrect topic names
- [-15 pts] Position jumps to target instead of smooth movement
- [-10 pts] State not published or incorrect rate
- [-5 pts] Missing or poor logging
- [-10 pts] Control loop logic errors

Testing Commands:
```bash
# Terminal 1: Run controller
python3 ex2-knee-controller.py

# Terminal 2: Run commander (after completing ex2-knee-commander.py)
python3 ex2-knee-commander.py

# Terminal 3: Monitor
ros2 topic echo /humanoid/knee/state
ros2 topic hz /humanoid/knee/state  # Should be ~100 Hz

# Manual testing without commander:
ros2 topic pub /humanoid/knee/command std_msgs/Float64 "{data: 1.57}" --once
```

Key Implementation Details:
1. Control loop runs at 100 Hz for smooth simulation
2. Velocity is constant (0.1 rad/s), not proportional to error
3. Position update: current += velocity * dt
4. Overshoot prevention: stop when within 0.01 rad of target
5. State published every iteration (100 Hz)
6. Logging throttled to every 0.5 seconds (every 50 iterations)

Common Mistakes:
1. Setting current_position = target_position directly → No smooth motion
2. Not checking for overshoot → Oscillation around target
3. Publishing state inside command_callback → Wrong rate
4. Using rclpy.spin_once() instead of timer → Blocking behavior
"""
