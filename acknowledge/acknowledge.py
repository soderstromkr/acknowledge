#functions 
from .completions import *
from .secret_key import API_key
#packages
import re
import time
import ast 
from tqdm import tqdm
import os
import openai 
import json
import pickle

#loads api key from secret_key.py
openai.api_key = API_key

# for few shot learning method
def few_shot(df,column, checkpoint_name, model=["text-davinci-003","gpt-3.5-turbo","ada","gpt-4"], delay=0):
    """ 
    Uses OpenAI's LLMs to extract structured data from text, based on the few-shot learning completions provided by the 
    completions file. 
    df: pandas dataframe for data
    column: column name to extract information from.
    checkpoint_name: name for checkpoint file, useful if doing several runs and want to compare them.
    model: the model to run, has to be one of "text-davinci-003","gpt-3.5-turbo","ada","gpt-4".
    delay: optional value to wait between runs, optional. Useful if servers are loaded. 
    """
    
    max_tokens = 500 #The maximum number of tokens to generate in the completion.
    stop = '\n\n[Output]:' #Up to 4 sequences where the API will stop generating further tokens. The returned text will not contain the stop sequence.
    temperature = 0 #What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic.
    
    print('Using {} with the following parameters:\nmax_tokens={}\nstop={}\ntemperature={}'.format(
        model,max_tokens,stop,temperature)
         )
       
    end = df[column].index.max()+1
    
    words = str(df['Funding Text'].to_list())
    word_count = len(re.findall(r'\w+', words))
    
    print('Dataset has {} rows and {} words'.format(end, word_count))
    del words, word_count
    
    if os.path.exists('checkpoints/{}_{}_fsl.pickle'.format(checkpoint_name, model)):
        print('Resuming from checkpoint')
        with open('checkpoints/{}_{}_fsl.pickle'.format(checkpoint_name, model), 'rb') as f:
            infra_list = pickle.load(f)
    else:
        infra_list=[]
    print('Saving to {}_{}_fsl.pickle'.format(checkpoint_name, model))
    start = len(infra_list)
    error_list=[]
    error_index_list=[]

    for i in (pbar := tqdm(range(start,end), position=0, leave=True)):
        pbar.set_description('Processing {}'.format(i))
        time.sleep(delay)
        body = df[column].iloc[i]
        
        #FLS variable mapping
        prompt='\n\n\n[Keys]:{}\n\n\n[Text1]:{}\n\n[Output1]:{}\n\n[Text2]:{}\n\n[Output2]:{}\n\n[Text3]:{}\n\n[Output3]:{}\n\n[Text4]:{}\n\n[Output4]:'.format(
                        keys, #keys
                        prompt_1,#trainx_1
                        json.dumps(completion_1),#trainy_1
                        prompt_2, #trainx_2 
                        json.dumps(completion_2), #trainy_2
                        prompt_3, #trainx_3 
                        json.dumps(completion_3), #trainy_3
                        body#testx_i
            )
        
        if model == "text-davinci-003":
            response = openai.Completion.create(
                model=model,
                prompt=prompt,
                temperature=temperature,
                stop=stop,
                max_tokens=max_tokens,
                )
            text = ast.literal_eval(response.choices[0]['text'])
            
        elif model == 'ada': #not recommended, bad results
            response = openai.Completion.create(
                model=model,
                prompt=prompt,
                temperature=temperature,
                stop=stop,
                max_tokens=max_tokens,
                )
            text = ast.literal_eval(response.choices[0]['text'])

        elif model == 'gpt-4':#limited beta
            completion = openai.ChatCompletion.create(
                model=model,
                messages=[
              {"role": "user", "content": "{}".format(prompt)}
              ],
                temperature=temperature,
                stop=stop,
                max_tokens=max_tokens
                )
            text = ast.literal_eval(completion.choices[0].message["content"])
            
        elif model == 'gpt-3.5-turbo':
            completion = openai.ChatCompletion.create(
                model=model,
                messages=[
              {"role": "user", "content": "{}".format(prompt)}
              ],
                temperature=temperature,
                stop=stop,
                max_tokens=max_tokens

    )
            try:
                text = ast.literal_eval(completion.choices[0].message["content"])
            except SyntaxError: # One run I got syntax errors when the model couldn't put the data in the right format, has not happened again.
                print('Found errors, check errors folder for missing data') 
                text = ast.literal_eval(json.dumps(error_completion))
                error_list.append(str(completion.choices[0].message["content"]))
                error_index_list.append(i)
        
        else: 
            return('Error: Select one of the following models: {}'.format(["text-davinci-003","gpt-3.5-turbo","ada", "gpt-4"]))
                       

        infra_list.append(text)

        with open('checkpoints/{}_{}_fsl.pickle'.format(checkpoint_name, model), 'wb') as f:
            pickle.dump(infra_list, f)

        with open('errors/error_list.pickle', 'wb') as g:
            pickle.dump(error_list, g)

    return 'Finished!'

