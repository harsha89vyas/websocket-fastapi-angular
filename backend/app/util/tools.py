"""Tool for asking human input."""

from typing import Callable, Optional

from pydantic import Field

from langchain.callbacks.manager import CallbackManagerForToolRun
from langchain.tools.base import BaseTool
import asyncio
def _print_func(text: str) -> None:
    print("\n")
    print(text)


class SessionHumanInputRun(BaseTool):
    """Tool that asks user for input."""

    name = "session_human"
    description = (
        "You can ask a human for guidance when you think you "
        "got stuck or you are not sure what to do next. "
        "The input should be a question for the human."
    )
    prompt_func: Callable[[str], None] = Field(default_factory=lambda: _print_func)
    input_func: Callable = Field(default_factory=lambda: input)
    session: str
    def _run(self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None) -> str:
        raise NotImplementedError("This tool is not meant to be run asynchronously.")
    async def _arun(
        self,
        query: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Use the Human input tool."""
        # loop = asyncio.get_event_loop()
        # coroutine = self.prompt_func(query, self.session)
        # loop.run_until_complete(coroutine)
        # coroutine = self.input_func(self.session)
        # return loop.run_until_complete(coroutine)
        await self.prompt_func(query, self.session)
        return await self.input_func(self.session)
