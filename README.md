# Steps_Predictor

Product Name: [TBD] Steps Predictor
Version: [1.0]
Date: [2024.08.30]

# About [Steps Predictor]

Steps Predictor is a powerful and versatile .NET MAUI application designed to predict users daily walking steps based on historical data with the help of a machine learning model.

# Development Environment Set Up

• .NET 7.0 SDK
• Python environment
• Flask framework
• Python libraries: pandas
• Git version control system

# Architecture

Our .NET MAUI app is designed as a modern, scalable, and user-friendly platform. It follows a microservices architecture, ensuring flexibility and reliability. Here's a simplified overview:

- **Frontend**: XAML
- **Backend**: .NET, ASP.NET, RESTful API, Flask

# Key Features

The project consists of three main components:

1. .NET MAUI App: Provides the user interface and layout.
2. .NET WebAPI: Stores user data and communicates with the .NET MAUI App through API calls.
3. Flask API (Python): Facilitates data transfer between the .NET WebAPI, preprocessing script, and machine learning model.
4. Preprocessing script (Python): Cleans uploaded user data, extracting significant information like dates and step counts. It sends the cleaned data back to the .NET WebAPI, which the .NET MAUI App can then access.

### I .NET MAUI App Key Features

- [ ]  User interface for file uploads
- [ ]  File validation for `.csv`, `.xlsx`, `.xml`, and `.json` formats
- [ ]  "Clean Data" button to initiate communication between Web API and Flask API
- [ ]  User interface to display predicted walking data

### **II .NET Web API Development**

- [ ]  API endpoint for accepting file uploads from the .NET MAUI app.
- [ ]  API endpoint to store and retrieve cleaned data.
- [ ]  API endpoint to communicate with .NET MAUI App for file cleaning:
    - Identify and locate the stored raw data file.
    - Send the file to the Flask API for cleaning.
- [ ]  API endpoint to communicate with the Flask API for data preprocessing.
- [ ]  API endpoint to request predictions from the machine learning model (via Flask API).
- [ ]  Set up a database (e.g., SQLite, SQL Server) to store user data and processed data.

### **III. Flask API Development**

Set up endpoints for:

- [ ]  Receiving data from the .NET Web API
- [ ]  Sending data to the preprocessing script
- [ ]  Receiving cleaned data and sending it back to the .NET Web API
- [ ]  Sending data to the machine learning model for predictions
- [ ]  Receiving predictions and sending them back to the .NET Web API

### **IV. Data Preprocessing and Cleaning in Python**

- [ ]  Develop a Python script to load, clean, and preprocess data (e.g., filter relevant information such as date and step count).
- [ ]  Implement functions to handle various file formats (`csv`, `xlsx`, `xml`, `json`).
- [ ]  Create a method to transmit the cleaned data back to the Flask API.

### **V. Machine Learning Model Development**

- [ ]  Get access to the training data for the model.
- [ ]  Develop a machine learning model to predict daily step counts.
- [ ]  Train the model using relevant walking data.
- [ ]  Save the trained model for deployment.
- [ ]  Implement the model's inference logic in the Flask API.
- [ ]  Test the model to ensure accurate predictions.

# Data Flow Diagram

For a more detailed understanding of how data flows within the application, we've prepared a data flow diagram:


# Issues and Solutions

### **Issue:**

### **Solution**:
