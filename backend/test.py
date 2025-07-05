from openai import OpenAI

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key="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",
)

prompt = "Potato___Early_blight"
completion = client.chat.completions.create(
  extra_headers={
    "HTTP-Referer": "<YOUR_SITE_URL>", # Optional. Site URL for rankings on openrouter.ai.
    "X-Title": "<YOUR_SITE_NAME>", # Optional. Site title for rankings on openrouter.ai.
  },
  extra_body={},
  model="mistralai/mistral-small-3.2-24b-instruct:free",
  messages=[
            {
              "role": "system",
              "content": "You will be prompted by the diagnosis of a potato disease. Provide a solution for it, unless the diagnosis is that it is healthy", # Our prompt goes here. We don't send an image.
            },
            {
              "role": "user",
              "content": prompt,
            }
          ],
)

print(completion.choices[0].message.content)