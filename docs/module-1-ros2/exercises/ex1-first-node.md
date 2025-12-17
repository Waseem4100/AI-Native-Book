---
title: "Exercise 1: Create Your First ROS 2 Node"
description: Build a ROS 2 node that publishes personalized messages
sidebar_position: 1
tags: [exercise, ros2, node, publisher, beginner]
---

# Exercise 1: Create Your First ROS 2 Node

**Difficulty**: Beginner (Guided)
**Time**: 30 minutes
**Prerequisites**: Chapter 2 (Nodes & Topics)

## Learning Objectives

By completing this exercise, you will:

1. Create a ROS 2 node from scratch
2. Implement a publisher that sends custom messages
3. Use a timer for periodic publishing
4. Visualize your node and topic using CLI tools

## Exercise Description

Create a ROS 2 node called `personal_greeter` that:
- Publishes your name and a counter to the `/greeting` topic every second
- Uses the `std_msgs/String` message type
- Logs each published message
- Runs until you press Ctrl+C

**Example output**:
```
[INFO] [personal_greeter]: Publishing: "Hello from Alice! Count: 0"
[INFO] [personal_greeter]: Publishing: "Hello from Alice! Count: 1"
[INFO] [personal_greeter]: Publishing: "Hello from Alice! Count: 2"
...
```

## Step-by-Step Instructions

### Step 1: Set Up Your Workspace

Create a directory for your ROS 2 exercises:

```bash
# Create workspace
mkdir -p ~/ros2_exercises/module1
cd ~/ros2_exercises/module1

# Source ROS 2 environment
source /opt/ros/humble/setup.bash
```

### Step 2: Create the Node File

Create a new Python file:

```bash
touch personal_greeter.py
chmod +x personal_greeter.py
```

Open `personal_greeter.py` in your text editor.

### Step 3: Write the Node Code

Follow this structure to implement your node:

```python
#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class PersonalGreeter(Node):
    """
    A ROS 2 node that publishes personalized greeting messages.

    TODO: Implement this class following the pattern from Chapter 2.
    """
    def __init__(self):
        # TODO: Call parent constructor with node name 'personal_greeter'
        pass

        # TODO: Create a publisher
        # - Message type: String
        # - Topic: '/greeting'
        # - Queue size: 10

        # TODO: Create a timer that calls publish_greeting every 1.0 seconds

        # TODO: Initialize counter variable to 0

        # TODO: Log initialization message

    def publish_greeting(self):
        """
        Callback function called by the timer.

        TODO: Implement this method to:
        1. Create a String message
        2. Set the message data to: "Hello from YOUR_NAME! Count: X"
        3. Publish the message
        4. Log the published message
        5. Increment the counter
        """
        pass

def main(args=None):
    # TODO: Initialize rclpy

    # TODO: Create an instance of PersonalGreeter

    # TODO: Keep the node running with spin()

    # TODO: Shutdown when Ctrl+C is pressed

if __name__ == '__main__':
    main()
```

### Step 4: Run Your Node

```bash
python3 personal_greeter.py
```

**Expected behavior**:
- You should see log messages appearing every second
- Each message should have an incrementing counter
- Press Ctrl+C to stop

### Step 5: Verify with CLI Tools

Open a **second terminal** while your node is running:

```bash
# Source ROS 2 (required in every terminal)
source /opt/ros/humble/setup.bash

# List all running nodes (should show /personal_greeter)
ros2 node list

# List all topics (should show /greeting)
ros2 topic list

# View messages being published
ros2 topic echo /greeting

# Check publishing rate
ros2 topic hz /greeting
# Should show approximately 1.0 Hz

# Get topic info
ros2 topic info /greeting
```

## Success Criteria

Your solution is complete when:

- ✅ The node starts without errors
- ✅ Messages are published to `/greeting` every second
- ✅ Each message contains your name and an incrementing counter
- ✅ `ros2 topic echo /greeting` shows the messages
- ✅ `ros2 topic hz /greeting` reports ~1.0 Hz
- ✅ Node shuts down cleanly with Ctrl+C

## Challenges (Optional)

Want to go further? Try these enhancements:

### Challenge 1: Multiple Topics

Modify your node to publish to two topics:
- `/greeting` - Your name and count (as before)
- `/timestamp` - Current time (use `time.time()`)

### Challenge 2: Configurable Rate

Add a parameter to change the publishing rate:
- Use `self.declare_parameter()` to create a `rate` parameter (default: 1.0)
- Use `self.get_parameter()` to read the value
- Use this value in `create_timer()`

**Hint**: See [ROS 2 parameter tutorial](https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Using-Parameters-In-A-Class-Python.html)

### Challenge 3: Subscriber Counter

Add a subscriber that listens to your own `/greeting` topic and counts how many messages have been received (verify your publisher is working).

## Common Issues and Solutions

**Issue**: `ModuleNotFoundError: No module named 'rclpy'`
- **Solution**: Make sure you've sourced ROS 2: `source /opt/ros/humble/setup.bash`

**Issue**: Node runs but no messages appear
- **Solution**: Check that you're calling `self.publisher_.publish(msg)` inside `publish_greeting()`

**Issue**: `ros2 topic echo` shows nothing
- **Solution**: Ensure both terminals have sourced ROS 2 environment

**Issue**: Timer doesn't fire
- **Solution**: Verify you're calling `rclpy.spin(node)` in `main()` - without this, callbacks never execute

## Verification Checklist

Before submitting, verify:

- [ ] File is executable (`chmod +x personal_greeter.py`)
- [ ] Shebang line present (`#!/usr/bin/env python3`)
- [ ] All imports are correct
- [ ] Node name is 'personal_greeter'
- [ ] Topic name is '/greeting'
- [ ] Message type is `std_msgs/String`
- [ ] Publishing rate is 1 Hz (every 1.0 seconds)
- [ ] Counter increments correctly
- [ ] Code includes docstrings and comments
- [ ] Node shuts down cleanly with Ctrl+C

## Solution

A complete solution is available in [`solutions/module-1/ex1-first-node.py`](../../../solutions/module-1/ex1-first-node.py).

**Try to complete the exercise on your own first!** Refer to:
- Chapter 2, Section "Creating a Publisher" for publisher examples
- Chapter 2, Section "Creating Your First ROS 2 Node" for node structure

## What You Learned

In this exercise, you:

✅ Created a ROS 2 node using the `Node` class
✅ Implemented a publisher using `create_publisher()`
✅ Used a timer with `create_timer()` for periodic execution
✅ Published messages to a topic
✅ Verified node operation with CLI tools (`ros2 node list`, `ros2 topic echo`)

## Next Steps

Ready for more? Continue to:

**[Exercise 2: Publisher-Subscriber System](./ex2-publisher-subscriber)** - Build a complete pub/sub system for joint control →

---

**Need help?** Review [Chapter 2: Nodes & Topics](../ch2-nodes-topics) or ask in the [discussion forum](https://github.com/your-org/physical-ai-textbook/discussions).
