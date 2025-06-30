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


@server.tool()
async def generate_feedback(
    name: Annotated[str, Field(description="The name the given person")],
    description: Annotated[str, Field(description="Key observations for the given person")]
) -> str:
    """Generate 360 feedback summary for peers or self"""

    prompt = (
        f'''
        Help me write a 360 peer feedback for "{name}". I'll give you some of my key observations of this person below
        triple backticks. You'll need to classify and expand the descriptions into two main categories: Strengths and
        Growth Areas.

        Use second-person view sentences (e.g., "You are a competent person"). Keep things concise but descriptive.
        Include provided examples but keep them brief. The tone should be positive but motivating. The feedback
        should be formed in bullet points (2-3 items each).

        You can optionally highlight qualities that are related to user-centricity, empathy, hunger, growth
        mindset, integrity, truthfulness, humility, servant leadership as it aligns with company values.

        ```

        {description}
        '''
    )
    return prompt


def main():
    server.run()


if __name__ == '__main__':
    main()
