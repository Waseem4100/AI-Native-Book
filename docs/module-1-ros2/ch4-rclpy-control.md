---
title: Python Control for Humanoid Joints
description: Master rclpy for controlling humanoid joints with position and velocity commands
sidebar_position: 4
tags: [ros2, rclpy, joint-control, position-control, velocity-control, pid]
---

# Chapter 4: Python Control for Humanoid Joints

## Learning Objectives

By the end of this chapter, you will be able to:

1. **Explain** the difference between position control and velocity control
2. **Implement** position control for humanoid joints using rclpy
3. **Implement** velocity control for smooth joint movements
4. **Create** a basic PID controller for accurate joint control
5. **Build** a multi-joint controller for coordinated humanoid motion

## Position Control vs Velocity Control

Humanoid robots have dozens of joints (ankles, knees, hips, spine, shoulders, elbows, wrists, neck). Each joint needs control commands. There are two fundamental approaches:

### Position Control

**Position control** commands specify the **target angle** for a joint.

```python
# Position control example
shoulder_joint.set_position(1.57)  # Move to 90 degrees (1.57 radians)
```

**How it works**:
1. You specify the desired position (angle)
2. The motor controller moves the joint to that position
3. Built-in feedback keeps the joint at that position

**Pros**:
- ✅ Simple to use
- ✅ Joint stays at commanded position
- ✅ Good for static poses (e.g., "T-pose", "sitting")

**Cons**:
- ❌ Less control over speed and acceleration
- ❌ Can be jerky if target changes abruptly
- ❌ Harder to create smooth, natural motion

**Use cases**: Reaching fixed positions, calibration, testing individual joints

### Velocity Control

**Velocity control** commands specify the **speed** at which the joint should move.

```python
# Velocity control example
shoulder_joint.set_velocity(0.5)  # Rotate at 0.5 rad/s (~28 deg/s)
```

**How it works**:
1. You specify the desired velocity (speed)
2. The motor controller maintains that velocity
3. You must handle stopping at the target position

**Pros**:
- ✅ Smooth, natural-looking motion
- ✅ Control over speed and acceleration
- ✅ Easier to coordinate multiple joints
- ✅ Better for dynamic movements (walking, reaching)

**Cons**:
- ❌ More complex - you must track position and stop at target
- ❌ Requires feedback loop (PID controller)
- ❌ Joint won't hold position unless you command zero velocity

**Use cases**: Walking, smooth reaching, coordinated multi-joint motion

### Real-World Analogy

**Position control** is like telling someone: "Stand at the 5-meter mark"
- They walk there and stay put

**Velocity control** is like telling someone: "Walk forward at 2 m/s"
- You must tell them when to stop, or they'll walk forever!

## Position Control with rclpy

Let's implement a position controller for a humanoid shoulder joint:

```python title="position_controller.py" showLineNumbers
#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64

class PositionController(Node):
    """
    Position controller for a single humanoid joint.

    Publishes target positions to a joint command topic.
    In a real robot, this would interface with ros2_control.
    """
    def __init__(self):
        super().__init__('position_controller')

        # Publisher for joint position commands
        self.position_pub = self.create_publisher(
            Float64,
            '/humanoid/shoulder_pitch/position_command',
            10
        )

        # Current target position
        self.target_position = 0.0  # radians

        self.get_logger().info('Position controller initialized')

    def set_target_position(self, position_rad):
        """
        Command the joint to move to a target position.

        Args:
            position_rad: Target angle in radians
        """
        self.target_position = position_rad

        # Create and publish message
        msg = Float64()
        msg.data = position_rad

        self.position_pub.publish(msg)

        self.get_logger().info(
            f'Commanded position: {position_rad:.3f} rad '
            f'({position_rad * 57.3:.1f}°)'
        )

    def move_through_positions(self):
        """Demonstrate position control with a sequence of poses."""
        positions = [
            (0.0, "Neutral"),
            (1.57, "Forward (90°)"),
            (0.785, "Mid-point (45°)"),
            (-0.785, "Backward (-45°)"),
            (0.0, "Return to neutral")
        ]

        for position, description in positions:
            self.get_logger().info(f'Moving to: {description}')
            self.set_target_position(position)

            # Wait for movement to complete (in real robot, check joint_states)
            rclpy.spin_once(self, timeout_sec=2.0)

def main(args=None):
    rclpy.init(args=args)
    controller = PositionController()

    # Execute position sequence
    controller.move_through_positions()

    controller.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

**Run it**:

```bash
python3 position_controller.py
```

**Expected Output**:
```
[INFO] [position_controller]: Position controller initialized
[INFO] [position_controller]: Moving to: Neutral
[INFO] [position_controller]: Commanded position: 0.000 rad (0.0°)
[INFO] [position_controller]: Moving to: Forward (90°)
[INFO] [position_controller]: Commanded position: 1.570 rad (90.0°)
...
```

## Velocity Control with rclpy

Now let's implement smooth velocity control:

```python title="velocity_controller.py" showLineNumbers
#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64
import math

