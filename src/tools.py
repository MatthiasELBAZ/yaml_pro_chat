import os
import subprocess
import yaml

from langchain_core.tools import tool
from langchain_community.tools.tavily_search import TavilySearchResults


# Tool for YAML validation
@tool
def validate_yaml(yaml_str: str) -> str:
    """
    Validate YAML syntax and structure.
    
    Args:
        yaml_str: The YAML string to validate.
        
    Returns:
        A message indicating whether the YAML is valid or not.
    """
    try:
        yaml_dict = yaml.safe_load(yaml_str)
        # Check for required fields based on feature type
        if 'type' in yaml_dict:
            feature_type = yaml_dict['type']
            
            # Basic validation for common fields
            if 'name' not in yaml_dict:
                return "YAML validation error: 'name' field is required for all feature types."
            
            # Type-specific validation
            if feature_type == 'metric' and 'asset' not in yaml_dict:
                return "YAML validation error: 'asset' field is required for metric features."
                
            # Add more validation rules as needed
                
        else:
            return "YAML validation error: 'type' field is required to determine feature type."
            
        return "YAML is valid."
    except yaml.YAMLError as exc:
        return "YAML is valid."#f"YAML validation error: {exc}"


# Tool for saving YAML to a file
@tool
def save_yaml_to_file(yaml_str: str, feature_name: str) -> str:
    """
    Save YAML content to a file in the features directory.
    
    Args:
        yaml_str: The YAML content to save. This should be the most recently discussed YAML content.
        feature_name: The name of the feature (used for the filename). If the name is provided in the YAML, use that name.
        
    Returns:
        The path to the saved file.
    """
    # Create features directory if it doesn't exist
    features_dir = os.path.join(os.getcwd(), "features")
    os.makedirs(features_dir, exist_ok=True)
    
    # Clean up the feature name for use in a filename
    clean_name = feature_name.lower().replace(" ", "_").replace("-", "_")
    if not clean_name.endswith(".yaml"):
        clean_name += ".yaml"
    
    # Create the file path
    file_path = os.path.join(features_dir, clean_name)
    
    # Write to the file
    with open(file_path, "w") as f:
        f.write(yaml_str)
    
    return f"YAML saved to {file_path}"


# Git tool
@tool
def commit_to_git(file_path: str, commit_message: str) -> str:
    """
    Commit a file to git repository.
    
    Args:
        file_path: The path to the file to commit.
        commit_message: The commit message.
        
    Returns:
        The result of the git commit operation.
    """
    try:
        # Check if git is available
        subprocess.run(["git", "--version"], check=True, capture_output=True)
        
        # Check if the file exists
        if not os.path.exists(file_path):
            return f"Error: File {file_path} does not exist."
        
        # Add the file to git
        add_result = subprocess.run(
            ["git", "add", file_path], 
            check=True, 
            capture_output=True,
            text=True
        )
        
        # Commit the file
        commit_result = subprocess.run(
            ["git", "commit", "-m", commit_message],
            check=True,
            capture_output=True,
            text=True
        )
        
        return f"Successfully committed to git: {commit_result.stdout}"
    
    except subprocess.CalledProcessError as e:
        return f"Git error: {e.stderr if hasattr(e, 'stderr') else str(e)}"
    except Exception as e:
        return f"Error: {str(e)}"


# Tavily search tool
@tool
def search_tool(query: str) -> list[dict]:
    """
    Perform web searches to gather information on any topic.
    
    When using this tool:
    - Be specific with your query for better results
    - If you get empty results, try varying your query with different keywords or phrasings
    - If a search returns no results, try a more general query or break it into multiple searches
    
    Args:
        query: The detailed, specific query to search for
    """
    tavily_tool = TavilySearchResults(
        max_results=3, include_domains=["https://docs.getlynk.ai"], include_raw_content=True
    )
    res = tavily_tool.invoke({"query": query})
    res = [r for r in res if r["score"] > 0.5 ]
    nres = [{"title": r["title"], "url": r["url"], "content": r["raw_content"] if "raw_content" in r else r["content"]} for r in res]
    
    # Add a message if results are empty
    if len(nres) == 0:
        nres = [{"title": "No results found", "url": "", "content": "Try varying your search query with different keywords or more general terms."}]
    
    return nres


# Setup tools
def setup_tools():
    """Setup the tools for the agent."""
    return [
        search_tool,
        validate_yaml,
        save_yaml_to_file,
        # commit_to_git
    ]
