import json

def load_content_from_json(file_path):
    """
    Loads course content from a single JSON file and returns it as a dictionary.

    Args:
        file_path (str): Path to the JSON file.

    Returns:
        dict: Parsed JSON content.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = json.load(f)
        return content
    except FileNotFoundError:
        print(f"❌ Error: {file_path} not found.")
        return {}
    except json.JSONDecodeError:
        print(f"❌ Error: {file_path} contains invalid JSON.")
        return {}

def get_categories(content):
    """
    Returns a list of top-level categories like 'Financial Literacy' or 'Civic Education'.

    Args:
        content (dict): Loaded course content.

    Returns:
        list: List of category names.
    """
    return list(content.keys())

def get_topics(content, category):
    """
    Returns the list of topics under a specific category.

    Args:
        content (dict): Loaded course content.
        category (str): The selected category name.

    Returns:
        list: List of topic names under the category.
    """
    return list(content.get(category, {}).keys())

def get_topic_details(content, category, topic):
    """
    Returns the title, content list, and summary of a given topic.

    Args:
        content (dict): Loaded course content.
        category (str): The selected category name.
        topic (str): The selected topic name.

    Returns:
        dict: Dictionary with title, content, and summary.
    """
    topic_data = content.get(category, {}).get(topic, {})
    return {
        "title": topic_data.get("title", topic),
        "content": topic_data.get("content", []),
        "summary": topic_data.get("summary", "")
    }
