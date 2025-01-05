import openai as AI
import sys
sys.path.append("D:\\Learning\\GenAi\\hackalthon\\Chatbot\\Config\\")
import API_Key as AP
AI.api_key = AP.Open_AI_Key

def check_verification_status(text):
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"Based on the following text, determine if the verification is successful: {text}. Check if the provided text contains any of the following phrases: 'verified', 'success', 'institution has been verified', 'you are all set', or 'your institution has been verified'. If any of these phrases are present, respond with: 'While analysing the image we could see that DL verification process is successfully completed from your end. So, do we need to perform DL pull process? Enter Yes or No.'"}
    ]
    
    response = AI.ChatCompletion.create(  # Correct method for chat models
        model='gpt-4',  # Correct model name
        messages=messages,
        max_tokens=4000,
        temperature=0
    )
    
    result = response['choices'][0]['message']['content'].strip()  # Correct response access
    return result
