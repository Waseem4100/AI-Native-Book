---
title: URDF Modeling
description: Build humanoid robot models using URDF and visualize them in RViz2
sidebar_position: 5
tags: [ros2, urdf, robot-modeling, rviz, kinematics, links, joints]
---

# Chapter 5: URDF Modeling

## Learning Objectives

By the end of this chapter, you will be able to:

1. **Explain** what URDF is and why robots need it
2. **Create** a URDF file describing a humanoid robot's structure
3. **Define** links, joints, and kinematic chains
4. **Visualize** your robot model in RViz2
5. **Build** a simple humanoid torso with arms

## What is URDF?

**URDF (Unified Robot Description Format)** is an XML format for describing a robot's physical structure. Think of it as a blueprint that tells ROS 2:

- **Links**: Rigid body parts (torso, thigh, shin, foot, hand, etc.)
- **Joints**: Connections between links (hip, knee, ankle, shoulder, elbow)
- **Geometry**: Shape of each part (box, cylinder, mesh)
- **Physical properties**: Mass, inertia, friction
- **Sensors and actuators**: Where cameras, LiDAR, motors are mounted

### Why Robots Need URDF

Without URDF, ROS 2 wouldn't know:
- How your robot is structured
- Where sensors are located relative to the body
- How joints connect and move
- How to compute forward/inverse kinematics
- How to visualize the robot

**URDF enables**:
- **Visualization** in RViz2 and Gazebo
- **Motion planning** (MoveIt2 uses URDF)
- **Sensor fusion** (transform sensor data to common frame)
- **Simulation** (Gazebo reads URDF for physics)
- **Control** (ros2_control uses URDF to configure controllers)

## URDF File Structure

A URDF file is XML with three main elements:

```xml
<robot name="my_humanoid">

  <!-- Links: Rigid body parts -->
  <link name="torso">
    <visual>...</visual>
    <collision>...</collision>
    <inertial>...</inertial>
  </link>

  <!-- Joints: Connections between links -->
  <joint name="shoulder" type="revolute">
    <parent link="torso"/>
    <child link="upper_arm"/>
    <axis xyz="0 1 0"/>
    <limit lower="-1.57" upper="1.57" effort="100" velocity="1.0"/>
  </joint>

  <link name="upper_arm">...</link>

</robot>
```

### Coordinate Frames

ROS 2 uses the **right-hand rule** for coordinate frames:

```
      Z (up)
      |
      |_____ Y (left)
     /
    X (forward)
```

- **X-axis**: Forward
- **Y-axis**: Left
- **Z-axis**: Up

All transforms (positions, orientations) follow this convention.

## Creating Your First URDF: A Simple Box Robot

Let's start with the simplest possible robot - a single box:

```xml title="simple_box_robot.urdf" showLineNumbers
<?xml version="1.0"?>
<robot name="simple_box_robot">

  <!-- Single link: a box representing the robot body -->
  <link name="base_link">

    <!-- Visual representation (what you see in RViz/Gazebo) -->
    <visual>
      <geometry>
        <box size="0.5 0.3 0.2"/>  <!-- width, depth, height in meters -->
      </geometry>
      <material name="blue">
        <color rgba="0 0 1 1"/>  <!-- R G B A (0-1 range) -->
      </material>
    </visual>

    <!-- Collision representation (for physics simulation) -->
    <collision>
      <geometry>
        <box size="0.5 0.3 0.2"/>
      </geometry>
    </collision>

    <!-- Inertial properties (for dynamics simulation) -->
    <inertial>
      <mass value="10.0"/>  <!-- kilograms -->
      <inertia ixx="0.1" ixy="0.0" ixz="0.0"
               iyy="0.1" iyz="0.0"
               izz="0.1"/>
    </inertial>

  </link>

</robot>
```

**Visualize it in RViz2**:

```bash
# Launch RViz with URDF
ros2 launch urdf_tutorial display.launch.py model:=simple_box_robot.urdf
```

You should see a blue box in RViz2!

## Adding a Joint: Robot Arm

Let's create a simple 2-link robot arm:

