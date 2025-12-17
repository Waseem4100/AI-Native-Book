---
title: Complete Humanoid Simulation
description: Build a complete humanoid simulation combining URDF, physics, sensors, and control
sidebar_position: 5
tags: [gazebo, complete-simulation, ros2-control, integration]
---

# Chapter 5: Complete Humanoid Simulation

## Learning Objectives

By the end of this chapter, you will be able to:

1. **Integrate** URDF, physics, sensors, and controllers into one simulation
2. **Configure** ros2_control for joint position and velocity control
3. **Launch** complete humanoid simulation with RViz visualization
4. **Test** robot behaviors in simulated environments
5. **Debug** common simulation issues

## Complete Humanoid URDF

Let's combine everything from previous chapters into a complete humanoid:

```xml title="complete_humanoid.urdf" showLineNumbers
<?xml version="1.0"?>
<robot name="complete_humanoid">

  <!-- ===== BODY STRUCTURE ===== -->

  <!-- Torso -->
  <link name="base_link">
    <visual>
      <geometry>
        <box size="0.3 0.2 0.5"/>
      </geometry>
      <material name="blue">
        <color rgba="0.2 0.2 0.8 1"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <box size="0.3 0.2 0.5"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="20.0"/>
      <inertia ixx="0.482" ixy="0" ixz="0"
               iyy="0.567" iyz="0" izz="0.217"/>
    </inertial>
  </link>

  <!-- Left Shoulder -->
  <joint name="left_shoulder_pitch" type="revolute">
    <parent link="base_link"/>
    <child link="left_upper_arm"/>
    <origin xyz="0 0.15 0.2" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="-3.14" upper="3.14" effort="100" velocity="2.0"/>
    <dynamics damping="0.7"/>
  </joint>

  <link name="left_upper_arm">
    <visual>
      <origin xyz="0 0 -0.15" rpy="0 0 0"/>
      <geometry>
        <cylinder radius="0.04" length="0.3"/>
      </geometry>
      <material name="skin">
        <color rgba="0.9 0.7 0.5 1"/>
      </material>
    </visual>
    <collision>
      <origin xyz="0 0 -0.15" rpy="0 0 0"/>
      <geometry>
        <cylinder radius="0.04" length="0.3"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="2.0"/>
      <inertia ixx="0.02" ixy="0" ixz="0"
               iyy="0.02" iyz="0" izz="0.005"/>
    </inertial>
  </link>

  <!-- Left Elbow -->
  <joint name="left_elbow_pitch" type="revolute">
    <parent link="left_upper_arm"/>
    <child link="left_forearm"/>
    <origin xyz="0 0 -0.3" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="0" upper="2.5" effort="50" velocity="2.0"/>
    <dynamics damping="0.5"/>
  </joint>

  <link name="left_forearm">
    <visual>
      <origin xyz="0 0 -0.125" rpy="0 0 0"/>
      <geometry>
        <cylinder radius="0.03" length="0.25"/>
      </geometry>
      <material name="skin">
        <color rgba="0.9 0.7 0.5 1"/>
      </material>
    </visual>
    <collision>
      <origin xyz="0 0 -0.125" rpy="0 0 0"/>
      <geometry>
        <cylinder radius="0.03" length="0.25"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="1.0"/>
      <inertia ixx="0.01" ixy="0" ixz="0"
               iyy="0.01" iyz="0" izz="0.002"/>
    </inertial>
  </link>

  <!-- Right arm (symmetric) -->
  <joint name="right_shoulder_pitch" type="revolute">
    <parent link="base_link"/>
    <child link="right_upper_arm"/>
    <origin xyz="0 -0.15 0.2" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="-3.14" upper="3.14" effort="100" velocity="2.0"/>
    <dynamics damping="0.7"/>
  </joint>

  <link name="right_upper_arm">
    <!-- Mirror of left_upper_arm -->
    <visual>
      <origin xyz="0 0 -0.15" rpy="0 0 0"/>
      <geometry>
        <cylinder radius="0.04" length="0.3"/>
      </geometry>
      <material name="skin">
        <color rgba="0.9 0.7 0.5 1"/>
      </material>
    </visual>
    <collision>
      <origin xyz="0 0 -0.15" rpy="0 0 0"/>
      <geometry>
        <cylinder radius="0.04" length="0.3"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="2.0"/>
      <inertia ixx="0.02" ixy="0" ixz="0"
               iyy="0.02" iyz="0" izz="0.005"/>
    </inertial>
  </link>

  <joint name="right_elbow_pitch" type="revolute">
    <parent link="right_upper_arm"/>
    <child link="right_forearm"/>
    <origin xyz="0 0 -0.3" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="0" upper="2.5" effort="50" velocity="2.0"/>
    <dynamics damping="0.5"/>
  </joint>

  <link name="right_forearm">
    <visual>
      <origin xyz="0 0 -0.125" rpy="0 0 0"/>
      <geometry>
        <cylinder radius="0.03" length="0.25"/>
      </geometry>
      <material name="skin">
        <color rgba="0.9 0.7 0.5 1"/>
      </material>
    </visual>
    <collision>
      <origin xyz="0 0 -0.125" rpy="0 0 0"/>
      <geometry>
        <cylinder radius="0.03" length="0.25"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="1.0"/>
      <inertia ixx="0.01" ixy="0" ixz="0"
               iyy="0.01" iyz="0" izz="0.002"/>
    </inertial>
  </link>

  <!-- ===== SENSORS ===== -->

  <!-- Depth Camera -->
  <link name="camera_link">
    <visual>
      <geometry>
        <box size="0.02 0.05 0.02"/>
      </geometry>
    </visual>
    <inertial>
      <mass value="0.05"/>
      <inertia ixx="0.0001" ixy="0" ixz="0"
               iyy="0.0001" iyz="0" izz="0.0001"/>
    </inertial>
  </link>

  <joint name="camera_joint" type="fixed">
    <parent link="base_link"/>
    <child link="camera_link"/>
    <origin xyz="0.15 0 0.3" rpy="0 0 0"/>
  </joint>

  <link name="camera_optical_frame"/>
  <joint name="camera_optical_joint" type="fixed">
    <parent link="camera_link"/>
    <child link="camera_optical_frame"/>
    <origin xyz="0 0 0" rpy="-1.5708 0 -1.5708"/>
  </joint>

  <!-- IMU -->
  <link name="imu_link">
    <inertial>
      <mass value="0.01"/>
      <inertia ixx="0.00001" ixy="0" ixz="0"
               iyy="0.00001" iyz="0" izz="0.00001"/>
    </inertial>
  </link>

  <joint name="imu_joint" type="fixed">
    <parent link="base_link"/>
    <child link="imu_link"/>
    <origin xyz="0 0 0" rpy="0 0 0"/>
  </joint>

  <!-- ===== GAZEBO CONFIGURATION ===== -->

  <!-- Gazebo materials -->
  <gazebo reference="base_link">
    <material>Gazebo/Blue</material>
  </gazebo>

  <gazebo reference="left_upper_arm">
    <material>Gazebo/SkinTan</material>
  </gazebo>

  <gazebo reference="right_upper_arm">
    <material>Gazebo/SkinTan</material>
  </gazebo>

  <!-- Depth camera plugin -->
  <gazebo reference="camera_link">
    <sensor name="depth_camera" type="depth">
      <update_rate>30</update_rate>
      <camera>
        <horizontal_fov>1.047</horizontal_fov>
        <image>
          <width>640</width>
          <height>480</height>
        </image>
        <clip>
          <near>0.3</near>
          <far>10.0</far>
        </clip>
      </camera>
      <plugin name="depth_camera_controller" filename="libgazebo_ros_camera.so">
        <frame_name>camera_optical_frame</frame_name>
      </plugin>
    </sensor>
  </gazebo>

  <!-- IMU plugin -->
  <gazebo reference="imu_link">
    <sensor name="imu_sensor" type="imu">
      <always_on>true</always_on>
      <update_rate>100</update_rate>
      <plugin name="imu_plugin" filename="libgazebo_ros_imu_sensor.so">
        <frame_name>imu_link</frame_name>
      </plugin>
    </sensor>
  </gazebo>

  <!-- ros2_control -->
  <gazebo>
    <plugin name="gazebo_ros2_control" filename="libgazebo_ros2_control.so">
      <parameters>$(find my_robot)/config/ros2_controllers.yaml</parameters>
    </plugin>
  </gazebo>

  <!-- Transmissions for each joint -->
  <transmission name="left_shoulder_trans">
    <type>transmission_interface/SimpleTransmission</type>
    <joint name="left_shoulder_pitch">
      <hardwareInterface>hardware_interface/EffortJointInterface</hardwareInterface>
    </joint>
    <actuator name="left_shoulder_motor">
      <mechanicalReduction>1</mechanicalReduction>
    </actuator>
  </transmission>

  <transmission name="left_elbow_trans">
    <type>transmission_interface/SimpleTransmission</type>
    <joint name="left_elbow_pitch">
      <hardwareInterface>hardware_interface/EffortJointInterface</hardwareInterface>
    </joint>
    <actuator name="left_elbow_motor">
      <mechanicalReduction>1</mechanicalReduction>
    </actuator>
  </transmission>

  <!-- Right arm transmissions (similar) -->

</robot>
```

