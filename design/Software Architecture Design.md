# **Architecture Design**

## **1\. Introduction**

- **Purpose**: This document outlines the architectural design of the Mastermind game simulator to ensure maintainability, scalability, and flexibility.

- **Scope**: The architecture covers the overall structure, components, and technologies used in the development of the application.

## **2\. Architecture Overview**

### **Three Layers Design**

- **Representation Layer**: Handles output to users and input from users.

- **Business Logic Layer**: Responsible for implementing the core business logic.

- **Data Access Layer**: Manages interactions between the business logic and data sources.

### **High-level vs Low-level Modules**

- **High-level Modules**: These include program procedures whose modifications can directly impact user experience. They define the program’s overall design.

- **Low-level Modules**: These implement the steps in higher-level procedures and can be organized in a library folder. Their changes do not affect the user experience directly.

### **Repository Pattern**

- Implement a repository pattern to create a separation between the storage mechanism and I/O operations. The business logic will interact with a concrete repository class rather than the data source directly.

### **Event Driven Architecture**

- Utilize event-driven architecture to decouple components, facilitating easy integration between the UI and business logic. This approach allows for straightforward addition of CLI, TUI, or GUI interfaces.

### **API Documentation**

- Provide clear API documentation for developers to understand how to interact with the game's components.

## **3\. Components**

### **Representation Layer**

- **View (TUI / GUI)**:

  - Main Menu

  - Game Mode Selector

  - Game Difficulty Selector

  - Gameboard Display

  - History Display

  - Settings Menu

  - Help Page

- **CLI**:

  - Trigger various events and pass appropriate data, e.g.:

    - mastermind new \<player1\> \<player2\> \<difficulty\> ➜ \<game id\>

    - mastermind retrieve \<game id\> ➜ \<game information\>

    - mastermind play \<game id\> \<action\> \<input\> ➜ \<success?\>

    - mastermind delete \<game id\> ➜ \<success?\>

    - mastermind install \<plugin path\> ➜ \<success?\> (\<name\>)

    - mastermind uninstall \<plugin name\> ➜ \<success?\>

    - mastermind config \<setting name\> \<new value\> ➜ \<success?\>

### **Business Logic Layer**

- **Event Handling Layer**:

  - **Handler**: Entities that process input from the view/UI, e.g.:

    - entered\_a\_guess(guess) ➜ validation.valid | validation.invalid

  - **HandlerPipeline**: Defines a procedure with a series of handlers as steps, providing a shared namespace:

    - StartNewGame(parameters)

- **Data Models**: Data classes that store and validate data, including:

  - GameParameter

  - GameStatus

  - GameEntities

  - Gameboard

  - Game

- **Services**: Modules utilized by the HandlerPipeline, typically operating on data models.

### **Adapter Layer**

- **Storage**:

  - Repository Design

  - I/O Interface / Adapter

- **UI Adapter**: Adjusts UI implementation based on the environment (e.g., certain frameworks may not work in Jupyter).

### **Lib (Lower-level Modules)**

- Event System

- Plugin System

## **4\. Technology Choices**

### **Programming Languages**

- **Python**: For the main application (UI and game logic).

- **Cython**: For performance-critical components (e.g., AI solver).

### **Supported Environment**

- Windows

- Linux

- Mac

- Android

- Jupyter Notebook

### **Testing Framework**

- **Unittest*- and **Pytest**

### **Version Control**

- **GitHub**: For source code management and collaboration.

### **Publishing Platform**

- GitHub

- PyPI

- Conda

## **5\. Non-Functional Requirements**

### **Performance**

- The application (TUI and GUI) should load within 5 seconds during the first run after installation.

- The GUI should operate without visible lag.

- The CLI should respond within 1 second most of the time, except during the first run.

- The AI-Solver should solve within 5 seconds. Alternative strategies should be employed if it takes longer, with user-configurable time limits.

### **Flexibility**

- The architecture should easily support plugins and extensions.

- It should allow for straightforward modifications and changes to underlying implementations.

### **Readability and Maintainability**

- The code should adhere to formatting and linting standards (e.g., using Ruff).

- All public classes and functions must include docstrings, with details proportional to their complexity.

- Docstrings should follow Google style.

- Comprehensive API documentation and user guides should be provided.
