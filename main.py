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
    ingest_parser.add_argument('--limit', type=int, default=None, help='Limit number of conversations to process')
    ingest_parser.add_argument('--batch-size', type=int, default=10, help='Batch size for ingestion')
    
    # Chat Command
    chat_parser = subparsers.add_parser('chat', help='Start the chat REPL')

    # Serve Command
    serve_parser = subparsers.add_parser('serve', help='Start the web server')
    
    args = parser.parse_args()
    
    if args.command == 'ingest':
        input_path = Path(args.input)
        if not input_path.exists():
            print(f"Error: Input directory '{input_path}' does not exist.")
            sys.exit(1)
        ingest_data(input_path, limit=args.limit, batch_size=args.batch_size)
        
    elif args.command == 'chat':
        import asyncio
        from chat_rag.interface import start_repl_async
        try:
            asyncio.run(start_repl_async())
        except KeyboardInterrupt:
            print("\nGoodbye!")

    elif args.command == 'serve':
        import uvicorn
        uvicorn.run("web.app:app", host="0.0.0.0", port=8000, reload=True)
        
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
