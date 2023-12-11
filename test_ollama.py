from ollama_connection import OllamaConnection

def main():
    # Sample commit data
    commit = {
        'author': {'name': 'TestAuthor'},
        'message': 'Sample commit message for testing'
    }

    # Simulated config section
    config_section = {
        'system_message': "Your system message here",
        'user_message': "Commit by {author_name}: {commit_message}"
    }

    # Initialize the OllamaConnection
    ollama_connection = OllamaConnection(config_section)

    # Generate a comment
    comment = ollama_connection.generate_comment(commit)
    
    # Print the generated comment
    print("Generated Comment:\n", comment)

if __name__ == "__main__":
    main()