## ros2_control Configuration

### Controller Configuration File

```yaml title="config/ros2_controllers.yaml" showLineNumbers
controller_manager:
  ros__parameters:
    update_rate: 100  # Hz

    # Joint state broadcaster
    joint_state_broadcaster:
      type: joint_state_broadcaster/JointStateBroadcaster

    # Position controller for arms
    arm_position_controller:
      type: position_controllers/JointGroupPositionController

# Joint State Broadcaster Configuration
joint_state_broadcaster:
  ros__parameters:
    joints:
      - left_shoulder_pitch
      - left_elbow_pitch
      - right_shoulder_pitch
      - right_elbow_pitch

# Arm Position Controller Configuration
arm_position_controller:
  ros__parameters:
    joints:
      - left_shoulder_pitch
      - left_elbow_pitch
      - right_shoulder_pitch
      - right_elbow_pitch

    interface_name: effort

    command_interfaces:
      - position

    state_interfaces:
      - position
      - velocity
```

### Complete Launch File

```python title="complete_simulation.launch.py" showLineNumbers
#!/usr/bin/env python3

import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, ExecuteProcess, RegisterEventHandler
from launch.event_handlers import OnProcessExit
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():

    # Paths
    pkg_share = FindPackageShare('my_robot').find('my_robot')
    urdf_file = os.path.join(pkg_share, 'urdf', 'complete_humanoid.urdf')
    world_file = os.path.join(pkg_share, 'worlds', 'indoor_environment.world')
    rviz_config = os.path.join(pkg_share, 'config', 'view.rviz')

    # Read URDF
    with open(urdf_file, 'r') as f:
        robot_desc = f.read()

    # 1. Launch Gazebo
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            FindPackageShare('gazebo_ros'),
            '/launch/gazebo.launch.py'
        ]),
        launch_arguments={'world': world_file}.items()
    )

    # 2. Spawn robot in Gazebo
    spawn_robot = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-entity', 'humanoid',
            '-topic', 'robot_description',
            '-x', '0',
            '-y', '0',
            '-z', '1.0',
        ],
        output='screen'
    )

    # 3. Robot state publisher
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': robot_desc,
            'use_sim_time': True
        }]
    )

    # 4. Joint state publisher (for manual control)
    joint_state_publisher_gui = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        output='screen',
        parameters=[{'use_sim_time': True}]
    )

    # 5. RViz
    rviz = Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d', rviz_config],
        parameters=[{'use_sim_time': True}],
        output='screen'
    )

    # 6. Load controllers
    load_joint_state_broadcaster = ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '--set-state', 'active',
             'joint_state_broadcaster'],
        output='screen'
    )

    load_arm_controller = ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '--set-state', 'active',
             'arm_position_controller'],
        output='screen'
    )

    # Load controllers after robot spawns
    load_controllers = RegisterEventHandler(
        event_handler=OnProcessExit(
            target_action=spawn_robot,
            on_exit=[load_joint_state_broadcaster, load_arm_controller],
        )
    )

    return LaunchDescription([
        gazebo,
        robot_state_publisher,
        spawn_robot,
        load_controllers,
        joint_state_publisher_gui,
        rviz,
    ])
```

