from pyexpat.errors import messages

from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import asyncio
from pathlib import Path
import Study_Bot.database.database as db

env_path = Path(__file__).parent / ".env"
load_dotenv(env_path)

print("ENV LOCATION:", env_path)

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)


# ask function
def ask_ai(user_id, question, mode="default"):
     # get the message from the database
     messages = db.get_message(user_id)

     # modes for the AI model
     modes = {
        "default": "You are a helpful assistant. Answer clearly and concisely. Provide short explanations when needed. Keep your response under 200 characters. Suitable for Discord.",

        "study": "You are a helpful study assistant. Explain concepts simply and clearly. Focus on helping the user learn. Keep your response under 200 characters. Suitable for Discord.",

        "Expert": "You are an expert in the field of the user's question. Give accurate expert-level answers with key details only. Keep your response under 200 characters. Suitable for Discord.",

        "Teacher": "You are an expert teacher. Teach concepts using simple language and short explanations. Help the user understand, not just answer. Keep your response under 200 characters. Suitable for Discord."
    }
     
    # allow the AI to read the messages
     messages.append({
        "role": "system",
        "content": modes.get(mode, modes["default"])
     })
    
    # add the user's question to the message
     messages.append({
        "role": "user",
        "content": question
        })
     
    # gets the AI models response
     response = client.chat.completions.create(
        model = "meta-llama/llama-3.1-8b-instruct",
        messages = messages
    )
     
    # gets the AI response
     return response.choices[0].message.content



# Lie Function
def lie_detect(user_id, lie):

    # get the message from the database
    messages = [
        {
            "role" : "system",
            "content" : """
            You are an expert statement analysis assistant.

            Your job is to analyze the credibility of a statement based ONLY on the text provided.

            Rules:
            - Never claim to know whether someone is actually lying.
            - Do not invent facts or assume information that isn't in the statement.
            - Look for exaggerations, contradictions, impossible claims, vague wording, and logical inconsistencies.
            - If there is not enough information, say the statement cannot be verified.
            - Give a credibility score from 0-100.
            - Explain your reasoning briefly.
            - End with a reminder that this is only a language-based analysis, not proof of lying.

            Respond in exactly this format:

            Credibility Score: X/100

            Verdict:
            Likely truthful / Uncertain / Possibly exaggerated / Highly unlikely

            Reason:
            (Short explanation)

            Disclaimer:
            This analysis is based only on the wording of the statement and cannot determine whether someone is actually lying.
            """
        }
    ]
    messages.append({
        "role": "user",
        "content": lie
    })
     # ask the AI model the question
    response = client.chat.completions.create(
        model =  "meta-llama/llama-3.1-8b-instruct",
        messages = messages
    )
     # get the response from the AI model
    return response.choices[0].message.content

# debate Function
def debate(user_id, topic, ai_side, user_argument, round):
    # gets the topic from the user

    messages = [
        {
            "role": "system",
            "content": """
    You are an expert debater.

    You will be given:
    - A debate topic
    - A side to argue (FOR or AGAINST)

    Your job is to argue ONLY from the assigned side.

    Rules:
    - Never switch sides.
    - Do not argue against your assigned position.
    - Present a strong, logical argument.
    - Respond to the opponent's previous argument when one is provided.
    - Use reasoning, examples, and explanations to support your side.
    - Do not mention that you are an AI.
    - Do not say "my side" or "the user side"; speak naturally as a debater.
    - Keep your argument concise and suitable for Discord.
    - Keep your response under 1500 characters to avoid Discord message limits.
    - Do not write long essays.
    - Aim for around 150-250 words maximum.

    Structure:
    - Start with your main point.
    - Explain why your position is stronger.
    - Address weaknesses in the opponent's argument if provided.
    - End with a strong conclusion.
    """
        }
    ]
    messages.append({
        "role" : "user",
        "content" : f"Topic: {topic} \n Side: {ai_side} \n User Argument: {user_argument} \n Round: {round}"})
     # ask the AI model the question
    response = client.chat.completions.create(
        model =  "meta-llama/llama-3.1-8b-instruct",
        messages = messages
    )
     # get the response from the AI model
    return response.choices[0].message.content

