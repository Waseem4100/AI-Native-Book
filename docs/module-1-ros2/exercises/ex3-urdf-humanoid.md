---
title: "Exercise 3: Build a Humanoid URDF Model"
description: Design and visualize a complete humanoid robot using URDF
sidebar_position: 3
tags: [exercise, urdf, robot-modeling, humanoid, rviz, advanced]
---

# Exercise 3: Build a Humanoid URDF Model

**Difficulty**: Advanced (Open-Ended)
**Time**: 2 hours
**Prerequisites**: Chapter 5 (URDF Modeling)

## Learning Objectives

By completing this exercise, you will:

1. Design a complete humanoid robot structure
2. Create a URDF file with multiple links and joints
3. Implement realistic joint limits and properties
4. Visualize and test your robot in RViz2
5. Verify kinematic chains for arms and legs

## Exercise Description

Create a URDF model for a humanoid robot with:

**Required Components**:
- **Torso**: Main body (rectangular box)
- **Head**: Sphere, connected to torso with neck joint
- **Arms** (both left and right):
  - Shoulder joint (revolute, pitch axis)
  - Upper arm link
  - Elbow joint (revolute, pitch axis)
  - Forearm link
- **Legs** (both left and right):
  - Hip joint (revolute, pitch axis)
  - Thigh link
  - Knee joint (revolute, pitch axis)
  - Shin link
  - Ankle joint (revolute, pitch axis)
  - Foot link

**Specifications**:
- **Total joints**: 13 (1 neck, 4 arm, 8 leg)
- **Total links**: 14 (1 torso, 1 head, 4 arm, 8 leg)
- **Coordinate system**: ROS standard (X forward, Y left, Z up)
- **Units**: Meters for length, kilograms for mass, radians for angles

**Visual Requirements**:
- All links must have visual geometry (boxes, cylinders, or spheres)
- All links must have materials with colors
- Realistic proportions (use reference dimensions below)

**Physical Requirements**:
- All links must have mass and inertia properties
- All joints must have limits (lower, upper, effort, velocity)
- Joint limits must be realistic for humanoid motion

## Reference Dimensions

Use these dimensions as a guide (you can adjust for your design):

| Component | Length | Width/Diameter | Mass |
|-----------|--------|----------------|------|
| Torso | 0.5m | 0.3m × 0.2m | 20kg |
| Head | 0.12m radius | - | 3kg |
| Upper arm | 0.3m | 0.04m radius | 2kg |
| Forearm | 0.25m | 0.03m radius | 1kg |
| Thigh | 0.4m | 0.06m radius | 5kg |
| Shin | 0.4m | 0.05m radius | 3kg |
| Foot | 0.2m × 0.1m × 0.05m | - | 1kg |

## Reference Joint Limits

| Joint | Type | Lower Limit | Upper Limit | Max Effort | Max Velocity |
|-------|------|-------------|-------------|------------|--------------|
| Neck pitch | Revolute | -45° (-0.785 rad) | 45° (0.785 rad) | 20 Nm | 1.0 rad/s |
| Shoulder pitch | Revolute | -180° (-3.14 rad) | 180° (3.14 rad) | 100 Nm | 2.0 rad/s |
| Elbow pitch | Revolute | 0° (0 rad) | 150° (2.62 rad) | 50 Nm | 2.0 rad/s |
| Hip pitch | Revolute | -90° (-1.57 rad) | 90° (1.57 rad) | 150 Nm | 2.0 rad/s |
| Knee pitch | Revolute | 0° (0 rad) | 150° (2.62 rad) | 100 Nm | 2.0 rad/s |
| Ankle pitch | Revolute | -45° (-0.785 rad) | 45° (0.785 rad) | 80 Nm | 1.5 rad/s |

## Step-by-Step Instructions

### Step 1: Plan Your Robot Structure

Before coding, sketch the robot structure:

```
           head
             |
         [neck_joint]
             |
           torso
          /  |  \
   [left  [right  [left   [right
   shoulder] shoulder] hip] hip]
     |        |      |      |
   left     right   left  right
   upper_arm ...    thigh  ...
     |              |
   [left_elbow]    [left_knee]
     |              |
   left_forearm    left_shin
                    |
                  [left_ankle]
                    |
                  left_foot
```

Draw this tree structure and label each link and joint.

### Step 2: Create URDF File Structure

Create `my_humanoid.urdf`:

```xml
<?xml version="1.0"?>
<robot name="my_humanoid">

  <!-- TODO: Define torso link here -->

  <!-- TODO: Define neck joint and head link -->

  <!-- TODO: Define left arm (shoulder joint, upper arm, elbow joint, forearm) -->

  <!-- TODO: Define right arm (mirror of left arm) -->

  <!-- TODO: Define left leg (hip, thigh, knee, shin, ankle, foot) -->

  <!-- TODO: Define right leg (mirror of left leg) -->

</robot>
```

