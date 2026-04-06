# Host Pricing Assistant

## Video Demonstration

https://youtu.be/feo0r0aSzsU

**Key Sections**
- Live Demo: 2:03 – 6:22

---

## Overview

Host Pricing Assistant is a full-stack web application that helps Airbnb-style hosts determine a recommended nightly price for their listing.

This project was built to transform prior regression-based machine learning coursework into a production-style application. Instead of stopping at notebook analysis, the project extends that work into a complete product with a frontend, backend, persistence layer, and live model inference.

The application allows a host to input listing details and optionally provide a nearby market price. It then generates a recommended nightly rate using a trained Ridge Regression model and saves the result to recommendation history.

---

## Problem

Pricing short-term rental listings can be difficult for hosts, especially without access to reliable market tools or structured pricing guidance. Many hosts rely on guesswork or incomplete comparisons, which can lead to underpricing, overpricing, or inconsistent decisions.

The goal of this project was to simulate a lightweight pricing assistant that:

- uses structured listing data
- incorporates market context when available
- produces a consistent, data-driven nightly price recommendation
- feels like a real product workflow rather than a standalone notebook

---

## Solution

Host Pricing Assistant provides a simple interface where a host can enter listing details and receive a recommended nightly price using a trained machine learning model.

The project combines:

- a React + TypeScript frontend for user interaction
- a FastAPI backend for API logic and inference
- a SQLite database for recommendation history
- a cleaned Airbnb-style dataset for training
- a Ridge Regression model for live pricing recommendations

The application also supports optional market-price input. If the user does not provide an observed market price, the backend estimates one using similar listings from the processed training data.

---

## Features

### User Inputs

The application accepts the following listing details:

- Listing Title
- City
- Property Type
- Beds
- Bathrooms
- Accommodates
- Observed Market Price (optional)

### Core Product Behavior

- Generates a recommended nightly price using a trained Ridge Regression model
- Allows Observed Market Price to be left blank
- Estimates a fallback market price when the user does not provide one
- Saves each recommendation to SQLite
- Displays recommendation history
- Automatically refreshes history after each submission
- Shows newest recommendations first
- Supports show/hide history toggle
- Correctly distinguishes between:
  - Observed Market Price
  - Estimated Market Price

---

## Example Workflow

1. The user enters listing details in the frontend form  
2. The user optionally enters an observed nearby market price  
3. The frontend sends the request to the FastAPI backend  
4. The backend validates the request  
5. If no market price is provided, the backend estimates one using fallback logic  
6. The inference layer loads the trained Ridge Regression model  
7. The model predicts a nightly price  
8. The backend stores the result in SQLite  
9. The frontend displays the recommendation and updated history  

---

## Tech Stack

### Frontend
- React  
- TypeScript  
- Vite  

### Backend
- FastAPI  
- Pydantic  
- SQLModel  

### Database
- SQLite  

### Machine Learning
- Python  
- pandas  
- scikit-learn  
- joblib  

### Development Workflow
- VS Code  
- Jupyter Notebook  

---

## Architecture

### Frontend Responsibilities

- Collect user input  
- Validate form values  
- Send API requests  
- Display recommended prices  
- Render recommendation history  
- Handle UX features such as toggling and labeling  

API logic is centralized in `client.ts`.

### Backend Responsibilities

- Validate requests with Pydantic  
- Route endpoints using FastAPI  
- Separate logic into services  
- Call ML inference layer  
- Estimate fallback market prices  
- Persist results in SQLite  

### Database Responsibilities

- Store recommendation history  
- Store final market price used  
- Track fallback usage  

### Machine Learning Responsibilities

- Train regression models  
- Save model artifacts  
- Load model for inference  
- Separate training and inference logic  

---

## Machine Learning Approach

### Data Source

The model was trained on a cleaned Airbnb-style dataset derived from:

- `airnb.csv`

Original columns included:

- Title  
- Detail  
- Date  
- Price(in dollar)  
- Offer price(in dollar)  
- Review and rating  
- Number of bed  

---

### Data Cleaning

- Detail → `listing_title`  
- Title → parsed into property type and location  
- Date → dropped  
- Price → `nightly_price` (target)  
- Beds extracted from raw field  

---

### Feature Engineering

- Beds used instead of bedrooms  
- `accommodates = beds * 2`  

---

### Property Type Standardization

Standardized categories:

- house  
- apartment  
- cabin  
- condo  
- room  
- villa  
- tiny_home  
- treehouse  
- cottage  
- guesthouse  
- hotel  
- loft  
- farm_stay  
- guest_suite  
- bungalow  
- chalet  
- unique_stay  
- other  

---

### Training Features

- property_type  
- city  
- beds  
- accommodates  
- competitor_avg_price  

Target:

- nightly_price  

---

### Model Selection and Evaluation

Two regression models were trained and compared:

#### Linear Regression
- MAE: ~20.03  
- RMSE: ~45.16  
- R²: ~0.9075  

#### Ridge Regression
- MAE: ~11.09  
- RMSE: ~29.42  
- R²: ~0.9608  

Ridge Regression was selected as the production model due to significantly lower error and higher explanatory power.

---

### Market Price Logic

Fallback hierarchy:

1. city + property type  
2. city  
3. property type  
4. global average  

---

## Recommendation History

Stores:

- listing details  
- recommended price  
- market price used  
- fallback flag  

Displays:

- Observed Market Price  
- Estimated Market Price  

---

## Project Structure

```
host-pricing-assistant/
├── backend/
├── data/
├── frontend/
└── .gitignore
```

---

## Setup Instructions

### Clone

```bash
git clone https://github.com/aedingbo/host-pricing-assistant.git
cd host-pricing-assistant
```

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Backend runs at:

```
http://127.0.0.1:8000
```

Docs:

```
http://127.0.0.1:8000/docs
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at:

```
http://localhost:5173
```

---

## API Endpoints

### Health
```
GET /health
```

### Create Recommendation
```
POST /api/v1/recommendations
```

### Get History
```
GET /api/v1/recommendations
```

---

## Key Design Decisions

- React for product-style UI  
- FastAPI for clean backend + ML integration  
- TypeScript for data consistency  
- SQLite for lightweight persistence  
- Ridge Regression for production model  
- Beds instead of bedrooms for data alignment  
- Optional market price for UX  
- Fallback pricing to preserve usability  

---

## Challenges

- Raw data inconsistencies → solved with parsing  
- Bedrooms mismatch → switched to beds  
- Property type chaos → standardized taxonomy  
- Market price ambiguity → engineered + fallback  
- Schema drift → reset SQLite  
- UX issues → improved validation + labeling  

---

## Why This Project Matters

This project demonstrates:

- notebook → production ML workflow  
- full-stack architecture  
- real data cleaning decisions  
- model evaluation + deployment  
- product-level thinking  

---

## Future Improvements

- add review features  
- add advanced models  
- improve location modeling  
- deploy to cloud  
- add dashboards  

---

## Summary

This project transforms regression-based ML work into a full-stack application.

It combines:

- data cleaning  
- feature engineering  
- model training  
- backend integration  
- frontend UX  

The result is a complete pricing assistant that reflects both machine learning and software engineering skills.
