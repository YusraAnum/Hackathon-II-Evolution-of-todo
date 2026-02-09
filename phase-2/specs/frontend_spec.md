# Frontend Specification - Todo Web Application

## Overview
This specification defines the frontend web application for the Todo application using Next.js 14 with Tailwind CSS and Better Auth for authentication.

## Tech Stack
- Next.js 14: React framework with App Router for modern web development
- Tailwind CSS: Utility-first CSS framework for styling
- Better Auth: Authentication library for secure user management

## Pages

### /signup
- Purpose: Allow new users to create an account
- Components: AuthForm with email and password fields
- Behavior: Redirect to /dashboard after successful signup
- Validation: Email format and password strength requirements

### /login
- Purpose: Allow existing users to authenticate
- Components: AuthForm with email and password fields
- Behavior: Redirect to /dashboard after successful login
- Validation: Email and password validation
- Link: "Forgot password?" and "Don't have an account? Sign up"

### /dashboard
- Purpose: Main application interface showing user's todos
- Components: Navbar, TodoList, TodoItem
- Behavior: Shows todos for authenticated user only
- Functionality: Add, update, delete, and toggle todos
- Redirect: If not authenticated, redirect to /login

## Component Structure

### AuthForm
- Reusable component for authentication flows
- Handles both signup and login forms
- Includes validation and error handling
- Manages form state and submission

### TodoList
- Container for displaying multiple TodoItem components
- Shows loading state when fetching todos
- Handles empty state when no todos exist
- Manages adding new todos

### TodoItem
- Displays individual todo with title and completion status
- Provides controls for editing, deleting, and toggling completion
- Shows creation timestamp
- Supports inline editing

### Navbar
- Navigation bar visible on authenticated pages
- Contains user profile information
- Logout button
- Links to different sections of the app

## Authentication Behavior
- Protected routes: Unauthenticated users redirected to /login
- Session management: Automatic token refresh and validation
- Logout: Clears local session and redirects to /login
- Auto-login prevention: Check for existing session on app load

## UI Requirements
- Responsive design supporting mobile, tablet, and desktop screens
- Clean, intuitive user interface with clear visual hierarchy
- Consistent color scheme and typography using Tailwind CSS
- Loading states for API interactions
- Error messages with clear feedback to users
- Accessible markup following WCAG guidelines

## User Experience
- Smooth navigation between pages with minimal loading times
- Immediate visual feedback for user actions (adding, toggling, deleting todos)
- Clear indication of completed vs. pending todos
- Intuitive form validation with helpful error messages
- Keyboard navigation support for accessibility

## Performance Requirements
- Page load time under 3 seconds on average connection
- Fast response to user interactions (< 200ms perceived delay)
- Optimized bundle size for faster initial loads

## Authentication Integration

- Authentication must be implemented using the Better Auth client SDK on the frontend.
- Authentication tokens must be stored in HTTP-only cookies (NOT localStorage).
- All API requests from the frontend must include credentials using:
  fetch(..., { credentials: "include" })
- Route protection must be handled using Next.js middleware.
- Unauthenticated users attempting to access protected routes must be redirected to /login.

## Environment Configuration

- The backend API base URL must be stored in an environment variable:
  NEXT_PUBLIC_API_URL
- All frontend API calls must use:
  ${process.env.NEXT_PUBLIC_API_URL}/api/v1/...

## Data Fetching Strategy

- Todo data fetching must be handled in Client Components.
- Use native fetch() inside useEffect for retrieving todos.
- Create, update, delete, and toggle actions must be performed using client-side API calls.
- No external state management or data-fetching libraries are allowed (no Redux, React Query, SWR, etc.).

## Required Folder Structure

The frontend must follow the monorepo structure defined in the constitution:

apps/frontend/
  app/
    login/
    signup/
    dashboard/
  components/
  lib/
    api.ts
    auth.ts
  middleware.ts

No frontend code may be placed outside apps/frontend/.