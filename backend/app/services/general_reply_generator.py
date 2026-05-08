import os

from openai import OpenAI

client = OpenAI(

    api_key=os.getenv("OPEN_ROUTER_API_KEY"),

    base_url="https://openrouter.ai/api/v1",

)

def generate_general_email_reply(masked_body: str) -> str:

    response = client.chat.completions.create(

        model="openai/gpt-4o-mini",

        messages=[

            {

                "role": "system",

                "content": """

You are replying on behalf of a Swiss restaurant.

Important restaurant information:
- The restaurant is open from Wednesday to Sunday.
- Opening hours are from 09:30 to 22:00.
- The restaurant is closed on Monday and Tuesday.

Write the reply in polite German.
Use a warm but professional Swiss restaurant tone.
Keep the answer short and clear.
Do not invent information.
If the question cannot be answered from the provided information, say that the team will clarify it.


                """,

            },

            {

                "role": "user",

                "content": masked_body,

            },

        ],

        temperature=0.3,

    )

    return response.choices[0].message.content





