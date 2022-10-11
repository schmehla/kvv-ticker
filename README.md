# kvv-ticker

This python script scrapes current traffic reports from the Karlsruhe Transport Association and sends them by email.

## Installation
1. Create virtual environment project folder: `python3 -m venv venv`
2. Activate virtual environment to install requirements: `pip install -r requirements.txt`
3. Quit virtual environment: `deactivate`
4. Create `mail_config.json` with the following fields: 
```json
{
  "MAIL_USER": string,
  "MAIL_PW": string,
  "SMTP_SERVER": string,
  "SMTP_PORT": number
}
```
5. Run shell script with email addresses to notify: `source run.sh email1@domain.com email2@domain.com ... emailN@domain.com`
6. Set up cron job to poll for new reports (only new reports are sent).
