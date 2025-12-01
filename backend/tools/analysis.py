import sys
import io
import contextlib

def execute_python_code(code: str) -> str:
    """
    Executes Python code and returns the output.
    Useful for data analysis, calculations, or plotting.
    
    Args:
        code: The Python code to execute.
        
    Returns:
        The stdout captured from the execution.
    """
    # Security Warning: In a real production app, use a sandboxed environment (e.g. Docker, Vertex AI Code Interpreter).
    # This is a simplified version for the capstone demo.
    
    output_buffer = io.StringIO()
    
    try:
        with contextlib.redirect_stdout(output_buffer):
            exec(code, {"__builtins__": __builtins__}, {})
        return output_buffer.getvalue()
    except Exception as e:
        return f"Error executing code: {e}"