**Launch everything**:

```bash
ros2 launch my_robot complete_simulation.launch.py
```

**What starts**:
1. ✅ Gazebo with custom world
2. ✅ Humanoid robot spawned at (0, 0, 1)
3. ✅ ros2_control controllers loaded
4. ✅ Joint state publisher GUI (sliders to move joints)
5. ✅ RViz visualization

## Controlling the Simulated Robot

### Method 1: Joint State Publisher GUI

Move sliders in the GUI window → Joints move in Gazebo

### Method 2: Command Line

```bash
# Command joint directly
ros2 topic pub /arm_position_controller/commands std_msgs/msg/Float64MultiArray \
  "{data: [1.57, 0.0, -1.57, 0.0]}"
# Sets: left_shoulder=90°, left_elbow=0°, right_shoulder=-90°, right_elbow=0°
```

### Method 3: Python Controller (from Module 1)

```python title="test_simulation.py" showLineNumbers
#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray
import math
import time

class SimulationTester(Node):
    """
    Test the complete humanoid simulation.

    Commands: Wave motion (both arms)
    """
    def __init__(self):
        super().__init__('simulation_tester')

        self.pub = self.create_publisher(
            Float64MultiArray,
            '/arm_position_controller/commands',
            10
        )

        self.timer = self.create_timer(0.1, self.control_loop)
        self.time_elapsed = 0.0

    def control_loop(self):
        """Send sinusoidal joint commands (wave motion)."""
        t = self.time_elapsed

        msg = Float64MultiArray()
        msg.data = [
            math.sin(t) * 1.5,      # left_shoulder (oscillate)
            math.sin(t * 2) * 0.5,  # left_elbow
            -math.sin(t) * 1.5,     # right_shoulder (opposite)
            math.sin(t * 2) * 0.5,  # right_elbow
        ]

        self.pub.publish(msg)
        self.time_elapsed += 0.1

def main(args=None):
    rclpy.init(args=args)
    node = SimulationTester()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

**Run**:

```bash
python3 test_simulation.py
```

Your humanoid should wave its arms in Gazebo!

## Creating Test Environments

### Simple Indoor Environment

```xml title="worlds/indoor_environment.world" showLineNumbers
<?xml version="1.0"?>
<sdf version="1.6">
  <world name="indoor_environment">

    <!-- Physics -->
    <physics type="ode">
      <max_step_size>0.001</max_step_size>
      <real_time_factor>1.0</real_time_factor>
    </physics>

    <!-- Ground and lighting -->
    <include>
      <uri>model://ground_plane</uri>
    </include>
    <include>
      <uri>model://sun</uri>
    </include>

    <!-- Walls (create a room) -->
    <model name="wall_north">
      <static>true</static>
      <pose>5 0 1.5 0 0 0</pose>
      <link name="link">
        <collision name="collision">
          <geometry>
            <box>
              <size>0.2 10 3</size>
            </box>
          </geometry>
        </collision>
        <visual name="visual">
          <geometry>
            <box>
              <size>0.2 10 3</size>
            </box>
          </geometry>
          <material>
            <ambient>0.7 0.7 0.7 1</ambient>
          </material>
        </visual>
      </link>
    </model>

    <!-- Table -->
    <include>
      <uri>model://cafe_table</uri>
      <pose>2 0 0 0 0 0</pose>
    </include>

    <!-- Chair -->
    <include>
      <uri>model://cafe_chair</uri>
      <pose>2 -0.5 0 0 0 1.57</pose>
    </include>

  </world>
