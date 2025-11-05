#!/usr/bin/env python3
"""
Quick view of the last recorded WhatsApp automation session.
Run this script to see your most recent recording without opening the full recorder.
"""

import json
import os
from datetime import datetime

def show_last_recording():
    """Display information about the last recording session."""
    history_file = "recording_history.json"
    
    try:
        if not os.path.exists(history_file):
            print("❌ No recording history found.")
            print("Create your first recording by running: python whatsapp_recorder.py")
            return
        
        with open(history_file, 'r', encoding='utf-8') as f:
            history = json.load(f)
        
        if not history:
            print("❌ Recording history is empty.")
            return
        
        last_session = history[-1]
        
        print("=" * 60)
        print("🎬 LAST WHATSAPP RECORDING SESSION")
        print("=" * 60)
        print(f"📅 Date: {last_session['timestamp']}")
        print(f"⏱️  Duration: {last_session.get('duration', 'Unknown')}")
        print(f"🎯 Actions recorded: {last_session['action_count']}")
        print(f"📝 Script file: {last_session['script_file']}")
        print(f"💾 Data file: {last_session['data_file']}")
        
        if last_session.get('actions_summary'):
            print(f"\n🎭 Actions performed:")
            for i, action in enumerate(last_session['actions_summary'], 1):
                print(f"   {i:2d}. {action}")
            
            if last_session['action_count'] > len(last_session['actions_summary']):
                remaining = last_session['action_count'] - len(last_session['actions_summary'])
                print(f"   ... and {remaining} more actions")
        
        print(f"\n📊 Total recording sessions: {len(history)}")
        
        # Check if files still exist
        print(f"\n📁 File status:")
        if os.path.exists(last_session['script_file']):
            print(f"   ✅ Script file exists: {last_session['script_file']}")
        else:
            print(f"   ❌ Script file missing: {last_session['script_file']}")
            
        if os.path.exists(last_session['data_file']):
            print(f"   ✅ Data file exists: {last_session['data_file']}")
        else:
            print(f"   ❌ Data file missing: {last_session['data_file']}")
        
        print(f"\n💡 To run the recorded script:")
        print(f"   python {last_session['script_file']}")
        print(f"\n💡 To start a new recording:")
        print(f"   python whatsapp_recorder.py")
        
    except json.JSONDecodeError:
        print("❌ Error: Recording history file is corrupted.")
    except Exception as e:
        print(f"❌ Error reading recording history: {e}")

def show_quick_history():
    """Show a quick overview of recent recordings."""
    history_file = "recording_history.json"
    
    try:
        if not os.path.exists(history_file):
            print("❌ No recording history found.")
            return
        
        with open(history_file, 'r', encoding='utf-8') as f:
            history = json.load(f)
        
        if not history:
            print("❌ Recording history is empty.")
            return
        
        print("=" * 60)
        print("📚 RECENT RECORDING SESSIONS")
        print("=" * 60)
        
        # Show last 5 sessions
        recent_sessions = history[-5:] if len(history) >= 5 else history
        
        for i, session in enumerate(reversed(recent_sessions), 1):
            print(f"{i:2d}. {session['timestamp']} | {session['action_count']} actions | {session.get('duration', '?')}")
            if session.get('actions_summary') and session['actions_summary']:
                preview = session['actions_summary'][0][:50]
                print(f"    First action: {preview}...")
            print()
        
        if len(history) > 5:
            print(f"... and {len(history) - 5} older sessions")
        
        print(f"Total sessions: {len(history)}")
        
    except Exception as e:
        print(f"❌ Error reading recording history: {e}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--history":
        show_quick_history()
    else:
        show_last_recording()
        
    print(f"\n💡 Run with '--history' to see recent sessions:")
    print(f"   python {os.path.basename(__file__)} --history")