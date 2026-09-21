# Privacy Policy

**Universal Agent Skills** operates under strict data sovereignty and local privacy principles.

## Core Privacy Principles

### 1. Zero External Telemetry
This repository and its Model Context Protocol tools collect no telemetry, analytics, or behavioral tracking data. No background requests are dispatched to tracking servers or analytics collectors.

### 2. Local Execution and Storage
All tools operate locally on the host machine or within the user designated runtime environment. Data passed to tools remains strictly within your execution session and is never persisted to external cloud databases without explicit user configuration.

### 3. Credential and Secret Isolation
API keys and environment variables supplied to the server are loaded strictly in memory for authorized API interactions (such as designated search or LLM providers). Credentials are never logged, never cached to disk, and never shared across tools.

### 4. Network Transparency
Tools only initiate outbound network connections to user requested endpoints or documented provider APIs. All network traffic adheres strictly to standard HTTPS encryption protocols.

### 5. Open Source Auditability
The entirety of the codebase is open source under the MIT License. Users and security teams can independently verify all network calls, file accesses, and data handling procedures directly within the repository source code.

## Contact and Questions
For any privacy inquiries or verification requests, contact the project maintainer:
* Maintainer: Mehansh Barthwal
* Email: mehanshbarthwal@gmail.com