# For instructions method
def instruction(df,column, checkpoint_name, model=["text-davinci-003","gpt-3.5-turbo","ada","gpt-4"], delay=0):
    """ 
    Uses OpenAI's LLMs to extract structured data from text, based on the instructions provided by the
    completions file.
    df: pandas dataframe for data
    column: column name to extract information from.
    checkpoint_name: name for checkpoint file, useful if doing several runs and want to compare them.
    model: the model to run, has to be one of "text-davinci-003","gpt-3.5-turbo","ada","gpt-4".
    delay: optional value to wait between runs, optional. Useful if servers are loaded. 
    """
    
    model = model
    stop = None
    temperature = 0 
    max_tokens=500
  
    print('Using {} with the following parameters:\nmax_tokens={}\nstop= {}\ntemperature={}'.format(
        model,max_tokens,stop,temperature)
         )
        
   
    end = df[column].index.max()+1
    
    words = str(df['Funding Text'].to_list())
    word_count = len(re.findall(r'\w+', words))
    
    print('Dataset has {} rows and {} words'.format(end, word_count))
    del words, word_count
    
    if os.path.exists('checkpoints/{}_{}instruction.pickle'.format(checkpoint_name, model)):
        print('Resuming from checkpoint')
        with open('checkpoints/{}_{}instruction.pickle'.format(checkpoint_name, model), 'rb') as f:
            infra_list = pickle.load(f)
    else:
        infra_list=[]
    print('Saving to {}_{}instruction.pickle'.format(checkpoint_name, model))
    start = len(infra_list)

    for i in (pbar := tqdm(range(start,end), position=0, leave=True)):
        pbar.set_description('Processing {}'.format(i))
        time.sleep(delay)
        body = df[column].iloc[i]        
        
        
        if model == "text-davinci-003":
            response = openai.Completion.create(
                model=model,
                prompt=instructions+body,
                temperature=temperature,
                stop=stop,
                max_tokens=max_tokens,
                )
            text = ast.literal_eval(response.choices[0]['text'])
            
        elif model == 'ada': #not recommended, bad results
            response = openai.Completion.create(
                model=model,
                prompt=instructions+body,
                temperature=temperature,
                stop=stop,
                max_tokens=max_tokens,
                )
            text = ast.literal_eval(response.choices[0]['text'])
            
        elif model == 'gpt-3.5-turbo':
            completion = openai.ChatCompletion.create( 
                model=model,
                messages=[
                    {"role": "user", "content": "{}".format(instructions+body)}
                    ],
                temperature=temperature,
                max_tokens=max_tokens,
                stop=stop,
                )

            text = ast.literal_eval(completion.choices[0].message["content"])
        
        elif model == 'gpt-4':#limted beta
            completion = openai.ChatCompletion.create( 
                model=model,
                messages=[
                    {"role": "user", "content": "{}".format(instructions+body)}
                    ],
                temperature=temperature,
                max_tokens=max_tokens,
                stop=stop,
                )

            text = ast.literal_eval(completion.choices[0].message["content"])
        
        else: 
            return('Error: Select one of the following models: {}'.format(["text-davinci-003","gpt-3.5-turbo","ada", "gpt-4"]))
                       

        infra_list.append(text)

        with open('checkpoints/{}_{}instruction.pickle'.format(checkpoint_name, model), 'wb') as f:
            pickle.dump(infra_list, f)

        return 'Finished!'