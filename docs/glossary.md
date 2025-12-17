---
title: Glossary
description: Robotics and Physical AI terminology reference
sidebar_position: 100
---

# Glossary

A comprehensive reference of robotics, ROS 2, and Physical AI terminology used throughout this textbook.

## A

**Action** - A ROS 2 communication pattern for long-running tasks that provide feedback and can be canceled. Used for complex robot behaviors like navigation.

**AMCL** - Adaptive Monte Carlo Localization. A probabilistic localization algorithm that uses particle filters to estimate a robot's position on a map.

**API** - Application Programming Interface. A set of functions and protocols for building and interacting with software.

## B

**Behavior Tree** - A hierarchical control structure for robot decision-making. Used in Nav2 for flexible navigation logic.

**Bipedal Locomotion** - Walking on two legs, a key challenge for humanoid robots requiring balance and gait control.

## C

**Callback** - A function that is automatically called when an event occurs, such as a message arriving on a topic or a timer firing.

**Collision Detection** - The process of identifying when objects in a simulation or physical space intersect, preventing robots from passing through obstacles.

**Continuous Joint** - A joint type in URDF that allows unlimited rotation (no joint limits), typically used for wheels.

**Costmap** - A grid-based representation of the environment where each cell has a cost indicating obstacle proximity. Used by Nav2 for path planning.

## D

**DDS** - Data Distribution Service. The middleware standard used by ROS 2 for scalable, real-time communication.

**Depth Camera** - A sensor that captures distance information for each pixel, creating a 3D representation of the scene. Essential for robot perception.

**Digital Twin** - A virtual replica of a physical robot or environment used for simulation, testing, and training before real-world deployment.

**Domain Randomization** - A technique in simulation where environment parameters (lighting, textures, physics) are randomized to improve sim-to-real transfer.

## E

**Embodied Intelligence** - AI systems that learn and interact through physical embodiment (robots), as opposed to purely digital AI.

## F

**Feedback** - Information sent back from a robot's sensors or action servers about current state or progress toward a goal.

**Fixed Joint** - A joint type in URDF that rigidly connects two links with no motion, used for attaching sensors or mounting components.

**Floating Joint** - A joint type in URDF providing 6 degrees of freedom (position and orientation), used for free-floating objects like drones.

**Forward Kinematics** - Computing the position and orientation of a robot's end-effector (like a hand) given all joint angles.

## G

**Gazebo** - An open-source 3D robotics simulator with accurate physics, sensor simulation, and ROS 2 integration.

**Grasp** - The action of a robot gripping an object. Requires precise control of fingers/gripper and force feedback.

## H

**Humanoid Robot** - A robot with human-like body structure (head, torso, arms, legs), designed to operate in human environments.

## I

**IMU** - Inertial Measurement Unit. A sensor that measures acceleration and angular velocity, used for robot stabilization and odometry.

**Inertia** - A body's resistance to changes in motion. Critical for accurate physics simulation of robots. Represented by a 3x3 inertia tensor in URDF.

**Inverse Kinematics** - Computing the joint angles required to achieve a desired end-effector position. The inverse problem of forward kinematics.

**Isaac ROS** - NVIDIA's hardware-accelerated ROS 2 packages for perception, using GPU and dedicated AI processors.

**Isaac Sim** - NVIDIA's photorealistic robotics simulator built on Omniverse, supporting RTX ray tracing and physics simulation.

## J

**Joint** - A connection between two robot links that allows relative motion (rotation or translation).

**Joint Limit** - The minimum and maximum angles or positions that a joint can reach, specified in URDF to prevent self-collision and match real hardware constraints.

**Joint State** - The current position, velocity, and effort (torque/force) of a robot's joints, typically published on the `/joint_states` topic.

## K

**Kinematic Chain** - A series of links connected by joints from a base to an end-effector, defining a path for motion propagation.

**Kinematics** - The study of motion without considering forces. Forward kinematics: joint angles → end-effector position. Inverse kinematics: desired position → joint angles.

## L

**LiDAR** - Light Detection and Ranging. A sensor that uses laser pulses to measure distances, creating a 2D or 3D point cloud of the environment.

**Link** - A rigid body component of a robot, defined in URDF with visual geometry, collision geometry, and inertial properties.

