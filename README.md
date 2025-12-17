# Physical AI & Humanoid Robotics Textbook

**Bridging the Digital Brain and the Physical Body**

A comprehensive, open-source textbook teaching students how to design, simulate, and deploy AI-powered humanoid robots using ROS 2, Gazebo, Unity, and NVIDIA Isaac.

## 📚 What You'll Learn

- **Module 1: ROS 2 Foundations** - Master robot middleware, communication patterns, and URDF modeling
- **Module 2: Simulation** (Coming Soon) - Physics-based simulation with Gazebo and Unity
- **Module 3: Isaac AI Brain** (Coming Soon) - NVIDIA Isaac Sim, VSLAM, and Nav2 navigation
- **Module 4: Vision-Language-Action** (Coming Soon) - LLM-powered voice-controlled robotics
- **Capstone Project** (Coming Soon) - Build "The Autonomous Humanoid Assistant"

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ and npm
- Git
- (Optional) ROS 2 Humble for code verification

### Installation

```bash
# Clone the repository
git clone https://github.com/your-org/physical-ai-textbook.git
cd physical-ai-textbook

# Install dependencies
npm install

# Start the development server
npm start
```

The site will open at `http://localhost:3000`

### Build for Production

```bash
npm run build
```

This generates static content into the `build` directory.

## 📖 Textbook Structure

```
docs/
├── intro.md                    # Homepage
├── glossary.md                 # Robotics terminology
├── module-1-ros2/              # ROS 2 Foundations
│   ├── index.md                # Module overview
│   ├── ch1-middleware.md       # Chapter 1
│   ├── ch2-nodes-topics.md     # Chapter 2
│   ├── ch3-services-actions.md # Chapter 3
│   ├── ch4-rclpy-control.md    # Chapter 4
│   ├── ch5-urdf-modeling.md    # Chapter 5
│   └── exercises/              # Hands-on exercises
└── appendix/                   # Reference materials
```

## 🎯 Learning Objectives

By completing this textbook, you will be able to:

1. **Create ROS 2 nodes** that control humanoid robot joints
2. **Build physics simulations** with sensors (LiDAR, depth cameras, IMU)
3. **Configure Nav2** for humanoid navigation and path planning
4. **Implement voice-to-action pipelines** using LLMs and Whisper
5. **Design and deploy** autonomous humanoid robots in simulation

## 🛠️ Technologies Covered

- **ROS 2 Humble** (Long-Term Support)
- **Gazebo 11** for physics simulation
- **Unity 2022.3 LTS** for high-fidelity visualization
- **NVIDIA Isaac Sim 2023.1+** for photorealistic simulation
- **Isaac ROS** for hardware-accelerated perception
- **Nav2** for robot navigation
- **OpenAI Whisper** for voice recognition
- **LLMs** (GPT-4, Claude, or open-source) for cognitive planning

## 👥 Target Audience

- **Undergraduate/Graduate Students** in Computer Science, Robotics, or Engineering
- **Industry Professionals** upskilling in Physical AI and humanoid robotics
- **Instructors** teaching robotics courses (10-14 week curriculum)
- **Hobbyists and Makers** interested in advanced robotics

## 📝 Contributing

See [quickstart.md](./specs/001-physical-ai-textbook/quickstart.md) for detailed contributor guidelines.

### Quick Contribution Guide

1. Fork the repository
2. Create a feature branch (`git checkout -b chapter-1-6-new-topic`)
3. Follow the 5-part pedagogical structure:
   - Learning Objectives
   - Conceptual Explanation
   - Code Examples
   - Hands-On Exercises
   - Comprehension Questions
4. Ensure chapters are ≤ 3000 words
5. Verify all code examples execute in target environments
6. Submit a pull request

## 📄 License

This textbook is licensed under the **MIT License**. See [LICENSE](./LICENSE) for details.

Educational content is designed for open access and free distribution.

## 🙏 Acknowledgments

- **ROS 2 Community** for the Robot Operating System
- **NVIDIA** for Isaac Sim and Isaac ROS
- **Gazebo Team** for physics simulation tools
- **Unity Technologies** for Unity Robotics Hub
- **Docusaurus Team** for the documentation framework

## 📬 Contact

- **Issues**: [GitHub Issues](https://github.com/your-org/physical-ai-textbook/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-org/physical-ai-textbook/discussions)

---

**Built with** [Docusaurus](https://docusaurus.io/) | **Powered by** Physical AI Education
