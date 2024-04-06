import streamlit as st
import pyaudio
import whisper
import openai
from airtable import Airtable

def init_assistant():
    if "init" not in st.session_state:
        client = openai.OpenAI(api_key=st.secrets['OPENAI_API'])
        st.session_state["client"] = client
        thread = client.beta.threads.create(
            messages=[
            {
            "role": "user",
            "content": "Chat Begins",
            }
        ]
        )
        hr_thread = client.chat.completions.create(
            model="ft:gpt-3.5-turbo-0125:personal:hrbotfinal:94rYXqzX",
            messages=[
                {"role": "user", "content": "Chat Begins"},
            ]
        )
        st.session_state["thread_id"] = thread.id
        st.session_state["hr_thread_id"] = hr_thread.id
        
        st.session_state["BASE_ID"] = st.secrets['BASE_ID']
        st.session_state["API_KEY"] = st.secrets['API_KEY']
        airtable_categories = Airtable(st.session_state["BASE_ID"], "categories", api_key=st.session_state["API_KEY"])
        airtable_questions = Airtable(st.session_state["BASE_ID"], "questions", api_key=st.session_state["API_KEY"])
        st.session_state["airtable_categories"] = airtable_categories
        st.session_state["airtable_questions"] = airtable_questions
        categories = st.session_state["airtable_categories"].get_all()
        st.session_state["categories"] = [category['fields']['cname'] for category in categories]
        st.session_state["model"] = whisper.load_model("small")
        st.session_state["audio"] = pyaudio.PyAudio()
        st.session_state["init"] = True
        return st.session_state