# **Software Requirement Specification**

## **Purpose**

This program aims to provide a simulator and solver for the Mastermind game.

## **Target Users**

### **General Public**

- **Availability**: Ensure easy accessibility for users without technical knowledge.

  - **Packaging**: Package our program as a Python project for easy installation via pip.

  - **Compilation**: Consider compiling the program into an executable (.exe) for Windows users who may not have Python installed.

  - **Distribution**: Share the program on various forums, blogs, Discord servers, etc.

- **Accessibility**: Design the program to be user-friendly and intuitive.

  - **Game Rules**: Clearly explain the game rules within the program.

  - **Instructions**: Provide tips on how to control the game.

  - **Documentation**: Offer clear documentation for installation, usage, and uninstallation.

  - **Troubleshooting**: Include instructions for troubleshooting and seeking help.

  - **Community**: Create a space for user discussion and community building, such as a discussion page.

### **Developers**

- **Availability**: Make the source code easily accessible for contributions.

  - **Public Repository**: Host the repository on GitHub as a public repo.

  - **License**: Use the MIT License.

  - **Promotion**: Share the program on technical forums, blogs, and Discord.

- **Accessibility**: Ensure the program is easy to understand, maintain, and modify.

  - **Organization**: Structure the code clearly and follow coding conventions.

  - **Documentation**: Use docstrings and comments to explain code functionality.

  - **Contribution Guidelines**: Provide clear instructions for contributing to the project.

  - **Flexibility**: Design the program to allow easy modifications and extensions.

- **Features**: Offer special features for developers.

  - Support for extensions and plug-ins.

  - Command line interface (CLI) support.

## **User Interface Design (TUI / GUI)**

1. **Main Menu**: Display options to navigate to other menus.

2. **New Game Menu**: Allow users to select their preferred game mode.

3. **Past Games Menu**: Users can resume or view past games and delete them if desired. Implement scrolling for a large number of games, with the latest game at the top.

4. **Settings Menu**: Options to clear cache, clear data, and check the program version.

5. **Game Board**: Display during gameplay, with customizable color or number representation.

6. **Help Feature**: Users can enter “?” or click a help button for game interpretation assistance.

7. **Initial Instructions**: Show game instructions during the first run.

8. **Difficulty Levels**: Allow users to choose from various difficulty levels (e.g., easy: 6x4-10, medium: 6x4-6, hard: 8x5-10).

9. **Default Options**: Provide preset options for easy setup.

10. **Display Settings**: Enable users to choose between number or color dots for display/input.

## **Documentation**

1. Provide guides for installation and uninstallation.

2. Include troubleshooting resources.

3. Ensure the documentation is visually engaging.

4. Include API documentation.

5. Explain the software design at a high level.

## **AI-Solver**

1. Implement an algorithm for the computer to solve the puzzle.

2. Include various solving strategies, such as brute-force, AI model guessing, random guessing, and strategic guessing algorithms.

3. Consider using Cython for the solver to enhance performance through compilation.
