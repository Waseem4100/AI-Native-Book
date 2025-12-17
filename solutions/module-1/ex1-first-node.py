#!/usr/bin/env python3
"""
Exercise 1 Solution: Personal Greeter Node

This is a complete solution for Exercise 1: Create Your First ROS 2 Node.
The node publishes personalized greeting messages with an incrementing counter
to the /greeting topic every second.

Author: Physical AI Textbook
License: MIT
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class PersonalGreeter(Node):
    """
    A ROS 2 node that publishes personalized greeting messages.

    This node demonstrates:
    - Creating a publisher
    - Using a timer for periodic execution
    - Publishing String messages
    - Logging with get_logger()
    """

    def __init__(self):
        """Initialize the PersonalGreeter node."""
        # Call parent constructor with node name 'personal_greeter'
        super().__init__('personal_greeter')

        # Create a publisher
        # - Message type: String
        # - Topic: '/greeting'
        # - Queue size: 10 (buffer up to 10 messages if subscriber is slow)
        self.publisher_ = self.create_publisher(
            String,
            '/greeting',
            10
        )

        # Create a timer that calls publish_greeting every 1.0 seconds
        self.timer = self.create_timer(1.0, self.publish_greeting)

        # Initialize counter variable to 0
        self.count = 0

        # Log initialization message
        self.get_logger().info('Personal Greeter node initialized')
        self.get_logger().info('Publishing to /greeting topic every 1 second')

    def publish_greeting(self):
        """
        Callback function called by the timer every second.

        Creates a greeting message with the person's name and count,
        publishes it, logs it, and increments the counter.
        """
        # Create a String message
        msg = String()

        # Set the message data
        # Replace "Alice" with your own name!
        msg.data = f'Hello from Alice! Count: {self.count}'

        # Publish the message
        self.publisher_.publish(msg)

        # Log the published message
        self.get_logger().info(f'Publishing: "{msg.data}"')

        # Increment the counter for next time
        self.count += 1


def main(args=None):
    """
    Main function for the node.

    Initializes rclpy, creates the node, spins (keeps it running),
    and shuts down cleanly.
    """
    # Initialize rclpy (ROS 2 Python client library)
    rclpy.init(args=args)

    # Create an instance of PersonalGreeter
    node = PersonalGreeter()

    try:
        # Keep the node running (responding to callbacks)
        # Without this, the node would exit immediately
        rclpy.spin(node)
    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        node.get_logger().info('Keyboard interrupt, shutting down...')

    # Clean shutdown
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()


"""
=== GRADING RUBRIC ===

Full Credit (100 points):
- [20 pts] Node initializes with correct name 'personal_greeter'
- [20 pts] Publisher created with correct topic '/greeting' and type String
- [20 pts] Timer created with 1.0 second interval
- [20 pts] Messages published with name and incrementing count
- [10 pts] Logging implemented correctly
- [10 pts] Code is clean, commented, and follows Python style

Partial Credit:
- [-5 pts] Missing or incorrect node name
- [-10 pts] Missing or incorrect topic name
- [-10 pts] Missing or incorrect timer interval
- [-15 pts] Counter doesn't increment
- [-5 pts] Missing docstrings or comments
- [-10 pts] Node doesn't shut down cleanly

Common Mistakes:
1. Forgetting to call super().__init__() → Node won't initialize
2. Not calling rclpy.spin() → Callbacks never execute
3. Using print() instead of self.get_logger() → Not ROS 2 compliant
4. Creating timer without callback → Timer never fires
5. Forgetting to increment counter → Same count every time

Testing Commands:
```bash
# Terminal 1: Run the node
python3 ex1-first-node.py

# Terminal 2: Verify operation
ros2 node list  # Should show /personal_greeter
ros2 topic list  # Should show /greeting
ros2 topic echo /greeting  # Should show messages
ros2 topic hz /greeting  # Should show ~1.0 Hz
ros2 topic info /greeting --verbose  # Show detailed info
```

Expected Output:
```
[INFO] [personal_greeter]: Personal Greeter node initialized
[INFO] [personal_greeter]: Publishing to /greeting topic every 1 second
[INFO] [personal_greeter]: Publishing: "Hello from Alice! Count: 0"
[INFO] [personal_greeter]: Publishing: "Hello from Alice! Count: 1"
[INFO] [personal_greeter]: Publishing: "Hello from Alice! Count: 2"
...
```

Extensions for Advanced Students:
1. Add command-line argument for custom name:
   ```python
   import sys
   name = sys.argv[1] if len(sys.argv) > 1 else "Alice"
   ```

2. Add ROS 2 parameter for name:
   ```python
   self.declare_parameter('name', 'Alice')
   name = self.get_parameter('name').value
   ```

3. Add timestamp to message:
   ```python
   import datetime
   timestamp = datetime.datetime.now().strftime('%H:%M:%S')
   msg.data = f'[{timestamp}] Hello from Alice! Count: {self.count}'
   ```

4. Add QoS profile for reliable delivery:
   ```python
   from rclpy.qos import QoSProfile, ReliabilityPolicy
   qos = QoSProfile(depth=10, reliability=ReliabilityPolicy.RELIABLE)
   self.publisher_ = self.create_publisher(String, '/greeting', qos)
   ```
"""
