# Network Security System

A FastAPI application that predicts whether a URL is potentially phishing based on URL and webpage security features. The project includes a MongoDB-backed training pipeline, a browser form for single predictions, and a CSV prediction endpoint.

## Features

- Ingests training data from MongoDB.
- Validates data and checks for feature drift.
- Transforms data with a saved preprocessing pipeline.
- Trains and evaluates several scikit-learn classification models.
- Provides a browser form for entering URL security features.
- Provides a batch prediction endpoint for the existing test CSV.

## Project Structure

```text
app.py                         FastAPI application
main.py                        Standalone training pipeline runner
form_data.py                   Pydantic form schema
requirements.txt               Python dependencies
Network_Data/phisingData.csv   Local source dataset
Network_Security_System/       Pipeline, components, entities, and utilities
templates/form.html            Browser prediction form
valid_data/test.csv            Batch prediction input
final_model/                   Saved model and preprocessor
predicted_output/output.csv    Batch prediction output
Artifacts/                     Timestamped training artifacts
```

## Requirements

- Python 3.9 or newer
- MongoDB connection string
- Network access for MongoDB and, during training, any configured MLflow/DagsHub services

## Installation

Create and activate a virtual environment from the project root:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Create a `.env` file in the project root and add:

```env
MONGODB_URL=your_mongodb_connection_string
```

Keep the connection string private. Do not commit `.env` or credentials to source control.

## Run the Application

Start the FastAPI server from the project root:

```powershell
python app.py
```

The application runs at `http://localhost:8000`.

Useful pages and endpoints:

| Method | Path | Purpose |
| --- | --- | --- |
| GET | `/` | Redirects to the FastAPI documentation |
| GET | `/docs` | Opens Swagger API documentation |
| GET | `/form` | Displays the phishing prediction form |
| POST | `/form` | Reads form fields and returns a prediction in the form page |
| GET | `/train` | Runs the complete training pipeline |
| POST | `/predict` | Predicts rows from `valid_data/test.csv` and writes `predicted_output/output.csv` |

The saved files `final_model/model.pkl` and `final_model/preprocessor.pkl` must exist before using `/form` or `/predict`. Train the project with `GET /train` or run the training script directly:

```powershell
python main.py
```

## Form Fields

The form accepts the following 30 numeric features. Values are encoded as `-1`, `0`, or `1` according to the dataset:

```text
having_IP_Address, URL_Length, Shortining_Service, having_At_Symbol,
double_slash_redirecting, Prefix_Suffix, having_Sub_Domain, SSLfinal_State,
Domain_registeration_length, Favicon, port, HTTPS_token, Request_URL,
URL_of_Anchor, Links_in_tags, SFH, Submitting_to_email, Abnormal_URL,
Redirect, on_mouseover, RightClick, popUpWidnow, Iframe, age_of_domain,
DNSRecord, web_traffic, Page_Rank, Google_Index, Links_pointing_to_page,
Statistical_report
```

`Result` is the target column used during training and is not entered in the browser form. The form displays the returned prediction after submission.

## Training Workflow

The pipeline runs these stages:

1. **Data ingestion:** reads records from the configured MongoDB database and creates train/test artifacts.
2. **Data validation:** checks the dataset structure and feature drift.
3. **Data transformation:** separates the `Result` target, converts target labels, imputes missing values, and saves transformed data.
4. **Model training:** compares multiple scikit-learn models and saves the selected model and preprocessor in `final_model/`.

Training artifacts are written into timestamped directories under `Artifacts/`. Application logs are written under `logs/`.

## Batch Prediction

The `/predict` endpoint currently reads `valid_data/test.csv` rather than the uploaded file contents. It adds a `Predicted_output` column and saves the result to:

```text
predicted_output/output.csv
```

Run the server from the project root because templates, model files, and data paths are relative paths.
