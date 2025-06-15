# mcp-kvn MCP server

My personal MCP server.

## Installation

### Published Server

```
"mcp-kvn": {
  "command": "uvx",
  "args": ["--from", "git+https://github.com/kputrajaya/mcp-kvn", "mcp-kvn"]
}
```

### Development Server

```
"mcp-kvn": {
  "command": "uv",
  "args": ["--directory", "[path]\mcp-kvn", "run", "mcp-kvn"]
}
```