</sdf>
```

## Debugging Simulation Issues

### Check TF Tree

Verify all sensor frames are connected:

```bash
# View TF tree
ros2 run tf2_tools view_frames

# Generates frames.pdf showing all coordinate frames
# Verify: base_link → camera_link → camera_optical_frame
```

### Monitor Topics

```bash
# List all topics
ros2 topic list

# Should see:
# /joint_states
# /humanoid/camera/depth/points
# /humanoid/imu/data
# /tf, /tf_static

# Check topic rates
ros2 topic hz /joint_states
# Should show ~100 Hz

ros2 topic hz /humanoid/camera/depth/points
# Should show ~30 Hz
```

### Gazebo Verbose Mode

For debugging physics or plugin issues:

```bash
gazebo --verbose world.world
```

## Common Integration Issues

### Issue: Controllers Don't Load

**Symptom**: `ros2 control list_controllers` shows no controllers

**Solution**:
1. Verify `libgazebo_ros2_control.so` plugin in URDF
2. Check controller YAML file path is correct
3. Ensure transmissions are defined for all joints

```bash
# Manually load controller
ros2 control load_controller joint_state_broadcaster
ros2 control set_controller_state joint_state_broadcaster active
```

### Issue: Sensor Data Not Publishing

**Symptom**: `ros2 topic list` doesn't show sensor topics

**Solution**:
1. Check sensor plugin filename (e.g., `libgazebo_ros_camera.so`)
2. Verify `<always_on>true</always_on>` for sensor
3. Check Gazebo terminal for plugin load errors

### Issue: Robot Sinks Into Ground

**Symptom**: Robot slowly penetrates floor

**Solution**:
```xml
<!-- Increase contact stiffness -->
<gazebo reference="base_link">
  <kp>1000000.0</kp>
  <kd>10.0</kd>
</gazebo>

<!-- OR reduce physics step size -->
<physics type="ode">
  <max_step_size>0.0005</max_step_size>  <!-- Halve from 0.001 -->