```xml title="robot_arm.urdf" showLineNumbers
<?xml version="1.0"?>
<robot name="robot_arm">

  <!-- Base link (fixed to the world) -->
  <link name="base_link">
    <visual>
      <geometry>
        <cylinder radius="0.1" length="0.05"/>
      </geometry>
      <material name="gray">
        <color rgba="0.5 0.5 0.5 1"/>
      </material>
    </visual>
    <inertial>
      <mass value="1.0"/>
      <inertia ixx="0.01" ixy="0" ixz="0" iyy="0.01" iyz="0" izz="0.01"/>
    </inertial>
  </link>

  <!-- Joint connecting base to upper arm -->
  <joint name="shoulder_joint" type="revolute">
    <parent link="base_link"/>
    <child link="upper_arm"/>

    <!-- Joint position relative to parent frame -->
    <origin xyz="0 0 0.025" rpy="0 0 0"/>
    <!-- xyz: x, y, z offset in meters -->
    <!-- rpy: roll, pitch, yaw in radians -->

    <!-- Joint axis (rotation around Y-axis) -->
    <axis xyz="0 1 0"/>

    <!-- Joint limits -->
    <limit lower="-1.57" upper="1.57" effort="100" velocity="1.0"/>
    <!-- lower/upper: angle limits in radians -->
    <!-- effort: max torque in Nm -->
    <!-- velocity: max angular velocity in rad/s -->
  </joint>

  <!-- Upper arm link -->
  <link name="upper_arm">
    <visual>
      <origin xyz="0 0 0.15" rpy="0 0 0"/>  <!-- Center of box -->
      <geometry>
        <box size="0.05 0.05 0.3"/>  <!-- Long in Z direction -->
      </geometry>
      <material name="red">
        <color rgba="1 0 0 1"/>
      </material>
    </visual>
    <inertial>
      <mass value="0.5"/>
      <inertia ixx="0.01" ixy="0" ixz="0" iyy="0.01" iyz="0" izz="0.001"/>
    </inertial>
  </link>

  <!-- Joint connecting upper arm to forearm -->
  <joint name="elbow_joint" type="revolute">
    <parent link="upper_arm"/>
    <child link="forearm"/>
    <origin xyz="0 0 0.3" rpy="0 0 0"/>  <!-- At end of upper arm -->
    <axis xyz="0 1 0"/>
    <limit lower="0" upper="2.5" effort="50" velocity="1.0"/>
  </joint>

  <!-- Forearm link -->
  <link name="forearm">
    <visual>
      <origin xyz="0 0 0.125" rpy="0 0 0"/>
      <geometry>
        <box size="0.04 0.04 0.25"/>
      </geometry>
      <material name="green">
        <color rgba="0 1 0 1"/>
      </material>
    </visual>
    <inertial>
      <mass value="0.3"/>
      <inertia ixx="0.005" ixy="0" ixz="0" iyy="0.005" iyz="0" izz="0.0005"/>
    </inertial>
  </link>

</robot>
```

**Visualize and control**:

```bash
# Launch with joint state publisher GUI
ros2 launch urdf_tutorial display.launch.py model:=robot_arm.urdf

# A GUI window will appear - move the sliders to control joints!
```

## Joint Types

URDF supports 6 joint types:

| Type | Motion | Use Case | Example |
|------|--------|----------|---------|
| **revolute** | Rotation (limited) | Most robot joints | Shoulder, elbow, knee |
| **continuous** | Rotation (unlimited) | Wheels, spinning sensors | Wheel axle |
| **prismatic** | Linear translation | Telescoping parts | Elevator, gripper |
| **fixed** | No motion | Rigidly attached | Camera mount |
| **floating** | 6-DOF (x,y,z,roll,pitch,yaw) | Free-floating objects | Quadrotor base |
| **planar** | 2D motion (x,y,yaw) | Rarely used | Mobile base (simplified) |

**Most common in humanoids**: `revolute` (all arm/leg joints), `fixed` (sensor mounts)

## Building a Humanoid Torso with Arms

Let's create a simple humanoid upper body:

