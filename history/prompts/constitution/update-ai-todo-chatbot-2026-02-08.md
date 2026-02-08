---
id: phr-constitution-update-ai-todo-chatbot-2026-02-08
title: Update Constitution for AI Todo Chatbot
stage: constitution
created: 2026-02-08
tags: [constitution, phase-3, ai, todo, chatbot]
---

# Update Constitution for AI Todo Chatbot

## Summary
Updated the project constitution to reflect Phase 3 requirements for extending the existing Todo App into an AI-powered chatbot. The new constitution maintains the Spec-Driven Development workflow while incorporating AI-specific requirements, MCP tools, and the technology stack for the AI Todo Chatbot.

## PROMPT_TEXT
# Phase 3 Constitution – AI Todo Chatbot

## Goal
Extend the existing Phase 2 Todo App into an AI-powered chatbot
using Spec-Driven development
Don't touch phase 1

## Core Rules

1. No manual code without tasks
2. Fix all Phase-2 frontend & backend errors first
3.. Backend must be stateless
4. Conversation state stored in database
5. MCP tools are the only way to mutate data
6. JWT authentication is mandatory
7. No breaking existing Phase-2 functionality

## Tech Stack (Locked)
- Frontend: Next.js + OpenAI ChatKit
- Backend: FastAPI + SQLModel
- AI: OpenAI Agents SDK
- MCP: Official MCP SDK
- Auth: Better Auth (JWT)
- DB: Neon PostgreSQL

## Quality Rules
- Zero runtime errors
- Graceful error handling
- Clean UI
- Production-ready code

- ## Agent Behavior
- Always confirm actions
- Handle errors gracefully
- Never hallucinate task IDs
- Use MCP tools strictly

## User Input

```text
# Phase 3 Constitution – AI Todo Chatbot

## Goal
Extend the existing Phase 2 Todo App into an AI-powered chatbot
using Spec-Driven development
Don't touch phase 1

## Core Rules

1. No manual code without tasks
2. Fix all Phase-2 frontend & backend errors first
3.. Backend must be stateless
4. Conversation state stored in database
5. MCP tools are the only way to mutate data
6. JWT authentication is mandatory
7. No breaking existing Phase-2 functionality

## Tech Stack (Locked)
- Frontend: Next.js + OpenAI ChatKit
- Backend: FastAPI + SQLModel
- AI: OpenAI Agents SDK
- MCP: Official MCP SDK
- Auth: Better Auth (JWT)
- DB: Neon PostgreSQL

## Quality Rules
- Zero runtime errors
- Graceful error handling
- Clean UI
- Production-ready code

- ## Agent Behavior
- Always confirm actions
- Handle errors gracefully
- Never hallucinate task IDs
- Use MCP tools strictly
```

## RESPONSE_TEXT

The constitution was successfully updated from version 1.1.0 to 2.0.0, with major changes to reflect Phase 3 requirements:

1. Added AI Todo Chatbot Extension Goal principle
2. Added Fix All Phase-2 Errors First Rule
3. Added Backend Statelessness Rule
4. Added Database Conversation State Rule
5. Added MCP Tools Data Mutation Rule
6. Added JWT Authentication Mandate
7. Added No Breaking Existing Functionality Rule
8. Updated technology stack to include AI and MCP components
9. Updated quality rules to include AI-specific requirements
10. Updated agent behavior to emphasize MCP tools and error handling

Removed Phase 1-specific principles that were no longer applicable to Phase 3.

## Changes Made
- Updated constitution version from 1.1.0 to 2.0.0 (major update)
- Added Phase 3-specific principles aligned with AI Todo Chatbot goals
- Maintained Spec-Driven Development workflow requirements
- Integrated MCP tools and AI-specific constraints
- Preserved existing quality and process rules where applicable

## Files Modified
- .specify/memory/constitution.md