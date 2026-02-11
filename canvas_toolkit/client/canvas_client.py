"""Canvas API client for fetching courses and assignments."""

import requests
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from .exceptions import CanvasAPIError, AuthenticationError, RateLimitError


class CanvasClient:
    """Client for interacting with Canvas LMS API."""

    def __init__(self, base_url: str, api_token: str):
        """
        Initialize Canvas API client.

        Args:
            base_url: Canvas instance URL (e.g., "https://babson.instructure.com")
            api_token: Canvas API access token
        """
        self.base_url = base_url.rstrip('/')
        self.api_token = api_token
        self.headers = {"Authorization": f"Bearer {api_token}"}

    def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> List[Dict]:
        """
        Make a GET request to Canvas API with pagination support.

        Args:
            endpoint: API endpoint (e.g., "/api/v1/courses")
            params: Query parameters

        Returns:
            List of results from all pages

        Raises:
            AuthenticationError: If authentication fails
            RateLimitError: If rate limit is exceeded
            CanvasAPIError: For other API errors
        """
        url = f"{self.base_url}{endpoint}"
        params = params or {}
        params.setdefault("per_page", 100)

        all_results = []

        while url:
            try:
                response = requests.get(url, headers=self.headers, params=params)

                # Handle specific error codes
                if response.status_code == 401:
                    raise AuthenticationError(
                        "Invalid Canvas API token. Please check your token and try again."
                    )
                elif response.status_code == 429:
                    raise RateLimitError(
                        "Canvas API rate limit exceeded. Please wait and try again."
                    )
                elif response.status_code == 403:
                    raise CanvasAPIError(
                        "Access forbidden. Check that your API token has the required permissions."
                    )

                response.raise_for_status()
                data = response.json()

                # Handle both list and dict responses
                if isinstance(data, list):
                    all_results.extend(data)
                else:
                    all_results.append(data)

                # Handle pagination via Link header
                url = None
                if 'Link' in response.headers:
                    links = response.headers['Link'].split(',')
                    for link in links:
                        if 'rel="next"' in link:
                            url = link[link.find('<')+1:link.find('>')]
                            params = None  # Params are in the URL now
                            break

            except requests.RequestException as e:
                if isinstance(e, (AuthenticationError, RateLimitError, CanvasAPIError)):
                    raise
                raise CanvasAPIError(f"Canvas API request failed: {str(e)}")

        return all_results

    def test_connection(self) -> bool:
        """
        Test Canvas API connection and token validity.

        Returns:
            True if connection is successful

        Raises:
            AuthenticationError: If token is invalid
            CanvasAPIError: If connection fails
        """
        try:
            self._make_request("/api/v1/users/self")
            return True
        except Exception:
            raise

    def get_courses(self, include_concluded: bool = False) -> List[Dict]:
        """
        Fetch all courses for the authenticated user.

        Args:
            include_concluded: If True, include completed courses

        Returns:
            List of course dictionaries with keys: id, name, course_code, etc.
        """
        params = {}
        if not include_concluded:
            params["enrollment_state"] = "active"

        courses = self._make_request("/api/v1/courses", params)

        # Filter out courses without a name (usually placeholders)
        return [c for c in courses if c.get("name")]

    def get_course_assignments(self, course_id: str) -> List[Dict]:
        """
        Fetch all assignments for a specific course.

        Args:
            course_id: Canvas course ID

        Returns:
            List of assignment dictionaries
        """
        endpoint = f"/api/v1/courses/{course_id}/assignments"
        assignments = self._make_request(endpoint)

        # Add course_id to each assignment for reference
        for assignment in assignments:
            assignment["_course_id"] = course_id

        return assignments

    def get_all_assignments(
        self,
        course_ids: Optional[List[str]] = None,
        include_concluded: bool = False
    ) -> List[Dict]:
        """
        Fetch assignments from all courses or specific courses.

        Args:
            course_ids: Optional list of course IDs to fetch. If None, fetches from all courses.
            include_concluded: If True, include assignments from concluded courses

        Returns:
            List of all assignments with added _course_name field
        """
        # Get courses if not specified
        if course_ids is None:
            courses = self.get_courses(include_concluded=include_concluded)
            course_ids = [str(c["id"]) for c in courses]
            course_names = {str(c["id"]): c["name"] for c in courses}
        else:
            # Fetch course names for the specified IDs
            all_courses = self.get_courses(include_concluded=True)
            course_names = {str(c["id"]): c["name"] for c in all_courses if str(c["id"]) in course_ids}

        all_assignments = []

        for course_id in course_ids:
            try:
                assignments = self.get_course_assignments(course_id)

                # Add course name to each assignment
                course_name = course_names.get(course_id, "Unknown Course")
                for assignment in assignments:
                    assignment["_course_name"] = course_name

                all_assignments.extend(assignments)

            except CanvasAPIError as e:
                # Log error but continue with other courses
                print(f"Warning: Could not fetch assignments from course {course_id}: {e}")
                continue

        return all_assignments

    def get_course_announcements(self, course_id: str, days_back: int = 30) -> List[Dict]:
        """
        Fetch recent announcements for a course. Uses discussion_topics endpoint with only_announcements filter.

        Args:
            course_id: Canvas course ID
            days_back: Number of days back to fetch announcements (default: 30)

        Returns:
            List of announcement dictionaries
        """
        # Calculate start date
        start_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')

        endpoint = f"/api/v1/courses/{course_id}/discussion_topics"
        params = {
            "only_announcements": True,
            "start_date": start_date
        }

        announcements = self._make_request(endpoint, params)

        # Add course_id to each announcement for reference
        for announcement in announcements:
            announcement["_course_id"] = course_id

        return announcements

    def get_all_announcements(
        self,
        course_ids: Optional[List[str]] = None,
        days_back: int = 30
    ) -> List[Dict]:
        """
        Fetch announcements from all courses or specific courses.

        Args:
            course_ids: Optional list of course IDs to fetch. If None, fetches from all courses.
            days_back: Number of days back to fetch announcements (default: 30)

        Returns:
            List of all announcements with added _course_name field
        """
        # Get courses if not specified
        if course_ids is None:
            courses = self.get_courses(include_concluded=False)
            course_ids = [str(c["id"]) for c in courses]
            course_names = {str(c["id"]): c["name"] for c in courses}
        else:
            # Fetch course names for the specified IDs
            all_courses = self.get_courses(include_concluded=True)
            course_names = {str(c["id"]): c["name"] for c in all_courses if str(c["id"]) in course_ids}

        all_announcements = []

        for course_id in course_ids:
            try:
                announcements = self.get_course_announcements(course_id, days_back)

                # Add course name to each announcement
                course_name = course_names.get(course_id, "Unknown Course")
                for announcement in announcements:
                    announcement["_course_name"] = course_name

                all_announcements.extend(announcements)

            except CanvasAPIError as e:
                # Log error but continue with other courses
                print(f"Warning: Could not fetch announcements from course {course_id}: {e}")
                continue

        return all_announcements

    def get_course_modules(self, course_id: str) -> List[Dict]:
        """
        Fetch modules for a course. Uses include[]=items and include[]=content_details to get everything in one call.

        Args:
            course_id: Canvas course ID

        Returns:
            List of module dictionaries
        """
        endpoint = f"/api/v1/courses/{course_id}/modules"
        params = {
            "include[]": ["items", "content_details"]
        }

        modules = self._make_request(endpoint, params)

        # Add course_id to each module for reference
        for module in modules:
            module["_course_id"] = course_id

        return modules

    def get_all_modules(
        self,
        course_ids: Optional[List[str]] = None
    ) -> List[Dict]:
        """
        Fetch modules from all courses or specific courses.

        Args:
            course_ids: Optional list of course IDs to fetch. If None, fetches from all courses.

        Returns:
            List of all modules with added _course_name field
        """
        # Get courses if not specified
        if course_ids is None:
            courses = self.get_courses(include_concluded=False)
            course_ids = [str(c["id"]) for c in courses]
            course_names = {str(c["id"]): c["name"] for c in courses}
        else:
            # Fetch course names for the specified IDs
            all_courses = self.get_courses(include_concluded=True)
            course_names = {str(c["id"]): c["name"] for c in all_courses if str(c["id"]) in course_ids}

        all_modules = []

        for course_id in course_ids:
            try:
                modules = self.get_course_modules(course_id)

                # Add course name to each module
                course_name = course_names.get(course_id, "Unknown Course")
                for module in modules:
                    module["_course_name"] = course_name

                all_modules.extend(modules)

            except CanvasAPIError as e:
                # Log error but continue with other courses
                print(f"Warning: Could not fetch modules from course {course_id}: {e}")
                continue

        return all_modules
