#!/usr/bin/env python
"""
Database Reset Script
यह पुरानी database को drop करके नई tables बनाता है
"""
import sys
from app import create_app, db

def reset_database():
    """Drop all tables and recreate them"""
    app = create_app()
    
    with app.app_context():
        print("🗑️  Dropping all tables...")
        db.drop_all()
        print("✅ All tables dropped!")
        
        print("\n🔨 Creating new tables...")
        db.create_all()
        print("✅ All tables created!")
        
        print("\n" + "="*50)
        print("✅ DATABASE RESET SUCCESSFUL!")
        print("="*50)
        print("\n📋 New tables created with columns:")
        print("  • User (id, username, email, password, is_email_verified, otp, otp_expiry)")
        print("  • Income (id, amount, source, date, user_id)")
        print("  • Expense (id, amount, category, description, date, user_id)")
        print("  • Watchlist (id, user_id, symbol, name, sector, added_date)")
        print("\n✨ Ab aap register kar sakte ho!")

if __name__ == '__main__':
    reset_database()
