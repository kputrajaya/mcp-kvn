import io
from typing import Annotated

from fastmcp import FastMCP
from pydantic import Field
from pypdf import PdfReader
import requests


server = FastMCP('mcp-kvn')


@server.tool()
async def summarize_bg(
    file: Annotated[str, Field(description="URL or path of the PDF rulebook")]
) -> str:
    """Summarize board game rules from a rulebook"""

    reader = None
    if file.startswith('http://') or file.startswith('https://'):
        response = requests.get(file)
        response.raise_for_status()
        pdf_object = io.BytesIO(response.content)
        reader = PdfReader(pdf_object)
    else:
        reader = PdfReader(file)

    text_content = ''
    for page in reader.pages:
        text_content += page.extract_text() + '\n'

    prompt = (
        f'''
        Summarize this board game rules (below triple backticks) into 2 main sections: "Setup" and "Guide".
        Use simple short sentences and be very concise. Group similar items into one. Return the summary as bullet
        points in this chat.

        1. "Setup" is how we should set up the table to play this game: what components to prepare on/aside the main
        area, what should each player get, etc. Do not state the obvious like "set up the board" or
        "prepare resource bank", but rather focus on unique to-do items.

        2. "Guide" is a step by step guide to play the game. Start with the objective of the game and how to win.
        Then, go to game structure and player actions. It's also important to explain when and how the game ends,
        including how to determine the winner.

        ```

        {text_content}
        '''
    )
    return prompt


def main():
    server.run()


if __name__ == '__main__':
    main()