### Step 3: Implement the Torso

Start with the torso (base of the robot):

```xml
<!-- Torso (main body) -->
<link name="torso">
  <visual>
    <geometry>
      <box size="0.3 0.2 0.5"/>  <!-- width, depth, height -->
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
    <!-- Inertia for a box: I = (1/12) * m * (d² + h²) for each axis -->
    <inertia ixx="1.0" ixy="0.0" ixz="0.0"
             iyy="1.0" iyz="0.0"
             izz="0.5"/>
  </inertial>
</link>
```

### Step 4: Implement Head and Neck

Add the neck joint and head:

```xml
<!-- Neck joint (connects torso to head) -->
<joint name="neck_pitch" type="revolute">
  <parent link="torso"/>
  <child link="head"/>

  <!-- Position: top of torso (Z = 0.25m) -->
  <origin xyz="0 0 0.25" rpy="0 0 0"/>

  <!-- Rotation axis: Y (pitch - nod yes/no) -->
  <axis xyz="0 1 0"/>

  <!-- Joint limits -->
  <limit lower="-0.785" upper="0.785" effort="20" velocity="1.0"/>
</joint>

<!-- Head link -->
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
    <!-- Inertia for sphere: I = (2/5) * m * r² -->
    <inertia ixx="0.02" ixy="0" ixz="0"
             iyy="0.02" iyz="0"
             izz="0.02"/>
  </inertial>
</link>
```

### Step 5: Implement One Arm (Left)

Complete the left arm chain:

```xml
<!-- TODO: Left shoulder joint -->
<!-- - Parent: torso -->
<!-- - Child: left_upper_arm -->
<!-- - Position: Top-left of torso (xyz="0 0.15 0.2") -->
<!-- - Axis: Y (pitch) -->

<!-- TODO: Left upper arm link -->
<!-- - Geometry: Cylinder (radius 0.04, length 0.3) -->
<!-- - Visual origin: (0, 0, -0.15) to center the cylinder -->
<!-- - Material: Skin color -->

<!-- TODO: Left elbow joint -->
<!-- - Parent: left_upper_arm -->
<!-- - Child: left_forearm -->
<!-- - Position: End of upper arm (xyz="0 0 -0.3") -->
<!-- - Axis: Y (pitch) -->

<!-- TODO: Left forearm link -->
<!-- - Geometry: Cylinder (radius 0.03, length 0.25) -->
<!-- - Visual origin: (0, 0, -0.125) -->
```

### Step 6: Mirror for Right Arm

Copy the left arm and adjust:
- Replace "left" with "right" in all names
- Change Y positions from positive to negative (0.15 → -0.15)

### Step 7: Implement One Leg (Left)

Complete the left leg chain:

```xml
<!-- TODO: Left hip joint -->
<!-- - Parent: torso -->
<!-- - Child: left_thigh -->
<!-- - Position: Bottom-left of torso (xyz="0 0.1 -0.25") -->

<!-- TODO: Left thigh link -->

<!-- TODO: Left knee joint -->
<!-- - Parent: left_thigh -->
<!-- - Child: left_shin -->

<!-- TODO: Left shin link -->

<!-- TODO: Left ankle joint -->
<!-- - Parent: left_shin -->
<!-- - Child: left_foot -->

<!-- TODO: Left foot link -->
<!-- - Geometry: Box (0.2 × 0.1 × 0.05) -->
```

### Step 8: Mirror for Right Leg

Copy the left leg, replace "left" with "right", adjust Y positions.

### Step 9: Visualize in RViz

```bash
# Check URDF syntax
check_urdf my_humanoid.urdf

# Should output: "Successfully parsed URDF"

# Launch RViz with your robot
ros2 launch urdf_tutorial display.launch.py model:=my_humanoid.urdf
```

In RViz, you should see:
- Complete humanoid robot
- Joint sliders in the GUI
- Move sliders to test joint motion

### Step 10: Verify Kinematic Chains

```bash
# Generate kinematic tree visualization
urdf_to_graphiz my_humanoid.urdf

# Opens a PDF showing the tree structure
# Verify:
# - Torso is the root
# - All limbs connect correctly
# - No orphaned links
```

## Success Criteria

Your URDF is complete when:

- ✅ All 14 links are defined with visual geometry
- ✅ All 13 joints are defined with correct parent/child
- ✅ All links have realistic mass and inertia
- ✅ All joints have realistic limits
- ✅ `check_urdf` reports no errors
- ✅ Robot appears correctly in RViz
- ✅ All joints can be moved with GUI sliders
- ✅ No links are floating or disconnected
- ✅ Robot proportions look humanoid
- ✅ Colors/materials make links distinguishable

