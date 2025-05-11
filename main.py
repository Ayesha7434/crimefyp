import streamlit as st
import os
from PIL import Image
import base64
import streamlit as st
from auth import Authentication
from crime_report import CrimeReporting
import time
import base64
import os

def get_base64_image(image_path):
    """Load an image and encode it to base64 string."""
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

def set_background_image(image_path):
    """Set a background image for a section."""
    base64_image = get_base64_image(image_path)
    background_css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{base64_image}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    .login-container {{
        background-color: rgba(255, 255, 255, 0.85);
        padding: 2rem;
        border-radius: 10px;
        max-width: 500px;
        margin: 0 auto;
        margin-top: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }}
    .center-text {{
        text-align: center;
    }}
    .crime-card {{
        background-color: rgba(255, 255, 255, 0.9);
        padding: 1.5rem;
        border-radius: 5px;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }}
    </style>
    """
    st.markdown(background_css, unsafe_allow_html=True)

def show_popup(message, type="success"):
    """Show a popup message."""
    if type == "success":
        st.success(message)
    elif type == "error":
        st.error(message)
    elif type == "info":
        st.info(message)
    elif type == "warning":
        st.warning(message)
    
    # Add a progress bar for visual feedback
    progress_bar = st.progress(0)
    for percent_complete in range(100):
        time.sleep(0.01)  # Small delay
        progress_bar.progress(percent_complete + 1)
    
    # Remove the progress bar
    progress_bar.empty()

def login_page():
    """Login page interface with centered layout."""
    # Apply a background image for login
    try:
        set_background_image("images/police_background.jpg")
    except:
        # If image not found, use a CSS gradient as fallback
        st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(120deg, #2980b9, #8e44ad);
        }
        </style>
        """, unsafe_allow_html=True)
    
    # Centered login container
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    st.markdown('<h1 class="center-text">🚨 Crime Reporting System</h1>', unsafe_allow_html=True)
    st.markdown('<h3 class="center-text">Login</h3>', unsafe_allow_html=True)
    
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Login", use_container_width=True):
            if Authentication.login_user(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.rerun()
    
    with col2:
        if st.button("Register", use_container_width=True):
            st.session_state.show_registration = True
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div style="position: fixed; bottom: 10px; left: 0; right: 0; text-align: center; color: white;">
        <p>© 2025 Crime Reporting System - Final Year Project</p>
    </div>
    """, unsafe_allow_html=True)

def registration_page():
    """User registration interface with enhanced validation and feedback."""
    try:
        set_background_image("images/police_background.jpg")
    except:
        st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(120deg, #2980b9, #8e44ad);
        }
        </style>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    st.markdown('<h1 class="center-text">🚨 Crime Reporting System</h1>', unsafe_allow_html=True)
    st.markdown('<h3 class="center-text">Register</h3>', unsafe_allow_html=True)
    
    # Add password requirements info box
    st.info("""
    Password Requirements:
    - At least 8 characters long
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one number
    - At least one special character (!@#$%^&*(),.?":{}|<>)
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        new_username = st.text_input("Username (min. 3 characters)")
        new_password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
    
    with col2:
        email = st.text_input("Email")
        phone = st.text_input("Phone (10-15 digits)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Create Account", use_container_width=True):
            if new_password != confirm_password:
                st.error("Passwords do not match!")
            else:
                Authentication.register_user(new_username, new_password, email, phone)
    
    with col2:
        if st.button("Back to Login", use_container_width=True):
            st.session_state.show_registration = False
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="position: fixed; bottom: 10px; left: 0; right: 0; text-align: center; color: white;">
        <p>© 2025 Crime Reporting System - Final Year Project</p>
    </div>
    """, unsafe_allow_html=True)

def crime_reporting_page():
    """Crime reporting interface with dashboard and imagery."""
    # Dashboard header with background image
    st.markdown("""
    <div style="background-color: #2c3e50; padding: 1rem; border-radius: 5px; margin-bottom: 1rem; color: white;">
        <h1 style="text-align: center;">🚨 Crime Reporting Dashboard</h1>
        <h3 style="text-align: center;">Welcome, {}</h3>
    </div>
    """.format(st.session_state.username), unsafe_allow_html=True)




# Add custom CSS for cards
    st.markdown("""
    <style>
    .crime-card {
    padding: 1.5rem;
    border-radius: 0.5rem;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    margin-bottom: 1rem;
    transition: transform 0.3s ease;
}
.crime-card:hover {
    transform: translateY(-5px);
}
    </style>
    """, unsafe_allow_html=True)

# Function to load and display local images
    def load_image(image_path):
        if os.path.exists(image_path):
            return Image.open(image_path)
        else:
            st.error(f"Image not found: {image_path}")
            return None

# Dashboard stats and visualizations in 3 columns
    col1, col2, col3 = st.columns(3)

    with col1:
    # Statistics card
        st.markdown("""
        <div class="crime-card">
        <h3 style="text-align: center;">📊 Crime Statistics</h3>
        </div>
        """, unsafe_allow_html=True)
    
    # Load and display local image
        image = load_image("1.jpg")
        if image:
            st.image(image, use_container_width=True)
    
        

    with col2:
    # Report card
        st.markdown("""
    <div class="crime-card">
        <h3 style="text-align: center;">📝 File a Report</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Load and display local image
        image = load_image("2.jpg")
        if image:
            st.image(image, use_container_width=True)
    
      

    with col3:
    # Emergency contacts card
        st.markdown("""
        <div class="crime-card">
        <h3 style="text-align: center;">🚓 Emergency Contacts</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Load and display local image
        image = load_image("3.jpg")
        if image:
            st.image(image, use_container_width=True)
    
        

# Dashboard footer
    st.markdown("### Dashboard Information")
    st.markdown("""
This dashboard provides crime statistics, reporting tools, and emergency contact information.
All data is regularly updated to ensure accuracy and relevance for your local area.
""")

    # Set background image for the dashboard
    
    # # Dashboard stats and visualizations in 3 columns
    # col1, col2, col3 = st.columns(3)
    
    # with col1:
    #     # Statistics card
    #     st.markdown("""
    #     <div class="crime-card">
    #         <h3 style="text-align: center;">📊 Crime Statistics</h3>
    #         <img src="https://source.unsplash.com/Nyvq2juw4_o/800x500" width="100%">
    #         <p style="text-align: center;">View comprehensive crime analytics for your area</p>
    #     </div>
    #     """, unsafe_allow_html=True)
        
    # with col2:
    #     # Report card
    #     st.markdown("""
    #     <div class="crime-card">
    #         <h3 style="text-align: center;">📝 File a Report</h3>
    #         <img src="1.jpg" width="100%">
    #         <p style="text-align: center;">Report incidents to local authorities</p>
    #     </div>
    #     """, unsafe_allow_html=True)
        
    # with col3:
    #     # Emergency contacts card
    #     st.markdown("""
    #     <div class="crime-card">
    #         <h3 style="text-align: center;">🚓 Emergency Contacts</h3>
    #         <img src="https://source.unsplash.com/YOZ1ZB9s4DQ/800x500" width="100%">
    #         <p style="text-align: center;">Access important emergency numbers</p>
    #     </div>
    #     """, unsafe_allow_html=True)

    



    
    # Government Reporting Resources
    st.markdown("""
    <div style="background-color: #f8f9fa; padding: 1rem; border-radius: 5px; margin: 1rem 0;">
        <h3 style="color: #2c3e50;">🏛️ Official Crime Reporting Resources</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="crime-card">
            <h4>Federal Investigation Agency (FIA)</h4>
            <a href="https://www.fia.gov.pk/complaints_dept" target="_blank">Report to FIA Online</a>
            <p>Official portal for reporting federal-level crimes</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="crime-card">
            <h4>Bahawalnagar Police District</h4>
            <p><strong>Contact Details:</strong></p>
            <ul>
                <li>Phone: 063-9240053</li>
                <li>Fax: 063-9240077</li>
                <li>Email: dpo.bwn@punjabpolice.gov.pk</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Emergency section
    st.markdown("""
    <div style="background-color: #f8f9fa; padding: 1rem; border-radius: 5px; margin: 1rem 0;">
        <h3 style="color: #2c3e50;">🚓 Emergency Contacts</h3>
    </div>
    """, unsafe_allow_html=True)
    
    emergency_col1, emergency_col2 = st.columns(2)
    
    with emergency_col1:
        st.markdown("""
        <div class="crime-card" style="border-left: 4px solid #dc3545;">
            <h4>Police Emergency</h4>
            <p><strong>Emergency Numbers:</strong></p>
            <ul>
                <li>National Emergency: 15</li>
                <li>Highway Patrol: 130</li>
                <li>Rescue Services: 1122</li>
            </ul>
            <p style="color: #dc3545;">For immediate assistance in life-threatening situations</p>
        </div>
        """, unsafe_allow_html=True)
    
    with emergency_col2:
        st.markdown("""
        <div class="crime-card" style="border-left: 4px solid #28a745;">
            <h4>Women's Helpline</h4>
            <p><strong>Protection Services:</strong></p>
            <ul>
                <li>Women's Helpline: 1043</li>
                <li>Child Protection: 1121</li>
                <li>Cyber Crime Wing: 9288888</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # Crime reporting form with better styling
    st.markdown("""
    <div style="background-color: #f8f9fa; padding: 1rem; border-radius: 5px; margin: 1rem 0;">
        <h3 style="color: #2c3e50;">📝 Submit a Crime Report</h3>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("crime_report_form"):
        crime_type = st.selectbox("Type of Crime", [
            "Theft", "Assault", "Burglary", "Fraud", 
            "Cybercrime", "Other"
        ])
        
        col1, col2 = st.columns(2)
        with col1:
            location = st.text_input("Location of Incident")
        with col2:
            incident_date = st.date_input("Date of Incident")
        
        description = st.text_area("Detailed Description")
        
        # Severity rating
        severity = st.slider("Incident Severity", 1, 10, 5, help="1 being least severe, 10 being most severe")
        
        submitted = st.form_submit_button("Submit Report")
        
        if submitted:
            # Prepare report dictionary
            report = {
                "crime_type": crime_type,
                "location": location,
                "incident_date": str(incident_date),
                "description": description,
                "severity": severity
            }
            
            # Save the report
            report_id = CrimeReporting.save_report(report, st.session_state.username)
            
            # Show popup
            show_popup(f"Crime report #{report_id} submitted successfully!")
            
            # Display notification that they'll be notified on status changes
            st.info("You will be notified when there are updates to your report status.")

def view_reports_page():
    """Page to view existing crime reports with search and filter."""
    st.markdown("""
    <div style="background-color: #2c3e50; padding: 1rem; border-radius: 5px; margin-bottom: 1rem; color: white;">
        <h1 style="text-align: center;">📋 Existing Crime Reports</h1>
    </div>
    """, unsafe_allow_html=True)
    
    # Search and filter options with better styling
    st.markdown("""
    <div style="background-color: #f8f9fa; padding: 1rem; border-radius: 5px; margin-bottom: 1rem;">
        <h4 style="color: #2c3e50;">Search and Filter Reports</h4>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        search_term = st.text_input("Search Reports", placeholder="Search by keywords...")
    
    with col2:
        filter_type = st.selectbox("Filter By", 
            ["None", "Category", "Status", "Date"]
        )
    
    with col3:
        filter_value = None
        if filter_type == "Category":
            filter_value = st.selectbox("Select Category", 
                ["All", "Theft", "Assault", "Burglary", "Fraud", "Cybercrime", "Other"]
            )
            filter_type = "crime_type" if filter_value != "All" else None
        elif filter_type == "Status":
            filter_value = st.selectbox("Select Status", 
                ["All", "Submitted", "Under Investigation", "Resolved", "Closed"]
            )
            filter_type = "status" if filter_value != "All" else None
        elif filter_type == "Date":
            filter_value = str(st.date_input("Select Date"))
            filter_type = "date"
        else:
            filter_type = None
    
    # Clear filters button
    if st.button("Clear Filters", type="primary"):
        search_term = ""
        filter_type = None
        filter_value = None
        st.rerun()
    
    # View reports with filters
    CrimeReporting.view_reports(filter_type, filter_value, search_term, st.session_state.username)
    
def notifications_page():
    """Page to view notifications."""
    st.markdown("""
    <div style="background-color: #2c3e50; padding: 1rem; border-radius: 5px; margin-bottom: 1rem; color: white;">
        <h1 style="text-align: center;">🔔 Your Notifications</h1>
    </div>
    """, unsafe_allow_html=True)
    
    reports = CrimeReporting.load_reports()
    
    # Filter for user's reports
    user_reports = [r for r in reports if r.get('reported_by') == st.session_state.username]
    
    if not user_reports:
        st.info("You don't have any reports yet.")
        return
    
    # Notification counter
    total_notifications = sum(1 for r in user_reports if 'notifications' in r for _ in r['notifications'])
    st.caption(f"You have {total_notifications} total notifications")
    
    notifications_found = False
    
    for report in user_reports:
        if 'notifications' in report and report['notifications']:
            notifications_found = True
            with st.expander(f"Notifications for Report #{report['id']} - {report.get('crime_type')}"):
                for notif in report['notifications']:
                    st.info(f"{notif['message']} - {notif['timestamp']}")
                
                # Add link to view the full report
                if st.button(f"View Full Report #{report['id']}", key=f"view_from_notif_{report['id']}"):
                    st.session_state.view_report_id = report['id']
                    st.session_state.active_tab = "View Reports"
                    st.rerun()
    
    if not notifications_found:
        st.info("No notifications yet. You'll be notified when your report status changes.")

def account_page():
    """User account page with enhanced security features."""
    st.markdown("""
    <div style="background-color: #2c3e50; padding: 1rem; border-radius: 5px; margin-bottom: 1rem; color: white;">
        <h1 style="text-align: center;">👤 Your Account</h1>
    </div>
    """, unsafe_allow_html=True)
    
    if 'user_info' in st.session_state:
        user_info = st.session_state.user_info
        
        # Personal Information Section
        st.markdown("""
        <div style="background-color: #f8f9fa; padding: 1rem; border-radius: 5px; margin: 1rem 0;">
            <h3 style="color: #2c3e50;">👤 Personal Information</h3>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="crime-card">
                <h4>Account Details</h4>
                <p><strong>Username:</strong> {}</p>
                <p><strong>Email:</strong> {}</p>
                <p><strong>Phone:</strong> {}</p>
                <p><strong>Role:</strong> {}</p>
                <p><strong>Last Login:</strong> {}</p>
            </div>
            """.format(
                user_info.get('username', ''),
                user_info.get('email', ''),
                user_info.get('phone', ''),
                user_info.get('role', 'user').capitalize(),
                user_info.get('last_login', 'Never')
            ), unsafe_allow_html=True)
        
        with col2:
            reports = CrimeReporting.load_reports()
            user_reports = [r for r in reports if r.get('reported_by') == st.session_state.username]
            
            status_counts = {}
            for report in user_reports:
                status = report.get('status', 'Submitted')
                status_counts[status] = status_counts.get(status, 0) + 1
            
            status_html = ""
            for status, count in status_counts.items():
                status_color = {
                    'Submitted': 'blue',
                    'Under Investigation': 'orange',
                    'Resolved': 'green',
                    'Closed': 'gray'
                }.get(status, 'blue')
                status_html += f'<li><span style="color:{status_color}">{status}</span>: {count}</li>'
            
            st.markdown(f"""
            <div class="crime-card">
                <h4>Report Statistics</h4>
                <p><strong>Total Reports:</strong> {len(user_reports)}</p>
                <p><strong>Reports by Status:</strong></p>
                <ul>{status_html}</ul>
            </div>
            """, unsafe_allow_html=True)
        
        # Security Settings Section
        st.markdown("""
        <div style="background-color: #f8f9fa; padding: 1rem; border-radius: 5px; margin: 1rem 0;">
            <h3 style="color: #2c3e50;">🔒 Security Settings</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Password Reset Form
        with st.expander("Reset Password"):
            with st.form("password_reset_form"):
                current_password = st.text_input("Current Password", type="password")
                new_password = st.text_input("New Password", type="password")
                confirm_new_password = st.text_input("Confirm New Password", type="password")
                
                # Password requirements info
                st.info("""
                Password Requirements:
                - At least 8 characters long
                - At least one uppercase letter
                - At least one lowercase letter
                - At least one number
                - At least one special character (!@#$%^&*(),.?":{}|<>)
                """)
                
                if st.form_submit_button("Reset Password"):
                    if new_password != confirm_new_password:
                        st.error("New passwords do not match!")
                    else:
                        success, message = Authentication.reset_password(
                            st.session_state.username,
                            current_password,
                            new_password
                        )
                        if success:
                            st.success(message)
                            # Clear the form
                            st.rerun()
                        else:
                            st.error(message)
        
        # Admin Section (only visible to admins)
        if user_info.get('role') == 'admin':
            st.markdown("""
            <div style="background-color: #f8f9fa; padding: 1rem; border-radius: 5px; margin: 1rem 0;">
                <h3 style="color: #2c3e50;">👑 Admin Controls</h3>
            </div>
            """, unsafe_allow_html=True)
            
            with st.expander("User Role Management"):
                users = Authentication.load_users()
                
                # Remove current admin from the list
                users_list = [user for user in users.keys() if user != st.session_state.username]
                
                if users_list:
                    selected_user = st.selectbox("Select User", users_list)
                    new_role = st.selectbox("New Role", ["user", "admin"])
                    
                    if st.button("Update Role"):
                        success, message = Authentication.update_user_role(
                            selected_user,
                            new_role,
                            st.session_state.username
                        )
                        if success:
                            st.success(message)
                        else:
                            st.error(message)
                else:
                    st.info("No other users to manage")
        
        # Account Activity Section
        st.markdown("""
        <div style="background-color: #f8f9fa; padding: 1rem; border-radius: 5px; margin: 1rem 0;">
            <h3 style="color: #2c3e50;">📊 Account Activity</h3>
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander("Recent Activity"):
            if user_reports:
                for report in sorted(user_reports, key=lambda x: x.get('timestamp', ''), reverse=True)[:5]:
                    st.markdown(f"""
                    <div class="crime-card">
                        <p><strong>Report #{report['id']}</strong> - {report.get('crime_type')}</p>
                        <p>Status: {report.get('status', 'Submitted')}</p>
                        <p>Submitted: {report.get('timestamp', 'Unknown')}</p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No recent activity")
                
    else:
        st.error("User information not available. Please log out and log in again.")

def main():
    """Main application controller."""
    # Initialize session state variables
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'show_registration' not in st.session_state:
        st.session_state.show_registration = False
    if 'username' not in st.session_state:
        st.session_state.username = None
    if 'active_tab' not in st.session_state:
        st.session_state.active_tab = "Report Crime"
    if 'report_to_update' not in st.session_state:
        st.session_state.report_to_update = None
    
    # Sidebar for navigation when logged in
    if st.session_state.logged_in:
        # Style the sidebar
        st.markdown("""
        <style>
        [data-testid="stSidebar"] {
            background-color: #2c3e50;
            color: white;
            padding: 1rem;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Add logo or badge to sidebar
        st.sidebar.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <h2>🚨 Crime Reporting</h2>
            <p>Serving the community</p>
        </div>
        """, unsafe_allow_html=True)
        
        menu = st.sidebar.radio("Navigation", 
            ["Report Crime", "View Reports", "Notifications", "Account", "Logout"],
            index=["Report Crime", "View Reports", "Notifications", "Account", "Logout"].index(st.session_state.active_tab) 
                  if st.session_state.active_tab in ["Report Crime", "View Reports", "Notifications", "Account", "Logout"] else 0
        )
        
        # Add user info to sidebar
        st.sidebar.markdown(f"""
        <div style="background-color: rgba(255, 255, 255, 0.1); padding: 1rem; border-radius: 5px; margin-top: 2rem;">
            <p>Logged in as: <strong>{st.session_state.username}</strong></p>
        </div>
        """, unsafe_allow_html=True)
        
        # Update active tab
        st.session_state.active_tab = menu
        
        if menu == "Report Crime":
            crime_reporting_page()
        elif menu == "View Reports":
            view_reports_page()
        elif menu == "Notifications":
            notifications_page()
        elif menu == "Account":
            account_page()
        elif menu == "Logout":
            # Clear session state
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.session_state.logged_in = False
            st.session_state.username = None
            st.rerun()
    else:
        # Show login or registration page
        if st.session_state.show_registration:
            registration_page()
        else:
            login_page()

if __name__ == "__main__":
    # Page configuration
    st.set_page_config(
        page_title="Crime Reporting System", 
        page_icon="🚨",
        layout="wide"
    )
    
    main()
