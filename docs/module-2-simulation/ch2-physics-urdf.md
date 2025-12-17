---
title: Physics & URDF in Gazebo
description: Integrate URDF models with Gazebo physics engines and configure realistic dynamics
sidebar_position: 2
tags: [gazebo, urdf, physics, ode, inertia]
---

# Chapter 2: Physics & URDF in Gazebo

## Learning Objectives

By the end of this chapter, you will be able to:

1. **Explain** how physics engines simulate forces, collisions, and motion
2. **Configure** ODE, Bullet, and Simbody physics engines
3. **Integrate** URDF models from Module 1 into Gazebo
4. **Add** Gazebo-specific tags to URDF for simulation
5. **Calculate** accurate inertial properties for realistic physics

## Physics Engines in Gazebo

### What is a Physics Engine?

A **physics engine** computes how objects move and interact based on:
- **Forces**: Gravity, motor torques, contact forces
- **Constraints**: Joints, fixed connections
- **Collisions**: Detect intersections and apply impulses

Every simulation step:
1. Detect collisions between objects
2. Compute forces (gravity, motors, contact)
3. Integrate equations of motion (F = ma)
4. Update positions and velocities

### Gazebo Supported Engines

| Engine | Accuracy | Speed | Best For |
|--------|----------|-------|----------|
| **ODE** (Default) | Medium | Fast | General robotics, wheeled robots |
| **Bullet** | High | Medium | Complex contacts, many collisions |
| **Simbody** | Very High | Slow | Biomechanics, articulated systems |
| **DART** | High | Medium | Manipulation, soft contacts |

**ODE (Open Dynamics Engine)** is the default and works well for most humanoid robots.

### Configuring Physics

In your world file:

```xml title="physics_config.world" showLineNumbers
<world name="physics_demo">

  <physics type="ode">
    <!-- Simulation step size (smaller = more accurate, slower) -->
    <max_step_size>0.001</max_step_size>

    <!-- Real-time factor target (1.0 = real-time) -->
    <real_time_factor>1.0</real_time_factor>

    <!-- ODE-specific parameters -->
    <ode>
      <solver>
        <type>quick</type>  <!-- quick | world -->
        <iters>50</iters>   <!-- Constraint solver iterations -->
        <sor>1.3</sor>      <!-- Successive Over-Relaxation -->
      </solver>

      <constraints>
        <cfm>0.0</cfm>      <!-- Constraint Force Mixing -->
        <erp>0.2</erp>      <!-- Error Reduction Parameter -->
        <contact_max_correcting_vel>100.0</contact_max_correcting_vel>
        <contact_surface_layer>0.001</contact_surface_layer>
      </constraints>
    </ode>
  </physics>

</world>
```

**Key parameters**:
- **`max_step_size`**: Time per physics tick (default: 0.001s = 1ms)
  - Smaller = more accurate but slower
  - Typical range: 0.0001 to 0.01
- **`iters`**: How many times to solve constraints
  - Higher = more stable joints but slower
  - Default: 50, increase for complex robots
- **`erp`**: How fast to correct joint errors (0-1)
  - 0.2 = gentle correction (stable)
  - 0.8 = aggressive correction (may oscillate)

## URDF to Gazebo Integration

### Basic URDF Spawning

Remember your humanoid URDF from Module 1? Let's spawn it in Gazebo:

```bash
# Method 1: Via ROS 2 service
ros2 service call /spawn_entity gazebo_msgs/srv/SpawnEntity \
  '{name: "my_humanoid", xml: "$(cat /path/to/humanoid.urdf)"}'

# Method 2: Via launch file (recommended)
```

**Launch file approach**:

```python title="spawn_humanoid.launch.py" showLineNumbers
#!/usr/bin/env python3

import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():

    # Path to URDF file
    urdf_file = os.path.join(
        os.getcwd(),
        'urdf',
        'humanoid.urdf'
    )

    # Read URDF content
    with open(urdf_file, 'r') as f:
        robot_desc = f.read()

    # Spawn entity node
    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-entity', 'my_humanoid',
            '-topic', '/robot_description',
            '-x', '0',
            '-y', '0',
            '-z', '1.0',  # Spawn 1 meter above ground
        ],
        output='screen',
    )

    # Publish robot description
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_desc}]
    )

    return LaunchDescription([
        robot_state_publisher,
        spawn_entity,
    ])
```

