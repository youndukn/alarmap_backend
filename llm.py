import requests
import openai
import prompts

HOST = 'localhost:5000'
URI = f'http://{HOST}/api/v1/generate'

OPENAI_KEY = "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"

# LLM function
def generate_text(prompt):
    request = {
        'prompt': prompt,
        'max_new_tokens': 250,
        'auto_max_new_tokens': False,

        # Generation params. If 'preset' is set to different than 'None', the values
        # in presets/preset-name.yaml are used instead of the individual numbers.
        'preset': 'None',
        'do_sample': True,
        'temperature': 0.3,
        'top_p': 0.1,
        'typical_p': 1,
        'epsilon_cutoff': 0,  # In units of 1e-4
        'eta_cutoff': 0,  # In units of 1e-4
        'tfs': 1,
        'top_a': 0,
        'repetition_penalty': 1.00,
        'repetition_penalty_range': 0,
        'top_k': 40,
        'min_length': 0,
        'no_repeat_ngram_size': 0,
        'num_beams': 1,
        'penalty_alpha': 0,
        'length_penalty': 1,
        'early_stopping': False,
        'mirostat_mode': 0,
        'mirostat_tau': 5,
        'mirostat_eta': 0.1,
        'guidance_scale': 1,
        'negative_prompt': '',

        'seed': -1,
        'add_bos_token': True,
        'truncation_length': 2048,
        'ban_eos_token': False,
        'skip_special_tokens': True,
        'stopping_strings': []
    }

    response = requests.post(URI, json=request)

    if response.status_code == 200:
        return response.json()['results'][0]['text']
    else:
        return None  # Handle error appropriately


openai.api_key = OPENAI_KEY

def chatgpt_generate_text(title, time):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
            "role": "system",
            "content": prompts.openai_system_prompt
            },
            {
            "role": "user",
            "content": prompts.openai_user_prompt.format(title, time)
            }
        ],
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    # Check if response object has the expected properties
    if 'choices' in response:
        return response.choices[0].message.content
    else:
        return ""