```xml title="humanoid_upper_body.urdf" showLineNumbers
<?xml version="1.0"?>
<robot name="humanoid_upper_body">

  <!-- Torso -->
  <link name="torso">
    <visual>
      <geometry>
        <box size="0.3 0.2 0.5"/>  <!-- Rectangular torso -->
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
      <inertia ixx="1.0" ixy="0" ixz="0" iyy="1.0" iyz="0" izz="0.5"/>
    </inertial>
  </link>

  <!-- Left Shoulder Joint -->
  <joint name="left_shoulder_pitch" type="revolute">
    <parent link="torso"/>
    <child link="left_upper_arm"/>
    <origin xyz="0 0.15 0.2" rpy="0 0 0"/>  <!-- Top-left of torso -->
    <axis xyz="0 1 0"/>  <!-- Pitch (forward/backward) -->
    <limit lower="-3.14" upper="3.14" effort="100" velocity="2.0"/>
  </joint>

  <!-- Left Upper Arm -->
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
    <inertial>
      <mass value="2.0"/>
      <inertia ixx="0.02" ixy="0" ixz="0" iyy="0.02" iyz="0" izz="0.005"/>
    </inertial>
  </link>

  <!-- Left Elbow Joint -->
  <joint name="left_elbow_pitch" type="revolute">
    <parent link="left_upper_arm"/>
    <child link="left_forearm"/>
    <origin xyz="0 0 -0.3" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="0" upper="2.5" effort="50" velocity="2.0"/>
  </joint>

  <!-- Left Forearm -->
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
    <inertial>
      <mass value="1.0"/>
      <inertia ixx="0.01" ixy="0" ixz="0" iyy="0.01" iyz="0" izz="0.002"/>
    </inertial>
  </link>

  <!-- Right Shoulder Joint -->
  <joint name="right_shoulder_pitch" type="revolute">
    <parent link="torso"/>
    <child link="right_upper_arm"/>
    <origin xyz="0 -0.15 0.2" rpy="0 0 0"/>  <!-- Top-right of torso -->
    <axis xyz="0 1 0"/>
    <limit lower="-3.14" upper="3.14" effort="100" velocity="2.0"/>
  </joint>

  <!-- Right Upper Arm -->
  <link name="right_upper_arm">
    <visual>
      <origin xyz="0 0 -0.15" rpy="0 0 0"/>
      <geometry>
        <cylinder radius="0.04" length="0.3"/>
      </geometry>
      <material name="skin">
        <color rgba="0.9 0.7 0.5 1"/>
      </material>
    </visual>
    <inertial>
      <mass value="2.0"/>
      <inertia ixx="0.02" ixy="0" ixz="0" iyy="0.02" iyz="0" izz="0.005"/>
    </inertial>
  </link>

  <!-- Right Elbow Joint -->
  <joint name="right_elbow_pitch" type="revolute">
    <parent link="right_upper_arm"/>
    <child link="right_forearm"/>
    <origin xyz="0 0 -0.3" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="0" upper="2.5" effort="50" velocity="2.0"/>
  </joint>

  <!-- Right Forearm -->
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
    <inertial>
      <mass value="1.0"/>
      <inertia ixx="0.01" ixy="0" ixz="0" iyy="0.01" iyz="0" izz="0.002"/>
    </inertial>
  </link>

  <!-- Head (optional) -->
  <joint name="neck_pitch" type="revolute">
    <parent link="torso"/>
    <child link="head"/>
    <origin xyz="0 0 0.3" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="-0.785" upper="0.785" effort="20" velocity="1.0"/>
  </joint>

  <link name="head">
    <visual>
      <geometry>
        <sphere radius="0.12"/>
      </geometry>
      <material name="skin">
        <color rgba="0.9 0.7 0.5 1"/>
      </material>
    </visual>
    <inertial>
      <mass value="3.0"/>
      <inertia ixx="0.05" ixy="0" ixz="0" iyy="0.05" iyz="0" izz="0.05"/>
    </inertial>
  </link>

</robot>
```

**Visualize**:

```bash
ros2 launch urdf_tutorial display.launch.py model:=humanoid_upper_body.urdf
```

