#!/usr/bin/env python
"""
Football News Website - Main Entry Point

This script starts the Flask web server for the Football News website.

Run this file to start the development server:
    python main.py

Then open your browser and navigate to:
    http://localhost:5000

For production deployment, use a production WSGI server like Gunicorn:
    gunicorn -w 4 -b 0.0.0.0:5000 app:app
"""

from app import app, db

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    print("\n" + "="*50)
    print("Football News Website")
    print("="*50)
    print("\nStarting Flask development server...")
    print("Visit: http://localhost:5000")
    print("Admin Dashboard: http://localhost:5000/admin/dashboard")
    print("\nPress Ctrl+C to stop the server")
    print("="*50 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
