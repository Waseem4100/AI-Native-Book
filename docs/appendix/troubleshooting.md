---
title: Troubleshooting
description: Common issues and solutions for ROS 2, Gazebo, and Physical AI development
sidebar_position: 2
---

# Troubleshooting

Common issues and solutions encountered while working through the Physical AI textbook.

## ROS 2 Issues

### `ros2: command not found`

**Cause**: ROS 2 environment not sourced.

**Solution**:
```bash
source /opt/ros/humble/setup.bash

# Make permanent by adding to ~/.bashrc
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

### No communication between publisher and subscriber

**Cause**: DDS discovery issue or QoS mismatch.

**Solution**:
```bash
# Check if nodes are running
ros2 node list

# Check if topics exist
ros2 topic list

# Check topic info (verify QoS settings)
ros2 topic info /your_topic_name --verbose

# Try with matching QoS profiles (reliable + transient local for both)
```

### `colcon build` fails with "package not found"

**Cause**: Missing dependencies.

**Solution**:
```bash
# Install missing dependencies automatically
rosdep install --from-paths src --ignore-src -r -y

# If rosdep not initialized:
sudo rosdep init
rosdep update
```

## Gazebo Issues

### Gazebo won't start or crashes immediately

**Cause**: Graphics driver issue.

**Solution**:
```bash
# Update graphics drivers
sudo apt update
sudo apt install nvidia-driver-535  # For NVIDIA GPUs

# Reboot
sudo reboot

# Test with software rendering (slower but more compatible)
LIBGL_ALWAYS_SOFTWARE=1 gazebo
```

### Robot model not appearing in Gazebo

**Cause**: URDF/SDF syntax error or missing mesh files.

**Solution**:
```bash
# Check URDF syntax
check_urdf your_robot.urdf

# Validate SDF
gz sdf -k your_world.sdf

# Check Gazebo logs for errors
# Logs are typically in ~/.gazebo/
```

### Physics behaving unrealistically

**Cause**: Physics parameters need tuning.

**Solution**: Adjust in SDF world file:
- Reduce `max_step_size` (e.g., 0.001 instead of 0.01)
- Increase solver iterations (`<iters>50</iters>`)
- Check collision geometry matches visual geometry
- Verify inertial properties are realistic

## Python / rclpy Issues

### `ModuleNotFoundError: No module named 'rclpy'`

**Cause**: ROS 2 Python environment not sourced or rclpy not installed.

**Solution**:
```bash
# Source ROS 2
source /opt/ros/humble/setup.bash

# Ensure rclpy is installed
sudo apt install python3-rclpy

# If using a Python virtual environment, don't - use system Python for ROS 2
```

### Node exits immediately with no error

**Cause**: Missing `rclpy.spin()` call.

**Solution**: Ensure your main function includes:
```python
def main():
    rclpy.init()
    node = YourNode()
    rclpy.spin(node)  # This line is essential!
    rclpy.shutdown()
```

## URDF / Visualization Issues

### Robot appears white/textureless in RViz

**Cause**: Color/material not specified in URDF.

**Solution**: Add material tags:
```xml
<visual>
  <geometry>
    <box size="0.1 0.1 0.1"/>
  </geometry>
  <material name="blue">
    <color rgba="0 0 1 1"/>
  </material>
</visual>
```

### Joints not moving in RViz/Gazebo

**Cause**: Joint controller not loaded or joint limits too restrictive.

**Solution**:
- Check joint limits in URDF (`<limit>` tag)
- Verify controller is publishing to correct topic
- Use `ros2 topic echo /joint_states` to see current joint values

## General Linux / System Issues

### Permission denied when accessing `/dev/ttyUSB0` or similar

**Cause**: User not in `dialout` group.

**Solution**:
```bash
sudo usermod -a -G dialout $USER
# Log out and log back in
```

### Disk space full

**Cause**: ROS logs or build artifacts consuming space.

**Solution**:
```bash
# Clean ROS 2 logs
rm -rf ~/.ros/log/*

# Clean colcon build artifacts
cd ~/your_ros2_workspace
rm -rf build install log

# Check disk usage
df -h
du -sh ~/.ros ~/.gazebo
```

## Getting More Help

If your issue isn't listed here:

1. **Search ROS Answers**: https://answers.ros.org/
2. **Check GitHub Issues**: [Textbook Issues](https://github.com/your-org/physical-ai-textbook/issues)
3. **ROS 2 Documentation**: https://docs.ros.org/en/humble/
4. **Ask in Discussions**: [GitHub Discussions](https://github.com/your-org/physical-ai-textbook/discussions)

When asking for help, include:
- Your Ubuntu version (`lsb_release -a`)
- ROS 2 version (`ros2 --version`)
- Full error message (copy-paste, don't screenshot)
- Steps to reproduce the issue
