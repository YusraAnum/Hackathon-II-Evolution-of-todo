# Hackathon II: Evolution of Todo App - Phase 1

## Overview
This is Phase 1 of the Hackathon II: Evolution of Todo App project, implementing an in-memory CLI-based Todo application following Spec-Driven Development (SDD) methodology. This phase focuses on creating a foundational todo system with core functionality.

## Phase 1 Goals
- Implement an in-memory CLI-based todo application
- Establish a solid foundation for future phases
- Demonstrate Spec-Driven Development workflow
- Include comprehensive testing and documentation

## Features
- **CLI Interface**: Command-line interface for todo management
- **Core Operations**: Add, list, complete, and delete todo items
- **In-Memory Storage**: Todos are stored in memory for this phase
- **Testing Framework**: Comprehensive tests for all functionality
- **Specification Artifacts**: Complete SDD documentation and planning

## Project Structure
```
├── src/                    # Source code
│   ├── cli.py             # Command-line interface
│   ├── models/            # Data models
│   │   └── todo.py        # Todo model
│   ├── lib/               # Library modules
│   │   └── storage.py     # Storage implementation
│   └── services/          # Business logic services
│       └── todo_service.py # Todo business logic
├── specs/                 # Specification artifacts
│   └── todo-system/       # Todo system specifications
├── tests/                 # Test suite
├── main.py               # Entry point
├── comprehensive_test.py # Comprehensive test runner
└── README.md             # This file
```

## Included Artifacts
This repository intentionally includes full Spec-Driven Development artifacts:
- **.claude/**: Claude Code configuration and agent files
- **.specify/**: SDD memory and scripts
- **history/**: Development history
- **specs/**: Detailed specifications and plans

## Prerequisites
- Python 3.8+

## How to Run
1. Clone the repository
2. Navigate to the project directory
3. Run the application:
   ```bash
   python main.py
   ```

## Available Commands
- `add <task>`: Add a new todo
- `list`: List all todos
- `complete <id>`: Mark a todo as complete
- `delete <id>`: Delete a todo

## Testing
Run the test suite:
```bash
python -m pytest tests/
```

Or run the comprehensive test:
```bash
python comprehensive_test.py
```

## Development Approach
This project follows strict Spec-Driven Development (SDD) methodology:
1. Constitution
2. Specification
3. Plan
4. Tasks
5. Implementation

All AI agents operate within these defined rules, ensuring consistent and well-documented development.

## Next Phases
Future phases will expand upon this foundation with persistent storage, web interface, and advanced features.