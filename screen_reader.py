#!/usr/bin/env python3
"""
Screen Reader Bot for Class Questions
Monitors screen every 10 seconds, uses OCR to read text, answers questions via Claude
"""

import time
import requests
import json
import subprocess
import sys
from pathlib import Path
from PIL import ImageGrab
import pytesseract
from datetime import datetime

# Configuration
CLAUDE_API_URL = "http://127.0.0.1:8082/api/messages"
SCREENSHOT_INTERVAL = 10  # seconds
MAX_RETRIES = 3

class ScreenReaderBot:
    def __init__(self):
        self.last_text = ""
        self.session_history = []
        self.setup_tesseract()
        
    def setup_tesseract(self):
        """Check if Tesseract is installed"""
        try:
            result = subprocess.run(['tesseract', '--version'], capture_output=True)
            if result.returncode == 0:
                print("✓ Tesseract OCR found")
            else:
                print("✗ Tesseract not found. Installing...")
                self.install_tesseract()
        except FileNotFoundError:
            print("✗ Tesseract not found. Please install manually or run install.ps1")
            
    def install_tesseract(self):
        """Install Tesseract via chocolatey"""
        try:
            subprocess.run(['choco', 'install', 'tesseract', '-y'], check=True)
            print("✓ Tesseract installed successfully")
        except Exception as e:
            print(f"Failed to auto-install Tesseract: {e}")
            print("Please run: choco install tesseract -y")
            
    def capture_screen(self):
        """Capture current screen"""
        try:
            screenshot = ImageGrab.grab()
            return screenshot
        except Exception as e:
            print(f"Error capturing screen: {e}")
            return None
            
    def extract_text(self, image):
        """Extract text from image using OCR"""
        try:
            text = pytesseract.image_to_string(image)
            return text.strip()
        except Exception as e:
            print(f"Error extracting text: {e}")
            return ""
            
    def send_to_claude(self, screen_text, question=""):
        """Send screen text and question to Claude"""
        prompt = f"""You are a helpful study assistant. 
        
Current screen content:
{screen_text}

{f'Student question: {question}' if question else 'Briefly summarize what is on screen and provide helpful context.'}

Provide a clear, concise answer."""
        
        payload = {
            "model": "claude-opus-4-1",
            "max_tokens": 1024,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
        
        for attempt in range(MAX_RETRIES):
            try:
                response = requests.post(CLAUDE_API_URL, json=payload, timeout=10)
                if response.status_code == 200:
                    result = response.json()
                    if 'content' in result:
                        return result['content'][0]['text']
                    return "No response from Claude"
                else:
                    print(f"Claude API error: {response.status_code}")
            except Exception as e:
                print(f"Attempt {attempt + 1}: Connection error: {e}")
                if attempt < MAX_RETRIES - 1:
                    time.sleep(2)
                    
        return "Could not reach Claude. Is it running on http://127.0.0.1:8082?"
        
    def display_answer(self, answer):
        """Display answer in formatted way"""
        print("\n" + "="*80)
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Claude's Answer:")
        print("="*80)
        print(answer)
        print("="*80 + "\n")
        
    def monitor_screen(self):
        """Main monitoring loop"""
        print("\n🤖 Screen Reader Bot Started")
        print(f"📍 Claude API: {CLAUDE_API_URL}")
        print(f"⏱️  Checking screen every {SCREENSHOT_INTERVAL} seconds")
        print("💡 Press Ctrl+C to stop\n")
        
        try:
            while True:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Capturing screen...")
                
                # Capture and extract text
                screenshot = self.capture_screen()
                if screenshot:
                    text = self.extract_text(screenshot)
                    
                    if text and text != self.last_text:
                        self.last_text = text
                        print(f"📝 Text detected ({len(text)} characters)")
                        
                        # Get Claude's analysis
                        answer = self.send_to_claude(text)
                        self.display_answer(answer)
                    else:
                        print("⏳ No new text detected")
                        
                # Wait for next interval
                time.sleep(SCREENSHOT_INTERVAL)
                
        except KeyboardInterrupt:
            print("\n\n✓ Bot stopped by user")
            sys.exit(0)
        except Exception as e:
            print(f"\n✗ Error: {e}")
            sys.exit(1)

def main():
    bot = ScreenReaderBot()
    bot.monitor_screen()

if __name__ == "__main__":
    main()