class VelocityController(Node):
    """
    Velocity controller for smooth joint motion.

    Sends velocity commands and tracks position to stop at target.
    """
    def __init__(self):
        super().__init__('velocity_controller')

        # Publisher for joint velocity commands
        self.velocity_pub = self.create_publisher(
            Float64,
            '/humanoid/shoulder_pitch/velocity_command',
            10
        )

        # Subscriber for joint state feedback
        self.state_sub = self.create_subscription(
            Float64,
            '/humanoid/shoulder_pitch/state',
            self.state_callback,
            10
        )

        # Controller state
        self.current_position = 0.0  # radians
        self.target_position = 0.0
        self.max_velocity = 1.0  # rad/s

        # Timer for control loop (100 Hz)
        self.timer = self.create_timer(0.01, self.control_loop)

        self.get_logger().info('Velocity controller initialized')

    def state_callback(self, msg):
        """Update current joint position from feedback."""
        self.current_position = msg.data

    def set_target_position(self, position_rad):
        """
        Set target position for the controller to reach.

        Args:
            position_rad: Target angle in radians
        """
        self.target_position = position_rad
        self.get_logger().info(f'New target: {position_rad:.3f} rad')

    def control_loop(self):
        """
        Control loop running at 100 Hz.

        Computes velocity command based on position error.
        """
        # Compute position error
        error = self.target_position - self.current_position

        # Stop if close enough (1 degree tolerance)
        if abs(error) < 0.017:  # ~1 degree
            velocity = 0.0
        else:
            # Proportional control: velocity proportional to error
            # This is a simple P controller (no I or D terms)
            velocity = self.max_velocity * math.tanh(error * 2)
            # tanh provides smooth acceleration/deceleration

        # Publish velocity command
        msg = Float64()
        msg.data = velocity

        self.velocity_pub.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    controller = VelocityController()

    # Set a target position
    controller.set_target_position(1.57)  # 90 degrees

    rclpy.spin(controller)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

**Key difference**: Velocity control requires:
1. **Feedback** - Subscribe to joint state to know current position
2. **Control loop** - Continuously compute velocity based on error
3. **Stop condition** - Detect when target is reached and command zero velocity

## PID Control for Accurate Tracking

A **PID (Proportional-Integral-Derivative)** controller provides smooth, accurate control:

- **P (Proportional)**: Velocity proportional to error
- **I (Integral)**: Corrects for steady-state error
- **D (Derivative)**: Dampens oscillations

```python title="pid_controller.py" showLineNumbers
#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64
import time

class PIDController(Node):
    """
    PID controller for precise joint control.

    Implements proportional, integral, and derivative terms
    for smooth, accurate joint motion.
    """
    def __init__(self):
        super().__init__('pid_controller')

        # Publishers and subscribers
        self.velocity_pub = self.create_publisher(
            Float64, '/humanoid/shoulder_pitch/velocity_command', 10)

        self.state_sub = self.create_subscription(
            Float64, '/humanoid/shoulder_pitch/state',
            self.state_callback, 10)

        # PID gains (tune these for your robot)
        self.Kp = 2.0   # Proportional gain
        self.Ki = 0.1   # Integral gain
        self.Kd = 0.5   # Derivative gain

        # PID state
        self.current_position = 0.0
        self.target_position = 0.0
        self.error_integral = 0.0
        self.previous_error = 0.0
        self.previous_time = time.time()

        # Limits
        self.max_velocity = 2.0  # rad/s
        self.integral_limit = 10.0  # Prevent integral windup

        # Control loop at 100 Hz
        self.timer = self.create_timer(0.01, self.control_loop)

        self.get_logger().info('PID controller initialized')
        self.get_logger().info(f'Gains: Kp={self.Kp}, Ki={self.Ki}, Kd={self.Kd}')

    def state_callback(self, msg):
        """Update current joint position."""
        self.current_position = msg.data

    def set_target_position(self, position_rad):
        """
        Set new target position and reset integral term.

        Args:
            position_rad: Target angle in radians
        """
        self.target_position = position_rad
        self.error_integral = 0.0  # Reset integral on new target
        self.get_logger().info(f'New target: {position_rad:.3f} rad')

    def control_loop(self):
        """
        PID control loop.

        Computes velocity command using P, I, and D terms.
        """
        current_time = time.time()
        dt = current_time - self.previous_time
        self.previous_time = current_time

        # Position error
        error = self.target_position - self.current_position

        # Proportional term
        P = self.Kp * error

        # Integral term (with anti-windup)
        self.error_integral += error * dt
        self.error_integral = max(-self.integral_limit,
                                   min(self.integral_limit, self.error_integral))
        I = self.Ki * self.error_integral

        # Derivative term
        error_derivative = (error - self.previous_error) / dt if dt > 0 else 0.0
        D = self.Kd * error_derivative

        # Compute velocity command
        velocity = P + I + D

        # Apply velocity limits
        velocity = max(-self.max_velocity, min(self.max_velocity, velocity))

        # Publish command
        msg = Float64()
        msg.data = velocity
        self.velocity_pub.publish(msg)

        # Log status every 50 iterations (2 Hz)
        if int(current_time * 100) % 50 == 0:
            self.get_logger().info(
                f'Error: {error:.3f} rad, P={P:.2f}, I={I:.2f}, D={D:.2f}, '
                f'Vel: {velocity:.2f} rad/s'
            )

        # Update previous error
        self.previous_error = error

def main(args=None):
    rclpy.init(args=args)
    controller = PIDController()

    # Command a target position
    controller.set_target_position(1.57)  # 90 degrees

    try:
        rclpy.spin(controller)
    except KeyboardInterrupt:
        pass

    controller.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

**PID Tuning Tips**:
- Start with `Kp=2.0, Ki=0.0, Kd=0.0` (P-only)
- Increase `Kp` until oscillations appear
- Add `Kd` to dampen oscillations
- Add small `Ki` to eliminate steady-state error

## Multi-Joint Coordinated Control

Real humanoid motion requires coordinating multiple joints. Let's control both shoulder and elbow:

```python title="multi_joint_controller.py" showLineNumbers
#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64
from sensor_msgs.msg import JointState

