import streamlit as st
from app_utils import *
import replicate
from elevenlabs import set_api_key, voices, generate, stream

st.set_page_config(layout="wide")

openai.api_key = st.secrets['OPENAI_API_KEY']
st.session_state.client = replicate.Client(api_token=st.secrets['REPLICATE_API_KEY'])
set_api_key(st.secrets["ELEVENLABS_API_KEY"])

if "title" not in st.session_state:
    st.session_state.title = 'Gen-Branch: Interactive Audio-Visual Simulation Generator'

st.markdown(f'<h1 style="text-align:center; font-size:40px;">{st.session_state.title}</h1>', unsafe_allow_html=True)

if "story_started" not in st.session_state:
    st.session_state.story_started = False
if "adapter" not in st.session_state:
    st.session_state.adapter = None
if "mode" not in st.session_state:
    st.session_state.mode = None

if st.session_state.mode is None:
    col1, col2, col3 = st.columns([1, 2, 1])
    selection = col2.selectbox("Choose a mode:", ["Interactive Narrative Mode", "Alignment Simulation Mode"])
    if col2.button("Submit"):
        st.session_state.mode = selection
        st.rerun()

elif st.session_state.mode == "Interactive Narrative Mode":
    def initialize_session_state():
        """Initialize session state variables."""
        for scale in narrative_axes:
            if scale not in st.session_state or not isinstance(st.session_state[scale], (int, float)):
                st.session_state[scale] = 3  # Default value for slider

    # Placeholders for the main display area
    initial_input_placeholder = st.empty()
    main_placeholder = st.empty()
    style_exp_placeholder = st.empty()
    style_placeholder = st.empty()
    text_placeholder = st.empty()
    radio_placeholder = st.empty()
    button_placeholder = st.empty()

    # Function to display loading state
    def display_loading(message, col2_content_placeholders=None):
        initial_input_placeholder.empty()  # clear the inputs
        style_exp_placeholder.empty()
        style_placeholder.empty()
        button_placeholder.empty()

        if col2_content_placeholders:
            # Clear the placeholders inside col2
            col2_text_placeholder, col2_radio_placeholder, col2_button_placeholder = col2_content_placeholders
            col2_text_placeholder.empty()
            col2_radio_placeholder.empty()
            col2_button_placeholder.empty()

        with main_placeholder.container():
            # Centering the image
            st.markdown('<br>', unsafe_allow_html=True)
            st.markdown(f'<div style="text-align: center"><img src="{loading_image_link}" width="700" /></div>', unsafe_allow_html=True)
            
            # Centering the message
            st.markdown(f'<div style="text-align: center; font-size: 24px; font-weight: bold;">{message}</div>', unsafe_allow_html=True)

    initialize_session_state()
    # Initialize session state variables if they don't exist
    if "selected_genre" not in st.session_state:
        st.session_state.selected_genre = None
    if "show_transcript" not in st.session_state:
        st.session_state.show_transcript = False

    # Collect user preferences
    if not st.session_state.story_started:
        with initial_input_placeholder.container():
            # Sliders for narrative control
            for axis in narrative_axes:
                widget_key = f"{axis}_slider"            
                value = st.slider(narrative_display_names[axis], 1, 5, st.session_state[axis], key=widget_key)
                st.session_state[axis] = value

            st.session_state.themes = st.text_input("Input any themes or specific ideas you want included in the story (e.g., futuristic AI, medieval castle, betrayal and passion, etc.):")

            # Gender selection
            gender = st.radio("Select gender of narrator:", ['Male', 'Female'], key="narrator_gender")
            st.session_state.voice = 'Josh' if gender == 'Male' else 'Bella'

            # Art style input
            st.markdown("""
            Enter your desired illustration styles. Feel free to combine styles, mediums, or artists for unique results.
            For instance:
            - 'Acrylic Painting'
            - 'Digital Art in the style of Picasso'
            - '3D Rendering combined with Watercolor'
            - 'Manga by Osamu Tezuka'
            """)
            st.session_state.style = st.text_input("Desired Illustration Styles:")

        if button_placeholder.button("Start"):
            if not all([getattr(st.session_state, attr) for attr in scale_descriptions.keys()]):
                st.warning("Please adjust all the sliders to set your preferences.")
            elif not st.session_state.style:
                st.warning("Please specify your style preferences")
            elif not st.session_state.themes:
                st.warning("Please input any key themes or ideas you want in the story")
            else:
                display_loading("Preferences submitted. Generating your story prompt...")
                st.session_state.preferences = generate_story_prompt(preference_maker.format(
                                seriousness_description=st.session_state.seriousness,
                                whimsicality_description=st.session_state.whimsicality,
                                depth_description=st.session_state.depth,
                                scariness_description=st.session_state.scariness,
                                romantic_intensity_description=st.session_state.romantic_intensity,
                                action_description=st.session_state.action_packed,
                                fantasy_description=st.session_state.fantasy_level,
                                mystery_description=st.session_state.mysteriousness,
                                historical_description=st.session_state.historical_setting,
                                humor_description=st.session_state.humor_quotient,
                                themes=st.session_state.themes
                                ))
                print('PREFERENCES', st.session_state.preferences)
                # Display or further process the story_prompt as

                # Your logic for story initialization goes here, using the descriptions from st.session_state.selected_descriptions
                story = Story(user_preferences=st.session_state.preferences)
                st.session_state.adapter = SimpleStoryAdapter(story)
                st.session_state.adapter.advance_story("Begin the narrative!")
                st.session_state.latest_chunk = st.session_state.adapter.get_latest_message_from_system()
                title = generate_title(title_prompt.format(story=[st.session_state.preferences]))
                st.session_state.title = title.strip('"')
                st.session_state.illustration = generate_illustration(st.session_state.latest_chunk, st.session_state.style, st.session_state.client)
                st.session_state.story_text = st.session_state.latest_chunk.split("OPTION 1:")[0].strip()
                st.session_state.audio = generate(text=st.session_state.story_text, voice=st.session_state.voice)
                # st.session_state.audio = replicate.run("afiaka87/tortoise-tts:e9658de4b325863c4fcdc12d94bb7c9b54cbfe351b7ca1b36860008172b91c71",
                #                                         input={"text": st.session_state.story_text})
                st.session_state.story_started = True
                st.rerun()