## Challenges (Optional)

### Challenge 1: Add Roll Joints

Real humanoids have 3-DOF shoulders and hips. Add:
- Shoulder roll (rotation around X-axis)
- Hip roll (rotation around X-axis)

This requires adding intermediate links between torso and arms/legs.

### Challenge 2: Add Hands and Fingers

Extend each arm with:
- Wrist joint (roll)
- Hand link (palm)
- 3 finger joints per hand (simplified)

### Challenge 3: Use Mesh Files

Replace primitive shapes with 3D meshes:
- Find or create `.stl` or `.dae` files
- Place in `meshes/` directory
- Reference with `<mesh filename="package://my_robot/meshes/head.stl"/>`

### Challenge 4: Add Sensors

Add sensors to your robot:
- Camera in the head (fixed joint)
- IMU in the torso (fixed joint)
- Force sensors in feet (fixed joints)

Use `<sensor>` tags or fixed joints with sensor links.

### Challenge 5: Prepare for Gazebo

Add tags required for Gazebo simulation:
- `<gazebo>` tags with material properties
- `<transmission>` tags for motor control
- Collision geometry for all links

## Common Issues and Solutions

**Issue**: Robot appears as disconnected parts
- **Solution**: Check that joint `<origin>` positions correctly place child links relative to parents

**Issue**: Limbs point in wrong directions
- **Solution**: Adjust `rpy` (roll, pitch, yaw) in joint `<origin>` tags

**Issue**: Joints don't move in RViz
- **Solution**: Verify joint type is `revolute`, not `fixed`
- **Solution**: Check joint limits allow movement (lower < upper)

**Issue**: Robot falls through floor in simulation
- **Solution**: Add collision geometry matching visual geometry
- **Solution**: Ensure inertia values are realistic (not zero or too small)

**Issue**: `check_urdf` reports "link not found"
- **Solution**: Ensure every joint's parent and child links are defined
- **Solution**: Check for typos in link names (case-sensitive!)

## Verification Checklist

Before submitting, verify:

- [ ] File is valid XML (proper opening/closing tags)
- [ ] Robot name is unique and descriptive
- [ ] All 14 links present: torso, head, 4 arm, 8 leg
- [ ] All 13 joints present: 1 neck, 4 arm, 8 leg
- [ ] Every link has `<visual>`, `<collision>`, `<inertial>`
- [ ] Every joint has `<parent>`, `<child>`, `<origin>`, `<axis>`, `<limit>`
- [ ] Joint limits are in radians (not degrees!)
- [ ] Masses are in kilograms
- [ ] Inertia matrices are realistic
- [ ] Colors/materials defined for visual clarity
- [ ] `check_urdf` passes without errors
- [ ] `urdf_to_graphiz` shows connected tree structure
- [ ] Robot visualizes correctly in RViz
- [ ] All joints movable via GUI sliders

## Inertia Calculation Reference

Use these formulas for common shapes:

**Box** (width w, depth d, height h, mass m):
```
Ixx = (1/12) * m * (d² + h²)
Iyy = (1/12) * m * (w² + h²)
Izz = (1/12) * m * (w² + d²)
```

**Cylinder** (radius r, length l, mass m, axis along Z):
```
Ixx = Iyy = (1/12) * m * (3*r² + l²)
Izz = (1/2) * m * r²
```

**Sphere** (radius r, mass m):
```
Ixx = Iyy = Izz = (2/5) * m * r²
```

For asymmetric objects, use CAD software to compute inertia.

## Solution

A complete solution is available in the `/solutions/module-1/` directory of the repository.

**Try to complete the exercise on your own first!** Refer to:
- Chapter 5 for URDF syntax and examples
- Chapter 5, "Building a Humanoid Torso with Arms" section

## What You Learned

In this exercise, you:

✅ Designed a complete humanoid robot structure
✅ Created links with visual, collision, and inertial properties
✅ Connected links with revolute joints
✅ Set realistic joint limits and physical parameters
✅ Visualized and tested the robot in RViz2
✅ Verified kinematic chains with `urdf_to_graphiz`
✅ Prepared a robot model for simulation and control

## Next Steps

**Congratulations!** You've completed all Module 1 exercises. You're ready for:

**Module 2: Simulation in Gazebo** (Coming Soon) - Simulate your humanoid with physics →

Before moving on:
1. Verify all three exercise solutions are complete
2. Review any chapters where you struggled
3. Experiment with your URDF model (try different dimensions, add complexity)

---

**Need help?** Review [Chapter 5: URDF Modeling](../ch5-urdf-modeling) or ask in the [discussion forum](https://github.com/your-org/physical-ai-textbook/discussions).

**Want to share your design?** Post your humanoid URDF in the discussions - we'd love to see what you created!
