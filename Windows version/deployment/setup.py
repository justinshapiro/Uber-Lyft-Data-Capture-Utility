from cx_Freeze import setup, Executable

setup(name="query_agent",
      version="1.0",
      description="Uber-Lyft Query Framework",
      executables=[Executable("query_agent.py")])