elif st.session_state.mode == 'Alignment Simulation Mode':
    alignment_axes = {
    "organization_type": "Type of Organization (Grassroots → Global Tech)",
    "cooperation_level": "Research Climate (Fully Collaborative → Fiercely Competitive)",
    "ai_capability": "AI Capability (Basic Script → Full AGI)",
    "regulation_intensity": "Regulatory Landscape (No Regulation → Totalitarian Control)",
    "public_perception": "Public Perception (Adoring → Outright Hostile)"
    }

    for scale in alignment_axes:
        if scale not in st.session_state:
            st.session_state[scale] = 3  # Default value for slider

        if f"{scale}_description" not in st.session_state:
            st.session_state[f"{scale}_description"] = ""

    # Placeholders for the main display area
    initial_input_placeholder = st.empty()
    main_placeholder = st.empty()
    style_exp_placeholder = st.empty()
    style_placeholder = st.empty()
    text_placeholder = st.empty()
    radio_placeholder = st.empty()
    button_placeholder = st.empty()

    # Function to display loading state
    def display_loading(message, col2_content_placeholders=None):
        initial_input_placeholder.empty()  # clear the inputs
        style_exp_placeholder.empty()
        style_placeholder.empty()
        button_placeholder.empty()

        if col2_content_placeholders:
            # Clear the placeholders inside col2
            col2_text_placeholder, col2_radio_placeholder, col2_button_placeholder = col2_content_placeholders
            col2_text_placeholder.empty()
            col2_radio_placeholder.empty()
            col2_button_placeholder.empty()

        with main_placeholder.container():
            # Centering the image
            st.markdown('<br>', unsafe_allow_html=True)
            st.markdown(f'<div style="text-align: center"><img src="{loading_image_link}" width="700" /></div>', unsafe_allow_html=True)
            
            # Centering the message
            st.markdown(f'<div style="text-align: center; font-size: 24px; font-weight: bold;">{message}</div>', unsafe_allow_html=True)


    if not st.session_state.story_started:
        # Collect user preferences
        with initial_input_placeholder.container():
            # Dropdown for alignment subarea
            alignment_subareas = [
                "Iterated Amplification",
                "Technical AI Ethics",
                "Embedding Human Values",
                "Corrigibility",
                "Inverse Reinforcement Learning",
                "Interpretability",
                "Reward Modeling",
                "Handling Deception",
                "Brain-based Approaches",
                "Building Prosocial AI"
            ]
            st.session_state.alignment_subarea = st.selectbox("Choose an alignment subarea to focus on:", alignment_subareas)

            # Updated Sliders for alignment research scenarios
            alignment_slider_descriptions = {
                "organization_type": ("Grassroots Collective", "Academic Lab", "Startup", "Established Corporation", "Global Tech Conglomerate"),
                "cooperation_level": ("Fully Collaborative", "Cooperative", "Neutral", "Slightly Competitive", "Fiercely Competitive"),
                "ai_capability": ("Basic Script", "Narrow AI", "Advanced Narrow AI", "Specialized AGI", "Full AGI Threshold"),
                "regulation_intensity": ("No Regulation", "Loose Regulation", "Moderate Regulation", "Stringent Oversight", "Totalitarian Control"),
                "public_perception": ("Adoring", "Supportive", "Neutral", "Concerned", "Outright Hostile")
            }

            for axis, (v1, v2, v3, v4, v5) in alignment_slider_descriptions.items():
                value = st.slider(alignment_axes[axis], 1, 5, st.session_state[axis], key=f"{axis}_slider", format="")
                description_mapping = {1: v1, 2: v2, 3: v3, 4: v4, 5: v5}
                st.write(f"Current setting: **{description_mapping[value]}**")
                
                st.session_state[axis] = value  # Store the numeric value
                st.session_state[f"{axis}_description"] = description_mapping[value]  # Store the description separately
                st.markdown("---")  # Add horizontal line for separation


            st.session_state.themes = st.text_input("Input any specific ideas or conditions you want included in the simulation (e.g., AI arms race between Google and Microsoft, determine if prosocial AI is deceptive, etc.):")

            # Gender selection
            gender = st.radio("Select gender of narrator:", ['Male', 'Female'], key="narrator_gender")
            st.session_state.voice = 'Josh' if gender == 'Male' else 'Bella'

            # Art style input
            st.markdown("""
            Enter your desired illustration styles. Feel free to combine styles, mediums, or artists for unique results.
            For instance:
            - 'Acrylic Painting'
            - 'Digital Art in the style of Picasso'
            - '3D Rendering combined with Watercolor'
            - 'Manga by Osamu Tezuka'
            """)
            st.session_state.style = st.text_input("Desired Illustration Styles:")

        if button_placeholder.button("Start Simulation"):
            if not st.session_state.style:
                st.warning("Please specify your style preferences")
            elif not st.session_state.themes:
                st.warning("Please input any key themes or ideas you want in the story")
            else:
                display_loading("Preferences submitted. Generating your story prompt...")
                st.session_state.preferences = generate_alignment_prompt(alignment_maker.format(
                organization_type_description=st.session_state.organization_type_description,
                cooperation_level_description=st.session_state.cooperation_level_description,
                ai_capability_description=st.session_state.ai_capability_description,
                regulation_intensity_description=st.session_state.regulation_intensity_description,
                public_perception_description=st.session_state.public_perception_description,
                alignment_subarea_description=st.session_state.alignment_subarea,
                themes=st.session_state.themes
                    ))

                print('PREFERENCES', st.session_state.preferences)
                # Display or further process the story_prompt as

                # Your logic for story initialization goes here, using the descriptions from st.session_state.selected_descriptions
                story = AlignmentSim(user_preferences=st.session_state.preferences)
                st.session_state.adapter = SimpleStoryAdapter(story)
                st.session_state.adapter.advance_story("Begin the alignment simulation!")
                st.session_state.latest_chunk = st.session_state.adapter.get_latest_message_from_system()
                title = generate_title(title_prompt.format(story=[st.session_state.preferences]))
                st.session_state.title = title.strip('"')
                st.session_state.illustration = generate_illustration(st.session_state.latest_chunk, st.session_state.style, st.session_state.client)
                st.session_state.story_text = st.session_state.latest_chunk.split("OPTION 1:")[0].strip()
                st.session_state.audio = generate(text=st.session_state.story_text, voice=st.session_state.voice)
                # st.session_state.audio = replicate.run("afiaka87/tortoise-tts:e9658de4b325863c4fcdc12d94bb7c9b54cbfe351b7ca1b36860008172b91c71",
                #                                         input={"text": st.session_state.story_text})
                st.session_state.story_started = True
                st.rerun()

