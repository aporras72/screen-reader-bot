# 🤖 Screen Reader Bot for Class Questions

A real-time Windows app that monitors your screen, extracts text using OCR, and answers any class questions using Claude.

## Features

✅ **Real-time Screen Monitoring** - Checks your screen every 10 seconds  
✅ **OCR Text Extraction** - Automatically reads text from your screen  
✅ **Claude Integration** - Gets instant answers via your local Claude instance  
✅ **Easy Installation** - PowerShell installer handles all dependencies  
✅ **Works Offline** - Uses your local Claude instance  

## Requirements

- Windows 10/11
- Python 3.8+
- Claude running on `http://127.0.0.1:8082`
- Administrator access (for installation)

## Installation

### Step 1: Prepare Claude
Make sure Claude is running on your terminal:
```bash
C:\Users\Alan\fcc-claude
```

It should be accessible at: `http://127.0.0.1:8082`

### Step 2: Clone the Repository
```powershell
git clone https://github.com/aporras72/screen-reader-bot.git
cd screen-reader-bot
```

### Step 3: Run the Installer
Open PowerShell as Administrator and run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force
.\install.ps1
```

This will automatically install:
- Tesseract OCR
- Python dependencies (Pillow, pytesseract, requests)

### Step 4: Start the Bot
```powershell
python screen_reader.py
```

You should see:
```
🤖 Screen Reader Bot Started
📍 Claude API: http://127.0.0.1:8082/api/messages
⏱️  Checking screen every 10 seconds
💡 Press Ctrl+C to stop
```

## How It Works

1. **Captures Screen** - Takes a screenshot every 10 seconds
2. **Extracts Text** - Uses Tesseract OCR to read all text on screen
3. **Sends to Claude** - Uploads the text to your local Claude instance
4. **Gets Answer** - Claude analyzes the content and provides helpful context/answers
5. **Displays Result** - Shows Claude's response in your terminal

## Usage Tips

- Open any classroom content, textbook, or notes on your screen
- The bot will automatically analyze and provide summaries/explanations
- If you have a specific question, ask Claude directly in the terminal (future enhancement)
- Monitor the terminal output to see what the bot detected

## Configuration

Edit `screen_reader.py` to change:

```python
CLAUDE_API_URL = "http://127.0.0.1:8082/api/messages"  # Claude endpoint
SCREENSHOT_INTERVAL = 10  # Check every N seconds
MAX_RETRIES = 3  # Retry attempts if Claude is unavailable
```

## Troubleshooting

### "Claude API error: Connection refused"
- Make sure Claude is running on your terminal
- Check that `http://127.0.0.1:8082` is accessible

### "Tesseract not found"
- Run installer again: `.\install.ps1`
- Or manually install: `choco install tesseract -y`

### "pytesseract module not found"
- Run: `pip install -r requirements.txt`

### "Access denied" on install
- Open PowerShell as Administrator
- Run: `Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force`

## Safety & Privacy

✅ **Local Processing** - All data stays on your machine  
✅ **No Cloud Upload** - Uses only your local Claude instance  
✅ **Screen Content** - Text extracted from your screen is only sent to local Claude  

## Future Enhancements

- [ ] Interactive question prompts
- [ ] Save chat history
- [ ] Highlight important sections on screen
- [ ] Custom timer intervals
- [ ] Subject-specific prompts

## Support

If you encounter issues:
1. Check the troubleshooting section above
2. Verify Claude is running and accessible
3. Try reinstalling: `.\install.ps1`
4. Check Python version: `python --version` (should be 3.8+)

---

**Built by:** @aporras72  
**Testing:** AI Model Testing Project  
**Status:** ✅ Ready to use
