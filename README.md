# Real-Time Chat Application

Welcome to the **Real-Time Chat Application**, a socket-based Python project designed for seamless and efficient real-time communication.

## Features

- **Player Status Management**:
  - Handles various player statuses: manual disconnections, bans, and active states.

- **Graceful Termination of Child Processes**:
  - Ensures proper termination of all child processes, avoiding zombie processes.

- **Administrator Message Monitoring**:
  - Provides a separate terminal window for administrators to view all messages, including private user messages.

- **Administrator Communication**:
  - Enables administrators to send and receive messages from users in real-time.

- **Blocking During Gameplay**:
  - Prevents blocked players from reconnecting to the current game session.

- **Broadcast Notifications for Blocking**:
  - Notifies all players when someone is blocked.

- **File Management for Blocked Users**:
  - Automatically deletes all files associated with a blocked player.
  - For voluntary disconnections or system failures, retains only the user's cookie folder to allow reconnection later.

- **Robust Error Handling**:
  - Highly fault-tolerant system tested across diverse scenarios to ensure stability and resilience against exceptions.

## Technologies Used

- **Python**: Core programming language for server and client implementation.
- **Socket Programming**: For real-time communication.
- **Multithreading**: To handle multiple clients and processes simultaneously.