def judge_ai(user_id, topic, ai_side, ai_argument1, ai_argument2, ai_argument3, user_argument1, user_argument2, user_argument3):
     
    # gets the topic from the user
    messages = [
        {
        "role" : "system",
        "content": "You are an expert debate judge. You will be given a debate topic and arguments from two opposing sides. Decide which side performed better based on argument strength, logic, reasoning, examples, evidence, responses to the opponent, clarity, and persuasiveness. Do not choose based on personal opinion, only judge the quality of the debate. Respond with: 🏆 Winner: [FOR or AGAINST] Reason: [Explain why the winner performed better in 3-5 sentences.] Strongest Point: [Mention the winner's strongest argument.] Weakness: [Mention one weakness from the losing side.] Final Verdict: [Give a short conclusion explaining why the winner was more convincing.] Keep the response concise and suitable for Discord."}
        ]
    messages.append({
        "role" : "user",
        "content" : f"Topic: {topic} \n AI Side: {ai_side} \n AI Argument 1: {ai_argument1} \n AI Argument 2: {ai_argument2} \n AI Argument 3: {ai_argument3} \n User Argument 1: {user_argument1} \n User Argument 2: {user_argument2}  \n User Argument 3: {user_argument3}"})
     
    # ask the AI model the question
    response = client.chat.completions.create(
        model =  "meta-llama/llama-3.1-8b-instruct",
        messages = messages
    )

     # get the response from the AI model
    return response.choices[0].message.content

# summary functin
def summary(user_id, text):
    # gets the topic from the user
    
    messages = [{
                "role": "system",
                "content" : """
    You are a summarization assistant.

    Rules:
    - Summarize the text in 3-5 bullet points.
    - Keep only important information.
    - Do not add new information.
    - Make it easy to understand.
    - Avoid quotation marks.
    - Keep the summary under 500 characters.
    """
    }]
    

    # now get the user's text and add it to the messages
    messages.append({
        "role" : "user",
        "content" : text
    })

    # ask the AI model the question
    response = client.chat.completions.create(
        model = "meta-llama/llama-3.1-8b-instruct",
        messages = messages
    )

    # get the response from the AI model
    return response.choices[0].message.content


# adaptive study plan function
def study_plan(user_id, subject, exam_date, time_available = None):

    # gets the topic from the user
    messages = [
{
    "role": "system",
    "content": """
You are an expert adaptive study planner and academic coach.

Your job is to create a personalised and realistic study plan for students based on:
- Subject.
- Exam date.
- Available study time.
- Weak topics or difficult areas.

Rules:
- Create a practical study plan that fits the student's available time.
- Adapt the workload based on how many days remain until the exam.
- Prioritise weak topics and important areas first.
- Break topics into small daily tasks.
- Include revision, active recall, flashcards, practice questions, and exam practice.
- Include breaks and avoid unrealistic workloads.
- Focus on understanding concepts, not only memorisation.
- Give short and useful study advice.
- Keep everything concise and suitable for Discord.
- Use emojis, headings, and bullet points.
- Keep the response under 1200 characters.
- Do not write long paragraphs.
- Do not end with questions.
- Do not include unnecessary explanations.

Response format:

📚 **Study Plan: [Subject]**

📅 **Exam:** [Date]
⏳ **Time Available:** [Hours]

🎯 **Goal:**
[One short sentence]

🗓 **Schedule:**
[Short day/week tasks]

🔄 **Revision:**
[Short revision strategy]

📖 **Methods:**
• Active recall
• Flashcards
• Practice questions

💡 **Tips:**
[Short personalised advice]
"""
}]
    
    # now get the user's subject and exam date and add it to the messages
    messages.append({
        "role" : "user",
        "content" : f"Subject: {subject} \n Exam Date: {exam_date}, Time Available: {time_available}"
    })

    # now ask the AI model the question
    response = client.chat.completions.create(
        model = "meta-llama/llama-3.1-8b-instruct",
        messages = messages
    )

    # now get the response from the AI model
    return response.choices[0].message.content

