import os
import openai

openai.api_key = os.getenv("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")

response = openai.Completion.create(
  model="code-davinci-002",
  prompt="##### Fix bugs in the below function\n \n### Buggy Python\nimport Random\na = random.randint(1,12)\nb = random.randint(1,12)\nfor i in range(10):\n    question = \"What is \"+a+\" x \"+b+\"? \"\n    answer = input(question)\n    if answer = a*b\n        print (Well done!)\n    else:\n        print(\"No.\")\n    \n### Fixed Python",
  temperature=0,
  max_tokens=182,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0,
  stop=["###"]
)