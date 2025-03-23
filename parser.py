from langchain.agents.agent import AgentOutputParser
from langchain.schema.agent import AgentAction, AgentFinish
import re
from typing import Union

class SafeAgentOutputParser(AgentOutputParser):
    def parse(self, text: str) -> Union[AgentAction, AgentFinish]:
        # Empêche les réponses qui contiennent à la fois Action et Final Answer
        if "Final Answer:" in text and "Action:" in text:
            # Ignore la Final Answer, ne garder que l'action
            text = re.split(r"Final Answer:", text)[0].strip()

        if "Final Answer:" in text:
            final_answer = text.split("Final Answer:")[-1].strip()
            return AgentFinish(return_values={"output": final_answer}, log=text)

        match = re.search(r"Action: (.*)", text)
        if not match:
            raise ValueError(f"Could not parse agent action: `{text}`")

        action = match.group(1).strip()
        input_match = re.search(r"Action Input:\s*(.*)", text)
        if not input_match:
            raise ValueError(f"Could not parse action input: `{text}`")
        action_input = input_match.group(1).strip()

        return AgentAction(tool=action, tool_input=action_input, log=text)