**LLM** - Large Language Model. AI models like GPT-4 or Claude trained on vast text data, used for cognitive planning in VLA systems.

**Localization** - The process of a robot determining its position within a known map.

## M

**Middleware** - Software that sits between the operating system and applications, providing communication and coordination services. ROS 2 is robot middleware.

## N

**Nav2** - Navigation2, the ROS 2 navigation stack for autonomous robot path planning, obstacle avoidance, and goal execution.

**Node** - The fundamental unit in ROS 2. A process that performs computation and communicates via topics, services, or actions.

## O

**Odometry** - Estimation of a robot's position change over time using wheel encoders, IMU, or visual sensors.

**ODE** - Open Dynamics Engine. A physics engine used by Gazebo for simulating rigid body dynamics.

## P

**Path Planning** - Computing a collision-free path from the robot's current position to a goal location.

**Physical AI** - Artificial intelligence embodied in physical robots that perceive and interact with the real world.

**PID Controller** - Proportional-Integral-Derivative controller. A feedback control algorithm that computes control commands based on error, accumulated error, and rate of error change.

**Planar Joint** - A joint type allowing 2D motion (x, y translation and yaw rotation), rarely used in practice.

**Position Control** - A control mode where the robot joint is commanded to move to a specific angle or position.

**Prismatic Joint** - A joint that allows linear sliding motion (like a telescope).

**Publisher** - A ROS 2 node that sends messages on a topic.

## Q

**QoS** - Quality of Service. ROS 2 policies that control message reliability, durability, and delivery guarantees.

## R

**rclpy** - The Python client library for ROS 2, used to create nodes, publishers, subscribers, services, and actions.

**Real-Time Factor** - In simulation, the ratio of simulated time to wall-clock time. A real-time factor of 1.0 means simulation runs at the same speed as reality.

**Revolute Joint** - A joint that allows rotational motion (like a hinge or human elbow).

**ROS 2** - Robot Operating System 2. Open-source middleware for robot software development, providing communication, tools, and libraries.

**RTX** - NVIDIA's real-time ray tracing technology, used in Isaac Sim for photorealistic rendering.

**RViz** - ROS Visualization tool. A 3D visualization environment for displaying sensor data, robot models (URDF), and planning outputs.

## S

**SDF** - Simulation Description Format. An XML format for describing robot models, environments, and physics properties in Gazebo.

**Service** - A ROS 2 communication pattern for synchronous request/response interactions.

**SLAM** - Simultaneous Localization and Mapping. A robot builds a map of its environment while simultaneously determining its location within that map.

**Subscriber** - A ROS 2 node that receives messages published on a topic.

**Synthetic Data** - Artificially generated training data created in simulation, used to train AI models without real-world data collection.

## T

**Timer** - A ROS 2 mechanism that calls a callback function at a specified rate, created with `create_timer()`.

**Topic** - A ROS 2 communication channel where nodes publish and subscribe to messages. Uses a publish-subscribe pattern.

**Torque** - Rotational force applied to a joint. Measured in Newton-meters (Nm).

**Transmission** - A URDF element defining how actuators connect to joints, required for Gazebo simulation and ros2_control.

## U

**URDF** - Unified Robot Description Format. An XML format for describing a robot's physical structure (links, joints, sensors) in ROS 2.

**USD** - Universal Scene Description. A file format used by NVIDIA Omniverse and Isaac Sim for 3D scene representation.

## V

**Velocity Control** - A control mode where the robot joint is commanded to move at a specific speed, requiring feedback to stop at the desired position.

**VLA** - Vision-Language-Action. An AI paradigm that integrates computer vision, natural language understanding (LLMs), and robotic action execution.

**VSLAM** - Visual Simultaneous Localization and Mapping. SLAM using camera images instead of LiDAR.

## W

**Whisper** - OpenAI's automatic speech recognition (ASR) model, used for converting voice commands to text.

## X

**Xacro** - XML Macros for ROS. A macro language that extends URDF to reduce repetition through variables, macros, and includes.

## Y

*No entries*

## Z

*No entries*

---

**Total Terms**: 70+ (Module 1 complete, expanding as modules are added)

**Missing a term?** Suggest additions via [GitHub Issues](https://github.com/your-org/physical-ai-textbook/issues).
