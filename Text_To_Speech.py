from google.cloud import texttospeech

def text_to_speech(input_text:str):
    try:

        #input_text = "hi, my name is and this is a sample video for my PC assignment. That was given to me. And this is a audio for that. In this assignment, I have to rearrange the audio with using"

        client = texttospeech.TextToSpeechClient(client_options={"api_key": 'AIzaSyAjGIaVVSXSyCiW-jPJ17lcHtZoDp-iZdY'})

        synthesis_input = texttospeech.SynthesisInput(text=input_text)

        voice = texttospeech.VoiceSelectionParams(
            language_code="en-US",
            name='en-US-Journey-D', ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL)

        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3)

        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config)

        with open("./output.mp3", "wb") as out:
            # Write the response to the output file.
            out.write(response.audio_content)
            #print('Audio content written to file "output.mp3"')

        return "./output.mp3"
    
    except Exception as e:
        raise e