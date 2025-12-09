import os
import requests
import logging
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)

TESTRAIL_URL = os.getenv("TESTRAIL_URL")
TESTRAIL_USERNAME = os.getenv("TESTRAIL_USERNAME")
TESTRAIL_API_KEY = os.getenv("TESTRAIL_API_KEY")

class TestRailService:
    def __init__(self):
        self.base_url = TESTRAIL_URL
        self.email = TESTRAIL_USERNAME
        self.password = TESTRAIL_API_KEY
        self.session = requests.Session()
        self.session.auth = (self.email, self.password)

    def _send_request(self, method: str, uri: str, data: Optional[Dict] = None) -> Any:
        url = f"{self.base_url.rstrip('/')}/index.php?/api/v2/{uri}"
        try:
            if method.upper() == 'GET':
                response = self.session.get(url)
            elif method.upper() == 'POST':
                response = self.session.post(url, json=data)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            if response.status_code >= 400:
                logger.error(f"TestRail API error: {response.status_code} - {response.text}")
                response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            logger.error(f"Timeout while accessing {url}")
            raise
        except requests.exceptions.ConnectionError:
            logger.error(f"Connection error while accessing {url}")
            raise
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error {e.response.status_code} for {url}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise

    # User API
    def get_current_user(self) -> Dict:
        """
        Get the current user information from TestRail.
        
        Returns:
            Dictionary containing user information
        """
        try:
            user_data = self._send_request('GET', 'get_current_user')
            return {
                'status': 'success',
                'user': user_data,
                'endpoint_used': f"{self.base_url}get_current_user"
            }
        except Exception as e:
            logger.error(f"Error fetching current user: {str(e)}")
            return {
                'status': 'error',
                'message': str(e),
                'error_type': 'unexpected_error',
                'endpoint_used': f"{self.base_url}get_current_user"
            }

    # Projects API
    def get_project(self, project_id: int) -> Dict:
        return self._send_request('GET', f'get_project/{project_id}')

    def get_projects(self, search_term: str = "") -> Dict[str, Any]:
        """
        Get all accessible projects with their IDs and basic information.
        
        Args:
            search_term: Optional search term to filter projects by name or key
        """        
        all_projects = []
        offset = 0
        limit = 250  # Use API's maximum limit per page
        
        while True:
            # Make API request with pagination parameters
            uri = f'get_projects&offset={offset}&limit={limit}'
            projects_data = self._send_request('GET', uri)
            
            # Handle error response
            if isinstance(projects_data, dict) and projects_data.get('status') == 'error':
                return projects_data
            
            # Handle different response formats
            if isinstance(projects_data, dict) and 'projects' in projects_data:
                projects_list = projects_data['projects']
                has_more = projects_data.get('_links', {}).get('next') is not None
            elif isinstance(projects_data, list):
                projects_list = projects_data
                has_more = len(projects_list) == limit  # Assume more if we got a full page
            else:
                projects_list = []
                has_more = False
            
            # Add projects to our collection
            all_projects.extend(projects_list)
            
            # Break if we have no more data
            if not has_more or len(projects_list) == 0:
                break
                
            # Move to next page
            offset += limit
        
        # Apply client-side filtering if search term is provided
        total_retrieved = len(all_projects)  # Store count before filtering
        if search_term:
            search_lower = search_term.lower()
            filtered_projects = []
            for project in all_projects:
                name = project.get('name', '').lower()
                
                if search_lower in name:
                    filtered_projects.append(project)
            all_projects = filtered_projects
        
        projects_list = all_projects
        
        # Format the results with enhanced information
        formatted_projects = {
            'total': len(projects_list),
            'projects': projects_list
        }
        return {
            'status': 'success',
            'results': formatted_projects,
            'search_term': search_term if search_term else 'All projects',
            'total_found': len(projects_list),
            'filtered': bool(search_term),
            'total_retrieved': total_retrieved,
            'pagination_used': offset > 0
        }    

    def add_project(self, data: Dict) -> Dict:
        return self._send_request('POST', 'add_project', data)

    def update_project(self, project_id: int, data: Dict) -> Dict:
        return self._send_request('POST', f'update_project/{project_id}', data)

    def delete_project(self, project_id: int) -> Dict:
        return self._send_request('POST', f'delete_project/{project_id}')

    # Cases API
    def get_case(self, case_id: int) -> Dict:
        return self._send_request('GET', f'get_case/{case_id}')

    def get_cases(self, project_id:int, ref: Optional[str] = None, search_term: Optional[str] = None, suite_id: Optional[int] = None, labels_id: Optional[List[int]] = None) -> Dict[str, Any]:
            """
            Get all test case for the given project id.
            
            Args:
                project_id: The ID of the project to get test cases from
                ref: Reference string to filter test cases by jira ticket key e.g. SALMU-2445,PDFR-11521
                search_term: optional search term to filter test cases by title or description
            """        
            all_cases = []
            offset = 0
            limit = 250  # Use API's maximum limit per page
            
            while True:
                # Make API request with pagination parameters
                uri = f'get_cases/{project_id}'
                if ref:
                    uri += f'&refs={ref}'
                if suite_id:
                    uri += f'&suite_id={suite_id}'
                if labels_id:
                    uri += f'&label_id={",".join(map(str, labels_id))}'
                    
                uri += f'&offset={offset}&limit={limit}'
                
                cases_data = self._send_request('GET', uri)
                
                # Handle error response
                if isinstance(cases_data, dict) and cases_data.get('status') == 'error':
                    return cases_data
                
                # Handle different response formats
                if isinstance(cases_data, dict) and 'cases' in cases_data:
                    cases_list = cases_data['cases']
                    has_more = cases_data.get('_links', {}).get('next') is not None
                elif isinstance(cases_data, list):
                    cases_list = cases_data
                    has_more = len(cases_list) == limit  # Assume more if we got a full page
                else:
                    cases_list = []
                    has_more = False
                
                # Add cases to our collection
                all_cases.extend(cases_list)
                
                # Break if we have no more data
                if not has_more or len(cases_list) == 0:
                    break
                    
                # Move to next page
                offset += limit
            
            # Apply client-side filtering if search term is provided
            total_retrieved = len(all_cases)  # Store count before filtering
            if search_term:
                search_lower = search_term.lower()
                filtered_cases = []
                for case in all_cases:
                    title = (case.get('title') or '').lower()
                    custom_description = (case.get('custom_description') or '').lower()

                    if (search_lower in title) or (search_lower in custom_description):
                        filtered_cases.append(case)
                cases_list = filtered_cases
            else:
                cases_list = all_cases
            
            # Format the results with enhanced information
            formatted_cases = {
                'total': len(cases_list),
                'cases': cases_list
            }
            return {
                'status': 'success',
                'results': formatted_cases,
                'search_term': search_term if search_term else 'All Cases',
                'total_found': len(all_cases),
                'filtered': bool(search_term),
                'total_retrieved': total_retrieved,
                'pagination_used': offset > 0
            }  


    def add_case(self, section_id: int, data: Dict) -> Dict:
        return self._send_request('POST', f'add_case/{section_id}', data)

    def update_case(self, case_id: int, data: Dict) -> Dict:
        return self._send_request('POST', f'update_case/{case_id}', data)

    def delete_case(self, case_id: int) -> Dict:
        return self._send_request('POST', f'delete_case/{case_id}')

    # Get labels
    def get_labels(self, project_id: int) -> List[str]:
        return self._send_request('GET', f'get_labels/{project_id}')
    
    # Sections API
    def get_section(self, section_id: int) -> Dict:
        return self._send_request('GET', f'get_section/{section_id}')

    def get_sections(self, project_id: int, suite_id: Optional[int] = None) -> Dict:
        uri = f'get_sections/{project_id}'
        if suite_id:
            uri += f'&suite_id={suite_id}'
        return self._send_request('GET', uri)

    def add_section(self, project_id: int, data: Dict) -> Dict:
        return self._send_request('POST', f'add_section/{project_id}', data)

    def update_section(self, section_id: int, data: Dict) -> Dict:
        return self._send_request('POST', f'update_section/{section_id}', data)

    def delete_section(self, section_id: int, soft: bool) -> Dict:
        url = f'delete_section/{section_id}'
        if soft:
            url += '?soft=1'
        return self._send_request('POST', url)

    def move_section(self, section_id: int, data: Dict) -> Dict:
        return self._send_request('POST', f'move_section/{section_id}', data)

    # Runs API
    def get_run(self, run_id: int) -> Dict:
        return self._send_request('GET', f'get_run/{run_id}')

    def get_runs(self, project_id: int, status: str, created_by: Optional[int] = None) -> List[Dict]:
        uri = f'get_runs/{project_id}'
        if status is not None:
            if status.lower() == 'active':
                uri += f'&is_completed=0'
            elif status.lower() == 'completed':
                uri += f'&is_completed=1'
            else:
                uri += f'&is_completed={''}'
        if created_by is not None:
            uri += f'&created_by={created_by}'
        return self._send_request('GET', uri)

    def add_run(self, project_id: int, data: Dict) -> Dict:
        return self._send_request('POST', f'add_run/{project_id}', data)

    def update_run(self, run_id: int, data: Dict) -> Dict:
        return self._send_request('POST', f'update_run/{run_id}', data)

    def close_run(self, run_id: int) -> Dict:
        return self._send_request('POST', f'close_run/{run_id}', {})

    def delete_run(self, run_id: int) -> Dict:
        return self._send_request('POST', f'delete_run/{run_id}')

    # Results API
    def get_results(self, test_id: int) -> List[Dict]:
        return self._send_request('GET', f'get_results/{test_id}')

    def get_results_for_run(self, run_id: int) -> List[Dict]:
        return self._send_request('GET', f'get_results_for_run/{run_id}')

    def add_results_for_cases(self, run_id: int, data: Dict) -> List[Dict]:
        return self._send_request('POST', f'add_results_for_cases/{run_id}', data)

    # Datasets API
    def get_datasets(self, project_id: int) -> List[Dict]:
        return self._send_request('GET', f'get_datasets/{project_id}')

    def get_dataset(self, dataset_id: int) -> Dict:
        return self._send_request('GET', f'get_dataset/{dataset_id}')

    def add_dataset(self, project_id: int, data: Dict) -> Dict:
        return self._send_request('POST', f'add_dataset/{project_id}', data)

    def update_dataset(self, dataset_id: int, data: Dict) -> Dict:
        return self._send_request('POST', f'update_dataset/{dataset_id}', data)

    def delete_dataset(self, dataset_id: int) -> Dict:
        return self._send_request('POST', f'delete_dataset/{dataset_id}')
