import json
import streamlit as st
from datetime import datetime

class CrimeReporting:
    @staticmethod
    def load_reports():
        """Load crime reports from JSON file."""
        try:
            with open('crime_reports.json', 'r') as f:
                content = f.read().strip()
                # If file is empty, return an empty list
                if not content:
                    return []
                return json.loads(content)
        except (FileNotFoundError, json.JSONDecodeError):
            # Create an empty file if it doesn't exist or is invalid
            with open('crime_reports.json', 'w') as f:
                json.dump([], f)
            return []
    
    @staticmethod
    def save_report(report, username):
        """Save a new crime report to JSON file."""
        reports = CrimeReporting.load_reports()
        
        # Add timestamp to the report
        report['timestamp'] = datetime.now().isoformat()
        
        # Generate a unique ID
        report['id'] = len(reports) + 1
        
        # Add username of reporter
        report['reported_by'] = username
        
        # Add status field for tracking
        report['status'] = 'Submitted'
        
        # Add feedback field
        report['feedback'] = []
        
        # Add notifications field
        report['notifications'] = [{
            'timestamp': datetime.now().isoformat(),
            'message': f"Report #{len(reports) + 1} has been submitted"
        }]
        
        reports.append(report)
        
        with open('crime_reports.json', 'w') as f:
            json.dump(reports, f, indent=4)
        
        return report['id']
    
    @staticmethod
    def filter_reports(reports, filter_type=None, filter_value=None, search_term=None):
        """Filter reports based on criteria."""
        filtered_reports = reports
        
        # Filter by type (category)
        if filter_type and filter_type != "All" and filter_value:
            if filter_type == "crime_type":
                filtered_reports = [r for r in filtered_reports if r.get('crime_type') == filter_value]
            elif filter_type == "status":
                filtered_reports = [r for r in filtered_reports if r.get('status') == filter_value]
            elif filter_type == "date":
                filtered_reports = [r for r in filtered_reports if r.get('incident_date') == filter_value]
        
        # Search term across multiple fields
        if search_term:
            search_term = search_term.lower()
            filtered_reports = [r for r in filtered_reports if 
                                search_term in r.get('crime_type', '').lower() or
                                search_term in r.get('location', '').lower() or
                                search_term in r.get('description', '').lower()]
        
        return filtered_reports
    
    @staticmethod
    def update_report_status(report_id, new_status):
        """Update the status of a report."""
        reports = CrimeReporting.load_reports()
        
        for report in reports:
            if report['id'] == report_id:
                old_status = report.get('status', 'Submitted')
                report['status'] = new_status
                
                # Add notification for status change
                if 'notifications' not in report:
                    report['notifications'] = []
                
                report['notifications'].append({
                    'timestamp': datetime.now().isoformat(),
                    'message': f"Status changed from {old_status} to {new_status}"
                })
                
                with open('crime_reports.json', 'w') as f:
                    json.dump(reports, f, indent=4)
                
                return True
        
        return False
    
    @staticmethod
    def add_feedback(report_id, feedback_text, username):
        """Add feedback to a report."""
        reports = CrimeReporting.load_reports()
        
        for report in reports:
            if report['id'] == report_id:
                if 'feedback' not in report:
                    report['feedback'] = []
                
                report['feedback'].append({
                    'user': username,
                    'text': feedback_text,
                    'timestamp': datetime.now().isoformat()
                })
                
                # Add notification for feedback
                if 'notifications' not in report:
                    report['notifications'] = []
                
                report['notifications'].append({
                    'timestamp': datetime.now().isoformat(),
                    'message': f"New feedback added by {username}"
                })
                
                with open('crime_reports.json', 'w') as f:
                    json.dump(reports, f, indent=4)
                
                return True
        
        return False
    
    @staticmethod
    def delete_report(report_id, username):
        """Delete a report if it belongs to the user or if user is admin."""
        reports = CrimeReporting.load_reports()
        
        for i, report in enumerate(reports):
            if report['id'] == report_id:
                # Check if the user has permission to delete
                if report.get('reported_by') == username or username == 'admin':
                    # Remove the report
                    del reports[i]
                    
                    # Save the updated list
                    with open('crime_reports.json', 'w') as f:
                        json.dump(reports, f, indent=4)
                    
                    return True
        
        return False
    
    @staticmethod
    def update_report(report_id, updated_data, username):
        """Update report details if it belongs to the user or if user is admin."""
        reports = CrimeReporting.load_reports()
        
        for report in reports:
            if report['id'] == report_id:
                # Check if the user has permission to update
                if report.get('reported_by') == username or username == 'admin':
                    # Track changes for notification
                    changes = []
                    
                    # Update fields
                    if 'crime_type' in updated_data and updated_data['crime_type'] != report.get('crime_type'):
                        changes.append(f"Crime type changed from '{report.get('crime_type')}' to '{updated_data['crime_type']}'")
                        report['crime_type'] = updated_data['crime_type']
                    
                    if 'location' in updated_data and updated_data['location'] != report.get('location'):
                        changes.append(f"Location changed from '{report.get('location')}' to '{updated_data['location']}'")
                        report['location'] = updated_data['location']
                    
                    if 'incident_date' in updated_data and updated_data['incident_date'] != report.get('incident_date'):
                        changes.append(f"Incident date changed from '{report.get('incident_date')}' to '{updated_data['incident_date']}'")
                        report['incident_date'] = updated_data['incident_date']
                    
                    if 'description' in updated_data and updated_data['description'] != report.get('description'):
                        changes.append("Report description was updated")
                        report['description'] = updated_data['description']
                    
                    if 'severity' in updated_data and updated_data['severity'] != report.get('severity'):
                        changes.append(f"Severity changed from {report.get('severity')} to {updated_data['severity']}")
                        report['severity'] = updated_data['severity']
                    
                    # Add notification for changes
                    if changes:
                        if 'notifications' not in report:
                            report['notifications'] = []
                        
                        report['notifications'].append({
                            'timestamp': datetime.now().isoformat(),
                            'message': f"Report updated by {username}: " + "; ".join(changes)
                        })
                        
                        # Save the updated reports
                        with open('crime_reports.json', 'w') as f:
                            json.dump(reports, f, indent=4)
                        
                        return True, changes
                    
                    return True, []  # No changes made
        
        return False, []
    
    @staticmethod
    def view_reports(filter_type=None, filter_value=None, search_term=None, username=None):
        """View crime reports with filtering and user-specific view."""
        reports = CrimeReporting.load_reports()
        
        # Apply filters
        if filter_type or search_term:
            reports = CrimeReporting.filter_reports(reports, filter_type, filter_value, search_term)
        
        if not reports:
            st.info("No crime reports found.")
            return
        
        # Display filter counts
        total_reports = len(CrimeReporting.load_reports())
        st.caption(f"Showing {len(reports)} of {total_reports} total reports")
        
        # Create columns for report details
        for report in reports:
            # Color-code based on severity
            severity = report.get('severity', 5)
            if severity <= 3:
                color = "green"
            elif severity <= 6:
                color = "orange"
            else:
                color = "red"
            
            # Show report status
            status = report.get('status', 'Submitted')
            status_color = {
                'Submitted': 'blue',
                'Under Investigation': 'orange',
                'Resolved': 'green',
                'Closed': 'gray'
            }.get(status, 'blue')
            
            with st.expander(f"Report #{report['id']} - {report.get('crime_type', 'Unknown Crime')} - {status}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Crime Type:** {report.get('crime_type', 'N/A')}")
                    st.write(f"**Location:** {report.get('location', 'N/A')}")
                    st.write(f"**Date of Incident:** {report.get('incident_date', 'N/A')}")
                    st.write(f"**Reported By:** {report.get('reported_by', 'Anonymous')}")
                
                with col2:
                    st.write(f"**Description:** {report.get('description', 'N/A')}")
                    st.write(f"**Reported At:** {report['timestamp']}")
                    st.markdown(f"**Severity:** <span style='color:{color}'>{severity}/10</span>", unsafe_allow_html=True)
                    st.markdown(f"**Status:** <span style='color:{status_color}'>{status}</span>", unsafe_allow_html=True)
                
                # Action buttons section (Update and Delete)
                if report.get('reported_by') == username or username == 'admin':
                    col1, col2 = st.columns(2)
                    with col1:
                        # Add report ID and timestamp to make key unique
                        update_key = f"update_{report['id']}_{report.get('timestamp', '')}"
                        if st.button(f"Update Report #{report['id']}", key=update_key):
                            st.session_state.report_to_update = report
                            st.rerun()
                    with col2:
                        # Add report ID and timestamp to make key unique
                        delete_key = f"delete_{report['id']}_{report.get('timestamp', '')}"
                        if st.button(f"Delete Report #{report['id']}", key=delete_key):
                            if CrimeReporting.delete_report(report['id'], username):
                                st.success(f"Report #{report['id']} has been deleted.")
                                st.rerun()
                            else:
                                st.error("Failed to delete report.")
                
                # Show Update Form if this report is selected for update
                if 'report_to_update' in st.session_state and st.session_state.report_to_update and st.session_state.report_to_update['id'] == report['id']:
                    st.subheader(f"Update Report #{report['id']}")
                    # Add report ID and timestamp to make form key unique
                    form_key = f"update_form_{report['id']}_{report.get('timestamp', '')}"
                    with st.form(form_key):
                        updated_crime_type = st.selectbox(
                            "Type of Crime", 
                            ["Theft", "Assault", "Burglary", "Fraud", "Cybercrime", "Other"],
                            index=["Theft", "Assault", "Burglary", "Fraud", "Cybercrime", "Other"].index(report.get('crime_type', 'Other')),
                            key=f"crime_type_{form_key}"
                        )
                        
                        updated_location = st.text_input(
                            "Location of Incident", 
                            value=report.get('location', ''),
                            key=f"location_{form_key}"
                        )
                        updated_date = st.date_input(
                            "Date of Incident", 
                            value=datetime.strptime(report.get('incident_date', datetime.now().strftime('%Y-%m-%d')), '%Y-%m-%d').date(),
                            key=f"date_{form_key}"
                        )
                        updated_description = st.text_area(
                            "Detailed Description", 
                            value=report.get('description', ''),
                            key=f"description_{form_key}"
                        )
                        updated_severity = st.slider(
                            "Incident Severity", 
                            1, 10, 
                            report.get('severity', 5),
                            key=f"severity_{form_key}"
                        )
                        
                        update_status = False
                        if username == 'admin':  # Only admin can update status
                            update_status = True
                            updated_status = st.selectbox(
                                "Status", 
                                ["Submitted", "Under Investigation", "Resolved", "Closed"],
                                index=["Submitted", "Under Investigation", "Resolved", "Closed"].index(report.get('status', 'Submitted')),
                                key=f"status_{form_key}"
                            )
                        
                        submit_update = st.form_submit_button("Submit Update")
                        
                        if submit_update:
                            # Prepare updated data
                            updated_data = {
                                'crime_type': updated_crime_type,
                                'location': updated_location,
                                'incident_date': str(updated_date),
                                'description': updated_description,
                                'severity': updated_severity
                            }
                            
                            # Update status if allowed
                            if update_status:
                                updated_data['status'] = updated_status
                            
                            # Update the report
                            success, changes = CrimeReporting.update_report(report['id'], updated_data, username)
                            
                            if success:
                                if changes:
                                    st.success(f"Report #{report['id']} updated successfully!")
                                else:
                                    st.info("No changes were made to the report.")
                                    
                                # Clear the update state
                                del st.session_state.report_to_update
                                st.rerun()
                            else:
                                st.error("Failed to update report.")
                
                # Notifications section
                if 'notifications' in report and report['notifications']:
                    st.write("**Notifications:**")
                    for notif in report['notifications']:
                        st.info(f"{notif['message']} - {notif['timestamp']}")
                
                # Feedback section
                st.write("**Feedback:**")
                if 'feedback' in report and report['feedback']:
                    for feedback in report['feedback']:
                        st.write(f"From {feedback['user']} on {feedback['timestamp']}: {feedback['text']}")
                
                # Add feedback form if this is the user's report or if they're an admin
                if username:  # Only logged-in users can add feedback
                    # Add report ID and timestamp to make feedback form key unique
                    feedback_form_key = f"feedback_form_{report['id']}_{report.get('timestamp', '')}"
                    with st.form(feedback_form_key):
                        feedback_text = st.text_area(
                            "Add Feedback or Update", 
                            key=f"feedback_{feedback_form_key}"
                        )
                        submit_feedback = st.form_submit_button("Submit Feedback")
                        
                        if submit_feedback and feedback_text:
                            if CrimeReporting.add_feedback(report['id'], feedback_text, username):
                                st.success("Feedback added successfully!")
                                st.rerun()
                            else:
                                st.error("Failed to add feedback.")
                
                st.divider()
