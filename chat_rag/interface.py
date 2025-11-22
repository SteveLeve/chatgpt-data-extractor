from rich.console import Console
from rich.markdown import Markdown
from chat_rag.query import query_async, setup_agent

console = Console()

async def start_repl_async():
    console.print("[bold green]ChatGPT RAG Interface[/bold green]")
    console.print("Type 'exit' or 'quit' to stop.")
    
    # Initialize agent once to maintain conversation history
    with console.status("[bold yellow]Initializing Agent...[/bold yellow]"):
        agent = setup_agent()
        
    # Set custom exception handler to suppress CancelledError noise from LlamaIndex instrumentation
    import asyncio
    loop = asyncio.get_running_loop()
    def handler(loop, context):
        if "exception" in context and isinstance(context["exception"], asyncio.CancelledError):
            return
        loop.default_exception_handler(context)
    loop.set_exception_handler(handler)
    
    while True:
        try:
            user_input = console.input("[bold blue]You:[/bold blue] ")
            if user_input.lower() in ('exit', 'quit'):
                break
            
            with console.status("[bold yellow]Thinking...[/bold yellow]"):
                # Pass the existing agent to preserve state
                response = await query_async(user_input, agent=agent)
            
            console.print("[bold green]Assistant:[/bold green]")
            console.print(Markdown(str(response)))
            console.print("\n")
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {e}")

def start_repl():
    """Legacy sync wrapper if needed, but main.py should use async"""
    import asyncio
    asyncio.run(start_repl_async())