</physics>
```

## Hands-On Exercises

Ready to build complete simulations? Complete these exercises:

1. **[Exercise 1: Build a Gazebo World](./exercises/ex1-gazebo-world)** (1 hour)
   - Create indoor environment with furniture and obstacles

2. **[Exercise 2: Add Sensors to Humanoid](./exercises/ex2-sensor-setup)** (1 hour)
   - Attach LiDAR, depth camera, and IMU to your URDF from Module 1

3. **[Exercise 3: Unity HRI Scene](./exercises/ex3-unity-scene)** (2 hours)
   - Build photorealistic Unity scene with ROS 2 integration

## Comprehension Questions

**Question 13**: Why do we need `use_sim_time: True` in launch files?

<details>
<summary>Click to reveal answer</summary>

**Answer**: **Simulation time** is different from **wall-clock time**.

**Without `use_sim_time`**:
- Nodes use your computer's clock (wall time)
- If simulation runs slower than real-time (RTF=0.5), timing is wrong
- TF transforms have mismatched timestamps
- Sensor fusion fails (IMU at t=1.0, camera at t=2.0 real time but both should be t=1.0 sim time)

**With `use_sim_time: True`**:
- Nodes subscribe to `/clock` topic (published by Gazebo)
- All timestamps use simulation time
- Pausing Gazebo pauses all node timers
- Consistent timing across all nodes

**Rule**: Always set `use_sim_time: True` when running with Gazebo/simulators.

</details>

---

**Question 14**: What's the difference between `<collision>` geometry and sensor rays?

<details>
<summary>Click to reveal answer</summary>

**Answer**:

- **`<collision>` geometry**: Used by **physics engine** for contact forces. Determines when objects physically touch and how they bounce/push each other. Affects motion.

- **Sensor rays** (LiDAR/depth camera): Used by **sensor plugins** for range measurements. Cast rays through the scene and report distances. Does **not** affect physics - purely for observation.

**Example**: A glass wall might have:
- Collision: Box (robot can't pass through)
- Sensor: Transparent (LiDAR passes through glass)
- Visual: Transparent textured mesh

This separation allows realistic sensor behavior (cameras see through glass, LiDAR doesn't always detect it).

</details>

---

**Question 15**: Why add noise to simulated sensors?

<details>
<summary>Click to reveal answer</summary>

**Answer**: **Sim-to-real transfer** - algorithms trained on perfect data fail on noisy real sensors.

**Real sensor issues**:
- LiDAR: ±3cm accuracy, misses black/shiny surfaces
- Cameras: Motion blur, auto-exposure, lens distortion
- IMU: Bias drift (0.1°/s), temperature sensitivity
- Depth cameras: Errors increase with distance (±5mm @ 1m, ±50mm @ 5m)

**With noise in simulation**:
- Algorithms must handle outliers (RANSAC, filtering)
- Localization uses multiple sensor fusion (not just LiDAR)
- Robust to real-world imperfections

**Without noise**:
- Perfect LiDAR → perfect SLAM in sim
- Real LiDAR → SLAM fails catastrophically

**Best practice**: Match noise parameters to sensor datasheets (stddev, bias, drift rates).

</details>

---

## Module 2 Summary

**Congratulations!** You've completed Module 2: Physics Simulation. You now know:

✅ How to launch Gazebo with custom worlds
✅ How physics engines simulate forces and collisions
✅ How to integrate URDF models with Gazebo tags
✅ How to use Unity for photorealistic HRI visualization
✅ How to attach and configure LiDAR, cameras, and IMUs
✅ How to build complete simulation environments

**You're ready for Module 3**, where you'll use NVIDIA Isaac Sim for photorealistic rendering and AI-powered perception!

## Next Steps

Complete all exercises before moving on:
1. **[Exercise 1: Build a Gazebo World](./exercises/ex1-gazebo-world)**
2. **[Exercise 2: Add Sensors to Humanoid](./exercises/ex2-sensor-setup)**
3. **[Exercise 3: Unity HRI Scene](./exercises/ex3-unity-scene)**

**Next Module**: Module 3: NVIDIA Isaac for AI-Robot Brain (Coming Soon) →

---

**Chapter Summary**: Complete humanoid simulation integrates URDF structure, Gazebo physics, sensor plugins, and ros2_control into unified launch files. Controllers are configured via YAML files specifying joint interfaces, update rates, and control modes. All nodes must use `use_sim_time: True` for synchronized timestamps from Gazebo's `/clock` topic. Test environments combine worlds (SDF), robots (URDF+Gazebo tags), and sensors (plugins) for realistic scenarios. RViz visualizes sensor data alongside Gazebo physics. Common issues include controller loading failures, TF frame errors, and contact penetration - all debuggable via ROS 2 CLI tools and verbose Gazebo output.
