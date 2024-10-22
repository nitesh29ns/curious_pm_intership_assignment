import streamlit as st
import cv2 as cv
import tempfile
from moviepy.editor import *
from google.cloud import speech
import os
import io



def speech_to_text(upload_video):
    try:
        client = speech.SpeechClient(client_options={"api_key": 'AIzaSyBx3pD4FQSKvMr4sKqb92lGue4AqIPIDsw'})

        audio_file = "./audio.wav"
        #f = st.file_uploader("Upload file")
        
        tfile = tempfile.NamedTemporaryFile(delete=False) 
        tfile.write(upload_video.read())

        audio = AudioFileClip(tfile.name)
        audio.write_audiofile(audio_file)


        with io.open(audio_file, "rb") as audio_file:
            content = audio_file.read()
            audio = speech.RecognitionAudio(content=content)

        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            enable_automatic_punctuation=True,
            audio_channel_count=2,
            language_code="en-US",
        )

        response = client.recognize(request={"config": config, "audio": audio})

        
        transript = ""

        for result in response.results:
            #text = "{}".format(result.alternatives[0].transcript)
            text = result.alternatives[0].transcript
            transript += text 
            

        return transript

    except Exception as e:
        raise e
    