### Adding Gazebo-Specific URDF Tags

Basic URDF from Module 1 needs extra tags for Gazebo:

```xml title="humanoid_gazebo.urdf" showLineNumbers
<?xml version="1.0"?>
<robot name="humanoid_gazebo">

  <!-- Basic link from Module 1 -->
  <link name="torso">
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
      <inertia ixx="1.0" ixy="0" ixz="0"
               iyy="1.0" iyz="0"
               izz="0.5"/>
    </inertial>
  </link>

  <!-- ========== GAZEBO-SPECIFIC TAGS ========== -->

  <!-- Gazebo material (for rendering) -->
  <gazebo reference="torso">
    <material>Gazebo/Blue</material>
    <mu1>0.8</mu1>  <!-- Friction coefficient 1 -->
    <mu2>0.8</mu2>  <!-- Friction coefficient 2 -->
    <kp>1000000.0</kp>  <!-- Contact stiffness -->
    <kd>1.0</kd>  <!-- Contact damping -->
  </gazebo>

  <!-- Joint with transmission (for control) -->
  <joint name="shoulder_joint" type="revolute">
    <parent link="torso"/>
    <child link="upper_arm"/>
    <origin xyz="0 0.15 0.2" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="-3.14" upper="3.14" effort="100" velocity="2.0"/>
    <dynamics damping="0.7" friction="0.0"/>
  </joint>

  <link name="upper_arm">
    <!-- Visual, collision, inertial as before -->
    <visual>
      <origin xyz="0 0 -0.15" rpy="0 0 0"/>
      <geometry>
        <cylinder radius="0.04" length="0.3"/>
      </geometry>
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
               iyy="0.02" iyz="0"
               izz="0.005"/>
    </inertial>
  </link>

  <!-- Gazebo joint properties -->
  <gazebo reference="shoulder_joint">
    <implicitSpringDamper>true</implicitSpringDamper>
    <provideFeedback>true</provideFeedback>
  </gazebo>

</robot>
```

**New Gazebo tags**:

- **`<gazebo reference="link_name">`**: Apply properties to a link
  - `<material>`: Gazebo material (from built-in library)
  - `<mu1>`, `<mu2>`: Friction coefficients (0 = frictionless, 1 = high friction)
  - `<kp>`: Contact stiffness (higher = harder contact)
  - `<kd>`: Contact damping (higher = more damping)

- **`<gazebo reference="joint_name">`**: Apply properties to a joint
  - `<implicitSpringDamper>`: Use implicit integration (more stable)
  - `<provideFeedback>`: Enable force/torque sensing

### Gazebo Materials

Built-in materials for realistic appearance:

```xml
<!-- Common Gazebo materials -->
<gazebo reference="link_name">
  <material>Gazebo/Blue</material>
  <!-- Other options:
       Gazebo/Red, Gazebo/Green, Gazebo/Grey
       Gazebo/Wood, Gazebo/Metal, Gazebo/Black
       Gazebo/White, Gazebo/Orange, Gazebo/Yellow
  -->
</gazebo>
```

## Accurate Inertial Properties

**Critical for realistic physics!** Incorrect inertia causes:
- Unstable motion (robot vibrates)
- Unrealistic acceleration
- Joint controllers don't transfer to real robot

### Computing Inertia for Primitives

**Box** (width `w`, depth `d`, height `h`, mass `m`):
```python
ixx = (1/12) * m * (d² + h²)
iyy = (1/12) * m * (w² + h²)
izz = (1/12) * m * (w² + d²)
```

**Cylinder** (radius `r`, length `l`, mass `m`):
```python
# Axis along Z
ixx = iyy = (1/12) * m * (3*r² + l²)
izz = (1/2) * m * r²
```

**Sphere** (radius `r`, mass `m`):
```python
ixx = iyy = izz = (2/5) * m * r²
```

### Example: Accurate Humanoid Torso

```xml
<link name="torso">
  <!-- Visual/Collision omitted for brevity -->

  <inertial>
    <mass value="20.0"/>  <!-- 20 kg torso -->

    <!-- Box: 0.3m wide, 0.2m deep, 0.5m tall -->
    <!-- ixx = (1/12) * 20 * (0.2² + 0.5²) = 0.482 -->
    <!-- iyy = (1/12) * 20 * (0.3² + 0.5²) = 0.567 -->
    <!-- izz = (1/12) * 20 * (0.3² + 0.2²) = 0.217 -->

    <inertia ixx="0.482" ixy="0.0" ixz="0.0"
             iyy="0.567" iyz="0.0"
             izz="0.217"/>

    <!-- Center of mass offset (if not at geometric center) -->
    <origin xyz="0 0 0.1" rpy="0 0 0"/>
  </inertial>
</link>
```

### Using CAD Software for Complex Shapes

For realistic meshes, export inertia from CAD:

**SolidWorks**:
1. Tools → Mass Properties
2. Copy mass and inertia tensor
3. Paste into URDF `<inertial>`

**Fusion 360**:
1. Inspect → Properties → Physical
2. Enable "Show Mass, Volume, etc."
3. Copy values

**Blender** (with physics add-ons):
1. Select object → Properties → Physics
2. Calculate mass properties

## Joint Dynamics

### Damping and Friction

```xml
<joint name="elbow_joint" type="revolute">
  <!-- ... parent, child, axis, limits ... -->

  <dynamics damping="0.7" friction="0.0"/>
  <!--
    damping: Resists velocity (Nm·s/rad)
      - Too low: Joint oscillates
      - Too high: Joint moves slowly
      - Typical: 0.1 - 2.0

    friction: Static/kinetic friction (Nm)
      - Models gear backlash, bearing resistance
      - Typical: 0.0 - 0.5
  -->
</joint>
```

**Tuning tips**:
1. Start with `damping=0.5`, `friction=0.0`
2. If joint oscillates, increase damping
3. If motion is too smooth, add friction

### Joint Limits and Safety

```xml
<joint name="knee_joint" type="revolute">
  <limit lower="0.0" upper="2.5" effort="150" velocity="3.0"/>
  <!--
    lower/upper: Angle limits (radians)
    effort: Max torque (Nm)
    velocity: Max angular velocity (rad/s)
  -->

  <safety_controller soft_lower_limit="0.1"
                     soft_upper_limit="2.4"
                     k_position="100"
                     k_velocity="10"/>
  <!--
    Soft limits: Start applying opposing force before hard limit
    k_position: Stiffness of virtual spring at limit
    k_velocity: Damping coefficient
  -->
</joint>
```

## Transmission for ros2_control

To control joints from ROS 2, add transmissions:

```xml
<transmission name="shoulder_transmission">
  <type>transmission_interface/SimpleTransmission</type>
  <joint name="shoulder_joint">
    <hardwareInterface>hardware_interface/EffortJointInterface</hardwareInterface>
  </joint>
  <actuator name="shoulder_motor">
    <mechanicalReduction>1</mechanicalReduction>
  </actuator>
</transmission>
```

**Then add Gazebo plugin**:

```xml
<gazebo>
  <plugin name="gazebo_ros2_control" filename="libgazebo_ros2_control.so">
    <parameters>$(find my_robot)/config/ros2_control.yaml</parameters>
  </plugin>
</gazebo>
```

We'll use this in Chapter 5 for complete joint control.

## Testing Physics Accuracy

### Drop Test

Test if physics is realistic:

```python title="drop_test.py" showLineNumbers
#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from gazebo_msgs.msg import ModelStates
import math

class DropTest(Node):
    """
    Verify physics accuracy by dropping an object and measuring fall time.

    Theory: h = (1/2) * g * t²
    For h=10m, g=9.81 m/s²: t ≈ 1.43 seconds
    """
    def __init__(self):
        super().__init__('drop_test')
        self.sub = self.create_subscription(
            ModelStates, '/gazebo/model_states',
            self.callback, 10)

        self.start_time = None
        self.start_height = 10.0

    def callback(self, msg):
        if 'test_box' in msg.name:
            idx = msg.name.index('test_box')
            z = msg.pose[idx].position.z

            if self.start_time is None and z < self.start_height - 0.1:
                self.start_time = self.get_clock().now()

            if z < 0.5 and self.start_time is not None:
                elapsed = (self.get_clock().now() - self.start_time).nanoseconds / 1e9
                expected = math.sqrt(2 * self.start_height / 9.81)
                error = abs(elapsed - expected) / expected * 100

                self.get_logger().info(
                    f'Fall time: {elapsed:.3f}s (expected {expected:.3f}s, '
                    f'error: {error:.1f}%)'
                )
                rclpy.shutdown()

def main(args=None):
    rclpy.init(args=args)
    node = DropTest()
    rclpy.spin(node)

if __name__ == '__main__':
    main()
```

