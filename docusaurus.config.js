// @ts-check
// Note: type annotations allow type checking and IDEs autocompletion

const {themes} = require('prism-react-renderer');
const lightTheme = themes.github;
const darkTheme = themes.dracula;

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Physical AI & Humanoid Robotics',
  tagline: 'Bridging the Digital Brain and the Physical Body',
  favicon: 'img/favicon.ico',

  // Set the production url of your site here
  url: 'https://waseem4100.github.io',
  // Set the /<baseUrl>/ pathname under which your site is served
  // Using '/' for local dev, switch to '/AI-Native-Book/' for GitHub Pages
  baseUrl: process.env.NODE_ENV === 'production' ? '/AI-Native-Book/' : '/',

  // GitHub pages deployment config.
  organizationName: 'Waseem4100',
  projectName: 'AI-Native-Book',

  onBrokenLinks: 'throw',

  // Even if you don't use internalization, you can use this field to set useful
  // metadata like html lang. For example, if your site is Chinese, you may want
  // to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  markdown: {
    mermaid: true,
    hooks: {
      onBrokenMarkdownLinks: 'warn',
    },
  },
  themes: ['@docusaurus/theme-mermaid'],

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          routeBasePath: '/', // Docs-only mode
          sidebarPath: require.resolve('./sidebars.js'),
          editUrl:
            'https://github.com/Waseem4100/AI-Native-Book/tree/master/',
        },
        blog: false, // Disable blog
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      // Replace with your project's social card
      image: 'img/docusaurus-social-card.jpg',
      navbar: {
        title: 'Physical AI Textbook',
        logo: {
          alt: 'Physical AI Logo',
          src: 'img/logo.svg',
        },
        items: [
          {
            type: 'docSidebar',
            sidebarId: 'tutorialSidebar',
            position: 'left',
            label: 'Textbook',
          },
          {
            href: 'https://github.com/your-org/physical-ai-textbook',
            label: 'GitHub',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Textbook',
            items: [
              {
                label: 'Introduction',
                to: '/',
              },
              {
                label: 'Module 1: ROS 2',
                to: '/module-1-ros2/',
              },
              {
                label: 'Glossary',
                to: '/glossary',
              },
            ],
          },
          {
            title: 'Resources',
            items: [
              {
                label: 'ROS 2 Documentation',
                href: 'https://docs.ros.org/en/humble/',
              },
              {
                label: 'Gazebo Documentation',
                href: 'http://classic.gazebosim.org/',
              },
              {
                label: 'Isaac Sim Documentation',
                href: 'https://docs.omniverse.nvidia.com/isaacsim/',
              },
            ],
          },
          {
            title: 'Community',
            items: [
              {
                label: 'GitHub',
                href: 'https://github.com/your-org/physical-ai-textbook',
              },
              {
                label: 'Discussions',
                href: 'https://github.com/your-org/physical-ai-textbook/discussions',
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} Physical AI Textbook. Built with Docusaurus.`,
      },
      prism: {
        theme: lightTheme,
        darkTheme: darkTheme,
        additionalLanguages: ['python', 'bash', 'yaml', 'xml', 'json'],
      },
    }),
};

module.exports = config;
