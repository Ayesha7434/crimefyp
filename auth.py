import json
import streamlit as st
from passlib.hash import pbkdf2_sha256
import re
from datetime import datetime

class Authentication:
    @staticmethod
    def validate_password(password):
        """Validate password strength."""
        if len(password) < 8:
            return False, "Password must be at least 8 characters long"
        if not re.search(r"[A-Z]", password):
            return False, "Password must contain at least one uppercase letter"
        if not re.search(r"[a-z]", password):
            return False, "Password must contain at least one lowercase letter"
        if not re.search(r"\d", password):
            return False, "Password must contain at least one number"
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            return False, "Password must contain at least one special character"
        return True, "Password is strong"

    @staticmethod
    def validate_email(email):
        """Validate email format."""
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.match(email_pattern, email):
            return True, "Valid email"
        return False, "Invalid email format"

    @staticmethod
    def validate_phone(phone):
        """Validate phone number format."""
        # Remove any spaces or special characters
        phone = re.sub(r'[^0-9]', '', phone)
        if len(phone) >= 10 and len(phone) <= 15:
            return True, "Valid phone number"
        return False, "Phone number must be between 10 and 15 digits"

    @staticmethod
    def hash_password(password):
        """Hash the password using PBKDF2."""
        return pbkdf2_sha256.hash(password)
    
    @staticmethod
    def verify_password(stored_password, provided_password):
        """Verify the provided password against the stored hash."""
        return pbkdf2_sha256.verify(provided_password, stored_password)
    
    @staticmethod
    def load_users():
        """Load users from JSON file."""
        try:
            with open('users.json', 'r') as f:
                content = f.read().strip()
                if not content:
                    return {}
                return json.loads(content)
        except (FileNotFoundError, json.JSONDecodeError):
            with open('users.json', 'w') as f:
                json.dump({}, f)
            return {}
    
    @staticmethod
    def save_users(users):
        """Save users to JSON file."""
        with open('users.json', 'w') as f:
            json.dump(users, f, indent=4)
    
    @staticmethod
    def register_user(username, password, email, phone):
        """Register a new user with validation."""
        users = Authentication.load_users()
        
        # Validate username
        if not username or len(username) < 3:
            st.error("Username must be at least 3 characters long!")
            return False
        
        # Check if username already exists
        if username in users:
            st.error("Username already exists!")
            return False
        
        # Validate password
        is_valid_password, password_message = Authentication.validate_password(password)
        if not is_valid_password:
            st.error(password_message)
            return False
        
        # Validate email
        is_valid_email, email_message = Authentication.validate_email(email)
        if not is_valid_email:
            st.error(email_message)
            return False
        
        # Validate phone
        is_valid_phone, phone_message = Authentication.validate_phone(phone)
        if not is_valid_phone:
            st.error(phone_message)
            return False
        
        # Hash the password and save user data
        hashed_password = Authentication.hash_password(password)
        users[username] = {
            "password": hashed_password,
            "email": email,
            "phone": phone,
            "role": "user",
            "created_at": datetime.now().isoformat(),
            "last_login": None
        }
        
        Authentication.save_users(users)
        st.success("Registration successful!")
        return True
    
    @staticmethod
    def login_user(username, password):
        """Authenticate a user and update last login."""
        users = Authentication.load_users()
        
        # Check if user exists
        if username not in users:
            st.error("User not found!")
            return False
        
        # Verify password
        if Authentication.verify_password(users[username]["password"], password):
            # Update last login time
            users[username]["last_login"] = datetime.now().isoformat()
            Authentication.save_users(users)
            
            st.success("Login successful!")
            # Save user info in session state for access across pages
            st.session_state.user_info = {
                "username": username,
                "email": users[username].get("email", ""),
                "phone": users[username].get("phone", ""),
                "role": users[username].get("role", "user"),
                "last_login": users[username].get("last_login", "")
            }
            return True
        
        st.error("Incorrect password!")
        return False

    @staticmethod
    def is_admin(username):
        """Check if user has admin role."""
        users = Authentication.load_users()
        return users.get(username, {}).get("role") == "admin"

    @staticmethod
    def update_user_role(username, new_role, admin_username):
        """Update user role (admin only)."""
        if not Authentication.is_admin(admin_username):
            return False, "Only administrators can update user roles"
        
        users = Authentication.load_users()
        if username not in users:
            return False, "User not found"
        
        users[username]["role"] = new_role
        Authentication.save_users(users)
        return True, f"Role updated to {new_role} for user {username}"

    @staticmethod
    def reset_password(username, old_password, new_password):
        """Reset user password."""
        users = Authentication.load_users()
        
        if username not in users:
            return False, "User not found"
        
        # Verify old password
        if not Authentication.verify_password(users[username]["password"], old_password):
            return False, "Current password is incorrect"
        
        # Validate new password
        is_valid_password, password_message = Authentication.validate_password(new_password)
        if not is_valid_password:
            return False, password_message
        
        # Update password
        users[username]["password"] = Authentication.hash_password(new_password)
        Authentication.save_users(users)
        return True, "Password updated successfully"