You should see a humanoid torso with two arms and a head! Use the GUI sliders to move the joints.

## Kinematic Chains

A **kinematic chain** is a sequence of links connected by joints.

**Example**: Right arm kinematic chain
```
torso → (right_shoulder_pitch) → right_upper_arm → (right_elbow_pitch) → right_forearm
```

**Why it matters**:
- **Forward kinematics**: Given joint angles, compute end-effector (hand) position
- **Inverse kinematics**: Given desired hand position, compute required joint angles
- **Path planning**: MoveIt2 uses kinematic chains to plan collision-free paths

### Checking Your Kinematic Tree

```bash
# Install urdf_tutorial if not already installed
sudo apt install ros-humble-urdf-tutorial

# View kinematic tree
urdf_to_graphiz humanoid_upper_body.urdf
# Creates a PDF showing all links and joints as a tree diagram

# Check URDF syntax
check_urdf humanoid_upper_body.urdf
# Should output: "robot name is: humanoid_upper_body"
# "Successfully parsed URDF"
```

## Using Meshes for Realistic Models

Instead of primitive shapes (box, cylinder, sphere), you can use 3D mesh files:

```xml
<visual>
  <geometry>
    <mesh filename="package://my_robot_description/meshes/head.stl" scale="1 1 1"/>
    <!-- Supports: .stl, .dae (COLLADA), .obj -->
  </geometry>
</visual>
```

**Where to get meshes**:
- CAD software (SolidWorks, Fusion 360) → Export as STL/DAE
- Blender (open-source 3D modeling)
- Download from robot manufacturer (e.g., Fetch, PR2, TurtleBot)

**Best practices**:
- Use **low-poly meshes** for real-time visualization
- Use **convex decomposition** for collision geometry (faster physics)
- Store meshes in `meshes/` directory within your ROS 2 package

## URDF Best Practices

### 1. Name Links and Joints Clearly

```xml
<!-- ❌ BAD -->
<link name="link1"/>
<joint name="j1" type="revolute"/>

<!-- ✅ GOOD -->
<link name="right_upper_arm"/>
<joint name="right_elbow_pitch" type="revolute"/>
```

### 2. Set Realistic Inertial Properties

```python
# For a cylinder (radius r, length l, mass m):
ixx = iyy = (1/12) * m * (3*r² + l²)
izz = (1/2) * m * r²

# For a box (width w, depth d, height h, mass m):
ixx = (1/12) * m * (d² + h²)
iyy = (1/12) * m * (w² + h²)
izz = (1/12) * m * (w² + d²)
```

Use physics calculators or CAD software to get accurate inertia tensors.

### 3. Match Visual and Collision Geometry

```xml
<!-- Visual can be detailed mesh -->
<visual>
  <geometry>
    <mesh filename="package://my_robot/meshes/arm_detailed.stl"/>
  </geometry>
</visual>

<!-- Collision should be simpler for performance -->
<collision>
  <geometry>
    <cylinder radius="0.05" length="0.3"/>
  </geometry>
</collision>
```

### 4. Use Xacro for Complex Robots

**Xacro** (XML Macros) reduces repetition:

```xml title="humanoid.urdf.xacro"
<?xml version="1.0"?>
<robot xmlns:xacro="http://www.ros.org/wiki/xacro" name="humanoid">

  <!-- Define a macro for an arm -->
  <xacro:macro name="arm" params="prefix parent">
    <joint name="${prefix}_shoulder_pitch" type="revolute">
      <parent link="${parent}"/>
      <child link="${prefix}_upper_arm"/>
      <origin xyz="0 ${0.15 if prefix == 'left' else -0.15} 0.2" rpy="0 0 0"/>
      <axis xyz="0 1 0"/>
      <limit lower="-3.14" upper="3.14" effort="100" velocity="2.0"/>
    </joint>

    <link name="${prefix}_upper_arm">
      <!-- ... link definition ... -->
    </link>

    <!-- Elbow joint and forearm... -->
  </xacro:macro>

  <!-- Use the macro for both arms -->
  <link name="torso">...</link>
  <xacro:arm prefix="left" parent="torso"/>
  <xacro:arm prefix="right" parent="torso"/>

</robot>
```