**Expected result**: Error < 5% (good physics)

## Common Physics Issues

### Issue: Robot Falls Through Ground

**Cause**: Missing collision geometry or too-large `contact_surface_layer`

**Solution**:
```xml
<!-- Ensure ground has collision -->
<collision name="ground_collision">
  <geometry>
    <plane><normal>0 0 1</normal></plane>
  </geometry>
</collision>

<!-- Reduce contact surface layer -->
<physics type="ode">
  <ode>
    <constraints>
      <contact_surface_layer>0.001</contact_surface_layer>
    </constraints>
  </ode>
</physics>
```

### Issue: Joints Are Unstable (Vibrating)

**Cause**: Insufficient constraint solver iterations or CFM too high

**Solution**:
```xml
<ode>
  <solver>
    <iters>100</iters>  <!-- Increase from 50 -->
  </solver>
  <constraints>
    <cfm>0.0</cfm>  <!-- Reduce from default -->
  </constraints>
</ode>
```

### Issue: Robot Moves Too Slowly

**Cause**: Excessive damping or incorrect mass

**Solution**:
1. Check joint damping (reduce if > 2.0)
2. Verify inertial mass is realistic (not 1000 kg!)
3. Check friction coefficients (`mu1`, `mu2`)

## Hands-On Exercises

**Try this**:

1. Take your URDF from Module 1 Exercise 3
2. Add Gazebo tags (`<gazebo reference="...">`)
3. Spawn in Gazebo
4. Verify physics:
   - Robot doesn't explode
   - Joints move smoothly
   - Falls realistically when unsupported

## Comprehension Questions

**Question 4**: Why do we need to specify inertia in URDF?

<details>
<summary>Click to reveal answer</summary>

**Answer**: Inertia determines how an object resists rotational acceleration (torque → angular acceleration relationship).

Without accurate inertia:
- Physics simulation is unrealistic (object spins too fast/slow)
- Controllers tuned in simulation won't work on real robot
- Joint torques are incorrect

**Formula**: τ = I × α (torque = inertia × angular acceleration)

Higher inertia = more torque needed to rotate = matches real robot behavior.

</details>

---

**Question 5**: What's the difference between `<collision>` and `<inertial>`?

<details>
<summary>Click to reveal answer</summary>

**Answer**:

- **`<collision>`**: Geometry for **contact detection**. Used by physics engine to detect when objects touch and compute contact forces. Should be simple (boxes, cylinders) for performance.

- **`<inertial>`**: **Mass properties** (mass, center of mass, inertia tensor). Used to compute how forces affect motion (F=ma, τ=Iα). Doesn't define shape - just how much the object "resists" changes in motion.

**Example**: A hollow cylinder and solid cylinder have the same `<collision>` geometry but different `<inertial>` properties (hollow has less mass, different inertia distribution).

</details>

---

**Question 6**: When should you use Bullet instead of ODE?

<details>
<summary>Click to reveal answer</summary>

**Answer**: Use **Bullet** when:

1. **Many simultaneous contacts** - Grasping, pushing, stacking objects
2. **Complex collision geometries** - Detailed meshes with many triangles
3. **Soft body simulation** - Deformable objects (less common in robotics)
4. **ODE is unstable** - Joints exploding, penetration artifacts

Stick with **ODE** (default) when:
- Simple robots with few contacts (wheeled, legged)
- Performance is critical
- Standard humanoid motion (walking, reaching)

**Trade-off**: Bullet is more accurate but 2-3x slower than ODE.

</details>

---

## Next Steps

You've mastered physics integration! Next, you'll learn how to use Unity for photorealistic human-robot interaction visualization.

**Next Chapter**: [Unity for HRI Visualization](./ch3-unity-interaction) →

---

**Chapter Summary**: Gazebo supports multiple physics engines (ODE, Bullet, Simbody, DART) with configurable accuracy and performance trade-offs. URDF models from Module 1 require Gazebo-specific tags (`<gazebo reference>`) for materials, friction, and control. Accurate inertial properties (mass, inertia tensor, center of mass) are critical for realistic physics - use formulas for primitives or export from CAD for complex shapes. Joint dynamics include damping (velocity resistance) and friction (static resistance). Physics accuracy can be tested with drop tests and validated against theoretical predictions.
