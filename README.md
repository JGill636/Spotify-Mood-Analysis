# Spotify-Mood-Analysis

This is a Flask application that integrates with the Spotify API to analyze the mood of a user's saved tracks. It categorizes each song based on its audio features and calculates the overall mood of the user's music library.

## Features

- User authentication via Spotify OAuth
- Fetches and analyzes user's saved tracks from Spotify
- Categorizes songs into different mood categories based on audio features
- Calculates and displays the overall mood of the user's music library
- Search bar to find specific tracks in the user's library

## Requirements

- Python 3.6+
- Spotify Developer account

## Setup

### 1. Clone the Repository

```
git clone https://github.com/yourusername/Spotify-Mood-Analysis.git
cd Spotify-Mood-Analysis
```
### 2. Create a Virtual Environment
```
python -m venv venv
venv\Scripts\activate # Linux and macOS use: source venv/bin/activate
```
### 3. Install Dependencies
```
pip install setuptools
python setup.py install
```
### 4. Retrieve API key and add redirect URI in Spotify Developer Dashboard
Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard) in order to create an app to get your key/ID and add http://localhost:5000/redirect to the list of redirect URIs for your application.

### 5. Set Up Environment Variables
Create a .env file in the project directory and add the following content:
```
SECRET_KEY=your_secret_key
SPOTIPY_CLIENT_ID=your_spotify_client_id
SPOTIPY_CLIENT_SECRET=your_spotify_client_secret
```
## Running the Application
`flask run`
Open your web browser and navigate to http://localhost:5000/ to access the application.
