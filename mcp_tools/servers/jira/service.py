    
import requests
from typing import Dict, Any
import os
import logging

# Set up logging
logger = logging.getLogger(__name__)

# Jira configuration
JIRA_BASE_URL = os.getenv("JIRA_BASE_URL", "https://wljira.wenlin.net")
JIRA_AUTH_TOKEN = os.getenv("JIRA_AUTH_TOKEN")

class JiraService:
    """Service class for interacting with Jira API."""
    
    def __init__(self):
        self.base_url = JIRA_BASE_URL
        self.auth_token = JIRA_AUTH_TOKEN
        self.headers = {
            'Authorization': f'Bearer {self.auth_token}',
            'Content-Type': 'application/json'
        }

    def get_ticket_details(self, ticket_key: str) -> Dict[str, Any]:
        """Fetch details for a specific Jira ticket."""
        try:
            url = f"{self.base_url}/rest/api/2/issue/{ticket_key}?fields=*all,customfield_13544"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()

            ticket_data = response.json()
            # Extract Sprint name from customfield_13543 if present
            sprint_name = None
            sprint_field = ticket_data['fields'].get('customfield_13543')
            if sprint_field and isinstance(sprint_field, list) and sprint_field[0]:
                import re
                match = re.search(r'name=([^,\]]+)', sprint_field[0])
                if match:
                    sprint_name = match.group(1)

            # Extract Tech Category value from customfield_14746 if present
            tech_category = None
            tech_cat_field = ticket_data['fields'].get('customfield_14746')
            if tech_cat_field and isinstance(tech_cat_field, dict):
                tech_category = tech_cat_field.get('value')

            # Extract Fix Version name from fixVersions if present
            fix_version = None
            fix_versions_field = ticket_data['fields'].get('fixVersions')
            if fix_versions_field and isinstance(fix_versions_field, list) and len(fix_versions_field) > 0:
                fix_version = fix_versions_field[0].get('name')

            # Extract Story Points from customfield_10121 if present
            story_points = ticket_data['fields'].get('customfield_10121')

            # Extract Saved Story Points from customfield_39640 if present (optional)
            saved_story_points = ticket_data['fields'].get('customfield_39640')

            # Extract Epic Link from customfield_13544 if present
            epic_link = ticket_data['fields'].get('customfield_13544')

            result = {
                'key': ticket_data['key'],
                'project_id': ticket_data['fields']['project']['id'],
                'project_key': ticket_data['fields']['project']['key'],
                'issue_type': ticket_data['fields']['issuetype']['name'],
                'summary': ticket_data['fields']['summary'],
                'acceptance_criteria': ticket_data['fields']['customfield_10253'],
                'description': ticket_data['fields']['description'],
                'status': ticket_data['fields']['status']['name'],
                'priority': ticket_data['fields']['priority']['name'],
                'assignee': ticket_data['fields']['assignee']['name'] if ticket_data['fields']['assignee'] else None,
                'components': [comp['name'] for comp in ticket_data['fields'].get('components', [])],
                'labels': ticket_data['fields'].get('labels', []),
                'sprint_name': sprint_name,
                'tech_category': tech_category,
                'fix_version': fix_version,
                'story_points': story_points,
                'epic_link': epic_link,
                'saved_story_points': saved_story_points,
            }
            # If issue_type is Bug, extract additional fields
            if result['issue_type'].lower() == 'bug':
                fields = ticket_data['fields']
                # Steps to Reproduce
                result['steps_to_reproduce'] = fields.get('customfield_25647')
                # Expected Result(s)
                result['expected_results'] = fields.get('customfield_26140')
                # Actual Result(s)
                result['actual_results'] = fields.get('customfield_27140')
                # Severity
                severity_field = fields.get('customfield_11947')
                result['severity'] = severity_field.get('value') if isinstance(severity_field, dict) else None
                # Detected In
                detected_in_field = fields.get('customfield_14849')
                result['detected_in'] = detected_in_field.get('value') if isinstance(detected_in_field, dict) else None
                # Root Cause
                root_cause_field = fields.get('customfield_12049')
                result['root_cause'] = root_cause_field.get('value') if isinstance(root_cause_field, dict) else None
                # Root Cause Description
                result['root_cause_description'] = fields.get('customfield_10415')
            return result
        except Exception as e:
            logger.error(f"Error fetching Jira ticket details: {str(e)}")
            raise
    
    def review_ticket_against_template(self, ticket_key: str, template_path: str = None, add_comment: bool = False) -> dict:
        """
        Review a JIRA ticket against the YAML-based template specification in template.md.
        Args:
            ticket_key: The JIRA ticket number (e.g., 'MS-TECH-123')
            template_path: Optional path to the template.md file (default: workspace root)
            add_comment: Whether to automatically add a comment to the ticket if issues are found
        Returns:
            dict: Structured feedback with findings, suggestions, and compliance status.
        """
        import re
        import os
        # 1. Get ticket details
        ticket = self.get_ticket_details(ticket_key)
        if not ticket or 'error' in ticket.get('status', '').lower():
            return {'status': 'error', 'message': f'Could not fetch ticket {ticket_key}', 'details': ticket}

        # 2. Load template.md
        if not template_path:
            # Default to servers/jira/template.md
            template_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'template.md'))
        try:
            with open(template_path, encoding='utf-8') as f:
                template_text = f.read()
        except Exception as e:
            return {'status': 'error', 'message': f'Could not read template.md: {str(e)}'}

        # 3. Parse the YAML template structure
        issue_type = ticket.get('issue_type', '').lower()
        
        # 4. Review ticket fields against YAML template requirements
        feedback = []
        errors = 0
        warnings = 0
        
        def check_required(field_name, value, advice=None):
            nonlocal errors
            if not value or (isinstance(value, str) and value.strip() in ['', '.']):
                msg = f"❌ Missing or invalid required field: {field_name}"
                if advice:
                    msg += f". {advice}"
                feedback.append(msg)
                errors += 1
                return False
            return True

        def check_optional(field_name, value, advice=None):
            nonlocal warnings
            if not value or (isinstance(value, str) and value.strip() in ['', '.']):
                msg = f"⚠️ Optional field missing: {field_name}"
                if advice:
                    msg += f". {advice}"
                feedback.append(msg)
                warnings += 1
                return False
            return True

        # Core required fields for all types
        check_required('Summary', ticket.get('summary'), 
                      "Must be non-empty and descriptive, not just '.'")
        
        # Check if Epic Link exists and is not closed
        epic_link = ticket.get('epic_link')
            
        if not epic_link:
            feedback.append("❌ Missing required field: Epic Link. Must reference an Epic that is not Closed.")
            errors += 1
        else:
            # Epic link exists, could add validation for epic status here if needed
            pass
        
        # Check Tech Category matches Epic's Tech Category
        tech_category = ticket.get('tech_category')
        if not tech_category:
            feedback.append("❌ Missing required field: Tech Category. Must match Epic's Tech Category.")
            errors += 1

        # Type-specific validations based on template requirements
        if 'story' in issue_type or issue_type == 'story':
            feedback.append("📋 **User Story Template Review:**")
            
            # REQUIRED: as_a, i_want_to, so_that (check in summary or description)
            description = ticket.get('description') or ''
            summary = ticket.get('summary') or ''
            combined_text = f"{summary} {description}"
            
            if not re.search(r'(?i)as\s+a\s+[^,\n]+', combined_text):
                check_required('as_a', None, "Must specify 'As a [user type]' (e.g., Consumer, Dev, Product Manager)")
            
            if not re.search(r'(?i)i\s+want\s+(to\s+)?[^,\n]+', combined_text):
                check_required('i_want_to', None, "Must specify 'I want to [action]'")
            
            if not re.search(r'(?i)so\s+that\s+[^,\n]+', combined_text):
                check_required('so_that', None, "Must specify 'So that [benefit/value]'")
            
            # REQUIRED: description (background, scope)
            check_required('Description', description, "Must include background and scope")
            
            # REQUIRED: acceptance_criteria (Gherkin/bullets; must define "done")
            if description and not re.search(r'(?i)(acceptance\s+criteria|given.*when.*then|\*\s+.*\n|\-\s+.*\n)', description):
                check_required('Acceptance Criteria', None, 
                              "Must be in Gherkin format (Given/When/Then) or bullet points that define 'done'")
            
            # Optional fields - only mention if not present, don't mark as errors
            if description and not re.search(r'(?i)(user\s+impact|impact)', description):
                feedback.append("ℹ️ Optional: Consider adding User Impact (who/how often/risk)")
            
            if description and not re.search(r'(?i)(dependencies|depends\s+on)', description):
                feedback.append("ℹ️ Optional: Consider listing Dependencies (tickets/APIs/systems)")
                
            if description and not re.search(r'(?i)(assumptions|assume)', description):
                feedback.append("ℹ️ Optional: Consider documenting Assumptions")

        elif 'bug' in issue_type or issue_type == 'bug':
            feedback.append("🐛 **Bug Template Review:**")
            
            # REQUIRED: description (when it started + impact)
            check_required('Description', ticket.get('description'), 
                          "Must explain when it started and the impact")
            
            # REQUIRED: steps_to_reproduce (numbered atomic steps)
            check_required('Steps to Reproduce', ticket.get('steps_to_reproduce'),
                          "Must be numbered atomic steps (1), (2), etc.")
            
            # REQUIRED: expected_result
            check_required('Expected Result', ticket.get('expected_results'),
                          "Must specify what should happen")
            
            # REQUIRED: actual_result  
            check_required('Actual Result', ticket.get('actual_results'),
                          "Must specify what actually happens")
            
            # REQUIRED: detected_in (env details: browser, OS, device, environment)
            check_required('Environment (Detected In)', ticket.get('detected_in'),
                          "Must include browser, OS, device, environment (Staging/Prod)")
            
            # REQUIRED: detected_by (Automated/Manual/Internal/External)
            detected_by = ticket.get('detected_by')
            if not detected_by or detected_by.lower() not in ['automated', 'manual', 'internal', 'external']:
                check_required('Detected By', detected_by,
                              "Must be Automated, Manual, Internal, or External")
            
            # REQUIRED: severity
            severity = ticket.get('severity')
            if not severity or severity.lower() not in ['critical', 'high', 'medium', 'low']:
                check_required('Severity', severity, "Must be Critical, High, Medium, or Low")
            
            # REQUIRED: priority
            priority = ticket.get('priority')
            if not priority or priority.lower() not in ['critical', 'high', 'medium', 'low', 'minor', 'unprioritized']:
                check_required('Priority', priority, 
                              "Must be Critical, High, Medium, Low, Minor, or Unprioritized")
            
            # REQUIRED: logs_screenshots (when available)
            logs_screenshots = ticket.get('logs_screenshots') or ticket.get('attachments')
            if not logs_screenshots:
                feedback.append("❌ Missing logs/screenshots. Required to attach when available for investigation")
                errors += 1
            
            # Optional: sprint
            if not ticket.get('sprint_name'):
                feedback.append("ℹ️ Optional: Consider adding Sprint assignment")

        elif 'task' in issue_type or issue_type == 'task':
            feedback.append("📝 **Task Template Review:**")
            
            # REQUIRED: description (objective + steps + tools)
            check_required('Description', ticket.get('description'),
                          "Must include objective, steps, and tools/technologies involved")
            
            # REQUIRED if validation is needed: acceptance_criteria
            description = ticket.get('description') or ''
            if description and any(keyword in description.lower() for keyword in ['validation', 'test', 'verify', 'check', 'validate']):
                if not re.search(r'(?i)(acceptance\s+criteria|given.*when.*then|\*\s+.*\n|\-\s+.*\n)', description):
                    check_required('Acceptance Criteria', None, 
                                  "Required since validation is mentioned. Use Gherkin format or bullet points")
            
            # Optional: dependencies
            if description and not re.search(r'(?i)(dependencies|depends\s+on)', description):
                feedback.append("ℹ️ Optional: Consider listing Dependencies (tasks/systems/resources)")

        else:
            feedback.append(f"⚠️ Issue type '{issue_type}' not recognized. Supported types: Story, Bug, Task")
            warnings += 1

        # Optional but recommended: attachments
        attachments = ticket.get('attachments')
        if not attachments:
            feedback.append("ℹ️ Optional: Consider adding attachments (Figma designs, logs, videos, specs) if relevant")

        # Check labels/components (not in template but helpful for organization)
        if not ticket.get('labels') and not ticket.get('components'):
            feedback.append("ℹ️ Optional: Consider adding labels or components for better organization")

        # 5. Overall compliance assessment
        compliant = (errors == 0)
        compliance_level = "EXCELLENT" if errors == 0 and warnings == 0 else \
                          "GOOD" if errors == 0 and warnings <= 2 else \
                          "NEEDS_IMPROVEMENT" if errors <= 2 else \
                          "POOR"

        # 6. Get reporter and assignee information with email addresses
        reporter_name = None
        reporter_email = None
        assignee_name = ticket.get('assignee')
        assignee_email = None
        
        try:
            url = f"{self.base_url}/rest/api/2/issue/{ticket_key}"
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                full_ticket_data = response.json()
                
                # Get creator (reporter) info - JIRA uses 'creator' field
                creator_data = full_ticket_data['fields'].get('creator')
                if creator_data:
                    reporter_name = creator_data.get('name')
                    reporter_email = creator_data.get('emailAddress')
                
                # Get assignee info
                assignee_data = full_ticket_data['fields'].get('assignee')
                if assignee_data:
                    assignee_name = assignee_data.get('name')
                    assignee_email = assignee_data.get('emailAddress')
                    
        except Exception as e:
            logger.warning(f"Could not fetch user info for {ticket_key}: {str(e)}")

        # 7. Generate formatted feedback message with JIRA mention tags for notifications
        reporter_tag = f"[~{reporter_name}]" if reporter_name else f"[~{reporter_email}]" if reporter_email else "Reporter"
        assignee_tag = f"[~{assignee_name}]" if assignee_name else f"[~{assignee_email}]" if assignee_email else "Unassigned"
        
        # Handle case where reporter and assignee are the same person
        cc_section = ""
        if assignee_name and assignee_name != reporter_name:
            cc_section = f"\n\nCC: {assignee_tag}"
        elif assignee_email and assignee_email != reporter_email:
            cc_section = f"\n\nCC: {assignee_tag}"
        
        if compliant:
            formatted_message = f"Hi {reporter_tag},\n\n✅ This ticket meets wenlin template standards - Thanks!{cc_section}\n\n---\n*This is an auto-generated comment from template validation.*"
        else:
            # Extract missing/incorrect fields
            format_incorrect = []
            missing_or_empty = []
            
            for item in feedback:
                if item.startswith('❌'):
                    # Parse the error message
                    if 'format' in item.lower() or 'criteria' in item.lower() or 'structure' in item.lower():
                        format_incorrect.append(item.replace('❌ ', '').replace('Missing or invalid required field: ', ''))
                    else:
                        missing_or_empty.append(item.replace('❌ ', '').replace('Missing or invalid required field: ', ''))
            
            formatted_message = f"Hi {reporter_tag},\n\n"
            formatted_message += "Please update this ticket to add/update below fields to meet wenlin template standards - Thanks\n\n"
            
            if format_incorrect:
                formatted_message += "Format Incorrect:\n"
                for item in format_incorrect:
                    formatted_message += f"• {item}\n"
                formatted_message += "\n"
            
            if missing_or_empty:
                formatted_message += "Missing or Empty:\n"
                for item in missing_or_empty:
                    formatted_message += f"• {item}\n"
                formatted_message += "\n"
            
            formatted_message += f"{cc_section}\n\n---\n*This is an auto-generated comment from template validation.*"
        
        # Add comment to ticket if requested and there are issues
        comment_status = None
        if add_comment and not compliant:
            comment_status = self._add_comment_to_ticket(ticket_key, formatted_message)
        
        return {
            'status': 'success',
            'ticket_key': ticket_key,
            'issue_type': issue_type,
            'compliant': compliant,
            'compliance_level': compliance_level,
            'errors': errors,
            'warnings': warnings,
            'formatted_message': formatted_message,
            'comment_status': comment_status,
            'template_version': '1.0',
            'template_type': 'yaml_spec',
            'tagged_users': {
                'reporter': {
                    'name': reporter_name,
                    'email': reporter_email
                },
                'assignee': {
                    'name': assignee_name,
                    'email': assignee_email
                }
            }
        }        

    def _format_review_comment(self, ticket_key: str, issue_type: str, passed: bool, feedback: list, reporter_name: str = None, assignee_name: str = None) -> str:
        """
        Format the review feedback into a structured comment for the ticket.
        
        Args:
            ticket_key: The ticket key being reviewed
            issue_type: The type of issue (story, bug, task)
            passed: Whether the ticket passed the review
            feedback: List of feedback items
            reporter_name: Name of the ticket reporter for tagging
            assignee_name: Name of the ticket assignee for tagging
            
        Returns:
            Formatted comment text
        """
        try:
            # Header with overall status
            if passed:
                header = f"✅ **Ticket Quality Review - PASSED**\n\n"
                header += f"This {issue_type} ticket meets the template requirements and best practices.\n\n"
            else:
                header = f"⚠️ **Ticket Quality Review - NEEDS IMPROVEMENT**\n\n"
                header += f"This {issue_type} ticket requires updates to meet template standards.\n\n"
            
            # Separate feedback into categories
            errors = [f for f in feedback if f.startswith('❌')]
            warnings = [f for f in feedback if f.startswith('⚠️')]
            info = [f for f in feedback if f.startswith('ℹ️')]
            
            comment_parts = [header]
            
            # Add errors section
            if errors:
                comment_parts.append("**❌ Required Improvements:**")
                for error in errors:
                    comment_parts.append(f"• {error[2:].strip()}")  # Remove emoji and leading space
                comment_parts.append("")
            
            # Add warnings section
            if warnings:
                comment_parts.append("**⚠️ Recommendations:**")
                for warning in warnings:
                    comment_parts.append(f"• {warning[3:].strip()}")  # Remove emoji and leading space
                comment_parts.append("")
            
            # Add best practices info (but keep it concise)
            if info and not any("Best Practices:" in item for item in info):
                comment_parts.append("**ℹ️ Additional Information:**")
                for info_item in info:
                    if not info_item.startswith('ℹ️ Best Practices:'):
                        comment_parts.append(f"• {info_item[3:].strip()}")
                comment_parts.append("")
            
            # Add footer with next steps
            if not passed:
                comment_parts.append("**Next Steps:**")
                comment_parts.append("1. Please address the required improvements above")
                comment_parts.append("2. Update the ticket fields as suggested")
                comment_parts.append("3. Ensure all acceptance criteria are clear and testable")
                comment_parts.append("")
            
            # Add user tags if available
            tags = []
            if reporter_name:
                tags.append(f"[~{reporter_name}]")
            if assignee_name and assignee_name != reporter_name:  # Don't duplicate if same person
                tags.append(f"[~{assignee_name}]")
            
            if tags:
                comment_parts.append(f"**Tagged for Review:** {' '.join(tags)}")
                comment_parts.append("")
            
            comment_parts.append(f"_Automated review generated for {ticket_key}_")
            
            return "\n".join(comment_parts)
            
        except Exception as e:
            logger.error(f"Error formatting review comment: {str(e)}")
            # Fallback to simple format
            status = "PASSED" if passed else "NEEDS IMPROVEMENT"
            simple_comment = f"Ticket Quality Review - {status}\n\n"
            simple_comment += "Feedback:\n"
            for item in feedback:
                simple_comment += f"• {item}\n"
            
            # Add tags even in fallback
            tags = []
            if reporter_name:
                tags.append(f"[~{reporter_name}]")
            if assignee_name and assignee_name != reporter_name:
                tags.append(f"[~{assignee_name}]")
            
            if tags:
                simple_comment += f"\nTagged: {' '.join(tags)}\n"
            
            return simple_comment

    def review_active_sprint_tickets(self, board_id: str) -> Dict[str, Any]:
        """
        Review all tickets in the active sprint for a given board.
        
        Args:
            board_id: The board ID to get the active sprint from
            
        Returns:
            Dict containing sprint details, review results, and summary
        """
        try:
            # Step 1: Get active sprint ID
            logger.info(f"Getting active sprint for board {board_id}")
            sprint_url = f"{self.base_url}/rest/agile/1.0/board/{board_id}/sprint?state=active"
            
            sprint_response = requests.get(sprint_url, headers=self.headers)
            sprint_response.raise_for_status()
            
            sprint_data = sprint_response.json()
            
            if not sprint_data.get('values'):
                return {
                    'status': 'error',
                    'message': f'No active sprint found for board {board_id}',
                    'board_id': board_id
                }
            
            # Extract sprint information
            active_sprint = sprint_data['values'][0]  # Get the first (and should be only) active sprint
            sprint_id = active_sprint['id']
            sprint_name = active_sprint['name']
            sprint_start = active_sprint.get('startDate')
            sprint_end = active_sprint.get('endDate')
            
            logger.info(f"Found active sprint: {sprint_name} (ID: {sprint_id})")
            
            # Step 2: Get all tickets in the sprint
            logger.info(f"Getting tickets for sprint {sprint_id}")
            tickets_url = f"{self.base_url}/rest/agile/1.0/sprint/{sprint_id}/issue"
            
            tickets_response = requests.get(tickets_url, headers=self.headers)
            tickets_response.raise_for_status()
            
            tickets_data = tickets_response.json()
            issues = tickets_data.get('issues', [])
            
            if not issues:
                return {
                    'status': 'success',
                    'message': f'No tickets found in sprint {sprint_name}',
                    'sprint_info': {
                        'id': sprint_id,
                        'name': sprint_name,
                        'start_date': sprint_start,
                        'end_date': sprint_end
                    },
                    'ticket_count': 0,
                    'review_results': []
                }
            
            logger.info(f"Found {len(issues)} tickets in sprint")
            
            # Step 3: Review each ticket
            review_results = []
            passed_tickets = []
            failed_tickets = []
            review_errors = []
            
            for issue in issues:
                ticket_key = issue['key']
                logger.info(f"Reviewing ticket {ticket_key}")
                
                try:
                    # Call the existing review method
                    review_result = self.review_ticket_against_template(ticket_key)
                    
                    if review_result.get('status') == 'success':
                        review_summary = {
                            'ticket_key': ticket_key,
                            'issue_type': review_result.get('issue_type'),
                            'compliant': review_result.get('compliant'),
                            'feedback_count': len(review_result.get('feedback', [])),
                            'comment_added': review_result.get('comment_added'),
                            'tagged_users': review_result.get('tagged_users')
                        }
                        
                        review_results.append(review_summary)
                        
                        if review_result.get('compliant'):
                            passed_tickets.append({
                                'key': ticket_key,
                                'type': review_result.get('issue_type'),
                                'summary': issue.get('fields', {}).get('summary', 'No summary')
                            })
                        else:
                            failed_tickets.append({
                                'key': ticket_key,
                                'type': review_result.get('issue_type'),
                                'summary': issue.get('fields', {}).get('summary', 'No summary'),
                                'issues_count': len([f for f in review_result.get('feedback', []) if f.startswith('❌')])
                            })
                    else:
                        error_summary = {
                            'ticket_key': ticket_key,
                            'error': review_result.get('message', 'Unknown error'),
                            'status': 'review_failed'
                        }
                        review_errors.append(error_summary)
                        
                except Exception as e:
                    logger.error(f"Error reviewing ticket {ticket_key}: {str(e)}")
                    review_errors.append({
                        'ticket_key': ticket_key,
                        'error': str(e),
                        'status': 'exception'
                    })
            
            # Step 4: Generate summary
            total_tickets = len(issues)
            passed_count = len(passed_tickets)
            failed_count = len(failed_tickets)
            error_count = len(review_errors)
            
            summary = {
                'total_tickets': total_tickets,
                'passed_validation': passed_count,
                'failed_validation': failed_count,
                'review_errors': error_count,
                'pass_rate': round((passed_count / total_tickets * 100), 2) if total_tickets > 0 else 0
            }
            
            return {
                'status': 'success',
                'board_id': board_id,
                'sprint_info': {
                    'id': sprint_id,
                    'name': sprint_name,
                    'start_date': sprint_start,
                    'end_date': sprint_end,
                    'goal': active_sprint.get('goal', ''),
                    'origin_board_id': active_sprint.get('originBoardId')
                },
                'summary': summary,
                'passed_tickets': passed_tickets,
                'failed_tickets': failed_tickets,
                'review_errors': review_errors if review_errors else None,
                'detailed_results': review_results,
                'message': f"Sprint review completed: {passed_count}/{total_tickets} tickets passed validation"
            }
            
        except requests.exceptions.HTTPError as e:
            error_msg = f"HTTP error during sprint review: {e.response.status_code}"
            if e.response.status_code == 404:
                error_msg += f" - Board {board_id} not found or no access"
            elif e.response.status_code == 403:
                error_msg += f" - Access denied to board {board_id}"
            
            logger.error(error_msg)
            return {
                'status': 'error',
                'message': error_msg,
                'board_id': board_id,
                'error_type': 'http_error',
                'status_code': e.response.status_code
            }
            
        except Exception as e:
            logger.error(f"Unexpected error during sprint review for board {board_id}: {str(e)}")
            return {
                'status': 'error',
                'message': str(e),
                'board_id': board_id,
                'error_type': 'unexpected_error'
            }

    def get_current_sprint_status(self, board_id: str) -> Dict[str, Any]:
        """
        Get the status of the current (active) sprint for a specific board.
        
        Args:
            board_id: The board ID to get the active sprint status for
            
        Returns:
            Dict containing current sprint status and metrics
        """
        try:
            logger.info(f"Getting current sprint status for board {board_id}")
            
            # Get only active sprints
            sprint_url = f"{self.base_url}/rest/agile/1.0/board/{board_id}/sprint?state=active"
            
            sprint_response = requests.get(sprint_url, headers=self.headers)
            sprint_response.raise_for_status()
            
            sprint_data = sprint_response.json()
            active_sprints = sprint_data.get('values', [])
            
            if not active_sprints:
                return {
                    'status': 'success',
                    'message': f'No active sprint found for board {board_id}',
                    'board_id': board_id,
                    'current_sprint': None
                }
            
            # Get the first active sprint (there should typically be only one)
            current_sprint = active_sprints[0]
            
            # Generate detailed report for the current sprint
            sprint_report = self._generate_single_sprint_report(current_sprint)
            
            return {
                'status': 'success',
                'board_id': board_id,
                'current_sprint': {
                    'id': current_sprint['id'],
                    'name': current_sprint['name'],
                    'state': current_sprint['state'],
                    'start_date': current_sprint.get('startDate'),
                    'end_date': current_sprint.get('endDate'),
                    'goal': current_sprint.get('goal', ''),
                    'report': sprint_report
                },
                'message': f"Current sprint status retrieved for {current_sprint['name']}"
            }
            
        except requests.exceptions.HTTPError as e:
            error_msg = f"HTTP error getting current sprint status: {e.response.status_code}"
            if e.response.status_code == 404:
                error_msg += f" - Board {board_id} not found"
            elif e.response.status_code == 403:
                error_msg += f" - Access denied to board {board_id}"
            
            logger.error(error_msg)
            return {
                'status': 'error',
                'message': error_msg,
                'board_id': board_id,
                'error_type': 'http_error',
                'status_code': e.response.status_code
            }
            
        except Exception as e:
            logger.error(f"Unexpected error getting current sprint status for board {board_id}: {str(e)}")
            return {
                'status': 'error',
                'message': str(e),
                'board_id': board_id,
                'error_type': 'unexpected_error'
            }

    def generate_sprint_report(self, board_id: str = None, sprint_id: str = None, start_date: str = None, end_date: str = None) -> Dict[str, Any]:
        """
        Generate comprehensive sprint reports with delivery, flow, and quality metrics.
        
        Args:
            board_id: The board ID to get sprints from (optional if sprint_id provided)
            sprint_id: The specific sprint ID to analyze (optional)
            start_date: Start date in YYYY-MM-DD format (optional)
            end_date: End date in YYYY-MM-DD format (optional)
            
        Returns:
            Dict containing sprint reports with detailed metrics
        """
        try:
            from datetime import datetime, timedelta
            import json
            
            # Validate input parameters
            if not board_id and not sprint_id:
                return {
                    'status': 'error',
                    'message': 'Either board_id or sprint_id must be provided',
                    'error_type': 'validation_error'
                }
            
            # If sprint_id is provided, get the specific sprint
            if sprint_id:
                logger.info(f"Generating sprint report for specific sprint {sprint_id}")
                
                # Get sprint details
                sprint_url = f"{self.base_url}/rest/agile/1.0/sprint/{sprint_id}"
                sprint_response = requests.get(sprint_url, headers=self.headers)
                sprint_response.raise_for_status()
                
                sprint = sprint_response.json()
                
                # Generate report for this specific sprint
                try:
                    sprint_report = self._generate_single_sprint_report(sprint)
                    return {
                        'status': 'success',
                        'sprint_id': sprint_id,
                        'board_id': sprint.get('originBoardId'),
                        'sprint_report': sprint_report,
                        'message': f"Generated report for sprint {sprint.get('name', sprint_id)}"
                    }
                except Exception as e:
                    logger.error(f"Error analyzing sprint {sprint_id}: {str(e)}")
                    return {
                        'status': 'error',
                        'sprint_id': sprint_id,
                        'message': f"Error analyzing sprint: {str(e)}",
                        'error_type': 'analysis_error'
                    }
            
            # If board_id is provided, get sprints for the board
            logger.info(f"Generating sprint report for board {board_id}")
            
            # Step 1: Prioritize active sprints when no date range is specified (current sprint status request)
            if not start_date and not end_date:
                # Get only active sprints for current sprint status
                logger.info("No date range specified - focusing on active sprint(s)")
                sprint_url = f"{self.base_url}/rest/agile/1.0/board/{board_id}/sprint?state=active&startAt=0&maxResults=100"
            else:
                # Get all sprints (active and closed) when date range is specified
                logger.info("Date range specified - analyzing all sprints in range")
                sprint_url = f"{self.base_url}/rest/agile/1.0/board/{board_id}/sprint?state=active,closed&startAt=0&maxResults=100"
            
            sprint_response = requests.get(sprint_url, headers=self.headers)
            sprint_response.raise_for_status()
            
            sprint_data = sprint_response.json()
            all_sprints = sprint_data.get('values', [])
            
            if not all_sprints:
                return {
                    'status': 'error',
                    'message': f'No sprints found for board {board_id}',
                    'board_id': board_id
                }
            
            # Step 2: Filter sprints by date range if provided
            filtered_sprints = []
            for sprint in all_sprints:
                sprint_start = sprint.get('startDate')
                sprint_end = sprint.get('endDate')
                
                # Skip sprints without dates
                if not sprint_start:
                    continue
                
                # Parse sprint dates
                try:
                    sprint_start_dt = datetime.fromisoformat(sprint_start.replace('Z', '+00:00'))
                    if sprint_end:
                        sprint_end_dt = datetime.fromisoformat(sprint_end.replace('Z', '+00:00'))
                    else:
                        sprint_end_dt = datetime.now()
                except:
                    continue
                
                # Apply date filters if provided
                include_sprint = True
                if start_date:
                    try:
                        start_dt = datetime.strptime(start_date, '%Y-%m-%d')
                        if sprint_end_dt < start_dt:
                            include_sprint = False
                    except:
                        pass
                
                if end_date and include_sprint:
                    try:
                        end_dt = datetime.strptime(end_date, '%Y-%m-%d')
                        if sprint_start_dt > end_dt:
                            include_sprint = False
                    except:
                        pass
                
                if include_sprint:
                    filtered_sprints.append(sprint)
            
            if not filtered_sprints:
                return {
                    'status': 'success',
                    'message': f'No sprints found in the specified date range',
                    'board_id': board_id,
                    'date_range': f"{start_date or 'all'} to {end_date or 'all'}",
                    'sprint_reports': []
                }
            
            logger.info(f"Found {len(filtered_sprints)} sprints to analyze")
            
            # Step 3: Generate report for each sprint
            sprint_reports = []
            
            for sprint in filtered_sprints:
                sprint_id = sprint['id']
                sprint_name = sprint['name']
                
                logger.info(f"Analyzing sprint: {sprint_name} (ID: {sprint_id})")
                
                try:
                    sprint_report = self._generate_single_sprint_report(sprint)
                    sprint_reports.append(sprint_report)
                    
                except Exception as e:
                    logger.error(f"Error analyzing sprint {sprint_name}: {str(e)}")
                    sprint_reports.append({
                        'sprint_id': sprint_id,
                        'sprint_name': sprint_name,
                        'status': 'error',
                        'error': str(e)
                    })
            
            # Step 4: Generate summary across all sprints
            summary_metrics = self._generate_sprint_summary(sprint_reports)
            
            return {
                'status': 'success',
                'board_id': board_id,
                'date_range': {
                    'start_date': start_date,
                    'end_date': end_date,
                    'sprints_analyzed': len(sprint_reports)
                },
                'summary_metrics': summary_metrics,
                'sprint_reports': sprint_reports,
                'message': f"Generated reports for {len(sprint_reports)} sprints"
            }
            
        except requests.exceptions.HTTPError as e:
            error_msg = f"HTTP error during sprint report generation: {e.response.status_code}"
            if e.response.status_code == 404:
                error_msg += f" - Board {board_id} not found"
            elif e.response.status_code == 403:
                error_msg += f" - Access denied to board {board_id}"
            
            logger.error(error_msg)
            return {
                'status': 'error',
                'message': error_msg,
                'board_id': board_id,
                'error_type': 'http_error',
                'status_code': e.response.status_code
            }
            
        except Exception as e:
            logger.error(f"Unexpected error during sprint report generation for board {board_id}: {str(e)}")
            return {
                'status': 'error',
                'message': str(e),
                'board_id': board_id,
                'error_type': 'unexpected_error'
            }

    def _generate_single_sprint_report(self, sprint: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate focused sprint report with only required sections.
        """
        from datetime import datetime
        import statistics
        
        sprint_id = sprint['id']
        sprint_name = sprint['name']
        sprint_state = sprint['state']
        sprint_start = sprint.get('startDate')
        sprint_end = sprint.get('endDate')
        
        # Get all issues in the sprint
        tickets_url = f"{self.base_url}/rest/agile/1.0/sprint/{sprint_id}/issue?maxResults=500"
        tickets_response = requests.get(tickets_url, headers=self.headers)
        tickets_response.raise_for_status()
        
        tickets_data = tickets_response.json()
        issues = tickets_data.get('issues', [])
        
        # Process tickets for analysis
        ticket_analysis = {
            'done': [],
            'in_progress': [],
            'to_do': [],
            'in_review': [],
            'in_qa': [],
            'high_priority': [],
            'bugs': [],
            'stories': [],
            'tasks': []
        }
        
        story_points_by_status = {
            'done': 0,
            'in_progress': 0,
            'to_do': 0,
            'in_review': 0,
            'in_qa': 0
        }
        
        tech_categories = {}
        aging_analysis = {}
        
        for issue in issues:
            fields = issue.get('fields', {})
            status = fields.get('status', {}).get('name', '').lower()
            issue_type = fields.get('issuetype', {}).get('name', '').lower()
            priority = fields.get('priority', {}).get('name', 'Unknown')
            assignee = fields.get('assignee')
            assignee_name = assignee.get('displayName', 'Unassigned') if assignee else 'Unassigned'
            created = fields.get('created', '')
            
            # Get story points (exclude 0 SP stories from main calculations)
            story_points = fields.get('customfield_10121', 0) or 0
            
            # Categorize by status
            if status in ['done', 'closed', 'resolved']:
                ticket_analysis['done'].append(issue)
                if story_points > 0:
                    story_points_by_status['done'] += story_points
            elif status in ['in progress', 'development', 'in development']:
                ticket_analysis['in_progress'].append(issue)
                if story_points > 0:
                    story_points_by_status['in_progress'] += story_points
            elif status in ['in review', 'code review', 'peer review']:
                ticket_analysis['in_review'].append(issue)
                if story_points > 0:
                    story_points_by_status['in_review'] += story_points
            elif status in ['in qa', 'testing', 'qa', 'in test']:
                ticket_analysis['in_qa'].append(issue)
                if story_points > 0:
                    story_points_by_status['in_qa'] += story_points
            else:
                ticket_analysis['to_do'].append(issue)
                if story_points > 0:
                    story_points_by_status['to_do'] += story_points
            
            # High priority flagging
            if priority.lower() in ['highest', 'critical', 'high', '1-highest', '2-high']:
                ticket_analysis['high_priority'].append({
                    'key': issue.get('key'),
                    'summary': fields.get('summary', ''),
                    'priority': priority,
                    'status': status,
                    'assignee': assignee_name,
                    'story_points': story_points
                })
            
            # Bug vs Story/Task categorization
            if 'bug' in issue_type or 'defect' in issue_type:
                ticket_analysis['bugs'].append(issue)
            elif 'story' in issue_type:
                ticket_analysis['stories'].append(issue)
            elif 'task' in issue_type:
                ticket_analysis['tasks'].append(issue)
            

            
            # Tech categorization based on summary/title keywords
            summary = fields.get('summary', '').lower()
            if any(keyword in summary for keyword in ['frontend', 'fe', 'ui', 'react', 'angular', 'vue']):
                tech_categories['Frontend'] = tech_categories.get('Frontend', 0) + 1
            elif any(keyword in summary for keyword in ['backend', 'be', 'api', 'service', 'database', 'server']):
                tech_categories['Backend'] = tech_categories.get('Backend', 0) + 1
            elif any(keyword in summary for keyword in ['test', 'qa', 'automation', 'regression']):
                tech_categories['Testing/QA'] = tech_categories.get('Testing/QA', 0) + 1
            elif any(keyword in summary for keyword in ['devops', 'deploy', 'infra', 'pipeline', 'ci/cd']):
                tech_categories['DevOps/Infrastructure'] = tech_categories.get('DevOps/Infrastructure', 0) + 1
            else:
                tech_categories['Other'] = tech_categories.get('Other', 0) + 1
            
            # Aging analysis
            if created:
                try:
                    created_dt = datetime.fromisoformat(created.replace('Z', '+00:00'))
                    age_days = (datetime.now(created_dt.tzinfo) - created_dt).days
                    
                    age_bucket = '0-7 days'
                    if age_days > 30:
                        age_bucket = '30+ days'
                    elif age_days > 14:
                        age_bucket = '15-30 days'
                    elif age_days > 7:
                        age_bucket = '8-14 days'
                    
                    status_key = 'Done' if status in ['done', 'closed', 'resolved'] else 'In Progress/Open'
                    
                    if status_key not in aging_analysis:
                        aging_analysis[status_key] = {}
                    aging_analysis[status_key][age_bucket] = aging_analysis[status_key].get(age_bucket, 0) + 1
                except:
                    pass
        
        # Calculate tech categorization percentages
        total_tickets = len(issues)
        tech_category_percentages = {}
        for category, count in tech_categories.items():
            tech_category_percentages[category] = {
                'count': count,
                'percentage': round((count / total_tickets * 100), 1) if total_tickets > 0 else 0
            }
        
        # Identify production bugs (bugs with high priority)
        production_bugs = [
            bug for bug in ticket_analysis['bugs'] 
            if bug.get('fields', {}).get('priority', {}).get('name', '').lower() in ['highest', 'critical', 'high', '1-highest', '2-high']
        ]
        
        # Calculate total story points (excluding 0 SP)
        total_story_points = sum(story_points_by_status.values())
        
        # Generate sprint health indicators
        completion_rate = round((story_points_by_status['done'] / total_story_points * 100), 1) if total_story_points > 0 else 0
        work_in_progress_rate = round(((story_points_by_status['in_progress'] + story_points_by_status['in_review']) / total_story_points * 100), 1) if total_story_points > 0 else 0
        
        health_indicators = {
            'completion_rate': completion_rate,
            'work_in_progress_rate': work_in_progress_rate,
            'high_priority_incomplete_count': len([hp for hp in ticket_analysis['high_priority'] if hp['status'] not in ['done', 'closed', 'resolved']]),
            'unassigned_work_count': len([issue for issue in issues if not issue.get('fields', {}).get('assignee') and issue.get('fields', {}).get('status', {}).get('name', '').lower() not in ['done', 'closed', 'resolved']]),
            'bug_rate': round((len(ticket_analysis['bugs']) / total_tickets * 100), 1) if total_tickets > 0 else 0
        }
        
        # Generate recommendations
        recommendations = []
        if completion_rate < 60:
            recommendations.append("🔴 Low completion rate - consider reducing scope or extending sprint")
        if health_indicators['high_priority_incomplete_count'] > 0:
            recommendations.append(f"⚠️ {health_indicators['high_priority_incomplete_count']} high priority items incomplete - focus team efforts")
        if health_indicators['unassigned_work_count'] > 0:
            recommendations.append(f"📋 {health_indicators['unassigned_work_count']} unassigned tickets - assign ownership")
        if health_indicators['bug_rate'] > 15:
            recommendations.append("🐛 High bug rate - consider quality improvement initiatives")
        if work_in_progress_rate > 40:
            recommendations.append("🔄 High WIP - encourage completing current work before starting new tasks")
        if not recommendations:
            recommendations.append("✅ Sprint health looks good - maintain current momentum")
        
        # Key achievements
        key_achievements = []
        if completion_rate >= 80:
            key_achievements.append(f"🎯 High completion rate: {completion_rate}% of story points delivered")
        if len(production_bugs) == 0:
            key_achievements.append("🛡️ No production bugs identified in sprint")
        if health_indicators['high_priority_incomplete_count'] == 0:
            key_achievements.append("✅ All high priority items completed")
        
        closed_high_value_stories = [
            issue for issue in ticket_analysis['done'] 
            if issue.get('fields', {}).get('customfield_10121', 0) and issue.get('fields', {}).get('customfield_10121', 0) >= 5
        ]
        if closed_high_value_stories:
            key_achievements.append(f"🚀 Completed {len(closed_high_value_stories)} high-value stories (5+ SP)")
        
        # Sprint success summary
        if completion_rate >= 80:
            success_level = "Excellent"
        elif completion_rate >= 60:
            success_level = "Good"
        elif completion_rate >= 40:
            success_level = "Fair"
        else:
            success_level = "Needs Improvement"
        
        return {
            'sprint_name': sprint_name,
            'story_points_breakdown': {
                'done': story_points_by_status['done'],
                'in_progress': story_points_by_status['in_progress'],
                'in_review': story_points_by_status['in_review'],
                'in_qa': story_points_by_status['in_qa'],
                'to_do': story_points_by_status['to_do'],
                'total': total_story_points
            },
            'aging_of_tickets': aging_analysis,
            'incomplete_high_priority_tickets': [
                hp for hp in ticket_analysis['high_priority'] 
                if hp['status'] not in ['done', 'closed', 'resolved']
            ],
            'sprint_health_indicators': health_indicators,
            'recommendations': recommendations,
            'sprint_success_summary': {
                'success_level': success_level,
                'completion_rate': completion_rate,
                'total_tickets': total_tickets,
                'story_points_delivered': story_points_by_status['done']
            },
            'key_achievements': key_achievements,
            'tech_categorization': tech_category_percentages,
            'bugs_vs_story_task_count': {
                'bugs': len(ticket_analysis['bugs']),
                'stories': len(ticket_analysis['stories']),
                'tasks': len(ticket_analysis['tasks']),
                'bug_percentage': round((len(ticket_analysis['bugs']) / total_tickets * 100), 1) if total_tickets > 0 else 0
            },
            'production_bugs': [
                {
                    'key': bug.get('key'),
                    'summary': bug.get('fields', {}).get('summary', ''),
                    'priority': bug.get('fields', {}).get('priority', {}).get('name', 'Unknown'),
                    'status': bug.get('fields', {}).get('status', {}).get('name', 'Unknown'),
                    'assignee': bug.get('fields', {}).get('assignee', {}).get('displayName', 'Unassigned') if bug.get('fields', {}).get('assignee') else 'Unassigned'
                }
                for bug in production_bugs
            ]
        }

    def _calculate_sprint_duration(self, start_date: str, end_date: str) -> int:
        """Calculate sprint duration in days."""
        try:
            from datetime import datetime
            
            if not start_date or not end_date:
                return 0
            
            start_dt = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
            end_dt = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
            return (end_dt - start_dt).days
        except:
            return 0

    def _assess_sprint_goal_success(self, points_done: int, points_committed: int, 
                                  items_done: int, items_committed: int, goal: str) -> str:
        """Assess sprint goal success based on completion rates."""
        if points_committed == 0 and items_committed == 0:
            return 'unknown'
        
        completion_rate = max(
            (points_done / points_committed) if points_committed > 0 else 0,
            (items_done / items_committed) if items_committed > 0 else 0
        )
        
        if completion_rate >= 0.9:
            return 'met'
        elif completion_rate >= 0.7:
            return 'partially_met'
        else:
            return 'missed'

    def _generate_sprint_summary(self, sprint_reports: list) -> Dict[str, Any]:
        """Generate summary metrics across all sprint reports."""
        import statistics
        
        if not sprint_reports:
            return {}
        
        # Filter out error reports
        valid_reports = [r for r in sprint_reports if r.get('status') != 'error']
        
        if not valid_reports:
            return {'note': 'No valid sprint reports to summarize'}
        
        # Aggregate metrics
        velocities = []
        throughputs = []
        completion_rates = []
        spillover_rates = []
        defect_rates = []
        cycle_times = []
        lead_times = []
        
        goal_success_counts = {'met': 0, 'partially_met': 0, 'missed': 0}
        
        for report in valid_reports:
            dp = report.get('delivery_predictability', {})
            fm = report.get('flow_metrics', {})
            qs = report.get('quality_stability', {})
            
            # Collect metrics
            if dp.get('velocity', {}).get('story_points_completed'):
                velocities.append(dp['velocity']['story_points_completed'])
            
            if dp.get('throughput', {}).get('work_items_completed'):
                throughputs.append(dp['throughput']['work_items_completed'])
            
            if dp.get('commitment_reliability', {}).get('completion_rate_by_points'):
                completion_rates.append(dp['commitment_reliability']['completion_rate_by_points'])
            
            if dp.get('spillover_rate', {}).get('spillover_percentage'):
                spillover_rates.append(dp['spillover_rate']['spillover_percentage'])
            
            if qs.get('defects_in_sprint', {}).get('defect_rate'):
                defect_rates.append(qs['defects_in_sprint']['defect_rate'])
            
            if fm.get('cycle_time', {}).get('median_days'):
                cycle_times.append(fm['cycle_time']['median_days'])
            
            if fm.get('lead_time', {}).get('median_days'):
                lead_times.append(fm['lead_time']['median_days'])
            
            # Sprint goal success
            goal_success = dp.get('sprint_goal_success', 'unknown')
            if goal_success in goal_success_counts:
                goal_success_counts[goal_success] += 1
        
        return {
            'sprints_analyzed': len(valid_reports),
            'average_velocity': round(statistics.mean(velocities), 2) if velocities else 0,
            'average_throughput': round(statistics.mean(throughputs), 2) if throughputs else 0,
            'average_completion_rate': round(statistics.mean(completion_rates), 2) if completion_rates else 0,
            'average_spillover_rate': round(statistics.mean(spillover_rates), 2) if spillover_rates else 0,
            'average_defect_rate': round(statistics.mean(defect_rates), 2) if defect_rates else 0,
            'average_cycle_time': round(statistics.mean(cycle_times), 2) if cycle_times else 0,
            'average_lead_time': round(statistics.mean(lead_times), 2) if lead_times else 0,
            'sprint_goal_success_distribution': goal_success_counts,
            'trends': {
                'velocity_trend': 'stable' if len(set(velocities[-3:])) <= 2 else 'variable' if velocities else 'no_data',
                'completion_trend': 'improving' if completion_rates and len(completion_rates) > 1 and completion_rates[-1] > completion_rates[0] else 'stable',
                'quality_trend': 'improving' if defect_rates and len(defect_rates) > 1 and defect_rates[-1] < defect_rates[0] else 'stable'
            }
        }

    def get_pull_request_details(self, ticket_key: str) -> Dict[str, Any]:
        """
        Get pull request details from customfield_25440 and add comments for open PRs.
        
        Args:
            ticket_key: The JIRA ticket key
            
        Returns:
            Dict containing PR count, state, and comment status
        """
        import json
        import re
        
        try:
            # Get ticket details including the custom field
            url = f"{self.base_url}/rest/api/2/issue/{ticket_key}"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            ticket_data = response.json()
            pr_field = ticket_data['fields'].get('customfield_25440')
            
            if not pr_field:
                return {
                    'status': 'success',
                    'ticket_key': ticket_key,
                    'pull_request_count': 0,
                    'pull_request_state': 'NONE',
                    'message': 'No pull request data found'
                }
            
            # Debug: log the raw field value
            logger.info(f"Raw PR field for {ticket_key}: {pr_field[:500]}...")
            
            # Try to extract devSummaryJson with improved regex
            dev_summary_match = re.search(r'"devSummaryJson":\s*"(.*?)"(?:,|\s*})', pr_field)
            if not dev_summary_match:
                # Alternative: look for the JSON structure directly in the string
                json_match = re.search(r'\{"cachedValue".*"isStale":[^}]*\}', pr_field)
                if json_match:
                    dev_summary_str = json_match.group(0)
                else:
                    return {
                        'status': 'error',
                        'message': 'Could not parse devSummaryJson from pull request field',
                        'raw_field': pr_field[:200] + '...' if len(pr_field) > 200 else pr_field
                    }
            else:
                # Unescape the JSON string
                dev_summary_str = dev_summary_match.group(1).replace('\\"', '"').replace('\\\\', '\\')
            
            try:
                dev_summary = json.loads(dev_summary_str)
            except json.JSONDecodeError:
                # Try to extract values using regex patterns if JSON parsing fails
                return self._extract_pr_data_with_regex(pr_field, ticket_key)
            
            # Extract pull request information
            cached_value = dev_summary.get('cachedValue', {})
            summary = cached_value.get('summary', {})
            pr_summary = summary.get('pullrequest', {})
            pr_overall = pr_summary.get('overall', {})
            
            pr_count = pr_overall.get('count', 0)
            pr_state = pr_overall.get('state', 'UNKNOWN')
            pr_details = pr_overall.get('details', {})
            
            open_count = pr_details.get('openCount', 0)
            merged_count = pr_details.get('mergedCount', 0)
            declined_count = pr_details.get('declinedCount', 0)
            
            result = {
                'status': 'success',
                'ticket_key': ticket_key,
                'pull_request_count': pr_count,
                'pull_request_state': pr_state,
                'open_count': open_count,
                'merged_count': merged_count,
                'declined_count': declined_count,
                'last_updated': pr_overall.get('lastUpdated'),
                'comment_added': False
            }
            
            # If there are open pull requests, add a comment
            if open_count > 0:
                # Get assignee and reporter information
                assignee_name = None
                reporter_name = None
                
                assignee_data = ticket_data['fields'].get('assignee')
                if assignee_data:
                    assignee_name = assignee_data.get('name')
                
                reporter_data = ticket_data['fields'].get('reporter')
                if reporter_data:
                    reporter_name = reporter_data.get('name')
                
                # Build comment with tags
                comment_text = "Pull Request Is Open. Please follow-up with reviewers."
                
                # Add tags if available
                tags = []
                if assignee_name:
                    tags.append(f"[~{assignee_name}]")
                if reporter_name and reporter_name != assignee_name:  # Don't duplicate if same person
                    tags.append(f"[~{reporter_name}]")
                
                if tags:
                    comment_text += f" {' '.join(tags)}"
                
                # comment_result = self._add_comment_to_ticket(ticket_key, comment_text)
                result['comment_added'] = False  # 'successfully' in comment_result.lower()
                result['comment_result'] = 'Comment addition disabled'  # comment_result
                result['tagged_users'] = {
                    'assignee': assignee_name,
                    'reporter': reporter_name
                }
            
            return result
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing error in get_pull_request_details: {str(e)}")
            return self._extract_pr_data_with_regex(pr_field, ticket_key)
        except Exception as e:
            logger.error(f"Error getting pull request details for {ticket_key}: {str(e)}")
            return {
                'status': 'error',
                'message': str(e),
                'ticket_key': ticket_key
            }

    def _extract_pr_data_with_regex(self, pr_field: str, ticket_key: str) -> Dict[str, Any]:
        """
        Fallback method to extract PR data using regex patterns when JSON parsing fails.
        """
        import re
        
        try:
            # Extract PR count using regex
            count_match = re.search(r'"count":\s*(\d+)', pr_field)
            pr_count = int(count_match.group(1)) if count_match else 0
            
            # Extract state
            state_match = re.search(r'"state":\s*"([^"]*)"', pr_field)
            pr_state = state_match.group(1) if state_match else 'UNKNOWN'
            
            # Extract details counts
            open_match = re.search(r'"openCount":\s*(\d+)', pr_field)
            merged_match = re.search(r'"mergedCount":\s*(\d+)', pr_field)
            declined_match = re.search(r'"declinedCount":\s*(\d+)', pr_field)
            
            open_count = int(open_match.group(1)) if open_match else 0
            merged_count = int(merged_match.group(1)) if merged_match else 0
            declined_count = int(declined_match.group(1)) if declined_match else 0
            
            # Extract last updated
            updated_match = re.search(r'"lastUpdated":\s*"([^"]*)"', pr_field)
            last_updated = updated_match.group(1) if updated_match else None
            
            result = {
                'status': 'success',
                'ticket_key': ticket_key,
                'pull_request_count': pr_count,
                'pull_request_state': pr_state,
                'open_count': open_count,
                'merged_count': merged_count,
                'declined_count': declined_count,
                'last_updated': last_updated,
                'comment_added': False,
                'parsing_method': 'regex_fallback'
            }
            
            # If there are open pull requests, add a comment
            if open_count > 0:
                # Need to get ticket data for assignee/reporter info in regex fallback
                try:
                    url = f"{self.base_url}/rest/api/2/issue/{ticket_key}"
                    response = requests.get(url, headers=self.headers)
                    response.raise_for_status()
                    ticket_data = response.json()
                    
                    # Get assignee and reporter information
                    assignee_name = None
                    reporter_name = None
                    
                    assignee_data = ticket_data['fields'].get('assignee')
                    if assignee_data:
                        assignee_name = assignee_data.get('name')
                    
                    reporter_data = ticket_data['fields'].get('reporter')
                    if reporter_data:
                        reporter_name = reporter_data.get('name')
                    
                    # Build comment with tags
                    comment_text = "Pull Request Is Open. Please follow-up with reviewers."
                    
                    # Add tags if available
                    tags = []
                    if assignee_name:
                        tags.append(f"[~{assignee_name}]")
                    if reporter_name and reporter_name != assignee_name:  # Don't duplicate if same person
                        tags.append(f"[~{reporter_name}]")
                    
                    if tags:
                        comment_text += f" {' '.join(tags)}"
                    
                    # comment_result = self._add_comment_to_ticket(ticket_key, comment_text)
                    result['comment_added'] = False  # 'successfully' in comment_result.lower()
                    result['comment_result'] = 'Comment addition disabled'  # comment_result
                    result['tagged_users'] = {
                        'assignee': assignee_name,
                        'reporter': reporter_name
                    }
                except Exception as tag_error:
                    # Fallback to simple comment if tagging fails
                    comment_text = "Pull Request Is Open. Please follow-up with reviewers."
                    # comment_result = self._add_comment_to_ticket(ticket_key, comment_text)
                    result['comment_added'] = False  # 'successfully' in comment_result.lower()
                    result['comment_result'] = 'Comment addition disabled'  # comment_result
                    result['tagging_error'] = str(tag_error)
            
            return result
            
        except Exception as e:
            logger.error(f"Regex parsing also failed for {ticket_key}: {str(e)}")
            return {
                'status': 'error',
                'message': f'Failed to parse pull request data using both JSON and regex methods: {str(e)}',
                'ticket_key': ticket_key,
                'raw_field_sample': pr_field[:200] + '...' if len(pr_field) > 200 else pr_field
            }

    def create_review_task(self, parent_details: Dict[str, Any], review_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a subtask for code review implementation under the parent story."""
        try:
            url = f"{self.base_url}/rest/api/2/issue"
            
            payload = {
                "fields": {
                    "project": {
                        "id": parent_details['project_id']
                    },
                    "parent": {
                        "key": parent_details['key']
                    },
                    "summary": review_data.get('title', 'Code Review Implementation Task'),
                    "description": review_data.get('description', 'Implementation of code review suggestions'),
                    "issuetype": {
                        "id": "5"  # Subtask ID
                    }
                }
            }

            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            
            created_task = response.json()
            return {
                'status': 'success',
                'message': f"Successfully created review task under {parent_details['key']}",
                'task_key': created_task.get('key'),
                'task_self': created_task.get('self')
            }
            
        except Exception as e:
            logger.error(f"Error creating review task: {str(e)}")
            return {
                'status': 'error',
                'message': str(e)
            }

    def search_jira_issues(self, query: str, max_results: int = 50) -> Dict[str, Any]:
        """
        Search for Jira issues based on a query string.
        
        This method will execute the provided JQL query against Jira's search API.
        """
        try:
            # Endpoint for Jira search
            url = f"{self.base_url}/rest/api/2/search"
            
            # Construct search parameters
            params = {
                'jql': query,
                'maxResults': max_results,
                'fields': 'key,summary,status,issuetype,priority,assignee,created,updated,customfield_10121,customfield_25440,customfield_26560,customfield_25354,customfield_25355,customfield_25356,customfield_13543'
            }
            
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            
            search_results = response.json()
            
            # Format the results with safe field access
            formatted_results = {
                'total': search_results.get('total', 0),
                'issues': []
            }
            
            for issue in search_results.get('issues', []):
                fields = issue.get('fields', {})
                
                # Safe field extraction with defaults
                issue_data = {
                    'key': issue.get('key', 'N/A'),
                    'summary': fields.get('summary', 'No summary'),
                    'status': fields.get('status', {}).get('name', 'Unknown') if fields.get('status') else 'Unknown',
                    'type': fields.get('issuetype', {}).get('name', 'Unknown') if fields.get('issuetype') else 'Unknown',
                    'priority': fields.get('priority', {}).get('name', 'Unknown') if fields.get('priority') else 'Unknown',
                    'assignee': fields.get('assignee', {}).get('displayName', 'Unassigned') if fields.get('assignee') else 'Unassigned',
                    'created': fields.get('created', 'Unknown'),
                    'updated': fields.get('updated', 'Unknown'),
                    'story_points': fields.get('customfield_10121', 0) or 0,
                    'dev_resource': fields.get('customfield_25440', 'Unknown'),
                    'qa_resource': fields.get('customfield_26560', 'Unknown'),
                    'sprint_name': fields.get('customfield_13543', 'Unknown')
                }
                
                formatted_results['issues'].append(issue_data)
            
            return {
                'status': 'success',
                'results': formatted_results,
                'query': query
            }
            
        except Exception as e:
            logger.error(f"Error searching Jira issues: {str(e)}")
            return {
                'status': 'error',
                'message': str(e)
            }

    def create_user_story(self, story_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a user story with custom fields for product management.
        
        Args:
            story_data: Dictionary containing story details including custom fields
        """
        try:
            url = f"{self.base_url}/rest/api/2/issue"
            
            # Custom field IDs from the configuration
            custom_fields = {
                'asAn': 'customfield_25354',
                'when': 'customfield_26560', 
                'wantTo': 'customfield_25355',
                'soICan': 'customfield_26559',
                'soThat': 'customfield_25356',
                'acceptanceCriteria': 'customfield_10253',
                'themeSquad': 'customfield_34040'
            }
            
            # Build the payload with required and optional fields
            payload = {
                "fields": {
                    "issuetype": {
                        "id": story_data.get('issue_type_id', '21')  # Default to Story type
                    },
                    "project": {
                        "id": story_data.get('project_id')  # Required
                    },
                    "summary": story_data.get('summary'),  # Required
                    "description": story_data.get('description', ''),
                    "priority": {
                        "id": story_data.get('priority_id', '6')  # Default to Medium priority
                    }
                }
            }
            
            # Add custom fields if provided
            if story_data.get('as_an'):
                payload['fields'][custom_fields['asAn']] = story_data['as_an']
            
            if story_data.get('when'):
                payload['fields'][custom_fields['when']] = story_data['when']
                
            if story_data.get('want_to'):
                payload['fields'][custom_fields['wantTo']] = story_data['want_to']
                
            if story_data.get('so_i_can'):
                payload['fields'][custom_fields['soICan']] = story_data['so_i_can']
                
            if story_data.get('so_that'):
                payload['fields'][custom_fields['soThat']] = story_data['so_that']
                
            if story_data.get('acceptance_criteria'):
                payload['fields'][custom_fields['acceptanceCriteria']] = story_data['acceptance_criteria']
            
            # Add theme/squad custom field if provided
            if story_data.get('theme_id') and story_data.get('team_id'):
                payload['fields'][custom_fields['themeSquad']] = {
                    "id": story_data['theme_id'],
                    "child": {
                        "id": story_data['team_id']
                    }
                }
            
            # Add assignee if provided
            if story_data.get('assignee'):
                payload['fields']['assignee'] = {
                    "name": story_data['assignee']
                }
            
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            
            created_story = response.json()
            return {
                'status': 'success',
                'message': f"Successfully created user story",
                'story_key': created_story.get('key'),
                'story_id': created_story.get('id'),
                'story_self': created_story.get('self'),
                'payload_sent': payload  # For debugging
            }
            
        except Exception as e:
            logger.error(f"Error creating user story: {str(e)}")
            return {
                'status': 'error',
                'message': str(e),
                'payload_sent': payload if 'payload' in locals() else None
            }

    def get_projects(self, search_term: str = "", max_results: int = 50) -> Dict[str, Any]:
        """
        Get all accessible Jira projects with their IDs and basic information.
        
        Args:
            search_term: Optional search term to filter projects by name or key
            max_results: Maximum number of projects to return
        """
        try:
            # Use the simpler endpoint that works in Postman
            url = f"{self.base_url}/rest/api/2/project"
            
            # Get all projects first
            response = requests.get(url, headers=self.headers, timeout=30)
            response.raise_for_status()
            
            projects_data = response.json()
            
            # If it's not a list, extract the values field
            if isinstance(projects_data, dict) and 'values' in projects_data:
                projects_list = projects_data['values']
            elif isinstance(projects_data, list):
                projects_list = projects_data
            else:
                projects_list = []
            
            # Apply client-side filtering if search term is provided
            if search_term:
                search_lower = search_term.lower()
                filtered_projects = []
                for project in projects_list:
                    name = project.get('name', '').lower()
                    key = project.get('key', '').lower()
                    description = project.get('description', '').lower() if project.get('description') else ''
                    
                    if (search_lower in name or 
                        search_lower in key or 
                        search_lower in description):
                        filtered_projects.append(project)
                projects_list = filtered_projects
            
            # Limit results
            projects_list = projects_list[:max_results]
            
            # Format the results with enhanced information
            formatted_projects = {
                'total': len(projects_list),
                'projects': []
            }
            
            for project in projects_list:
                # Extract avatar URLs if available
                avatar_info = {}
                if project.get('avatarUrls'):
                    avatar_info = {
                        'small': project['avatarUrls'].get('16x16'),
                        'medium': project['avatarUrls'].get('24x24'),
                        'large': project['avatarUrls'].get('48x48')
                    }
                
                project_info = {
                    'id': project.get('id'),
                    'key': project.get('key'),
                    'name': project.get('name'),
                    'description': project.get('description', 'No description'),
                    'lead': project.get('lead', {}).get('displayName', 'Unknown') if project.get('lead') else 'Unknown',
                    'lead_username': project.get('lead', {}).get('name', 'Unknown') if project.get('lead') else 'Unknown',
                    'project_type': project.get('projectTypeKey', 'Unknown'),
                    'category': project.get('projectCategory', {}).get('name', 'Uncategorized') if project.get('projectCategory') else 'Uncategorized',
                    'url': project.get('self', ''),
                    'avatars': avatar_info,
                    'is_simplified': project.get('simplified', False),
                    'style': project.get('style', 'classic')
                }
                formatted_projects['projects'].append(project_info)
            
            return {
                'status': 'success',
                'results': formatted_projects,
                'search_term': search_term if search_term else 'All projects',
                'endpoint_used': url,
                'total_found': len(projects_list),
                'filtered': bool(search_term)
            }
            
        except requests.exceptions.Timeout:
            error_msg = "Request timeout while fetching projects"
            logger.error(error_msg)
            return {
                'status': 'error',
                'message': error_msg,
                'error_type': 'timeout',
                'endpoint_used': f"{self.base_url}/rest/api/2/project"
            }
        except requests.exceptions.ConnectionError:
            error_msg = "Connection error while fetching projects"
            logger.error(error_msg)
            return {
                'status': 'error',
                'message': error_msg,
                'error_type': 'connection_error',
                'endpoint_used': f"{self.base_url}/rest/api/2/project"
            }
        except requests.exceptions.HTTPError as e:
            error_msg = f"HTTP error while fetching projects: {e.response.status_code}"
            logger.error(error_msg)
            return {
                'status': 'error',
                'message': error_msg,
                'error_type': 'http_error',
                'status_code': e.response.status_code,
                'endpoint_used': f"{self.base_url}/rest/api/2/project"
            }
        except Exception as e:
            error_msg = f"Unexpected error fetching projects: {str(e)}"
            logger.error(error_msg)
            return {
                'status': 'error',
                'message': error_msg,
                'error_type': 'unexpected_error',
                'endpoint_used': f"{self.base_url}/rest/api/2/project"
            }

    def get_project_by_id(self, project_id: str) -> Dict[str, Any]:
        """
        Get detailed information for a specific project by ID or key.
        
        Args:
            project_id: Project ID or project key (e.g., "12345" or "MS-TECH")
        """
        try:
            # Try to get project details using the project endpoint
            url = f"{self.base_url}/rest/api/2/project/{project_id}"
            
            response = requests.get(url, headers=self.headers, timeout=30)
            response.raise_for_status()
            
            project_data = response.json()
            
            # Extract comprehensive project information
            avatar_info = {}
            if project_data.get('avatarUrls'):
                avatar_info = {
                    'small': project_data['avatarUrls'].get('16x16'),
                    'medium': project_data['avatarUrls'].get('24x24'),
                    'large': project_data['avatarUrls'].get('48x48')
                }
            
            # Extract component information
            components = []
            for comp in project_data.get('components', []):
                component_info = {
                    'id': comp.get('id'),
                    'name': comp.get('name'),
                    'description': comp.get('description', 'No description'),
                    'lead': comp.get('lead', {}).get('displayName') if comp.get('lead') else 'Unknown',
                    'assignee_type': comp.get('assigneeType', 'Unknown')
                }
                components.append(component_info)
            
            # Extract version information
            versions = []
            for version in project_data.get('versions', []):
                version_info = {
                    'id': version.get('id'),
                    'name': version.get('name'),
                    'description': version.get('description', 'No description'),
                    'released': version.get('released', False),
                    'archived': version.get('archived', False),
                    'release_date': version.get('releaseDate'),
                    'start_date': version.get('startDate')
                }
                versions.append(version_info)
            
            # Extract issue type information
            issue_types = []
            for issue_type in project_data.get('issueTypes', []):
                issue_type_info = {
                    'id': issue_type.get('id'),
                    'name': issue_type.get('name'),
                    'description': issue_type.get('description', 'No description'),
                    'icon_url': issue_type.get('iconUrl'),
                    'subtask': issue_type.get('subtask', False)
                }
                issue_types.append(issue_type_info)
            
            # Extract role information
            roles = {}
            project_roles = project_data.get('roles', {})
            for role_name, role_url in project_roles.items():
                roles[role_name] = role_url
            
            project_info = {
                'id': project_data.get('id'),
                'key': project_data.get('key'),
                'name': project_data.get('name'),
                'description': project_data.get('description', 'No description'),
                'lead': {
                    'username': project_data.get('lead', {}).get('name') if project_data.get('lead') else 'Unknown',
                    'display_name': project_data.get('lead', {}).get('displayName') if project_data.get('lead') else 'Unknown',
                    'email': project_data.get('lead', {}).get('emailAddress') if project_data.get('lead') else 'Unknown'
                },
                'project_type': project_data.get('projectTypeKey', 'Unknown'),
                'category': {
                    'id': project_data.get('projectCategory', {}).get('id') if project_data.get('projectCategory') else None,
                    'name': project_data.get('projectCategory', {}).get('name', 'Uncategorized') if project_data.get('projectCategory') else 'Uncategorized',
                    'description': project_data.get('projectCategory', {}).get('description') if project_data.get('projectCategory') else None
                },
                'url': project_data.get('self', ''),
                'avatars': avatar_info,
                'is_simplified': project_data.get('simplified', False),
                'style': project_data.get('style', 'classic'),
                'assignee_type': project_data.get('assigneeType', 'PROJECT_LEAD'),
                'components': components,
                'versions': versions,
                'issue_types': issue_types,
                'roles': roles,
                'permissions': project_data.get('permissions', {}),
                'expand': project_data.get('expand', '')
            }
            
            return {
                'status': 'success',
                'project': project_info,
                'endpoint_used': url,
                'project_identifier': project_id
            }
            
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                error_msg = f"Project not found: {project_id}"
                logger.error(error_msg)
                return {
                    'status': 'error',
                    'message': error_msg,
                    'error_type': 'project_not_found',
                    'status_code': 404,
                    'project_identifier': project_id,
                    'endpoint_used': f"{self.base_url}/rest/api/2/project/{project_id}"
                }
            elif e.response.status_code == 403:
                error_msg = f"Access denied to project: {project_id}"
                logger.error(error_msg)
                return {
                    'status': 'error',
                    'message': error_msg,
                    'error_type': 'access_denied',
                    'status_code': 403,
                    'project_identifier': project_id,
                    'endpoint_used': f"{self.base_url}/rest/api/2/project/{project_id}"
                }
            else:
                error_msg = f"HTTP error while fetching project {project_id}: {e.response.status_code}"
                logger.error(error_msg)
                return {
                    'status': 'error',
                    'message': error_msg,
                    'error_type': 'http_error',
                    'status_code': e.response.status_code,
                    'project_identifier': project_id,
                    'endpoint_used': f"{self.base_url}/rest/api/2/project/{project_id}"
                }
        except requests.exceptions.Timeout:
            error_msg = f"Request timeout while fetching project: {project_id}"
            logger.error(error_msg)
            return {
                'status': 'error',
                'message': error_msg,
                'error_type': 'timeout',
                'project_identifier': project_id,
                'endpoint_used': f"{self.base_url}/rest/api/2/project/{project_id}"
            }
        except requests.exceptions.ConnectionError:
            error_msg = f"Connection error while fetching project: {project_id}"
            logger.error(error_msg)
            return {
                'status': 'error',
                'message': error_msg,
                'error_type': 'connection_error',
                'project_identifier': project_id,
                'endpoint_used': f"{self.base_url}/rest/api/2/project/{project_id}"
            }
        except Exception as e:
            error_msg = f"Unexpected error fetching project {project_id}: {str(e)}"
            logger.error(error_msg)
            return {
                'status': 'error',
                'message': error_msg,
                'error_type': 'unexpected_error',
                'project_identifier': project_id,
                'endpoint_used': f"{self.base_url}/rest/api/2/project/{project_id}"
            }

    def update_ticket(self, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an existing Jira ticket with new values for various fields.
        
        Args:
            update_data: Dictionary containing update details
        """
        try:
            ticket_key = update_data.get('ticket_key')
            if not ticket_key:
                return {
                    'status': 'error',
                    'message': 'ticket_key is required for updates'
                }
            
            url = f"{self.base_url}/rest/api/2/issue/{ticket_key}"
            
            # Custom field IDs (same as in create_user_story)
            custom_fields = {
                'asAn': 'customfield_25354',
                'when': 'customfield_26560', 
                'wantTo': 'customfield_25355',
                'soICan': 'customfield_26559',
                'soThat': 'customfield_25356',
                'acceptanceCriteria': 'customfield_10253',
                'themeSquad': 'customfield_34040'
            }
            
            # Build the update payload
            fields_to_update = {}
            
            # Handle summary update
            if update_data.get('summary') is not None:
                fields_to_update['summary'] = update_data['summary']
            
            # Handle description update
            if update_data.get('description') is not None:
                fields_to_update['description'] = update_data['description']
            
            # Handle assignee update
            if update_data.get('assignee') is not None:
                if update_data['assignee'] == "":
                    # Unassign the ticket
                    fields_to_update['assignee'] = None
                else:
                    fields_to_update['assignee'] = {
                        "name": update_data['assignee']
                    }
            
            # Handle priority update
            if update_data.get('priority_id') is not None:
                fields_to_update['priority'] = {
                    "id": update_data['priority_id']
                }
            
            # Handle user story custom fields
            if update_data.get('as_an') is not None:
                fields_to_update[custom_fields['asAn']] = update_data['as_an']
            
            if update_data.get('when') is not None:
                fields_to_update[custom_fields['when']] = update_data['when']
                
            if update_data.get('want_to') is not None:
                fields_to_update[custom_fields['wantTo']] = update_data['want_to']
                
            if update_data.get('so_i_can') is not None:
                fields_to_update[custom_fields['soICan']] = update_data['so_i_can']
                
            if update_data.get('so_that') is not None:
                fields_to_update[custom_fields['soThat']] = update_data['so_that']
                
            if update_data.get('acceptance_criteria') is not None:
                fields_to_update[custom_fields['acceptanceCriteria']] = update_data['acceptance_criteria']
            
            # Handle theme/squad custom field
            if update_data.get('theme_id') and update_data.get('team_id'):
                fields_to_update[custom_fields['themeSquad']] = {
                    "id": update_data['theme_id'],
                    "child": {
                        "id": update_data['team_id']
                    }
                }
            
            # Handle labels updates
            if update_data.get('labels') is not None:
                # Replace all labels
                fields_to_update['labels'] = update_data['labels']
            elif update_data.get('add_labels') or update_data.get('remove_labels'):
                # Get current labels first
                current_ticket = self.get_ticket_details(ticket_key)
                current_labels = set(current_ticket.get('labels', []))
                
                # Add new labels
                if update_data.get('add_labels'):
                    current_labels.update(update_data['add_labels'])
                
                # Remove specified labels
                if update_data.get('remove_labels'):
                    current_labels.difference_update(update_data['remove_labels'])
                
                fields_to_update['labels'] = list(current_labels)
            
            # Handle additional custom fields
            if update_data.get('custom_fields'):
                fields_to_update.update(update_data['custom_fields'])
            
            update_results = []
            
            # Perform field updates if any
            if fields_to_update:
                payload = {"fields": fields_to_update}
                
                response = requests.put(url, headers=self.headers, json=payload)
                
                if response.status_code == 204:
                    update_results.append("Fields updated successfully")
                else:
                    update_results.append(f"Field update failed: {response.status_code} - {response.text}")
            
            # Handle status transition separately
            if update_data.get('status_id') is not None:
                transition_result = self._transition_ticket_status(ticket_key, update_data['status_id'])
                update_results.append(transition_result)
            
            # Handle comment addition
            if update_data.get('comment'):
                comment_result = self._add_comment_to_ticket(ticket_key, update_data['comment'])
                update_results.append(comment_result)
            
            # Get updated ticket details
            updated_ticket = self.get_ticket_details(ticket_key)
            
            return {
                'status': 'success',
                'message': f"Successfully updated ticket {ticket_key}",
                'ticket_key': ticket_key,
                'updates_performed': update_results,
                'updated_ticket': updated_ticket,
                'fields_updated': list(fields_to_update.keys()) if fields_to_update else []
            }
            
        except Exception as e:
            logger.error(f"Error updating ticket {update_data.get('ticket_key', 'unknown')}: {str(e)}")
            return {
                'status': 'error',
                'message': str(e),
                'ticket_key': update_data.get('ticket_key', 'unknown')
            }
    
    def _transition_ticket_status(self, ticket_key: str, status_id: str) -> str:
        """
        Transition a ticket to a new status.
        
        Args:
            ticket_key: The ticket key
            status_id: The target status ID
        """
        try:
            # Get available transitions
            transitions_url = f"{self.base_url}/rest/api/2/issue/{ticket_key}/transitions"
            transitions_response = requests.get(transitions_url, headers=self.headers)
            
            if transitions_response.status_code != 200:
                return f"Failed to get transitions: {transitions_response.status_code}"
            
            transitions_data = transitions_response.json()
            transitions = transitions_data.get('transitions', [])
            
            # Find the transition that leads to the desired status
            target_transition = None
            for transition in transitions:
                if transition.get('to', {}).get('id') == status_id:
                    target_transition = transition
                    break
            
            if not target_transition:
                available_statuses = [t.get('to', {}).get('name', 'Unknown') for t in transitions]
                return f"No transition available to status ID {status_id}. Available transitions: {', '.join(available_statuses)}"
            
            # Perform the transition
            transition_payload = {
                "transition": {
                    "id": target_transition['id']
                }
            }
            
            transition_response = requests.post(transitions_url, headers=self.headers, json=transition_payload)
            
            if transition_response.status_code == 204:
                status_name = target_transition.get('to', {}).get('name', f'Status ID {status_id}')
                return f"Status transitioned to {status_name}"
            else:
                return f"Status transition failed: {transition_response.status_code} - {transition_response.text}"
                
        except Exception as e:
            return f"Status transition error: {str(e)}"
    
    def _add_comment_to_ticket(self, ticket_key: str, comment_text: str) -> str:
        """
        Add a comment to a ticket.
        
        Args:
            ticket_key: The ticket key
            comment_text: The comment text to add
        """
        try:
            comment_url = f"{self.base_url}/rest/api/2/issue/{ticket_key}/comment"
            comment_payload = {
                "body": comment_text
            }
            
            comment_response = requests.post(comment_url, headers=self.headers, json=comment_payload)
            
            if comment_response.status_code == 201:
                return "Comment added successfully"
            else:
                return f"Comment addition failed: {comment_response.status_code} - {comment_response.text}"
                
        except Exception as e:
            return f"Comment addition error: {str(e)}" 
        
    
    def create_bug_ticket(self, project_key: str, summary: str, description: str, severity: str,
                         steps_to_reproduce: str , expected_result: str , actual_result: str, 
                         detected_in: str , detected_by: str, priority: str = "3-Medium"
                         ) -> Dict[str, Any]:
        """Create a new bug ticket in Jira. All fields are required. Maps Severity, Detected In, and Detected By to Jira IDs."""
        try:
            url = f"{self.base_url}/rest/api/2/issue"
            # Get project id from project key
            project_url = f"{self.base_url}/rest/api/2/project/{project_key}"
            project_response = requests.get(project_url, headers=self.headers, verify=False)
            project_response.raise_for_status()
            project_id = project_response.json().get('id')

            # Mapping dictionaries
            severity_map = {
                "blocker": "48721",
                "critical": "12886",
                "high": "12887",
                "major": "48722",
                "medium": "12888",
                "minor": "48723",
                "low": "12889",
                "trivial": "48724",
                "-1": "-1"
            }
            detected_in_map = {
                "dev": "17473",
                "qa": "17472",
                "stg": "17474",
                "uat": "17475",
                "testpool": "43557",
                "prod beta": "36261",
                "prod": "17476",
                "dr": "43558",
                "production server": "48718",
                "qa server": "48719",
                "pre-production server": "48720",
                "-1": "-1"
            }
            detected_by_map = {
                "automated testing": "17477",
                "manual testing": "11962",
                "internal users": "11960",
                "external users": "11961",
                "-1": "-1"
            }

            # Prepare payload
            payload = {
                "fields": {
                    "project": {
                        "id": project_id
                    },
                    "summary": summary,
                    "description": description,
                    "issuetype": {
                        "name": "Bug"
                    },
                    "priority": {
                        "name": priority
                    }
                }
            }


            # Always set custom fields, default to '-1' if not found or not provided
            detected_in_id = detected_in_map.get(str(detected_in).strip().lower(), "-1")
            payload["fields"]["customfield_14849"] = {"id": detected_in_id}

            detected_by_id = detected_by_map.get(str(detected_by).strip().lower(), "-1")
            payload["fields"]["customfield_10940"] = {"id": detected_by_id}

            severity_id = severity_map.get(str(severity).strip().lower(), "-1")
            payload["fields"]["customfield_11947"] = {"id": severity_id}

            if steps_to_reproduce:
                payload["fields"]["customfield_25647"] = steps_to_reproduce

            if expected_result:
                payload["fields"]["customfield_26140"] = expected_result

            if actual_result:
                payload["fields"]["customfield_27140"] = actual_result

            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            created_ticket = response.json()
            return {
                'status': 'success',
                'message': f"Successfully created bug ticket {created_ticket.get('key')}",
                'ticket_key': created_ticket.get('key'),
                'ticket_self': created_ticket.get('self')
            }
        except Exception as e:
            logger.error(f"Error creating bug ticket: {str(e)}")
            return {
                'status': 'error',
                'message': str(e)
            }