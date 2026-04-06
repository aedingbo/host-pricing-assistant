# Technical Decisions

## Overview

This document captures the key technical decisions, tradeoffs, and architectural structure behind the Host Pricing Assistant application.

The goal of this project was not just to build a working application, but to demonstrate how a machine learning workflow can be extended into a production-style system with clear separation of concerns, realistic data constraints, and product-level behavior.

---

## System Architecture

The application follows a full-stack architecture with four primary layers:

1. Frontend (React + TypeScript)
2. Backend API (FastAPI)
3. Machine Learning Layer (scikit-learn)
4. Persistence Layer (SQLite)

### High-Level Flow

1. User submits listing data through the frontend
2. Frontend sends a request to the backend API
3. Backend validates input and applies business logic
4. Backend calls the ML inference layer
5. ML model generates a recommended price
6. Backend saves the result to SQLite
7. Response is returned to the frontend
8. Frontend updates the UI and recommendation history

---

## Frontend Decisions

### Framework Choice: React

React was selected to:

- simulate a real product UI workflow
- demonstrate frontend engineering capability
- support component-based architecture
- enable dynamic state updates for history and recommendations

### Language: TypeScript

TypeScript was used to:

- enforce consistent data contracts between frontend and backend
- reduce runtime errors
- improve developer clarity when handling API responses

### API Layer Separation

A dedicated API client (`client.ts`) was created to:

- centralize all backend communication
- keep UI components focused on rendering
- simplify future changes to API endpoints

### UX Decisions

Several UX decisions were made to reflect real product thinking:

- recommendation history is sorted newest-first
- history can be toggled (show/hide)
- numeric inputs can be cleared and re-entered
- labels distinguish between observed vs estimated values
- optional inputs do not block submission

---

## Backend Decisions

### Framework Choice: FastAPI

FastAPI was selected because:

- it provides clear request/response validation via Pydantic
- it integrates well with Python-based ML workflows
- it supports clean, modular API design
- it automatically generates API documentation

### Project Structure

The backend was structured into:

- routes (API endpoints)
- schemas (data validation)
- services (business logic)
- models (database layer)
- core (configuration)

This separation ensures:

- clear responsibility boundaries
- easier debugging
- better scalability for future features

### Service Layer

Business logic was intentionally moved into a service layer to:

- avoid bloating route handlers
- isolate pricing logic
- make the codebase easier to maintain

---

## Database Decisions

### Database Choice: SQLite

SQLite was selected because:

- it is lightweight and requires no setup
- it is sufficient for local MVP development
- it allows quick iteration and schema updates

### Stored Data

Each recommendation stores:

- listing inputs
- recommended price
- market price used
- fallback indicator
- explanation

### Schema Reset Decision

During development, the schema was reset when switching from `bedrooms` to `beds`.

This was chosen over migration because:

- the project is an MVP
- speed and clarity were prioritized over migration tooling

---

## Machine Learning Decisions

### Model Choice: Ridge Regression

Two models were evaluated:

- Linear Regression
- Ridge Regression

Ridge Regression was selected due to:

- lower error metrics (MAE, RMSE)
- higher R²
- better handling of feature variance

### Why Not Build Models From Scratch

Scikit-learn was used because:

- the goal was to productionize ML workflows, not reimplement algorithms
- industry practice relies on well-tested libraries
- time constraints favored integration over theoretical implementation

---

## Data Decisions

### Inspection-First Approach

The dataset was analyzed before designing the application.

This ensured:

- only supported features were used
- the model and UI stayed aligned
- assumptions did not break the pipeline

---

### Bedrooms vs Beds

Original plan:
- use bedrooms

Reality:
- dataset only provided bed counts

Decision:
- switch to beds
- derive accommodates as beds * 2

Reason:
- maintain data integrity
- avoid fabricating features

---

### Property Type Standardization

The raw dataset contained many inconsistent property types.

Solution:

- create a standardized taxonomy
- map raw values into consistent categories

Benefits:

- reduced noise in training
- improved model generalization
- aligned frontend dropdown with backend expectations

---

### Market Price Feature

The dataset did not contain a direct "observed market price."

To solve this:

- a derived feature `competitor_avg_price` was created during training
- based on grouped averages with fallback hierarchy

Hierarchy:

1. city + property type
2. city
3. property type
4. global average

---

## Product Logic Decisions

### Observed Market Price (User Input)

The UI label was changed from:

- "Competitor Average Price"

to:

- "Observed Market Price"

Reason:

- clearer and more intuitive for users
- better reflects how the value is collected

---

### Optional Market Price Input

Initially:
- market price was required

Final decision:
- make it optional

Reason:

- improves usability
- reflects real-world uncertainty
- prevents blocking predictions

---

### Fallback Market Price Logic

If the user does not provide a market price:

- backend estimates one using training-based grouping logic

This ensures:

- predictions always work
- user is not required to know market data
- model behavior stays consistent with training assumptions

---

### History Labeling Fix

Problem:

- history always displayed "Observed Market Price"

Issue:

- misleading when fallback was used

Solution:

- add `used_fallback_market_price` boolean
- conditionally render labels

Result:

- accurate UI
- improved trust in system output

---

## Notebook to Production Transition

A major goal of the project was to transition from:

- Jupyter Notebook experimentation

to:

- production-style inference

Key steps:

- separate training and inference logic
- save trained model artifact
- build inference wrapper
- integrate model into backend service

This avoids:

- copying notebook code into API routes
- mixing experimentation with production logic

---

## Tradeoffs

### Speed vs Perfection

Decisions such as:

- using SQLite instead of Postgres
- resetting schema instead of migrations
- limiting feature set

were made to:

- prioritize delivery
- focus on end-to-end functionality
- complete the MVP within time constraints

---

### Model Complexity vs Interpretability

Ridge Regression was chosen over more complex models because:

- it performed well enough
- it is easier to explain
- it aligns with the regression-focused coursework

---

## Summary

This project demonstrates how to:

- align data, model, and UI
- build a full-stack ML application
- make realistic product decisions under constraints
- transition from notebook-based workflows to production systems

The result is a system that reflects both machine learning understanding and practical engineering execution.
