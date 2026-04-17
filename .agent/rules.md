# Agent Rules & Instructions

You are equipped with the `jcodemunch` MCP server. Whenever you need to discover, search, or understand this project, you MUST use the `jcodemunch` tools as your primary method for codebase exploration.

## Project Discovery & Search Workflow (jcodemunch)

1. **Initial Indexing**: Before performing extensive searches, ensure the workspace is indexed by using `mcp_jcodemunch_index_folder` pointing to the project root directory.
2. **High-Level Overview**: Use `mcp_jcodemunch_get_repo_outline` and `mcp_jcodemunch_get_file_tree` to fetch the architectural layout of the codebase without reading every file.
3. **Semantic Symbol Search**: Use `mcp_jcodemunch_search_symbols` to find specific classes, methods, and functions instead of standard textual `grep`.
4. **Deep-Dive into Files**: When inspecting a specific file, use `mcp_jcodemunch_get_file_outline` to get a structured summary of its contents (symbols, signatures, and docstrings).
5. **Retrieving Code**: Use `mcp_jcodemunch_get_symbol` to fetch exact semantic blocks or `mcp_jcodemunch_get_file_content` for complete files.
6. **Fallback Search**: Use `mcp_jcodemunch_search_text` if you need to find specific strings, comments, or configurations that are not tied to a symbol.

_Favor semantic understanding through `jcodemunch` for code structure, but freely use traditional tools (like `grep` or `find`) when searching for exact string literals, error messages, or navigating non-code configuration files._
