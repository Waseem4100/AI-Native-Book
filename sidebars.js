/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.
 */

// @ts-check

/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  tutorialSidebar: [
    {
      type: 'doc',
      id: 'intro',
      label: 'Introduction',
    },
    {
      type: 'category',
      label: 'Module 1: ROS 2 Foundations',
      collapsed: false,
      items: [
        'module-1-ros2/index',
        'module-1-ros2/ch1-middleware',
        'module-1-ros2/ch2-nodes-topics',
        'module-1-ros2/ch3-services-actions',
        'module-1-ros2/ch4-rclpy-control',
        'module-1-ros2/ch5-urdf-modeling',
        {
          type: 'category',
          label: 'Exercises',
          collapsed: true,
          items: [
            'module-1-ros2/exercises/ex1-first-node',
            'module-1-ros2/exercises/ex2-publisher-subscriber',
            'module-1-ros2/exercises/ex3-urdf-humanoid',
          ],
        },
      ],
    },
    {
      type: 'category',
      label: 'Appendix',
      collapsed: true,
      items: [
        'appendix/prerequisites',
        'appendix/troubleshooting',
        'appendix/resources',
      ],
    },
    {
      type: 'doc',
      id: 'glossary',
      label: 'Glossary',
    },
  ],
};

module.exports = sidebars;