class MultiJointController(Node):
    """
    Coordinates multiple joints for humanoid arm motion.

    Manages shoulder and elbow joints simultaneously.
    """
    def __init__(self):
        super().__init__('multi_joint_controller')

        # Publishers for each joint
        self.publishers = {
            'shoulder_pitch': self.create_publisher(
                Float64, '/humanoid/shoulder_pitch/position_command', 10),
            'elbow_pitch': self.create_publisher(
                Float64, '/humanoid/elbow_pitch/position_command', 10)
        }

        # Subscriber for joint states
        self.state_sub = self.create_subscription(
            JointState, '/joint_states', self.joint_state_callback, 10)

        # Current joint positions
        self.current_positions = {
            'shoulder_pitch': 0.0,
            'elbow_pitch': 0.0
        }

        self.get_logger().info('Multi-joint controller initialized')

    def joint_state_callback(self, msg):
        """Update current positions from joint_states topic."""
        for i, name in enumerate(msg.name):
            if name in self.current_positions:
                self.current_positions[name] = msg.position[i]

    def set_joint_position(self, joint_name, position):
        """
        Command a single joint to a target position.

        Args:
            joint_name: Name of the joint
            position: Target angle in radians
        """
        if joint_name not in self.publishers:
            self.get_logger().error(f'Unknown joint: {joint_name}')
            return

        msg = Float64()
        msg.data = position
        self.publishers[joint_name].publish(msg)

        self.get_logger().info(
            f'{joint_name}: {position:.3f} rad ({position * 57.3:.1f}°)'
        )

    def execute_motion_sequence(self):
        """
        Execute a coordinated motion sequence.

        Demonstrates reaching motion with shoulder and elbow.
        """
        motions = [
            {
                'name': 'Rest position',
                'shoulder_pitch': 0.0,
                'elbow_pitch': 0.0
            },
            {
                'name': 'Reach forward',
                'shoulder_pitch': 1.57,   # 90° forward
                'elbow_pitch': 0.0        # Straight
            },
            {
                'name': 'Bend elbow',
                'shoulder_pitch': 1.57,   # Keep at 90°
                'elbow_pitch': 1.57       # 90° bend
            },
            {
                'name': 'Reach up',
                'shoulder_pitch': 3.14,   # 180° (overhead)
                'elbow_pitch': 0.0        # Straight
            },
            {
                'name': 'Return to rest',
                'shoulder_pitch': 0.0,
                'elbow_pitch': 0.0
            }
        ]

        for motion in motions:
            self.get_logger().info(f'\n=== {motion["name"]} ===')
            self.set_joint_position('shoulder_pitch', motion['shoulder_pitch'])
            self.set_joint_position('elbow_pitch', motion['elbow_pitch'])

            # Wait for motion to complete
            rclpy.spin_once(self, timeout_sec=3.0)

def main(args=None):
    rclpy.init(args=args)
    controller = MultiJointController()

    # Execute coordinated motion
    controller.execute_motion_sequence()

    controller.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

