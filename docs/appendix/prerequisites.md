---
title: Prerequisites & Setup
description: Required software and knowledge for Physical AI textbook
sidebar_position: 1
---

# Prerequisites & Setup

This guide covers the prerequisite knowledge and software setup required to complete the Physical AI & Humanoid Robotics textbook.

## Knowledge Prerequisites

### Required

**Python Programming** (Basic Level)
- Variables, data types (int, float, string, list, dict)
- Functions and classes
- Loops (`for`, `while`) and conditionals (`if`, `elif`, `else`)
- Basic file I/O

**Recommended Resources**:
- [Python.org Official Tutorial](https://docs.python.org/3/tutorial/)
- [Real Python](https://realpython.com/) tutorials

**Linux Terminal** (Basic Level)
- Navigate directories (`cd`, `ls`, `pwd`)
- Create/delete files and directories (`touch`, `mkdir`, `rm`)
- Edit files (`nano`, `vim`, or GUI editor)
- Install packages (`apt`, `pip`)

**Recommended Resources**:
- [Linux Journey](https://linuxjourney.com/)
- [Ubuntu Command Line for Beginners](https://ubuntu.com/tutorials/command-line-for-beginners)

### Recommended (Helpful But Not Required)

- **Git basics**: Clone, commit, push (you'll learn as you go)
- **Coordinate systems**: Understanding of 3D space (x, y, z axes)
- **Basic physics**: Concepts of force, velocity, acceleration
- **Linear algebra**: Vectors and matrices (used in robotics math)

## Software Setup

### 1. Operating System

**Recommended**: Ubuntu 22.04 LTS

**Alternatives**:
- **Docker**: Run Ubuntu container on Windows/Mac
- **Windows WSL2**: Windows Subsystem for Linux
- **Virtual Machine**: VirtualBox or VMware

**Why Ubuntu?** ROS 2 Humble has official support and most robotics tools are Linux-native.

### 2. ROS 2 Humble Installation

**System Requirements**:
- Ubuntu 22.04 LTS
- 4GB RAM minimum (8GB+ recommended)
- 20GB free disk space

**Installation Steps**:

```bash
# Set locale
sudo apt update && sudo apt install locales
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8

# Add ROS 2 GPG key
sudo apt install software-properties-common
sudo add-apt-repository universe
sudo apt update && sudo apt install curl -y
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg

# Add repository to sources list
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

# Install ROS 2 Humble Desktop
sudo apt update
sudo apt upgrade
sudo apt install ros-humble-desktop

# Install development tools
sudo apt install ros-dev-tools

# Source ROS 2 (add to ~/.bashrc for persistence)
source /opt/ros/humble/setup.bash
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
```

**Verify Installation**:

```bash
# Check ROS 2 version
ros2 --version

# Run demo nodes (in separate terminals)
# Terminal 1
ros2 run demo_nodes_cpp talker

# Terminal 2
ros2 run demo_nodes_py listener
```

If you see messages being published and received, ROS 2 is installed correctly!

### 3. Gazebo 11 Installation (For Module 2)

```bash
# Install Gazebo Classic 11
sudo apt install gazebo11

# Install ROS 2 Gazebo packages
sudo apt install ros-humble-gazebo-ros-pkgs

# Verify installation
gazebo --version
```

**Test Gazebo**:

```bash
gazebo
```

A window should open with an empty world.

### 4. Python Packages

```bash
# Install Python 3 and pip (usually pre-installed on Ubuntu 22.04)
sudo apt install python3-pip

# Install common robotics Python packages
pip3 install numpy scipy matplotlib

# Install ROS 2 Python dependencies
sudo apt install python3-colcon-common-extensions
```

### 5. Code Editor / IDE

**Recommended Options**:

**Visual Studio Code** (Most Popular)
```bash
# Download from https://code.visualstudio.com/
# Or install via snap
sudo snap install --classic code

# Recommended VS Code extensions:
# - Python (Microsoft)
# - ROS (Microsoft)
# - URDF (SMARTlab)
```

**Alternatives**:
- PyCharm (Community or Professional)
- Sublime Text
- Vim/Emacs (for advanced users)

### 6. Git

```bash
# Install Git
sudo apt install git

# Configure Git
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

## Optional Setup (For Advanced Modules)

### For Module 3: NVIDIA Isaac Sim

**Requirements**:
- NVIDIA RTX GPU (RTX 2060 or better)
- 32GB RAM
- 50GB free disk space
- Ubuntu 20.04 or 22.04

**Installation**:
1. Download [NVIDIA Omniverse Launcher](https://developer.nvidia.com/isaac-sim)
2. Install Isaac Sim 2023.1.0+ through Omniverse
3. Follow [official Isaac Sim installation guide](https://docs.omniverse.nvidia.com/isaacsim/)

**Cloud Alternative**: Use NVIDIA Isaac Sim on cloud platforms (AWS, GCP) if you don't have an RTX GPU.

### For Module 4: OpenAI Whisper & LLMs

```bash
# Install Whisper
pip3 install openai-whisper

# Install audio processing library
sudo apt install ffmpeg

# For LLM API access, you'll need:
# - OpenAI API key (https://platform.openai.com/)
# - OR Anthropic API key for Claude (https://console.anthropic.com/)
# - OR local open-source LLM (Ollama, LM Studio)
```

## Troubleshooting Common Issues

### Issue: `ros2: command not found`

**Solution**: Source ROS 2 setup file
```bash
source /opt/ros/humble/setup.bash
# Add to ~/.bashrc to make permanent
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
```

### Issue: Gazebo crashes on startup

**Solution**: Update graphics drivers
```bash
# For NVIDIA GPUs
sudo apt install nvidia-driver-535

# Reboot after installation
sudo reboot
```

### Issue: Permission denied when accessing devices

**Solution**: Add user to dialout group (for USB devices like cameras)
```bash
sudo usermod -a -G dialout $USER
# Log out and log back in for changes to take effect
```

## System Check Script

Run this script to verify your setup:

```bash
#!/bin/bash
# save as check_setup.sh and run: bash check_setup.sh

echo "=== Physical AI Textbook Setup Check ==="
echo ""

# Check Ubuntu version
echo "Ubuntu Version:"
lsb_release -a
echo ""

# Check ROS 2
echo "ROS 2 Humble:"
if command -v ros2 &> /dev/null; then
    ros2 --version
else
    echo "❌ ROS 2 not found"
fi
echo ""

# Check Python
echo "Python:"
python3 --version
echo ""

# Check Gazebo
echo "Gazebo:"
if command -v gazebo &> /dev/null; then
    gazebo --version
else
    echo "❌ Gazebo not found (required for Module 2)"
fi
echo ""

# Check Git
echo "Git:"
git --version
echo ""

echo "=== Setup check complete ==="
```

## Next Steps

Once your environment is set up:

1. **Test ROS 2**: Run the demo nodes to ensure communication works
2. **Clone this repository**: Get the textbook source code
3. **Start Module 1**: Begin with [ROS 2 Foundations](../module-1-ros2/)

## Getting Help

- **ROS 2 Documentation**: https://docs.ros.org/en/humble/
- **ROS Answers**: https://answers.ros.org/
- **Ubuntu Forums**: https://ubuntuforums.org/
- **Textbook Discussions**: [GitHub Discussions](https://github.com/your-org/physical-ai-textbook/discussions)

---

**Ready?** Head to [Module 1: ROS 2 Foundations](../module-1-ros2/) to begin your Physical AI journey!