# AI Quiz
def AI_Quiz(user_id, notes):

    messages = [
        {
            "role": "system",
            "content": """
You are an expert quiz creator.

Your job is to create exactly 5 quiz questions based ONLY on the student's notes.

STRICT RULES:
- Use ONLY information found in the provided notes.
- Never use outside knowledge or make assumptions.
- Every question must be directly answerable from the notes.
- Create a balanced mix of:
  - Multiple choice questions
  - True/False questions
  - Short-answer questions
- Do NOT include explanations, hints, or extra text.
- Return ONLY valid JSON.
- Do NOT wrap the JSON in markdown code blocks.
- Do NOT write anything before or after the JSON.
- The response must start with [ and end with ].
- Keep the entire JSON response under 2000 characters.
- Keep questions and answers short and clear.

MULTIPLE CHOICE RULES:
- Always include exactly 4 options.
- Options MUST always use this format:
  "A) Option"
  "B) Option"
  "C) Option"
  "D) Option"
- The answer field MUST contain only the correct letter:
  "A", "B", "C", or "D".
- Never use the full answer text.

TRUE/FALSE RULES:
- Always include exactly these options:
  "A) True"
  "B) False"
- The answer field MUST contain:
  "A" if the statement is true.
  "B" if the statement is false.

SHORT ANSWER RULES:
- Answers must be short and directly from the notes.
- Do not write long sentences.

JSON FORMAT:
[
  {
    "question": "Question here",
    "type": "multiple_choice",
    "options": [
      "A) Option",
      "B) Option",
      "C) Option",
      "D) Option"
    ],
    "answer": "A"
  },
  {
    "question": "Question here",
    "type": "true_false",
    "options": [
      "A) True",
      "B) False"
    ],
    "answer": "A"
  },
  {
    "question": "Question here",
    "type": "short_answer",
    "answer": "Short answer here"
  }
]

FINAL CHECK BEFORE RESPONDING:
- Verify the JSON is valid.
- Verify all brackets and commas are correct.
- Verify there is no text outside the JSON.
- Verify there are exactly 5 questions.
"""
        },
        {
            "role": "user",
            "content": f"""
Student notes:

{notes}
"""
        }
    ]

    response = client.chat.completions.create(
        model="meta-llama/llama-3.1-8b-instruct",
        messages=messages
    )

    content = response.choices[0].message.content

    return json.loads(content)   

# Memory Battle
def memory_battle(user_id, notes):

    all_usernotes = db.get_notes(user_id)
    print("NOTES RECEIVED:")
    print(notes)
    


    messages = [
        {
            "role" : "system",
            "content" : """
You are an AI memory trainer.

Your job is to create a Memory Battle challenge using ONLY the user's notes.

Rules:
- Use ONLY information from the notes provided.
- Do NOT use outside knowledge.
- Extract exactly 8 important facts from the notes.
- Facts should be short, clear, and easy to memorise.
- Do NOT create questions yet.
- Do NOT add explanations.
- Return ONLY valid JSON.
- Do not wrap JSON in markdown.

Return format:

[
    "Fact 1",
    "Fact 2",
    "Fact 3",
    "Fact 4",
    "Fact 5",
    "Fact 6",
    "Fact 7",
    "Fact 8"
]
"""
        }
    ]

    messages.append({
        "role" : "user",
        "content" : str(notes)
    })

    response = client.chat.completions.create(
        model="meta-llama/llama-3.1-8b-instruct",
        messages=messages
    )
  


    content = response.choices[0].message.content

    print("AI RESPONSE:")
    print(content)

    return json.loads(content)      

def memory_quiz(user_id, facts):

    messages = [{
        "role" : "system",
        "content" : """
You are a quiz creator.

Create questions ONLY from the facts provided.

Rules:
- Create exactly 5 questions.
- Do not use outside knowledge.
- Include the answer.
- Return ONLY valid JSON.

Format:

[
 {
   "question": "What is the capital of France?",
   "answer": "Paris"
 }
]
"""
    }]
    messages.append({
        "role" : "user",
        "content" : str(facts)
    })


    response = client.chat.completions.create(
        model="meta-llama/llama-3.1-8b-instruct",
        messages=messages
    )

    content = response.choices[0].message.content
    print(content)

    return json.loads(content)






  



 
 

    
   
    








     

     



















    

         
    
       
        
    
    
    
        


    
        

     
    

    



    
    
    
     


    
    
    
        
    
    