if st.session_state.story_started and st.session_state.adapter:
    with main_placeholder.container():
        # Create two columns
        col1, col2 = st.columns([2,1])

        # Image in the left column (col1)

        col1.image(st.session_state.illustration)

         # Create placeholders within the right column (col2)
        text_placeholder_in_col2 = col2.empty()
        radio_placeholder_in_col2 = col2.empty()
        button_placeholder_in_col2 = col2.empty()
        
        # If starting a new iteration, reset the session state variables
        if "audio_has_played" not in st.session_state or not st.session_state.audio_has_played:
            st.session_state.audio_has_played = False
            st.session_state.audio_playing = True
            st.session_state.audio_start_time = time.time()

        audio_duration = autoplay_audio(st.session_state.audio)

        # Only enter loop if audio_playing is True
        while st.session_state.audio_playing and not st.session_state.audio_has_played:
            elapsed_time = time.time() - st.session_state.audio_start_time

            if elapsed_time >= audio_duration:
                st.session_state.audio_playing = False
                st.session_state.audio_has_played = True  # Set this to True to mark the end of this audio iteration

        option_1, option_2 = extract_options_from_chunk(st.session_state.latest_chunk)
        
        if option_1 and option_2:
            formatted_text = '\n'.join([f'#### {paragraph}' for paragraph in st.session_state.story_text.split('\n') if paragraph])
            text_placeholder_in_col2.markdown(f"{formatted_text}\n\n---\n\n")

            user_choice = radio_placeholder_in_col2.radio("## What will you choose?", [option_1, option_2]) 
            if button_placeholder_in_col2.button("Submit"):
                # Reset audio-related session state variables for the next audio playback
                del st.session_state.audio_start_time
                
                display_loading("Choice locked in. Generating the next part of your story...", 
                                (text_placeholder_in_col2, radio_placeholder_in_col2, button_placeholder_in_col2))

                st.session_state.adapter.submit_choice(user_choice)
                
                # Update session_state variables
                st.session_state.audio_has_played = False
                st.session_state.latest_chunk = st.session_state.adapter.get_latest_message_from_system()
                st.session_state.story_text = st.session_state.latest_chunk.split("OPTION 1:")[0].strip()
                st.session_state.audio = generate(text=st.session_state.story_text, voice=st.session_state.voice)
                # st.session_state.audio = replicate.run("afiaka87/tortoise-tts:e9658de4b325863c4fcdc12d94bb7c9b54cbfe351b7ca1b36860008172b91c71",
                #                                     input={"text": st.session_state.story_text})
                st.session_state.illustration = generate_illustration(st.session_state.latest_chunk, st.session_state.style, st.session_state.client)
                st.rerun()