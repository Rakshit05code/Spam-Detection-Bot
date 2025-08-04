# Kickflip - Discord Spam Detection and Moderation Bot

Kickflip is an automated Discord moderation bot that uses machine learning to detect and manage spam messages in real time. Built with Python and discord.py, Kickflip helps keep your Discord servers clean by automatically warning and kicking users who post spam.

## Features

- **ML-Powered Spam Detection:** Utilizes a logistic regression model with TF-IDF vectorization, trained on a custom dataset.
- **Automatic Moderation:** Issues warnings and kicks users after reaching a warning threshold (default 3 warnings).
- **Manual Warning Command:** Administrators can manually warn users using the `!warn` command.
- **Persistent Warnings:** Tracks user warnings in a local SQLite database.
- **Secure Configuration:** Loads bot token securely using an environment `.env` file.
- **Extensible Codebase:** Easy to customize the model or moderation rules.



## Repository Contents

- `main.py` — The Discord bot script including message handling and moderation logic.
- `model_train.py` — Script to train and save the spam detection model from your labeled dataset.
- `final_dataset.csv` — Sample labeled dataset with messages and spam labels.
- `spam_classifier.pkl` — Trained machine learning model used by the bot.
- `.env` — Environment file (not included in repo) containing your Discord bot token.
- `warnings.db` — SQLite database generated at runtime to store user warning counts.
- `requirements.txt` — Python package dependencies.

- Invite your bot to your Discord server with appropriate permissions (reading messages, sending messages, kicking members).
- The bot will automatically warn users posting messages classified as spam.
- Use the `!warn @user` command to manually issue warnings.



## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Contributing

Contributions and suggestions are welcome! Feel free to open issues or pull requests.

---

Made with ❤️ to keep your Discord servers safe and spam-free with smart automation.
