from rich.console import Console
from rich.markdown import Markdown
from chat_rag.query import query

console = Console()

def start_repl():
    console.print("[bold green]ChatGPT RAG Interface[/bold green]")
    console.print("Type 'exit' or 'quit' to stop.")
    
    while True:
        try:
            user_input = console.input("[bold blue]You:[/bold blue] ")
            if user_input.lower() in ('exit', 'quit'):
                break
            
            with console.status("[bold yellow]Thinking...[/bold yellow]"):
                response = query(user_input)
            
            console.print("[bold green]Assistant:[/bold green]")
            console.print(Markdown(str(response)))
            console.print("\n")
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {e}")
