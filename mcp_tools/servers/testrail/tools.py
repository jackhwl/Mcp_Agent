from fastmcp import FastMCP, Context
from typing import Dict, List, Any, Optional
import logging
from .service import TestRailService

logger = logging.getLogger(__name__)

def register_testrail_tools(mcp: FastMCP, testrail_service: TestRailService):
    """Register all TestRail-related MCP tools with the FastMCP server."""

    @mcp.tool()
    async def testrail_healthcheck(ctx: Context) -> Dict[str, Any]:
        """Check the health and connectivity of the TestRail integration.
        
        Verifies TestRail service availability by attempting to fetch user details
        
        Returns:
            Dict with status ('success'/'error'), user data,
            or error message if failed
        """
        try:
            await ctx.info("Running TestRail MCP Server healthcheck...")
            user_data = testrail_service.get_current_user()
            if user_data.get('status') == 'success':
                await ctx.info(f"✅ TestRail healthcheck successful - User: {user_data['user'].get('name', 'Unknown')}")
            else:
                await ctx.error(f"❌ TestRail healthcheck failed - {user_data.get('message', 'Unknown error')}")

        except Exception as e:
            error_msg = f"TestRail healthcheck failed: {str(e)}"
            logger.error(error_msg)
            await ctx.error(error_msg)
            return {
                "status": "error", 
                "message": error_msg,
                "instructions": [
                    "1. Check that TestRail server URL is accessible",
                    "2. Verify API credentials are correct",
                    "3. Ensure proper permissions are granted for the API user"
                ]
            }

    @mcp.tool()
    async def get_project(project_id: int, ctx: Context) -> Dict:
        """Retrieve detailed information about a specific TestRail project.
        
        Fetches complete project information including name, announcement,
        suite mode, completion status, and other configuration details.
        
        Args:
            project_id: Unique identifier of the project to retrieve
            
        Returns:
            Dict containing project details including:
                - id: Project identifier
                - name: Project name
                - announcement: Project announcement if set
                - show_announcement: Whether announcement is visible
                - is_completed: Project completion status
                - suite_mode: Test suite organization mode
                - url: Project URL in TestRail
        """
        try:
            await ctx.info(f"Retrieving TestRail project details for ID: {project_id}")
            
            result = testrail_service.get_project(project_id)
            
            if result:
                project_name = result.get('name', 'Unknown')
                await ctx.info(f"Successfully retrieved project: {project_name}")
            else:
                await ctx.error(f"Project {project_id} not found or not accessible")
                
            return result
            
        except Exception as e:
            error_msg = f"Failed to get project {project_id}: {str(e)}"
            logger.error(error_msg)
            await ctx.error(error_msg)
            return {
                'status': 'error',
                'message': error_msg,
                'project_id': project_id
            }

    @mcp.tool()
    async def get_projects_from_testrail( search_term: str, ctx: Context) -> Dict[str, Any]:
        """Retrieve a list of all accessible TestRail projects.
        
        Fetches all projects that the authenticated user has permission to view.
        Useful for getting an overview of available projects or finding project IDs.

        Args:
            search_term: Optional search term to filter projects by name or key

        Returns:
            Dict with status ('success'/'error'), project data, or error message if failed
        """
        try:
            await ctx.info("Fetching all accessible TestRail projects...")

            projects = testrail_service.get_projects(search_term)

            if projects:
                await ctx.info(f"Successfully retrieved {projects.get('total_found')} projects")
            else:
                await ctx.info("No projects found or accessible")

            return projects

        except Exception as e:
            error_msg = f"Failed to get projects: {str(e)}"
            logger.error(error_msg)
            await ctx.error(error_msg)
            return {"status": "error", "message": error_msg}
        

    @mcp.tool()
    async def add_project(ctx: Context, name: str, announcement: Optional[str] = None, show_announcement: Optional[bool] = None, suite_mode: Optional[int] = None) -> Dict:
        """Create a new TestRail project with specified configuration.

        Creates a new project in TestRail with customizable settings for test organization.
        
        Args:
            name: The name of the project (required)
            announcement: Project announcement message to display to users (optional)
            show_announcement: Controls visibility of the announcement (optional)
            suite_mode: Test suite organization mode (optional):
                1 = Single suite mode (basic)
                2 = Single suite with baselines (versioned)
                3 = Multiple suites (advanced organization)
        
        Returns:
            Dict containing the created project details including project ID
            
        Example:
            add_project("Web App Testing", 
                       announcement="New test project for web application",
                       suite_mode=3)
        """
        try:
            await ctx.info(f"Creating new TestRail project: {name}")
            
            data = {'name': name}
            if announcement is not None:
                data['announcement'] = announcement
            if show_announcement is not None:
                data['show_announcement'] = show_announcement
            if suite_mode:
                data['suite_mode'] = suite_mode
                
            result = testrail_service.add_project(data)
            
            if result and result.get('id'):
                await ctx.info(f"Successfully created project: {name} (ID: {result.get('id')})")
            else:
                await ctx.error(f"Failed to create project: {name}")
                
            return result
            
        except Exception as e:
            error_msg = f"Error creating project '{name}': {str(e)}"
            logger.error(error_msg)
            await ctx.error(error_msg)
            return {
                'status': 'error',
                'message': error_msg,
                'project_name': name
            }

    @mcp.tool()
    async def update_project(ctx: Context, project_id: int, name: Optional[str] = None, announcement: Optional[str] = None, show_announcement: Optional[bool] = None, is_completed: Optional[bool] = None) -> Dict:
        """Update an existing TestRail project.
        
        Modifies project settings and metadata while preserving existing data.
        
        Args:
            project_id: The ID of the project to update
            name: The new name of the project (optional)   
            announcement: The new announcement of the project (optional)
            show_announcement: Whether to show the announcement (optional)
            is_completed: Whether the project is completed (optional)
            
        Returns:
            Dict containing the updated project details
        """
        try:
            await ctx.info(f"Updating TestRail project ID: {project_id}")
            
            data = {}
            if name:
                data['name'] = name
            if announcement:
                data['announcement'] = announcement
            if show_announcement is not None:
                data['show_announcement'] = show_announcement
            if is_completed is not None:
                data['is_completed'] = is_completed
                
            if not data:
                await ctx.info("No updates provided - no changes made")
                return {'status': 'warning', 'message': 'No updates provided'}
                
            result = testrail_service.update_project(project_id, data)
            
            if result:
                await ctx.info(f"Successfully updated project {project_id}")
            else:
                await ctx.error(f"Failed to update project {project_id}")
                
            return result
            
        except Exception as e:
            error_msg = f"Error updating project {project_id}: {str(e)}"
            logger.error(error_msg)
            await ctx.error(error_msg)
            return {
                'status': 'error',
                'message': error_msg,
                'project_id': project_id
            }

    @mcp.tool()
    async def delete_project(ctx: Context, project_id: int) -> Dict:
        """Delete a TestRail project.
        
        Permanently removes a project and all its associated data.
        WARNING: This action cannot be undone.
        
        Args:
            project_id: ID of the project to delete
            
        Returns:
            Dict with operation status and details
        """
        try:
            await ctx.info(f"⚠️ Deleting TestRail project ID: {project_id} - This action cannot be undone!")
            
            result = testrail_service.delete_project(project_id)
            
            await ctx.info(f"Successfully deleted project {project_id}")
            
            return {
                'status': 'success',
                'message': f'Project {project_id} deleted successfully',
                'project_id': project_id
            }
            
        except Exception as e:
            error_msg = f"Error deleting project {project_id}: {str(e)}"
            logger.error(error_msg)
            await ctx.error(error_msg)
            return {
                'status': 'error',
                'message': error_msg,
                'project_id': project_id
            }

    @mcp.tool()
    async def get_case(ctx: Context, case_id: int) -> Dict:
        """Retrieve a specific test case by ID.
        
        Fetches detailed information about a test case including steps,
        expectations, metadata, and associated information.
        
        Args:
            case_id: Unique identifier of the test case to retrieve
            
        Returns:
            Dict containing test case details
        """
        try:
            await ctx.info(f"Retrieving test case ID: {case_id}")
            
            result = testrail_service.get_case(case_id)
            
            if result:
                case_title = result.get('title', 'Unknown')
                await ctx.info(f"Successfully retrieved test case: {case_title}")
            else:
                await ctx.error(f"Test case {case_id} not found or not accessible")
                
            return result
            
        except Exception as e:
            error_msg = f"Failed to get test case {case_id}: {str(e)}"
            logger.error(error_msg)
            await ctx.error(error_msg)
            return {
                'status': 'error',
                'message': error_msg,
                'case_id': case_id
            }

    @mcp.tool()
    async def get_cases(ctx: Context, project_id: int, ref: Optional[str], search_term: Optional[str], suite_id: Optional[int] = None, labels_id: Optional[List[int]] = None) -> List[Dict]:
        """Retrieve all test cases for a project with optional filtering.
        
        Fetches test cases from a project, filtered by search_term, suite and labels.
        
        Args:
            project_id: ID of the project to get cases from
            ref: Optional Reference string to filter test cases by jira ticket key e.g. SALMU-2445, PDFR-11521
            search_term: Optional search term to filter cases by title or content
            suite_id: Optional suite ID to filter cases
            labels_id: Optional list of label IDs to filter cases
            
        Returns:
            List of test case dictionaries
        """
        try:

            await ctx.info(f"Retrieving test cases for project {project_id} having labels {labels_id} and filtering by search term '{search_term}'")
            
            cases = testrail_service.get_cases(project_id, ref, search_term,suite_id, labels_id)

            if cases['status'] == 'success':
                await ctx.info(f"Successfully retrieved {cases.get('total_found', 0)} test cases")
            else:
                await ctx.info("No test cases found with the specified criteria")
                
            return cases
            
        except Exception as e:
            error_msg = f"Failed to get test cases for project {project_id}: {str(e)}"
            logger.error(error_msg)
            await ctx.error(error_msg)
            return []

    @mcp.tool()
    async def get_labels(ctx: Context, project_id: int) -> List[str]:
        """Retrieve all labels for a project.
        
        Fetches the list of available labels that can be used for
        categorizing and filtering test cases within a project.
        
        Args:
            project_id: ID of the project to get labels from
            
        Returns:
            List of label strings
        """
        try:
            await ctx.info(f"Retrieving labels for project {project_id}")
            
            labels = testrail_service.get_labels(project_id)
            
            if labels:
                await ctx.info(f"Successfully retrieved {len(labels)} labels")
            else:
                await ctx.info("No labels found for this project")
                
            return labels
            
        except Exception as e:
            error_msg = f"Failed to get labels for project {project_id}: {str(e)}"
            logger.error(error_msg)
            await ctx.error(error_msg)
            return []

    @mcp.tool()
    async def add_case(ctx: Context, section_id: int, title: str, refs: str, template: str = "Test Case (Steps)", custom_description: Optional[str] = None, type_id: Optional[int] = None, priority_id: Optional[int] = None, estimate: Optional[str] = None, custom_steps: Optional[str] = None, custom_expected: Optional[str] = None, custom_steps_separated: Optional[List[Dict[str, str]]] = None, milestone_id: Optional[int] = None) -> Dict:
        """Create a new test case in TestRail with detailed steps and expectations.

        Creates a structured test case that can be either step-based or text-based,
        with support for various metadata like priorities and time estimates.

        Args:
            section_id: ID of the section where the test case will be created (required)
            title: Name/title of the test case (required)
            refs: Comma-separated references (e.g., "JIRA-123, REQ-456") (required)
            template: Test case format, either "Test Case (Steps)" or "Test Case (Text)" (default: Steps)
            custom_description: Detailed description of the test case
            type_id: Test case type identifier (e.g., Functional, Integration)
            priority_id: Priority level ID (e.g., 1=Critical, 2=High)
            estimate: Estimated execution time (e.g., "30s", "1m 45s")
            custom_steps: Steps description for text template
            custom_expected: Expected results for text template
            custom_steps_separated: List of step dictionaries for steps template:
                [{"content": "Step description", "expected": "Expected result"}]
            milestone_id: Associated milestone/release ID

        Returns:
            Dict containing the created test case details including case ID

        Example:
            add_case(
                section_id=123,
                title="User Login Validation",
                refs="AUTH-789",
                custom_steps_separated=[
                    {
                        "content": "Enter valid credentials",
                        "expected": "User successfully logs in"
                    }
                ],
                priority_id=2
            )
        """
        try:
            await ctx.info(f"Creating new test case '{title}' in section {section_id}")
            
            # Validate required parameters
            if not title or not refs:
                error_msg = "Title and refs are required for creating a test case"
                await ctx.error(error_msg)
                return {
                    'status': 'error',
                    'message': error_msg
                }
            
            data = {
                'title': title,
                'refs': refs,
                'template': template
            }
            if type_id is not None:
                data['type_id'] = type_id
            if priority_id is not None:
                data['priority_id'] = priority_id
            if estimate is not None:
                data['estimate'] = estimate
            if milestone_id is not None:
                data['milestone_id'] = milestone_id
            if refs is not None:
                data['refs'] = refs
            if custom_description is not None:
                data['custom_description'] = custom_description
            if template == "Test Case (Text)":
                data['template_id'] = 1  # Default template for Test Case (Text)
                if custom_steps is not None:
                    data['custom_steps'] = custom_steps
                if custom_expected is not None:
                    data['custom_expected'] = custom_expected
            else:  # Default to Test Case (Steps)
                data['template_id'] = 2 
                if custom_steps_separated is not None:
                    data['custom_steps_separated'] = custom_steps_separated       
            data['custom_automation_candidate'] = 1  # Mark as not automated by default
            
            result = testrail_service.add_case(section_id, data)
            
            if result and result.get('id'):
                await ctx.info(f"Successfully created test case: {title} (ID: {result.get('id')})")
            else:
                await ctx.error(f"Failed to create test case: {title}")
                
            return result
            
        except Exception as e:
            error_msg = f"Error creating test case '{title}': {str(e)}"
            logger.error(error_msg)
            await ctx.error(error_msg)
            return {
                'status': 'error',
                'message': error_msg,
                'title': title,
                'section_id': section_id
            }

    @mcp.tool()
    async def update_case(ctx: Context, case_id: int, title: Optional[str] = None, type_id: Optional[int] = None, priority_id: Optional[int] = None, estimate: Optional[str] = None, milestone_id: Optional[int] = None, refs: Optional[str] = None, custom_steps: Optional[str] = None, custom_expected: Optional[str] = None, custom_steps_separated: Optional[List[Dict[str, str]]] = None, steps_separated: Optional[List[Dict[str, str]]] = None) -> Dict:
        """Update an existing test case with new information.
        
        Modifies test case details while preserving existing data for
        fields that are not specified.
    
        Args:
            case_id: The ID of the test case
            title: The title of the test case (optional)
            type_id: The ID of the case type (optional)
            priority_id: The ID of the priority (optional)
            estimate: The estimate, e.g. '30s' or '1m 45s' (optional)
            milestone_id: The ID of the milestone (optional)
            refs: A comma-separated list of references (optional)
            custom_steps: Steps as string
            custom_expected: case expected result
            custom_steps_separated: A list of test steps (optional)
            steps_separated: A list of test steps (optional)
            
        Returns:
            Dict containing the updated test case details
        """
        try:
            await ctx.info(f"Updating test case ID: {case_id}")
            
            data = {}
            if title:
                data['title'] = title
            if type_id:
                data['type_id'] = type_id
            if priority_id:
                data['priority_id'] = priority_id
            if estimate:
                data['estimate'] = estimate
            if milestone_id:
                data['milestone_id'] = milestone_id
            if refs:
                data['refs'] = refs
            if custom_steps:
                data['custom_steps'] = custom_steps
            if custom_expected:
                data['custom_expected'] = custom_expected
            if custom_steps_separated:
                data['custom_steps_separated'] = custom_steps_separated
            if steps_separated:
                data['steps_separated'] = steps_separated
                
            if not data:
                await ctx.info("No updates provided - no changes made")
                return {'status': 'warning', 'message': 'No updates provided'}
                
            result = testrail_service.update_case(case_id, data)
            
            if result:
                case_title = result.get('title', f'Case {case_id}')
                await ctx.info(f"Successfully updated test case: {case_title}")
            else:
                await ctx.error(f"Failed to update test case {case_id}")
                
            return result
            
        except Exception as e:
            error_msg = f"Error updating test case {case_id}: {str(e)}"
            logger.error(error_msg)
            await ctx.error(error_msg)
            return {
                'status': 'error',
                'message': error_msg,
                'case_id': case_id
            }

    @mcp.tool()
    async def delete_case(case_id: int, ctx: Context = None) -> Dict:
        """Delete a test case by ID.
        
        Permanently removes a test case and all its associated data.
        WARNING: This action cannot be undone.
        
        Args:
            case_id: ID of the test case to delete
            
        Returns:
            Dict with operation status and details
        """
        try:
            if ctx:
                await ctx.info(f"⚠️ Deleting test case ID: {case_id} - This action cannot be undone!")
            
            result = testrail_service.delete_case(case_id)
            
            if ctx:
                await ctx.info(f"Successfully deleted test case {case_id}")
            
            return {
                'status': 'success',
                'message': f'Test case {case_id} deleted successfully',
                'case_id': case_id
            }
            
        except Exception as e:
            error_msg = f"Error deleting test case {case_id}: {str(e)}"
            logger.error(error_msg)
            if ctx:
                await ctx.error(error_msg)
            return {
                'status': 'error',
                'message': error_msg,
                'case_id': case_id
            }

    @mcp.tool()
    async def get_section(ctx: Context, section_id: int) -> Dict:
        """Retrieve detailed information about a specific test section.
        
        Test sections are used to group test cases into logical categories
        or functional areas within a project or test suite.
        
        Args:
            section_id: Unique identifier of the section to retrieve
            
        Returns:
            Dict containing section details including:
                - id: Section identifier
                - name: Section name
                - description: Section description
                - parent_id: ID of parent section (if nested)
                - depth: Nesting level of the section
                - display_order: Order in the section hierarchy
        """
        try:
            await ctx.info(f"Retrieving section details for ID: {section_id}")
            
            result = testrail_service.get_section(section_id)
            
            if result:
                section_name = result.get('name', 'Unknown')
                await ctx.info(f"Successfully retrieved section: {section_name}")
            else:
                await ctx.error(f"Section {section_id} not found or not accessible")
                
            return result
            
        except Exception as e:
            error_msg = f"Error retrieving section {section_id}: {str(e)}"
            logger.error(error_msg)
            await ctx.error(error_msg)
            return {
                'status': 'error',
                'message': error_msg,
                'section_id': section_id
            }

    @mcp.tool()
    async def get_sections(ctx: Context, project_id: int, suite_id: Optional[int] = None) -> Dict:
        """Retrieve all test sections in a project, optionally filtered by test suite.
        
        Returns the complete section hierarchy, including nested sections,
        that are used to organize test cases within a project or suite.
        
        Args:
            project_id: ID of the project to get sections from
            suite_id: Optional ID of a specific test suite to filter sections
            
        Returns:
            Dict containing a list of section objects, each including:
                - id: Section identifier
                - name: Section name
                - description: Section description
                - parent_id: ID of parent section
                - depth: Nesting level
                - display_order: Order in hierarchy
                
        Example:
            sections = get_sections(
                project_id=123,
                suite_id=456  # Optional: limit to specific suite
            )
        """
        try:
            filter_text = f" for suite {suite_id}" if suite_id else ""
            await ctx.info(f"Retrieving sections for project {project_id}{filter_text}")
            
            result = testrail_service.get_sections(project_id, suite_id)
            
            if result:
                section_count = len(result) if isinstance(result, list) else result.get('count', 0)
                await ctx.info(f"Successfully retrieved {section_count} sections")
            else:
                await ctx.info("No sections found for the specified criteria")
                
            return result
            
        except Exception as e:
            error_msg = f"Error retrieving sections for project {project_id}: {str(e)}"
            logger.error(error_msg)
            await ctx.error(error_msg)
            return {
                'status': 'error',
                'message': error_msg,
                'project_id': project_id
            }

    @mcp.tool()
    async def add_section(ctx: Context, project_id: int, name: str, description: str, suite_id: Optional[int] = None, parent_id: Optional[int] = None) -> Dict:
        """Add a new section to a project.
        
        Creates a new test section for organizing test cases within
        a project or test suite hierarchy.
        
        Args:   
            project_id: The ID of the project
            name: The name of the section
            description: The description of the section
            suite_id: The ID of the suite (optional)
            parent_id: The ID of the parent section (optional)
            
        Returns:
            Dict containing the created section details
        """
        try:
            await ctx.info(f"Creating new section '{name}' in project {project_id}")
            
            data = {'name': name, 'description': description}
            if suite_id:
                data['suite_id'] = suite_id
            if parent_id:
                data['parent_id'] = parent_id
                
            result = testrail_service.add_section(project_id, data)
            
            if result and result.get('id'):
                await ctx.info(f"Successfully created section: {name} (ID: {result.get('id')})")
            else:
                await ctx.error(f"Failed to create section: {name}")
                
            return result
            
        except Exception as e:
            error_msg = f"Error creating section '{name}': {str(e)}"
            logger.error(error_msg)
            await ctx.error(error_msg)
            return {
                'status': 'error',
                'message': error_msg,
                'name': name,
                'project_id': project_id
            }

    @mcp.tool()
    async def update_section(ctx: Context, section_id: int, name: Optional[str] = None, description: Optional[str] = None) -> Dict:
        """Update an existing test section.
        
        Modifies section properties while preserving existing data for
        fields that are not specified.
        
        Args:
            section_id: ID of the section to update
            name: New name for the section (optional)
            description: New description for the section (optional)
            
        Returns:
            Dict containing the updated section details
        """
        try:
            await ctx.info(f"Updating section ID: {section_id}")
            
            data = {}
            if name:
                data['name'] = name
            if description:
                data['description'] = description
                
            if not data:
                await ctx.info("No updates provided - no changes made")
                return {'status': 'warning', 'message': 'No updates provided'}
                
            result = testrail_service.update_section(section_id, data)
            
            if result:
                section_name = result.get('name', f'Section {section_id}')
                await ctx.info(f"Successfully updated section: {section_name}")
            else:
                await ctx.error(f"Failed to update section {section_id}")
                
            return result
            
        except Exception as e:
            error_msg = f"Error updating section {section_id}: {str(e)}"
            logger.error(error_msg)
            await ctx.error(error_msg)
            return {
                'status': 'error',
                'message': error_msg,
                'section_id': section_id
            }

    @mcp.tool()
    async def delete_section(ctx: Context, section_id: int, soft: bool) -> Dict:
        """Delete a test section.
        
        Removes a section and optionally its content. Can perform soft delete
        to preserve data or hard delete to permanently remove.
        
        Args:
            section_id: ID of the section to delete
            soft: Whether to perform soft delete (preserves data) or hard delete
            
        Returns:
            Dict with operation status and details
        """
        try:
            delete_type = "soft" if soft else "hard"
            await ctx.info(f"⚠️ Performing {delete_type} delete of section {section_id}")
            
            result = testrail_service.delete_section(section_id, soft)
            
            await ctx.info(f"Successfully deleted section {section_id} ({delete_type} delete)")
            
            return {
                'status': 'success',
                'message': f'Section {section_id} deleted successfully ({delete_type})',
                'section_id': section_id,
                'delete_type': delete_type
            }
            
        except Exception as e:
            error_msg = f"Error deleting section {section_id}: {str(e)}"
            logger.error(error_msg)
            await ctx.error(error_msg)
            return {
                'status': 'error',
                'message': error_msg,
                'section_id': section_id
            }

    @mcp.tool()
    async def move_section(ctx: Context, section_id: int, parent_id: Optional[int], after_id: Optional[int]) -> Dict:
        """Move a section to a new parent or position.
        
        Reorganizes section hierarchy by moving a section to a different
        parent or changing its position within the same parent.
        
        Args:
            section_id: ID of the section to move
            parent_id: ID of the new parent section (optional)
            after_id: ID of the section to place this section after (optional)
            
        Returns:
            Dict containing the updated section details
        """
        try:
            move_info = []
            if parent_id:
                move_info.append(f"to parent {parent_id}")
            if after_id:
                move_info.append(f"after section {after_id}")
                
            move_text = ", ".join(move_info) if move_info else "with no specific positioning"
            await ctx.info(f"Moving section {section_id} {move_text}")
            
            data = {'parent_id': parent_id, 'after_id': after_id}
            result = testrail_service.move_section(section_id, data)
            
            if result:
                await ctx.info(f"Successfully moved section {section_id}")
            else:
                await ctx.error(f"Failed to move section {section_id}")
                
            return result
            
        except Exception as e:
            error_msg = f"Error moving section {section_id}: {str(e)}"
            logger.error(error_msg)
            await ctx.error(error_msg)
            return {
                'status': 'error',
                'message': error_msg,
                'section_id': section_id
            }

    @mcp.tool()
    async def get_run(run_id: int, ctx: Context) -> Dict:
        """Retrieve detailed information about a specific test run.
        
        Test runs represent an execution instance of test cases, tracking
        the results and progress of testing activities.
        
        Args:
            run_id: Unique identifier of the test run to retrieve
            
        Returns:
            Dict containing run details including:
                - id: Run identifier
                - name: Run name
                - description: Run description
                - milestone_id: Associated milestone
                - assignedto_id: User the run is assigned to
                - include_all: Whether all tests are included
                - is_completed: Completion status
                - completed_on: Completion timestamp
                - passed_count: Number of passed tests
                - blocked_count: Number of blocked tests
                - untested_count: Number of untested cases
                - retest_count: Number of tests marked for retest
                - failed_count: Number of failed tests
                - custom_status_count: Count of custom status results
                - url: Test run URL in TestRail
        """
        try:
            await ctx.info(f"Retrieving test run details for ID: {run_id}")
            
            result = testrail_service.get_run(run_id)
            
            if result:
                run_name = result.get('name', 'Unknown')
                is_completed = result.get('is_completed', False)
                status = "completed" if is_completed else "active"
                await ctx.info(f"Successfully retrieved test run: {run_name} ({status})")
            else:
                await ctx.error(f"Test run {run_id} not found or not accessible")
                
            return result
            
        except Exception as e:
            error_msg = f"Error retrieving test run {run_id}: {str(e)}"
            logger.error(error_msg)
            await ctx.error(error_msg)
            return {
                'status': 'error',
                'message': error_msg,
                'run_id': run_id
            }

    @mcp.tool()
    async def get_runs(project_id: int, ctx: Context, status: str, created_by: Optional[int] = None) -> List[Dict]:
        """Retrieve all test runs in a project.
        
        Returns a list of all test runs, including active and completed runs,
        for the specified project based on status filter. Useful for monitoring testing progress
        and accessing historical test execution data.
        
        Args:
            project_id: ID of the project to get runs from.
            status: filter for run completion status. e.g. active, completed
            created_by: filter for user who created the run e.g. 123

        Returns:
            List of dictionaries, each containing run information:
                - id: Run identifier
                - name: Run name
                - description: Run description
                - milestone_id: Associated milestone
                - assignedto_id: Assigned user ID
                - is_completed: Completion status
                - completed_on: Completion timestamp
                - passed_count: Number of passed tests
                - blocked_count: Number of blocked tests
                - untested_count: Number of untested cases
                - retest_count: Number of tests for retest
                - failed_count: Number of failed tests
                - url: Test run URL
        """
        try:
            await ctx.info(f"Retrieving test runs for project {project_id}")
            await ctx.info(f"Status filter: {status}, Created by: {created_by}")
            runs = testrail_service.get_runs(project_id, status, created_by)
            
            # if runs:
            #     active_runs = sum(1 for run in runs if not run.get('is_completed', False))
            #     completed_runs = len(runs) - active_runs
            #     await ctx.info(f"Successfully retrieved {len(runs)} test runs ({active_runs} active, {completed_runs} completed)")
            # else:
            #     await ctx.info("No test runs found for this project")
                
            return runs
            
        except Exception as e:
            error_msg = f"Error retrieving test runs for project {project_id}: {str(e)}"
            logger.error(error_msg)
            await ctx.error(error_msg)
            return []

    @mcp.tool()
    async def add_run(ctx: Context, project_id: int, suite_id: int, name: str, description: Optional[str] = None, milestone_id: Optional[int] = None, assignedto_id: Optional[int] = None, include_all: Optional[bool] = False, case_ids: Optional[List[int]] = None) -> Dict:
        """Create a new test run in a project.
        
        Initiates a new test execution cycle with specified test cases
        and configuration settings.
        
        Args:
            project_id: ID of the project to create the run in
            suite_id: ID of the test suite for this run
            name: Name for the test run
            description: Optional description of the test run
            milestone_id: Optional milestone to associate with this run
            assignedto_id: Optional user ID to assign the run to
            include_all: Whether to include all test cases from the suite
            case_ids: Optional list of specific case IDs to include
            
        Returns:
            Dict containing the created test run details
        """
        try:
            await ctx.info(f"Creating new test run '{name}' in project {project_id}")
            
            data = {'suite_id': suite_id, 'name': name}
            if description:
                data['description'] = description
            if milestone_id:
                data['milestone_id'] = milestone_id
            if assignedto_id:
                data['assignedto_id'] = assignedto_id
            if include_all is not None:
                data['include_all'] = include_all
            if case_ids:
                data['case_ids'] = case_ids
                await ctx.info(f"Including {len(case_ids)} specific test cases")
            elif include_all:
                await ctx.info("Including all test cases from the suite")
                
            result = testrail_service.add_run(project_id, data)
            
            if result and result.get('id'):
                await ctx.info(f"Successfully created test run: {name} (ID: {result.get('id')})")
            else:
                await ctx.error(f"Failed to create test run: {name}")
                
            return result
            
        except Exception as e:
            error_msg = f"Error creating test run '{name}': {str(e)}"
            logger.error(error_msg)
            await ctx.error(error_msg)
            return {
                'status': 'error',
                'message': error_msg,
                'name': name,
                'project_id': project_id
            }

    @mcp.tool()
    async def update_run(ctx: Context, run_id: int, name: Optional[str] = None, description: Optional[str] = None, milestone_id: Optional[int] = None, assignedto_id: Optional[int] = None, include_all: Optional[bool] = None, case_ids: Optional[List[int]] = None) -> Dict:
        """Update an existing test run.
        
        Modifies test run properties and configuration while preserving
        existing data for fields that are not specified.
        
        Args:
            run_id: ID of the test run to update
            name: New name for the test run (optional)
            description: New description for the test run (optional)
            milestone_id: New milestone ID to associate (optional)
            assignedto_id: New user ID to assign the run to (optional)
            include_all: Whether to include all test cases (optional)
            case_ids: New list of specific case IDs to include (optional)
            
        Returns:
            Dict containing the updated test run details
        """
        try:
            await ctx.info(f"Updating test run ID: {run_id}")
            
            data = {}
            if name:
                data['name'] = name
            if description:
                data['description'] = description
            if milestone_id:
                data['milestone_id'] = milestone_id
            if assignedto_id:
                data['assignedto_id'] = assignedto_id
            if include_all is not None:
                data['include_all'] = include_all
            if case_ids:
                data['case_ids'] = case_ids
                await ctx.info(f"Updating to include {len(case_ids)} specific test cases")
                
            if not data:
                await ctx.info("No updates provided - no changes made")
                return {'status': 'warning', 'message': 'No updates provided'}
                
            result = testrail_service.update_run(run_id, data)
            
            if result:
                run_name = result.get('name', f'Run {run_id}')
                await ctx.info(f"Successfully updated test run: {run_name}")
            else:
                await ctx.error(f"Failed to update test run {run_id}")
                
            return result
            
        except Exception as e:
            error_msg = f"Error updating test run {run_id}: {str(e)}"
            logger.error(error_msg)
            await ctx.error(error_msg)
            return {
                'status': 'error',
                'message': error_msg,
                'run_id': run_id
            }

    @mcp.tool()
    async def close_run(ctx: Context, run_id: int) -> Dict:
        """Close a test run.
        
        Marks a test run as completed, preventing further test result
        updates and finalizing the test execution cycle.
        
        Args:
            run_id: ID of the test run to close
            
        Returns:
            Dict with operation status and details
        """
        try:
            await ctx.info(f"Closing test run ID: {run_id}")
            
            result = testrail_service.close_run(run_id)
            
            await ctx.info(f"Successfully closed test run {run_id}")
            
            return {
                'status': 'success',
                'message': f'Test run {run_id} closed successfully',
                'run_id': run_id
            }
            
        except Exception as e:
            error_msg = f"Error closing test run {run_id}: {str(e)}"
            logger.error(error_msg)
            await ctx.error(error_msg)
            return {
                'status': 'error',
                'message': error_msg,
                'run_id': run_id
            }

    @mcp.tool()
    async def delete_run(run_id: int, ctx: Context) -> Dict:
        """Delete a test run.
        
        Permanently removes a test run and all its associated test results.
        WARNING: This action cannot be undone.
        
        Args:
            run_id: ID of the test run to delete
            
        Returns:
            Dict with operation status and details
        """
        try:
            await ctx.info(f"⚠️ Deleting test run ID: {run_id} - This action cannot be undone!")
            
            result = testrail_service.delete_run(run_id)
            
            await ctx.info(f"Successfully deleted test run {run_id}")
            
            return {
                'status': 'success',
                'message': f'Test run {run_id} deleted successfully',
                'run_id': run_id
            }
            
        except Exception as e:
            error_msg = f"Error deleting test run {run_id}: {str(e)}"
            logger.error(error_msg)
            await ctx.error(error_msg)
            return {
                'status': 'error',
                'message': error_msg,
                'run_id': run_id
            }

    @mcp.tool()
    async def get_results(test_id: int, ctx: Context) -> List[Dict]:
        """Retrieve all test results for a specific test.
        
        Gets the complete history of test results for a given test,
        including all executions and their details.
        
        Args:
            test_id: ID of the test to get results for
            
        Returns:
            List of dictionaries, each containing result information:
                - id: Result identifier
                - test_id: Test identifier
                - status_id: Result status (1=Passed, 2=Blocked, 3=Untested, 4=Retest, 5=Failed)
                - created_by: User who created the result
                - created_on: Creation timestamp
                - comment: Result comments/notes
                - version: System version tested
                - elapsed: Time taken for test
                - defects: Associated defect references
        """
        try:
            await ctx.info(f"Retrieving test results for test ID: {test_id}")
            
            results = testrail_service.get_results(test_id)
            
            if results:
                await ctx.info(f"Successfully retrieved {len(results)} test results")
            else:
                await ctx.info("No test results found for this test")
                
            return results
            
        except Exception as e:
            error_msg = f"Error retrieving test results for test {test_id}: {str(e)}"
            logger.error(error_msg)
            await ctx.error(error_msg)
            return []

    @mcp.tool()
    async def add_result(ctx: Context,test_id: int, status_id: int, comment: Optional[str] = None, version: Optional[str] = None, elapsed: Optional[str] = None, defects: Optional[str] = None, assignedto_id: Optional[int] = None) -> Dict:
        """Add a test result for a specific test case execution.
        
        Records the outcome of a test execution with detailed information
        about the test run, including status, timing, and any issues found.
        
        Args:
            test_id: ID of the test to add result for (required)
            status_id: Result status ID (required):
                1 = Passed
                2 = Blocked
                3 = Untested
                4 = Retest
                5 = Failed
            comment: Additional notes about the test result
            version: Version of the system under test
            elapsed: Time taken to execute the test (e.g., "30s", "2m 45s")
            defects: References to related defects/issues
            assignedto_id: User ID to assign the result to
            
        Returns:
            Dict containing the created test result details
            
        Example:
            add_result(
                test_id=123,
                status_id=5,  # Failed
                comment="Test failed due to timeout",
                version="2.0.0",
                elapsed="1m 30s",
                defects="BUG-789"
            )
        """
        try:
            status_names = {1: "Passed", 2: "Blocked", 3: "Untested", 4: "Retest", 5: "Failed"}
            status_name = status_names.get(status_id, f"Status {status_id}")
            
            await ctx.info(f"Adding test result for test {test_id}: {status_name}")
            
            data = {'status_id': status_id}
            if comment:
                data['comment'] = comment
            if version:
                data['version'] = version
            if elapsed:
                data['elapsed'] = elapsed
            if defects:
                data['defects'] = defects
            if assignedto_id:
                data['assignedto_id'] = assignedto_id
                
            result = testrail_service.add_result(test_id, data)
            
            if result and result.get('id'):
                await ctx.info(f"Successfully added test result: {status_name} (ID: {result.get('id')})")
            else:
                await ctx.error(f"Failed to add test result for test {test_id}")
                
            return result
            
        except Exception as e:
            error_msg = f"Error adding test result for test {test_id}: {str(e)}"
            logger.error(error_msg)
            await ctx.error(error_msg)
            return {
                'status': 'error',
                'message': error_msg,
                'test_id': test_id
            }

    @mcp.tool()
    async def get_dataset(dataset_id: int, ctx: Context) -> Dict:
        """Retrieve information about a specific test data set.
        
        Test data sets are collections of test data that can be used
        across multiple test cases for data-driven testing.
        
        Args:
            dataset_id: Unique identifier of the dataset to retrieve
            
        Returns:
            Dict containing dataset details including:
                - id: Dataset identifier
                - name: Dataset name
                - description: Dataset description
                - project_id: Associated project ID
                - config: Dataset configuration
                - entries: Test data entries
        """
        try:
            await ctx.info(f"Retrieving dataset details for ID: {dataset_id}")
            
            result = testrail_service.get_dataset(dataset_id)
            
            if result:
                dataset_name = result.get('name', 'Unknown')
                await ctx.info(f"Successfully retrieved dataset: {dataset_name}")
            else:
                await ctx.error(f"Dataset {dataset_id} not found or not accessible")
                
            return result
            
        except Exception as e:
            error_msg = f"Error retrieving dataset {dataset_id}: {str(e)}"
            logger.error(error_msg)
            await ctx.error(error_msg)
            return {
                'status': 'error',
                'message': error_msg,
                'dataset_id': dataset_id
            }

    @mcp.tool()
    async def get_datasets(project_id: int, ctx: Context) -> List[Dict]:
        """Retrieve all test data sets in a project.
        
        Gets a list of all available test data sets that can be used
        for data-driven testing within the specified project.
        
        Args:
            project_id: ID of the project to get datasets from
            
        Returns:
            List of dictionaries, each containing dataset information:
                - id: Dataset identifier
                - name: Dataset name
                - description: Dataset description
                - project_id: Associated project ID
                - config: Dataset configuration
                - entries_count: Number of data entries
        """
        try:
            await ctx.info(f"Retrieving datasets for project {project_id}")
            
            datasets = testrail_service.get_datasets(project_id)
            
            if datasets:
                await ctx.info(f"Successfully retrieved {len(datasets)} datasets")
            else:
                await ctx.info("No datasets found for this project")
                
            return datasets
            
        except Exception as e:
            error_msg = f"Error retrieving datasets for project {project_id}: {str(e)}"
            logger.error(error_msg)
            await ctx.error(error_msg)
            return []

    @mcp.tool()
    async def add_dataset(ctx: Context, project_id: int, name: str, description: Optional[str] = None) -> Dict:
        """Create a new test data set in a project.
        
        Creates a container for test data that can be used across multiple
        test cases for data-driven testing scenarios.
        
        Args:
            project_id: ID of the project to create dataset in (required)
            name: Name of the dataset (required)
            description: Detailed description of the dataset's purpose and content
            
        Returns:
            Dict containing the created dataset details including:
                - id: Dataset identifier
                - name: Dataset name
                - description: Dataset description
                - project_id: Associated project ID
                
        Example:
            add_dataset(
                project_id=123,
                name="Login Test Data",
                description="Test credentials for various user roles"
            )
        """
        try:
            await ctx.info(f"Creating new dataset '{name}' in project {project_id}")
            
            data = {'name': name}
            if description:
                data['description'] = description
                
            result = testrail_service.add_dataset(project_id, data)
            
            if result and result.get('id'):
                await ctx.info(f"Successfully created dataset: {name} (ID: {result.get('id')})")
            else:
                await ctx.error(f"Failed to create dataset: {name}")
                
            return result
            
        except Exception as e:
            error_msg = f"Error creating dataset '{name}': {str(e)}"
            logger.error(error_msg)
            await ctx.error(error_msg)
            return {
                'status': 'error',
                'message': error_msg,
                'name': name,
                'project_id': project_id
            }

    @mcp.tool()
    async def update_dataset(ctx: Context, dataset_id: int, name: Optional[str] = None, description: Optional[str] = None) -> Dict:
        """Update an existing test data set.
        
        Modifies dataset properties while preserving existing data for
        fields that are not specified.
        
        Args:
            dataset_id: ID of the dataset to update
            name: New name for the dataset (optional)
            description: New description for the dataset (optional)
            
        Returns:
            Dict containing the updated dataset details
        """
        try:
            await ctx.info(f"Updating dataset ID: {dataset_id}")
            
            data = {}
            if name:
                data['name'] = name
            if description:
                data['description'] = description
                
            if not data:
                await ctx.info("No updates provided - no changes made")
                return {'status': 'warning', 'message': 'No updates provided'}
                
            result = testrail_service.update_dataset(dataset_id, data)
            
            if result:
                dataset_name = result.get('name', f'Dataset {dataset_id}')
                await ctx.info(f"Successfully updated dataset: {dataset_name}")
            else:
                await ctx.error(f"Failed to update dataset {dataset_id}")
                
            return result
            
        except Exception as e:
            error_msg = f"Error updating dataset {dataset_id}: {str(e)}"
            logger.error(error_msg)
            await ctx.error(error_msg)
            return {
                'status': 'error',
                'message': error_msg,
                'dataset_id': dataset_id
            }

    @mcp.tool()
    async def delete_dataset(ctx: Context, dataset_id: int) -> Dict:
        """
        Delete a test data set.
        """
        return testrail_service.delete_dataset(dataset_id)

    @mcp.tool()
    async def add_results_for_cases(run_id: int, results: List[Dict], ctx: Context) -> List[Dict]:
        """Submit test execution results for multiple test cases in a test run.

        Batch updates test results for multiple cases in a single test run, allowing
        efficient reporting of test execution outcomes with detailed information.

        Args:
            run_id: ID of the test run to update (required)
            results: List of result dictionaries with the following fields:
                - case_id (required): ID of the test case
                - status_id (required): Result status (e.g., 1=Passed, 2=Blocked, 3=Untested, 4=Retest, 5=Failed)
                - comment (optional): Additional notes or failure details
                - version (optional): Version of the system under test
                - elapsed (optional): Time taken (e.g., "30s", "2m 45s")
                - defects (optional): Related defect references
                - assignedto_id (optional): User ID to assign the result to

        Returns:
            List of dictionaries containing the added test results

        Example:
            add_results_for_cases(
                run_id=456,
                results=[
                    {
                        "case_id": 123,
                        "status_id": 1,
                        "comment": "Test passed successfully",
                        "elapsed": "45s",
                        "version": "2.0.0"
                    },
                    {
                        "case_id": 124,
                        "status_id": 5,
                        "comment": "Failed: Database connection error",
                        "defects": "BUG-789"
                    }
                ]
            )
        """
        try:
            await ctx.info(f"Adding batch test results for run {run_id} - {len(results)} results")
            
            # Validate required fields
            for i, result in enumerate(results):
                if not result.get('case_id') or not result.get('status_id'):
                    error_msg = f"Result {i+1} missing required case_id or status_id"
                    await ctx.error(error_msg)
                    return {
                        'status': 'error',
                        'message': error_msg
                    }
            
            data = {'results': results}
            batch_results = testrail_service.add_results_for_cases(run_id, data)
            
            if batch_results:
                await ctx.info(f"Successfully added {len(batch_results)} test results")
            else:
                await ctx.error(f"Failed to add batch test results for run {run_id}")
                
            return batch_results
            
        except Exception as e:
            error_msg = f"Error adding batch test results for run {run_id}: {str(e)}"
            logger.error(error_msg)
            await ctx.error(error_msg)
            return {
                'status': 'error',
                'message': error_msg,
                'run_id': run_id
            }

    @mcp.tool()
    async def get_results_for_run(run_id: int, ctx: Context) -> List[Dict]:
        """Retrieve test execution results for a specific test run.

        This function fetches all test results associated with a given
        test run, providing insights into the outcomes of test case
        executions.

        Args:
            run_id: ID of the test run to retrieve results for

        Returns:
            List of dictionaries, each containing result information:
                - case_id: ID of the test case
                - status_id: Result status (e.g., 1=Passed, 2=Blocked, 3=Untested, 4=Retest, 5=Failed)
                - comment: Additional notes or failure details
                - version: Version of the system under test
                - elapsed: Time taken (e.g., "30s", "2m 45s")
                - defects: Related defect references
                - assignedto_id: User ID to whom the result is assigned
        """
        try:
            await ctx.info(f"Retrieving test results for run {run_id}")
            
            results = testrail_service.get_results_for_run(run_id)
            
            if results:
                await ctx.info(f"Successfully retrieved {len(results)} test results for run {run_id}")
            else:
                await ctx.info(f"No test results found for run {run_id}")
                
            return results
            
        except Exception as e:
            error_msg = f"Error retrieving test results for run {run_id}: {str(e)}"
            logger.error(error_msg)
            await ctx.error(error_msg)
            return []
