---
title: "Exercise 2: Publisher-Subscriber System"
description: Build a complete joint control system with publisher and subscriber
sidebar_position: 2
tags: [exercise, ros2, publisher, subscriber, joint-control, intermediate]
---

# Exercise 2: Publisher-Subscriber System

**Difficulty**: Intermediate
**Time**: 1 hour
**Prerequisites**: Chapter 2 (Nodes & Topics), Chapter 4 (Joint Control)

## Learning Objectives

By completing this exercise, you will:

1. Create a publisher node that sends joint commands
2. Create a subscriber node that receives and processes joint commands
3. Implement a complete pub/sub system for robot control
4. Test bidirectional communication between nodes

## Exercise Description

Build a joint control system for a humanoid knee joint with two nodes:

### Node 1: Knee Command Publisher (`knee_commander.py`)
- Publishes target angles to `/humanoid/knee/command` topic
- Uses `std_msgs/Float64` message type
- Sends a sequence of knee bend angles (0° → 45° → 90° → 45° → 0°)
- Publishes one command every 2 seconds
- Logs each command sent

### Node 2: Knee State Subscriber (`knee_controller.py`)
- Subscribes to `/humanoid/knee/command` topic
- Receives target angles and simulates knee movement
- Publishes current knee position to `/humanoid/knee/state` topic every 0.1 seconds
- Uses simple motion: moves toward target at fixed velocity
- Logs received commands and current position

**Expected System Behavior**:

```
Terminal 1 (Subscriber):
[INFO] [knee_controller]: Knee controller started
[INFO] [knee_controller]: Received command: 0.785 rad (45.0°)
[INFO] [knee_controller]: Current position: 0.100 rad
[INFO] [knee_controller]: Current position: 0.200 rad
...
[INFO] [knee_controller]: Target reached: 0.785 rad

Terminal 2 (Publisher):
[INFO] [knee_commander]: Commanding: 0.785 rad (45°)
[INFO] [knee_commander]: Commanding: 1.571 rad (90°)
...
```

## Step-by-Step Instructions

### Part 1: Create the Subscriber (Knee Controller)

Create `knee_controller.py`:

```python
#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64

class KneeController(Node):
    """
    Simulates a knee joint controller.

    Subscribes to command topic, simulates movement toward target,
    and publishes current state.
    """
    def __init__(self):
        super().__init__('knee_controller')

        # TODO: Create subscriber for command topic
        # - Topic: '/humanoid/knee/command'
        # - Message type: Float64
        # - Callback: self.command_callback
        # - Queue size: 10

        # TODO: Create publisher for state topic
        # - Topic: '/humanoid/knee/state'
        # - Message type: Float64
        # - Queue size: 10

        # Controller state
        self.current_position = 0.0  # radians
        self.target_position = 0.0   # radians
        self.velocity = 0.1          # rad/s (speed of movement)

        # TODO: Create timer for control loop (100 Hz = 0.01 seconds)
        # - Callback: self.control_loop

        self.get_logger().info('Knee controller started')

    def command_callback(self, msg):
        """
        Called when a command message arrives.

        TODO: Implement this method to:
        1. Extract target position from message
        2. Update self.target_position
        3. Log the received command in radians and degrees
        """
        pass

    def control_loop(self):
        """
        Control loop running at 100 Hz.

        TODO: Implement this method to:
        1. Compute error (target - current)
        2. If error is small (< 0.01 rad), set velocity to 0
        3. Otherwise, move toward target at self.velocity
           - If error is positive, increase position
           - If error is negative, decrease position
        4. Publish current position to state topic
        5. (Optional) Log position every 50 iterations
        """
        pass

def main(args=None):
    # TODO: Initialize rclpy
    # TODO: Create KneeController instance
    # TODO: Spin
    # TODO: Shutdown

if __name__ == '__main__':
    main()
```

### Part 2: Create the Publisher (Knee Commander)

Create `knee_commander.py`:

```python
#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64

class KneeCommander(Node):
    """
    Publishes knee joint commands in a sequence.

    Demonstrates sending a series of target positions to
    simulate knee bending motion.
    """
    def __init__(self):
        super().__init__('knee_commander')

        # TODO: Create publisher
        # - Topic: '/humanoid/knee/command'
        # - Message type: Float64
        # - Queue size: 10

        # Define motion sequence (angle in radians, description)
        self.motion_sequence = [
            (0.0, "Straight leg (0°)"),
            (0.785, "Slight bend (45°)"),
            (1.571, "Right angle (90°)"),
            (0.785, "Return to 45°"),
            (0.0, "Straight leg (0°)")
        ]

        self.current_step = 0

        # TODO: Create timer (2.0 seconds interval)
        # - Callback: self.publish_next_command

        self.get_logger().info('Knee commander started')

    def publish_next_command(self):
        """
        Publish the next command in the sequence.

        TODO: Implement this method to:
        1. Get current step from motion_sequence
        2. Create Float64 message
        3. Set message data to target angle
        4. Publish message
        5. Log the command (radians and degrees)
        6. Increment current_step (wrap around to 0 at end)
        """
        pass

def main(args=None):
    # TODO: Initialize rclpy
    # TODO: Create KneeCommander instance
    # TODO: Spin
    # TODO: Shutdown

if __name__ == '__main__':
    main()
```

### Part 3: Test the System

Make files executable:

```bash
chmod +x knee_controller.py
chmod +x knee_commander.py
```

**Terminal 1** - Start controller (subscriber):

