# Backend Setup

This guide provides instructions for setting up and running the backend for the document authentication workflow.

## Prerequisites

- Python 3.8 or higher
- pip package manager

## Installation

1. **Navigate to the backend folder**
    ```bash
    cd /path/to/doc-auth-workflow/backend
    ```

2. **Create and activate a virtual environment**
    ```bash
    # Create virtual environment
    python -m venv venv

    # Activate virtual environment
    # On Windows
    venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3. **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

1. **Set up environment variables**
    
    Copy the example environment file:
    ```bash
    cp .env.example .env
    ```

    Then edit the `.env` file in the backend directory with your specific configuration:
    ```
    DEBUG=True
    SECRET_KEY=your_secret_key_here
    DATABASE_URL=your_database_url
    
    # Facebook OAuth
    FB_CLIENT_ID=your_facebook_client_id
    FB_CLIENT_SECRET=your_facebook_client_secret
    REDIRECT_URI=http://localhost:8000/oauth/callback
    
    # Add other required environment variables
    ```

2. **Configure the application**
    ```bash
    python manage.py configure
    ```

## Running the Server

1. **Start the development server**
    ```bash
    python manage.py runserver
    ```
    The server will start at http://127.0.0.1:8000/

## Setting Up Ngrok for Facebook OAuth

1. **Install Ngrok**
   - Download and install Ngrok from [https://ngrok.com/download](https://ngrok.com/download)

2. **Run the Backend with Uvicorn**
    - In VS Code terminal, start the FastAPI application:
      ```bash
      uvicorn main:app --reload --host 0.0.0.0 --port 8000
      ```
    - The server will start and listen on all network interfaces at port 8000

3. **Run Ngrok**
    - Open Command Prompt as Administrator
    - Run the following command to create a tunnel to your local server:
      ```bash
      ngrok http 8000
      ```
    - Ngrok will display a public URL (e.g., https://a1b2c3d4.ngrok.io)

3. **Configure Facebook OAuth**
   - Copy the Ngrok HTTPS URL
   - Go to your Facebook Business App settings
   - In the OAuth settings, paste the Ngrok URL followed by your callback path:
    ```
    https://a1b2c3d4.ngrok.io/oauth/callback
    https://a1b2c3d4.ngrok.io
    ```
   - Update your `.env` file with the new redirect URI:
     ```
     REDIRECT_URI=https://a1b2c3d4.ngrok.io/oauth/callback
     ```