**Output**:
```
[INFO] [multi_joint_controller]: Multi-joint controller initialized

=== Rest position ===
[INFO] [multi_joint_controller]: shoulder_pitch: 0.000 rad (0.0°)
[INFO] [multi_joint_controller]: elbow_pitch: 0.000 rad (0.0°)

=== Reach forward ===
[INFO] [multi_joint_controller]: shoulder_pitch: 1.570 rad (90.0°)
[INFO] [multi_joint_controller]: elbow_pitch: 0.000 rad (0.0°)
...
```

## Best Practices for Joint Control

### 1. Always Check Joint Limits

```python
def safe_set_position(self, position):
    """Set position with limit checking."""
    MIN_POS = -2.0  # radians
    MAX_POS = 2.0

    if position < MIN_POS or position > MAX_POS:
        self.get_logger().warn(
            f'Position {position:.2f} exceeds limits [{MIN_POS}, {MAX_POS}]'
        )
        position = max(MIN_POS, min(MAX_POS, position))

    self.set_target_position(position)
```

### 2. Limit Velocity for Safety

```python
def apply_velocity_limit(self, velocity, max_vel=1.0):
    """Clamp velocity to safe range."""
    return max(-max_vel, min(max_vel, velocity))
```

### 3. Use Joint States for Feedback

```python
# Subscribe to joint_states for current positions
self.state_sub = self.create_subscription(
    JointState, '/joint_states', self.joint_state_callback, 10)
```

### 4. Implement Emergency Stop

```python
def emergency_stop(self):
    """Stop all joints immediately."""
    for joint_name in self.publishers:
        msg = Float64()
        msg.data = 0.0  # Zero velocity
        self.publishers[joint_name].publish(msg)

    self.get_logger().warn('EMERGENCY STOP')
```

## Hands-On Exercises

Ready to practice? Complete these exercises:

1. **[Exercise 2: Publisher-Subscriber System](./exercises/ex2-publisher-subscriber)** (1 hour)
   - Implement velocity control for knee joint

2. **[Exercise 3: Build Humanoid URDF Model](./exercises/ex3-urdf-humanoid)** (2 hours)
   - Add PID controllers for all joints

## Comprehension Questions

**Question 10**: When would you use position control instead of velocity control?

<details>
<summary>Click to reveal answer</summary>

**Answer**: Use **position control** when:
- You need the joint to hold a specific position (e.g., static poses like "T-pose")
- Simplicity is more important than smooth motion
- You're testing or calibrating individual joints
- The motion doesn't need to be natural-looking (e.g., industrial robot)

Use **velocity control** when:
- You need smooth, natural motion (walking, reaching)
- You're coordinating multiple joints
- You want control over speed and acceleration
- The robot is performing dynamic tasks

In practice, many humanoid robots use velocity control during motion and switch to position control when holding poses.

</details>

---

**Question 11**: What does each term (P, I, D) in a PID controller do?

<details>
<summary>Click to reveal answer</summary>

**Answer**:
- **P (Proportional)**: Provides force proportional to current error. Larger error → faster response. Without I and D, causes oscillation.

- **I (Integral)**: Corrects accumulated error over time. Eliminates steady-state error (e.g., joint drifting away from target due to gravity). Can cause overshoot if too large.

- **D (Derivative)**: Resists change in error (dampens oscillations). Provides "braking" as joint approaches target. Makes system more stable.

**Tuning**: Start with P only, increase until oscillations appear. Add D to dampen. Add small I to eliminate steady-state error.

</details>

---

**Question 12**: Why do we need to subscribe to `/joint_states` in velocity control?

<details>
<summary>Click to reveal answer</summary>

**Answer**: In velocity control, you command a **speed**, not a position. Without feedback, you don't know:
- Where the joint currently is
- When to stop (you'll overshoot the target)
- If the joint is moving correctly

The `/joint_states` topic provides:
- Current position of each joint
- Current velocity
- (Optional) Current effort/torque

With this feedback, your controller can:
1. Compute position error (target - current)
2. Decide velocity based on error
3. Stop when error is small enough

This closed-loop feedback is essential for accurate velocity control.

</details>

---

## Next Steps

You've mastered joint control with rclpy! Next, you'll learn how to describe your robot's physical structure using **URDF** (Unified Robot Description Format).

**Next Chapter**: [URDF Modeling](./ch5-urdf-modeling) →

---

**Chapter Summary**: Humanoid joint control uses **position control** (simple, holds position) or **velocity control** (smooth, natural motion). Velocity control requires feedback from `/joint_states` and a control loop. PID controllers provide smooth, accurate tracking by combining proportional, integral, and derivative terms. Multi-joint controllers coordinate multiple joints for complex behaviors like reaching and walking. Always implement joint limits, velocity limits, and emergency stops for safety.
