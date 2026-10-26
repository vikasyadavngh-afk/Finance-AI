# Finance AI Android app

A starter Android personal-expense tracker built with Python + Kivy.

## Features in this version
- Add expense amount, category, optional note
- Shows total expenses and entry count
- Lists recent entries
- Saves entries locally in `finance_data.json`

## Build an Android APK
The easiest repeatable build is GitHub Actions:
1. Create a GitHub repository named `FinanceAI-Android`.
2. Upload all files from this folder, including `.github/workflows/build-apk.yml`.
3. Open the repository's **Actions** tab and run **Build Finance AI APK**.
4. When the workflow finishes, open the run and download the `finance-ai-apk` artifact.

For a local Linux build, install Buildozer and its Android dependencies, then run:
`buildozer android debug`

## Important
- This is a first working prototype, not a financial-advice engine.
- It does not connect to bank accounts and does not send data to a server.
- Expense data is stored locally on the device. Uninstalling the app or clearing app data may delete it; keep backups.
- No login/password is configured in this prototype.
