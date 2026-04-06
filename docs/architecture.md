# System Architecture

## Overview

The Host Pricing Assistant is a full-stack application that combines a React frontend, a FastAPI backend, a machine learning inference layer, and a SQLite database.

The system is designed to simulate a production-style workflow where user input flows through validation, business logic, model inference, and persistence before returning a result to the UI.

---

## High-Level Architecture

```
Frontend (React)
        ↓
Backend API (FastAPI)
        ↓
Service Layer (Business Logic)
        ↓
ML Inference (Ridge Regression)
        ↓
SQLite Database (Persistence)
        ↓
Response to Frontend
```

---

## Component Breakdown

### Frontend (React + TypeScript)

Responsible for:

- collecting user input
- validating form fields
- sending API requests
- displaying price recommendations
- rendering recommendation history
- handling UX features (toggle, ordering, labeling)

The frontend communicates with the backend through a centralized API client.

---

### Backend API (FastAPI)

Responsible for:

- handling HTTP requests
- validating input with Pydantic schemas
- routing requests to appropriate services
- returning structured responses

Key endpoints:

- `GET /health`
- `POST /api/v1/recommendations`
- `GET /api/v1/recommendations`

---

### Service Layer

Responsible for:

- implementing pricing logic
- handling fallback market price estimation
- calling the ML inference layer
- preparing data for persistence

This layer separates business logic from API routing.

---

### Machine Learning Layer

Responsible for:

- loading the trained Ridge Regression model
- constructing feature inputs for prediction
- generating recommended nightly prices

Inputs:

- property_type
- city
- beds
- accommodates
- market price (observed or estimated)

---

### Database (SQLite)

Responsible for:

- storing recommendation history
- storing the market price used in predictions
- tracking whether fallback logic was used

Key stored fields:

- listing details
- recommended price
- market price
- fallback flag
- explanation

---

## Data Flow

1. User submits listing details from the frontend
2. Backend validates request data
3. Service layer determines if market price is provided
4. If missing, fallback market price is estimated
5. ML model predicts recommended price
6. Result is saved in SQLite
7. Response is returned to frontend
8. Frontend updates UI and history

---

## Key Design Principles

### Separation of Concerns

Each layer has a clear responsibility:

- frontend handles UI
- backend handles API logic
- service layer handles business logic
- ML layer handles prediction
- database handles persistence

---

### Alignment Between Data, Model, and UI

- frontend inputs match model features
- cleaned dataset matches application schema
- model expects the same fields provided by the user or fallback logic

---

### Production-Oriented Structure

The application avoids:

- mixing ML logic into API routes
- relying on notebook code in production
- tightly coupling UI and backend logic

Instead, it follows a modular structure that mirrors real-world systems.

---

## Summary

The architecture demonstrates how a machine learning model can be integrated into a full-stack application with clear data flow, modular design, and product-level behavior.

The system emphasizes:

- clean separation between components
- realistic handling of missing inputs
- alignment between training data and production inference
