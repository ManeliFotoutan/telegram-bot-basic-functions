# Telegram Bot Project

## Bot Setup with BotFather

To create a Telegram bot and get an access token, you need to use the **@BotFather** bot. This bot is specifically designed to create and manage Telegram bots and provides all the necessary tools to create one. Here's how you can create a new bot using @BotFather:

### Steps:

1. **Open a chat with @BotFather**: Open Telegram and search for @BotFather. Click on the chat to enter the conversation.

2. **Start the conversation with @BotFather**: After entering the chat, click the *Start* button or type `/start` and send it. This will show you a list of available commands.

3. **Create a new bot**: To create a new bot, type `/newbot` and send it. @BotFather will ask you to choose a name for your bot. This name can be anything, such as *MyFirstBot*.

4. **Choose a username for your bot**: After selecting the name, @BotFather will ask you to choose a username for your bot. This username must be unique and end with *bot*, e.g., *my_first_bot*.

5. **Receive your API token**: Once the username is chosen, @BotFather will send you a message containing your bot's API token. This token is a unique string that identifies your bot and allows it to interact with the Telegram API. Be sure to keep this token safe and never share it.

   The message from @BotFather will look like this:

   ```
   Done! Congratulations on your new bot. You will find it at t.me/my_first_bot.
   You can now add a description, about section, and profile picture for your bot.

   Use this token to access the HTTP API:
   your_tocken

   For a description of the Bot API, see this page: https://core.telegram.org/bots/api
   ```

## Files Overview

### 1. **file_downloader.py**
This bot allows users to download files by providing a URL. It handles file downloads and uploads them to the user. It also schedules file deletion after 60 seconds to avoid unnecessary storage use.

- **Main Functionality**: Handles downloading and uploading files from URLs provided by users.
- **Special Features**: Deletes downloaded files after a delay to free up space.

### 2. **inline_query.py**
This bot responds to inline queries with preset results. It can send a welcome message or allow users to interact with the bot by sending a "Join the Bot" link or a greeting message.

- **Main Functionality**: Handles inline queries and provides a list of predefined responses.

### 3. **inlinekeyboardbutton.py**
This bot displays an inline keyboard with buttons. Clicking on the buttons sends different responses, such as a contact number for customer support or an option to submit a problem.

- **Main Functionality**: Displays an inline keyboard with two options and responds to user choices.

### 4. **keyboard_button.py**
This bot uses a reply keyboard with two buttons. Users can choose one of the two options, and the bot will echo their selected choice.

- **Main Functionality**: Provides a reply keyboard with two options, echoes user input.

### 5. **logger.py**
This bot logs activities and provides basic logging for all actions. It’s useful for debugging and tracking bot activity.

- **Main Functionality**: Logs bot activity for debugging purposes.

### 6. **message_handler.py**
This bot handles different types of messages. It can respond to text messages, documents, audio files, photos, and even specific user patterns.

- **Main Functionality**: Handles various message types and performs custom actions like replying to specific text inputs.

### 7. **simple_form.py**
This bot collects user data step by step. It asks for the user’s name and age and stores this information for future reference.

- **Main Functionality**: Collects user profile information through multiple steps.

### 8. **text_to_speech.py**
This bot converts text to speech using Google Text-to-Speech (gTTS). It converts any text sent to the bot into an audio file and sends it to the user.

- **Main Functionality**: Converts text to speech and sends the audio file to the user.

### 9. **first_proj.py**
This bot presents two options to users: "Contact us" and "Report a problem." Depending on the choice, it provides either a clickable phone number or a form to submit a problem.

- **Main Functionality**: Displays options to users and handles contact and problem submission requests.

### 10. **second_proj.py**
This bot gives an explanation about its functionality, allows users to download a YouTube video by sending a URL, and uploads the video directly to the chat.

- **Main Functionality**: Downloads and uploads YouTube videos to the chat.

### 11. **third_proj.py**
This bot allows users to send images, which it compresses before sending them back. It also includes an inline query feature for interaction.

- **Main Functionality**: Compresses images and handles inline queries.

---

## Setup Instructions

1. **Clone the repository**: 
   ```bash
   git clone https://github.com/your-repository-url.git
   ```

2. **Install dependencies**:
   Ensure that you have `telebot`, `requests`, `gtts`, and other required libraries:
   ```bash
   pip install pyTelegramBotAPI requests gtts
   ```

3. **Set up your `.env` file**:
   Create a `.env` file in the project directory and add your bot’s API token:
   ```bash
   API_TOKEN=your-telegram-bot-api-token
   ```

4. **Run your bot**:
   After setting up, run the Python script for the bot you want to start. For example:
   ```bash
   python file_downloader.py
   ```

