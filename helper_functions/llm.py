import json
from helper_functions import constants
from openai import AzureOpenAI

client = AzureOpenAI(
    azure_endpoint=constants.AZUREOPENAI_ENDPOINT,
    api_key=constants.AZUREOPENAI_API_KEY,
    api_version=constants.AZUREOPENAI_API_VERION,
)  

def get_embedding(input): # len 1
    response = client.embeddings.create(
        input=input,
        model=constants.EMBEDDING_MODEL,
    )
    return [x.embedding for x in response.data]

def get_completion(
        prompt, 
        temperature=0, 
        top_p=1.0, 
        max_tokens=1024, 
        n=1, 
        json_output=False
    ):
    if json_output == True:
        output_json_structure = {"type": "json_object"}
    else:
        output_json_structure = None

    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create( #originally was openai.chat.completions
        model=constants.AZUREOPENAI_MODEL,
        messages=messages,
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens,
        n=1,
        response_format=output_json_structure,
    )
    return response.choices[0].message.content

# Note that this function directly take in "messages" as the parameter.
def get_completion_by_messages(messages, temperature=0, top_p=1.0, max_tokens=1024, n=1):
    response = client.chat.completions.create(
        model=constants.AZUREOPENAI_MODEL,
        messages=messages,
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens,
        n=1
    )
    return response.choices[0].message.content


# def llm_text(
#         self, 
#         system_prompt: str,
#         user_content: str,
#         response_format: dict = {"type": "json_object"},
#         temperature: float = 0,
#         top_p: float = 0.95,
#         frequency_penalty: float = 0,
#         presence_penalty: float = 0,
#         stop=None
#     ):  
#     response = self.client.chat.completions.create(
#       model=constants.AZUREOPENAI_MODEL,
#       messages=[
#           {"role": "system", "content": system_prompt},
#           {"role": "user", "content": user_content},
#       ],
#       response_format=response_format,
#       temperature=temperature,
#       top_p=top_p,
#       frequency_penalty=frequency_penalty,
#       presence_penalty=presence_penalty,
#       stop=stop

#     )
    
#     return response.choices[0].message.content

def post_process_llm_response(self, processing_prompt: str, response_content: str):
    
    try:
    #   response_content = self.llm_text(
    #         system_prompt=processing_prompt,
    #         user_content=response_content
    #     )
        cleaned_response = json.loads(response_content)
        return cleaned_response
    except json.JSONDecodeError:
        cleaned = re.sub(r"^```(?:json)?\n|```$", "", response_content.strip(), flags=re.MULTILINE)
        cleaned_response = json.loads(cleaned)
        return cleaned_response

    
# -------
# -------

# def get_embedding(input, model='text-embedding-ada-002'): # len 1
#     response = client.embeddings.create(
#         input=input,
#         model=model
#     )
#     return [x.embedding for x in response.data]

# def get_embedding(input, model='text-embedding-ada-002'): # len 1536
#     """Function to generate embeddings for text using the provided model."""
#     response = client.embeddings.create(
#         input=input,
#         model=model
#     )
#     return response.data[0].embedding