```bash
source /opt/ros/humble/setup.bash
python3 knee_controller.py
```

**Terminal 2** - Start commander (publisher):

```bash
source /opt/ros/humble/setup.bash
python3 knee_commander.py
```

**Terminal 3** - Monitor with CLI tools:

```bash
source /opt/ros/humble/setup.bash

# List nodes (should show both knee_controller and knee_commander)
ros2 node list

# List topics
ros2 topic list

# Echo command topic
ros2 topic echo /humanoid/knee/command

# Echo state topic
ros2 topic echo /humanoid/knee/state

# Check rates
ros2 topic hz /humanoid/knee/command  # Should be ~0.5 Hz
ros2 topic hz /humanoid/knee/state    # Should be ~100 Hz
```

## Success Criteria

Your solution is complete when:

- ✅ Both nodes start without errors
- ✅ Commander publishes commands every 2 seconds
- ✅ Controller receives commands and logs them
- ✅ Controller publishes state at 100 Hz
- ✅ Controller simulates smooth movement toward target
- ✅ `ros2 topic echo` shows messages on both topics
- ✅ System runs continuously until Ctrl+C

## Challenges (Optional)

### Challenge 1: Add Service for Reset

Create a service `/reset_knee` that:
- Resets knee to 0° position
- Uses `std_srvs/Trigger` service type
- Returns success message

**Hint**: Review Chapter 3 (Services) for service implementation.

### Challenge 2: Add Velocity Control

Modify `knee_controller.py` to:
- Subscribe to `/humanoid/knee/velocity_command` (in addition to position)
- Support both position and velocity control modes
- Use a parameter to switch between modes

### Challenge 3: Add Action for Smooth Motion

Implement an action server in `knee_controller.py`:
- Action name: `/move_knee`
- Goal: target position and duration
- Feedback: current position and progress percentage
- Result: final position and time elapsed

**Hint**: Review Chapter 3 (Actions) for action implementation.

## Common Issues and Solutions

**Issue**: Subscriber doesn't receive messages
- **Solution**: Ensure both nodes are running and have sourced ROS 2 environment
- **Solution**: Check topic names match exactly (case-sensitive!)

**Issue**: Control loop doesn't run
- **Solution**: Verify you created the timer with `create_timer(0.01, self.control_loop)`

**Issue**: Position jumps instead of smooth movement
- **Solution**: In control loop, increment position by small amount (`self.velocity * dt`) instead of jumping directly to target

**Issue**: Commander publishes too fast
- **Solution**: Check timer interval is 2.0 seconds, not 0.2 or 2.0 milliseconds

## Verification Checklist

Before submitting, verify:

- [ ] Both files are executable
- [ ] Shebang lines present (`#!/usr/bin/env python3`)
- [ ] All imports correct
- [ ] Node names are 'knee_controller' and 'knee_commander'
- [ ] Topic names match: `/humanoid/knee/command` and `/humanoid/knee/state`
- [ ] Message type is `std_msgs/Float64` for all topics
- [ ] Commander publishes every 2 seconds
- [ ] Controller control loop runs at 100 Hz
- [ ] Controller simulates smooth motion (not instant jumps)
- [ ] Code includes docstrings and comments
- [ ] Nodes shut down cleanly with Ctrl+C

## Extension: Visualize in RViz (Optional)

Want to see your knee joint in action?

Create a simple URDF with a knee joint:

```xml title="knee_robot.urdf"
<?xml version="1.0"?>
<robot name="knee_robot">
  <link name="thigh">
    <visual>
      <geometry>
        <cylinder radius="0.05" length="0.4"/>
      </geometry>
      <material name="blue"><color rgba="0 0 1 1"/></material>
    </visual>
  </link>

  <joint name="knee" type="revolute">
    <parent link="thigh"/>
    <child link="shin"/>
    <origin xyz="0 0 -0.2" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="0" upper="2.5" effort="100" velocity="1.0"/>
  </joint>

  <link name="shin">
    <visual>
      <origin xyz="0 0 -0.2" rpy="0 0 0"/>
      <geometry>
        <cylinder radius="0.04" length="0.4"/>
      </geometry>
      <material name="green"><color rgba="0 1 0 1"/></material>
    </visual>
  </link>
</robot>
```

Launch RViz:

```bash
ros2 launch urdf_tutorial display.launch.py model:=knee_robot.urdf
```

Publish joint states from your controller to visualize movement!

## Solution

A complete solution is available in [`solutions/module-1/ex2-publisher-subscriber.py`](../../../solutions/module-1/ex2-publisher-subscriber.py).

**Try to complete the exercise on your own first!** Refer to:
- Chapter 2 for publisher/subscriber patterns
- Chapter 4 for joint control concepts

## What You Learned

In this exercise, you:

✅ Created a publisher node that sends commands
✅ Created a subscriber node that processes commands
✅ Implemented a control loop for simulated joint movement
✅ Published state feedback from controller
✅ Tested a complete pub/sub system with multiple topics
✅ Monitored system behavior with CLI tools

## Next Steps

Ready for the final exercise? Continue to:

**[Exercise 3: Build a Humanoid URDF Model](./ex3-urdf-humanoid)** - Create a complete humanoid robot →

---

**Need help?** Review [Chapter 2: Nodes & Topics](../ch2-nodes-topics) and [Chapter 4: Joint Control](../ch4-rclpy-control), or ask in the [discussion forum](https://github.com/your-org/physical-ai-textbook/discussions).
