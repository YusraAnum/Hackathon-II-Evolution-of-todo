# Data Model: In-Memory Todo System (Phase 1)

## Todo Entity

The Todo entity represents a single task in the system with the following attributes:

### Attributes

- **id** (string): Unique identifier assigned automatically upon creation
- **description** (string): Text content describing the task
- **status** (string): Either "incomplete" or "complete"
- **created_at** (datetime): Timestamp automatically assigned upon creation

### Valid Values

- **status**: Only accepts "incomplete" or "complete" values
- **id**: Generated using UUID4 to ensure uniqueness
- **description**: Any valid string representing the task description
- **created_at**: Automatically set to current datetime when the Todo is created

## Relationships

- The system maintains a single collection of Todo items in memory
- Each Todo item has a unique identifier that serves as the key in the in-memory storage

## Storage Mechanism

- Todos are stored in an in-memory dictionary (hash map) where:
  - Key: The unique identifier (id) of the Todo item
  - Value: The Todo object itself
- Storage is ephemeral and exists only during runtime
- No persistence beyond program execution