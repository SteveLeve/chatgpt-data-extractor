import json
import os

def parse_chatgpt_export(json_file_path, output_dir='output'):
    """
    Parses a ChatGPT export JSON file and saves each conversation
    as a separate Markdown file.
    """
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Load the JSON data from the export file
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: {json_file_path} not found.")
        return

    for conversation in data:
        title = conversation.get('title', 'Untitled Conversation')
        # Sanitize the title to use as a valid filename
        filename = "".join(x for x in title if x.isalnum() or x in " -_").strip()
        filename = filename.replace(' ', '_')
        if not filename:
            filename = f"conversation_{conversation.get('id', 'unknown')}"

        # Write the conversation to a new markdown file
        output_path = os.path.join(output_dir, f"{filename}.md")

        with open(output_path, 'w', encoding='utf-8') as outfile:
            # Add title and metadata
            outfile.write(f"# {title}\n\n")

            # Get the 'mapping' key and sort the items for chronological order
            mapping = conversation.get('mapping', {})
            sorted_messages = []
            for node_id, node_data in mapping.items():
                message = node_data.get('message')
                if message:
                    sorted_messages.append(message)

            # Sort messages by create_time
            sorted_messages.sort(key=lambda x: x.get('create_time', 0))

            # Write each message (user and assistant) to the file
            for message in sorted_messages:
                author_role = message.get('author', {}).get('role')
                content_parts = message.get('content', {}).get('parts', [])

                if author_role and content_parts:
                    # Format the content based on the role
                    if author_role == 'user':
                        outfile.write(f"**User:**\n\n")
                    elif author_role == 'assistant':
                        outfile.write(f"**Assistant:**\n\n")

                    for part in content_parts:
                        outfile.write(f"{part}\n\n")

    print(f"Successfully parsed {len(data)} conversations.")
    print(f"Files saved to the '{output_dir}' directory.")

if __name__ == '__main__':
    # Make sure conversations.json is in the same folder
    parse_chatgpt_export('conversations.json')
