from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
import mcp.server.stdio
import toml

from mcp_kvn.tools import summarize_bg

server = Server('mcp-kvn')


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    '''
    List available tools.
    Each tool specifies its arguments using JSON Schema validation.
    '''
    return [
        types.Tool(
            name='summarize-bg',
            description='Summarize a board game rulebook PDF from local file or URL',
            inputSchema={
                'type': 'object',
                'properties': {
                    'file': {'type': 'string'},
                },
                'required': ['file'],
            },
        )
    ]


@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    '''
    Handle tool execution requests.
    Tools can modify server state and notify clients of changes.
    '''
    match name:
        case 'summarize-bg':
            if not arguments:
                raise ValueError('Missing arguments')
            file = arguments.get('file')
            if not file:
                raise ValueError('Missing file')

            result = await summarize_bg(file)
            return [types.TextContent(type='text', text=result)]
        case _:
            raise ValueError(f'Unknown tool: {name}')


async def main():
    # Run the server using stdin/stdout streams
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        with open('pyproject.toml', 'r') as f:
            project = toml.load(f)['project']
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name=project['name'],
                server_version=project['version'],
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )
