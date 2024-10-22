import streamlit as st
import openai
import requests
import json
from Speech_To_Text import speech_to_text
from Text_To_Speech import text_to_speech
from merge import merge_video_audio


def main():

    st.set_page_config(layout="wide")

    st.title("Upload Video for AI audio..") 

    uploaded_video = st.file_uploader("Upload video",type={"mp4"})
    if uploaded_video:
        transcript = speech_to_text(uploaded_video)
        st.success(f"Transcript: {transcript}")


    col1, col2 = st.columns(2)
    with col1:
        st.title("Azure OpenAI GPT-4o Connectivity Test") 
        st.header("for the correct the transcription removing any grammatical mistakes.")
        
        # Azure OpenAI connection details
        # Here, we define the API key and endpoint URL for connecting to Azure OpenAI.
        azure_openai_key =  "22ec84421ec24230a3638d1b51e3a7dc"  # Replace with your actual key. if you don't have one, get from Azure or from Community https://curious.pm
        azure_openai_endpoint = " https://internshala.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2024-08-01-preview"  # Replace with your actual endpoint URL
        
        # Button to initiate the connection and request
        # User clicks this button to initiate the request to Azure OpenAI.
        if st.button("Connect and Get Response"):
            
        # Check if both the key and endpoint are provided
        # Ensure that the key and endpoint are not empty before proceeding.
            if azure_openai_key and azure_openai_endpoint:
                try:
                    # Setting up headers for the API request
                    # Define the headers needed for the API request, including the API key for authentication.
                    headers = {
                        "Content-Type": "application/json",  # Specifies that we are sending JSON data
                        "api-key": azure_openai_key  # The API key for authentication
                    }
                    
                    # Data to be sent to Azure OpenAI
                    # Define the payload, which includes the message prompt and token limit.
                    # **** This is where you can customize the message prompt and token limit. ****
                    data = {
                        "messages": [
                            {"role": "system", "content": "correct the transcription removing any grammatical mistakes."}, # give the system an context.
                            {"role": "user", "content": f"{transcript}"}],  # The message we want the model to respond to
                        "max_tokens": 50  # Limit the response length
                    }
                    
                    # Making the POST request to the Azure OpenAI endpoint
                    # Send the request to the Azure OpenAI endpoint using the defined headers and data.
                    response = requests.post(azure_openai_endpoint, headers=headers, json=data)
                    
                    # Check if the request was successful
                    # Handle the response, checking the status and displaying the result.
                    if response.status_code == 200:
                        result = response.json()  # Parse the JSON response
                        st.success(result["choices"][0]["message"]["content"].strip())  # Display the response content from the AI
                        
                        with st.spinner("generate audio.."):
                            #convert the text into audio.
                            audio = text_to_speech(result["choices"][0]["message"]["content"].strip())
                            st.success(f"audio generated {audio}")

                        with st.spinner("Merge video with audio.."):
                            #merge the AI audio with the video
                            merge = merge_video_audio(input_video=uploaded_video.name, input_audio=audio)
                            st.success(f"video merge :{merge}")

                        if merge:
                            with col2:    
                                video_file = open(f"{merge}", "rb")
                                video_bytes = video_file.read()
                                st.video(video_bytes)

                    
                    else:
                        # Handle errors if the request was not successful
                        st.error(f"Failed to connect or retrieve response: {response.status_code} - {response.text}")
                except Exception as e:
                    # Handle any exceptions that occur during the request
                    st.error(f"Failed to connect or retrieve response: {str(e)}")
            else:
                # Warn the user if key or endpoint is missing
                st.warning("Please enter all the required details.")

            

            

if __name__ == "__main__":
    main()