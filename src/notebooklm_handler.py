"""NotebookLM integration module using notebooklm-mcp-cli."""

import os
import subprocess
import logging
import time
import json
from typing import Optional, Tuple

logger = logging.getLogger(__name__)


class NotebookLMHandler:
    """Handle NotebookLM operations via CLI."""
    
    def __init__(self, notebook_id: str):
        """
        Initialize NotebookLM handler.
        
        Args:
            notebook_id: NotebookLM notebook ID
        """
        self.notebook_id = notebook_id
        self.max_retries = 3
        self.retry_delay = 5  # seconds
    
    def _run_command(self, command: list) -> Tuple[bool, str]:
        """
        Run a CLI command with retry logic.
        
        Args:
            command: Command list to execute
            
        Returns:
            Tuple of (success: bool, output: str)
        """
        for attempt in range(self.max_retries):
            try:
                logger.debug(f"Running command (attempt {attempt + 1}/{self.max_retries}): {' '.join(command)}")
                
                result = subprocess.run(
                    command,
                    capture_output=True,
                    text=True,
                    encoding='utf-8',
                    errors='replace',  # Replace problematic characters instead of crashing
                    timeout=120,  # 2 minute timeout
                    env={**os.environ, "PYTHONIOENCODING": "utf-8"}
                )
                
                if result.returncode == 0:
                    logger.debug("Command succeeded")
                    return True, result.stdout.strip() if result.stdout else ""
                else:
                    logger.warning(f"Command failed with return code {result.returncode}: {result.stderr}")
                    
                    # Check if it's an authentication error
                    if "authentication" in result.stderr.lower() or "login" in result.stderr.lower():
                        logger.info("Authentication error detected, attempting to re-authenticate")
                        if self._authenticate():
                            # Retry the command after successful authentication
                            continue
                    
                    if attempt < self.max_retries - 1:
                        time.sleep(self.retry_delay * (attempt + 1))
                        continue
                    
                    return False, result.stderr.strip()
                    
            except subprocess.TimeoutExpired:
                logger.error("Command timed out")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay * (attempt + 1))
                    continue
                return False, "Command timed out"
                
            except Exception as e:
                logger.error(f"Error running command: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay * (attempt + 1))
                    continue
                return False, str(e)
        
        return False, "Max retries exceeded"
    
    def _authenticate(self) -> bool:
        """
        Authenticate with NotebookLM CLI.
        
        Returns:
            True if authentication successful, False otherwise
        """
        logger.info("Attempting to authenticate with NotebookLM CLI")
        logger.info("NOTE: If authentication window doesn't open, run 'nlm login' manually in a separate terminal")
        
        try:
            # First check if already authenticated
            check_cmd = ["nlm", "login", "--check"]
            result = subprocess.run(
                check_cmd, 
                capture_output=True, 
                text=True,
                encoding='utf-8',
                errors='replace',
                timeout=30,
                env={**os.environ, "PYTHONIOENCODING": "utf-8"}
            )
            
            output_lower = result.stdout.lower() if result.stdout else ""
            if result.returncode == 0 and ("authenticated" in output_lower or "valid" in output_lower):
                logger.info("Already authenticated")
                return True
            
            # Need to authenticate - run login with output redirected to avoid Unicode errors
            logger.warning("Not authenticated. Authentication window should open...")
            logger.warning("If this fails, please run 'nlm login' in a separate PowerShell window")
            
            login_cmd = ["nlm", "login"]
            
            # Run with UTF-8 environment and capture output to avoid console encoding issues
            result = subprocess.run(
                login_cmd,
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace',
                timeout=120,
                env={**os.environ, "PYTHONIOENCODING": "utf-8"}
            )
            
            # Check result - if return code is 0, assume success even if output had encoding issues
            if result.returncode == 0:
                logger.info("Authentication command completed")
                # Verify authentication worked
                time.sleep(2)
                verify_result = subprocess.run(
                    check_cmd,
                    capture_output=True,
                    text=True,
                    encoding='utf-8',
                    errors='replace',
                    timeout=30,
                    env={**os.environ, "PYTHONIOENCODING": "utf-8"}
                )
                verify_output = verify_result.stdout.lower() if verify_result.stdout else ""
                if verify_result.returncode == 0 and ("authenticated" in verify_output or "valid" in verify_output):
                    logger.info("Authentication verified successfully")
                    return True
                else:
                    logger.error("Authentication command ran but verification failed")
                    return False
            else:
                logger.error(f"Authentication failed: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            logger.error("Authentication timed out - user may not have completed login")
            return False
        except Exception as e:
            logger.error(f"Error during authentication: {e}")
            return False
    
    def ensure_authenticated(self) -> bool:
        """
        Ensure NotebookLM CLI is authenticated.
        
        Returns:
            True if authenticated, False otherwise
        """
        try:
            check_cmd = ["nlm", "login", "--check"]
            result = subprocess.run(
                check_cmd,
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace',
                timeout=30,
                env={**os.environ, "PYTHONIOENCODING": "utf-8"}
            )
            
            # Check for authentication status (can be "authenticated" or "valid")
            output_lower = result.stdout.lower() if result.stdout else ""
            if result.returncode == 0 and ("authenticated" in output_lower or "valid" in output_lower):
                logger.info("NotebookLM CLI is authenticated")
                return True
            else:
                logger.warning("NotebookLM CLI is not authenticated")
                return self._authenticate()
                
        except Exception as e:
            logger.error(f"Error checking authentication: {e}")
            return False
    
    def add_source(self, video_url: str) -> bool:
        """
        Add a video URL as a source to the notebook.
        
        Args:
            video_url: YouTube video URL
            
        Returns:
            True if successful, False otherwise
        """
        logger.info(f"Adding video source: {video_url}")
        
        # Ensure authenticated
        if not self.ensure_authenticated():
            logger.error("Cannot add source: not authenticated")
            return False
        
        command = ["nlm", "source", "add", self.notebook_id, "--url", video_url]
        success, output = self._run_command(command)
        
        if success:
            logger.info(f"Successfully added video source: {video_url}")
            return True
        else:
            logger.error(f"Failed to add video source: {output}")
            return False
    
    def query_notebook(self, prompt: str) -> Optional[str]:
        """
        Query the notebook with a prompt.
        
        Args:
            prompt: Query prompt
            
        Returns:
            Response text or None if failed
        """
        logger.info(f"Querying notebook with prompt: {prompt[:50]}...")
        
        # Ensure authenticated
        if not self.ensure_authenticated():
            logger.error("Cannot query notebook: not authenticated")
            return None
        
        command = ["nlm", "notebook", "query", self.notebook_id, prompt]
        success, output = self._run_command(command)
        
        if success:
            logger.info("Successfully queried notebook")
            
            # Parse JSON response from NotebookLM CLI
            try:
                response_data = json.loads(output)
                # Extract the answer from the JSON structure
                if isinstance(response_data, dict) and "value" in response_data:
                    answer = response_data["value"].get("answer", "")
                    logger.info(f"Extracted answer ({len(answer)} characters)")
                    return answer
                else:
                    # If not in expected format, return raw output
                    logger.warning("Response not in expected JSON format, returning raw output")
                    return output
            except json.JSONDecodeError as e:
                logger.warning(f"Could not parse JSON response: {e}")
                logger.warning("Returning raw output")
                return output
        else:
            logger.error(f"Failed to query notebook: {output}")
            return None
    
    def process_video(self, video_url: str, prompt: str) -> Optional[str]:
        """
        Process a video: add as source and query with prompt.
        
        Args:
            video_url: YouTube video URL
            prompt: Query prompt
            
        Returns:
            Response text or None if failed
        """
        logger.info(f"Processing video: {video_url}")
        
        # Add video as source
        if not self.add_source(video_url):
            logger.error("Failed to add video source, cannot continue")
            return None
        
        # Wait a bit for the source to be processed
        logger.info("Waiting for source to be processed...")
        time.sleep(10)
        
        # Query the notebook
        response = self.query_notebook(prompt)
        
        if response:
            logger.info("Successfully processed video")
            return response
        else:
            logger.error("Failed to process video")
            return None
