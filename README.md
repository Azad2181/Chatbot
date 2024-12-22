# This is Parcel Tracking Bot

![chatsss](https://github.com/user-attachments/assets/cb6c0809-fc91-4a59-b0cf-898989248d07)

## Check it: 

https://github.com/user-attachments/assets/728e7838-e871-466f-92ca-08965cc5d7c5


## Overview
This Parcel Tracking Bot is a user-friendly and reliable bot designed to keep you updated about your shipments. With real-time tracking and prompt responses, this bot ensures an efficient parcel management experience.

---

## Features
- **Real-Time Parcel Tracking:** Get accurate updates about the current location and status of your parcels.
- **Professional Assistance:** The bot maintains a friendly and professional tone while addressing user queries.
- **Database Integration:** Stores and retrieves conversation history for better contextual responses.
- **Customizable Configuration:** Configure API keys and settings easily through a JSON file.
- **Emergency Support:** Handles urgent delivery requests and provides solutions to common parcel-related issues.

---

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/steadfast-parcel-bot.git
   cd steadfast-parcel-bot
   ```

2. **Install Dependencies**:
   Ensure you have Python 3.9+ installed. Then run:
   ```bash
   pip install -r requirements.txt
   ```

3. **Setup Configuration**:
   - Rename `config.sample.json` to `config.json`.
   - Add your API key and other necessary details.

4. **Initialize the Database**:
   Ensure MySQL is installed and set up. Update the `db_config` in `bot.py` with your database credentials.
   ```bash
   MySQL -u root -p < scripts/init_db.sql
   ```

5. **Run the Application**:
   ```bash
   uvicorn bot:app --host 0.0.0.0 --port 9091
   ```

---

## API Endpoints

### `POST /msg`
Send a message to the bot and receive a response.

- **Request Body**:
  ```json
  {
    "message": "Your query here"
  }
  ```

- **Response**:
  ```json
  {
    "response": "Bot's response"
  }
  ```

### `POST /reset`
Reset all conversation history.

- **Response**:
  ```json
  {
    "message": "Conversation history reset"
  }
  ```

---

## Project Structure

```plaintext
.
├── bot.py             # Core logic for the bot
├── config.json        # Configuration file
├── conversations.json # Sample conversation data
├── requirements.txt   # Python dependencies
└── README.md          # Project documentation
```

---

## Configuration Details

Update the following keys in the `config.json` file:

- **gemini_api_key**: Your API key for the Gemini generative AI model.
- **name**: Name of the bot.
- **Description**: A short description of the bot.

---

## Contribution

We welcome contributions to improve this Parcel Tracking Bot. Please follow these steps:

1. Fork the repository.
2. Create a new branch (`feature/your-feature`).
3. Commit your changes.
4. Open a pull request.

---

## License
This project is licensed under the MIT License. See `LICENSE` for more details.

---

---

## Acknowledgments

Special thanks to all contributors and users for their valuable feedback in improving the bot.

---