**Convert Xacro to URDF**:

```bash
xacro humanoid.urdf.xacro > humanoid.urdf
```

## Hands-On Exercise

Ready to build your own humanoid? Complete this exercise:

**[Exercise 3: Build a Humanoid URDF Model](./exercises/ex3-urdf-humanoid)** (2 hours)
- Create a full humanoid robot with legs, torso, arms, and head
- Visualize and control it in RViz2
- Export it for use in Gazebo (Module 2)

## Comprehension Questions

**Question 13**: What is the difference between `<visual>` and `<collision>` geometry in URDF?

<details>
<summary>Click to reveal answer</summary>

**Answer**:
- **`<visual>`**: What you **see** in RViz and Gazebo. Can be detailed meshes for realistic appearance. Doesn't affect physics.

- **`<collision>`**: What the **physics engine** uses for collision detection. Should be simpler (boxes, cylinders, convex hulls) for performance. Affects simulation speed.

**Best practice**: Use detailed meshes for visual, simple primitives for collision.

**Example**: A robot hand might have a detailed visual mesh but use a simple box for collision to make simulation faster.

</details>

---

**Question 14**: Why do we need to specify inertial properties (`<mass>`, `<inertia>`) in URDF?

<details>
<summary>Click to reveal answer</summary>

**Answer**: Inertial properties are required for **physics simulation** in Gazebo. They determine:
- How the robot responds to forces (gravity, contact, motor torques)
- How much torque is needed to move joints
- How the robot behaves during collisions

Without realistic inertia:
- Simulated robot may move unnaturally (too fast, jerky)
- Controllers tuned in simulation won't work on real robot
- Physics may be unstable (exploding joints, falling through floor)

**Best practice**: Get inertia from CAD software or calculate using formulas for primitive shapes.

</details>

---

**Question 15**: What is a kinematic chain, and why does MoveIt2 need it?

<details>
<summary>Click to reveal answer</summary>

**Answer**: A **kinematic chain** is a sequence of links connected by joints from a base to an end-effector (like a hand).

**Example**: Arm chain
```
torso → shoulder → upper_arm → elbow → forearm → wrist → hand
```

**Why MoveIt2 needs it**:
1. **Forward kinematics**: Given joint angles [θ1, θ2, θ3], compute hand position [x, y, z]
2. **Inverse kinematics**: Given desired hand position [x, y, z], compute required joint angles [θ1, θ2, θ3]
3. **Path planning**: Plan collision-free trajectories by moving along the kinematic chain

Without knowing the kinematic structure, MoveIt2 can't plan how to move the arm to reach a target.

</details>

---

## Module 1 Summary

**Congratulations!** You've completed Module 1: ROS 2 Foundations. You now know:

✅ What middleware is and why ROS 2 uses DDS
✅ How to create ROS 2 nodes with publishers and subscribers
✅ When to use topics, services, and actions
✅ How to control humanoid joints with position and velocity commands
✅ How to create URDF models and visualize them in RViz2

**You're ready for Module 2**, where you'll simulate your humanoid in Gazebo with realistic physics!

## Next Steps

**Next Module**: [Module 2: Simulation in Gazebo](../../module-2-gazebo-unity/index) →

Complete all exercises before moving on:
1. **[Exercise 1: Create Your First ROS 2 Node](./exercises/ex1-first-node)**
2. **[Exercise 2: Publisher-Subscriber System](./exercises/ex2-publisher-subscriber)**
3. **[Exercise 3: Build a Humanoid URDF Model](./exercises/ex3-urdf-humanoid)**

---

**Chapter Summary**: URDF (Unified Robot Description Format) describes robot structure using links (rigid bodies) and joints (connections). Links have visual geometry (what you see), collision geometry (for physics), and inertial properties (mass, inertia). Joints connect links and define motion type (revolute, prismatic, fixed, etc.). Kinematic chains enable forward/inverse kinematics for motion planning. RViz2 visualizes URDF models, and Gazebo uses them for physics simulation. URDF is fundamental to all ROS 2 robotics workflows.
