import argparse
import sys
from pathlib import Path
from chat_rag.ingest import ingest_data
from chat_rag.interface import start_repl

def main():
    parser = argparse.ArgumentParser(description="ChatGPT Data Extractor & RAG")
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Ingest Command
    ingest_parser = subparsers.add_parser('ingest', help='Ingest data into the RAG pipeline')
    ingest_parser.add_argument('--input', default='source-data', help='Path to source data')
    
    # Chat Command
    chat_parser = subparsers.add_parser('chat', help='Start the chat REPL')
    
    args = parser.parse_args()
    
    if args.command == 'ingest':
        input_path = Path(args.input)
        if not input_path.exists():
            print(f"Error: Input directory '{input_path}' does not exist.")
            sys.exit(1)
        ingest_data(input_path)
        
    elif args.command == 'chat':
        start_repl()
        
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
