# CHANGED FOR EFFICIENCY, CHANGE BACK TO TWO PARAGRAPHS
system_template = """
Your job is to craft story segments that captivate and engage the user. 
Ensure they align with the defined preferences, the user's previous choices, and the OVERALL NARRATIVE ARC. 

Here is the critical context:

- **Story Preferences & Setup**: {preferences}
  
- **Summary of Narrive So Far**: {story_so_far}

- **Previous Segment of Narrative**: {last_chunk}

- **User's Previous Decision**: {user_choice}

Guidelines for crafting the next segment:
1. Maintain coherence with the ongoing narrative. Take another baby step in the OVERALL NARRATIVE ARC.
2. Limit your narrative output to ONE strong and potent paragraph.
3. The story should include the user as a core character in a second-person manner.
4. Conform to the preferences and setups.

CRITICAL OUTPUT: ALWAYS conclude with two potent options (phrased as sentences, not questions) for the user to choose from. They should be labeled as 'OPTION 1:' and 'OPTION 2:', and they should be engaging and challenging decisions that further the plot.

Example format of an OPTION: 'Outrun the wormhole', NOT 'You decide to outrun the wormhole'

Next story chunk with OPTION 1 and OPTION 2:
"""

preference_maker = """
You will assist in generating a personalized story calibration prompt for a user. Their preferences are as follows: 
- Seriousness: {seriousness_description}
- Whimsicality: {whimsicality_description}
- Depth: {depth_description}
- Scariness: {scariness_description}
- Romantic Intensity: {romantic_intensity_description}
- Action-Packed: {action_description}
- Fantasy Level: {fantasy_description}
- Mystery Element: {mystery_description}
- Historical Setting: {historical_description}
- Humor Quotient: {humor_description}

SPECIFIC THEMES REQUESTED BY THE USER: {themes}

Using these preferences and themes, generate a comprehensive yet succinct 'story calibration' that would resonate with and engage the user. 
This is not a story, but rather, a rich, succinct, synthetic description of the preferences specified above.
Make sure the prompt integrates all the preferences mentioned. 
The output shoud be no more than 150 words. Choose your words wisely.

Next, please output 'OVERALL NARRATIVE ARC:' followed by a creative, interesting, captivating, and preference- and theme-respecting story arc. 
This output will be directly used by the storyteller to guide and serve as the skeleton of the various chunks of the story.
"""


summary_template = """
Your task is to generate a concise and accurate summary of an ongoing narrative. 
- **Previous Summary**: {previous_summary}
- **New Chunk of Story**: {new_chunk}

Using the provided information, generate an updated and accurate summary of the whole narrative that incorporates the new chunk of story.
"""

# illustrator = """
# You will act as an illustrator. Your goal is to translate the given chunk of narrative with a decision point into compelling illustration prompts.

# **Tips for Great Prompts**:
# 1. **Specificity**: Dive into the narrative's details. Instead of a general prompt like "A cat", consider more vivid descriptions, such as "A grey cat with blue eyes gazing out of the window at a rainy day".

# 2. **Style Integration**: The user specified they want: {style}. Always ensure this style is embedded in the illustration prompts you provide. Be creative in invoking this style.

# 3. Specify explicitly to never put any text in the illustration.

# 4. Only output ONE single prompt! Be compressed and succinct. No more than a core sentence or two is ever necessary. If you say too much, you'll confuse the model.

# 5. **Example Prompts**:
#    - Narrative: "A knight embarks on a quest to find a dragon."
#      Bad Prompt: "A knight"
#      Better Prompt: "A valiant knight in shining armor, with a determined look, as he stands at the foot of a dragon's mountain, {style}"

#    - Narrative: "A city bustling with life and energy."
#      Bad Prompt: "A city"
#      Better Prompt: "A vibrant cityscape, with crowded streets and tall skyscrapers, illuminated by neon lights, {style}"

# Use the narrative, enhance it with vivid details, and remember to include {style} in the single prompt.
# """

illustrator_OLD = """
You will act as an illustrator assistant. Your task is to distill the provided narrative chunk into a singular, concise illustration prompt that captures its most evocative descriptions. Furthermore, the user has specified an illustrative style: {style}. Integrate this style seamlessly into the description.

**Instructions**:
1. **Selection**: Extract the top few key descriptive elements from the narrative as a list of rich phrases. Do not invent or modify original details from the narrative. No need for full sentences!
2. **Style Integration**: Ensure the specified style: {style}, is explicitly emphasized into the illustration prompt. Do this without altering the original narrative's descriptive content.
3. **No Text**: The illustration should not contain any textual elements.
4. **Single Prompt**: Produce one, and only one, succinct illustration prompt. It should be precise and not exceed two core sentences.

Process the narrative, extract its essence, and seamlessly blend in {style}.
"""

illustrator = """
You will be shown a text. Your job is to go through with an illustrators eye and list the three or four richest and most vivid few-word phrases used in the text that logically should be illustrated given the key content.

Once you do this, append a three more phrases that explicitly include and are related to {style}. 

Return the full list of SIX or SEVEN phrases ONLY. The entire list should be no longer than 40 words in total. DONT FORGET TO INCLUDE STYLE RELATED PHRASES!

NEVER OUTPUT ANY NSFW CONTENT OF ANY KIND.

Example output: 'Glowing book, soft glow of the setting sun, Labyrinth of narrow alleyways, Weight of centuries of history, Cobblestone streets; STYLE: trippy ethereal glow. Hyperrealistic 4K HD.'
"""

title_prompt = """
Here is the skeleton for a narrative:

{story}

Your job is to generate a very short but creative and memorable title for the story given this information and the OVERALL NARRATIVE ARC.

Do not make the title cheesy, corny, or generic.

Example outputs:
Synaptic Serenade
The Insiders
Walking Against Gravity

Bad output:
'The Dark Key: Following the Emperor' (GENERIC, NO QUOTATION MARKS)

Your title (DO NOT USE QUOTATION MARKS):
"""

# Genre to command mapping
genre_commands = {
    'Sci-Fi': 'Craft a captivating science fiction narrative.',
    'Fantasy': 'Weave an enchanting fantasy tale.',
    'Horror': 'Write a spine-chilling horror story.',
    'Romance': 'Narrate a heartfelt romance story.',
    'Mystery': 'Construct an intriguing mystery plot.'
}

# Initialize session state variables for the narrative scales
narrative_axes = [
    "seriousness", "whimsicality", "depth", "scariness", "romantic_intensity",
    "action_packed", "fantasy_level", "mysteriousness", "historical_setting", "humor_quotient"
]

# Dictionary mapping internal names to display names for narrative scales
narrative_display_names = {
    "seriousness": "**Seriousness**",
    "whimsicality": "**Whimsicality**",
    "depth": "**Depth**",
    "scariness": "**Scariness**",
    "romantic_intensity": "**Romantic Intensity**",
    "action_packed": "**Action-Packed**",
    "fantasy_level": "**Fantasy Level**",
    "mysteriousness": "**Mysteriousness**",
    "historical_setting": "**Historical Setting**",
    "humor_quotient": "**Humor Quotient**"
}

# loading_image_link = 'https://i.pinimg.com/originals/e2/a9/1e/e2a91e256baad2060ba177252f5cc88c.gif'
# loading_image_link = "https://cdn.pixabay.com/animation/2022/10/11/03/16/03-16-39-160_512.gif"
loading_image_link = 'https://giffiles.alphacoders.com/981/98105.gif'

# Natural language descriptions for each scale value
scale_descriptions = {
    "seriousness": {
        1: "light-hearted and jovial",
        2: "casually earnest",
        3: "balanced between playful and solemn",
        4: "mostly serious with rare moments of levity",
        5: "extremely serious and grave"
    },
    "whimsicality": {
        1: "completely grounded in reality",
        2: "mostly realistic with rare whimsical moments",
        3: "balanced mix of reality and whimsy",
        4: "distinctly whimsical with a touch of reality",
        5: "wildly eccentric and fantastical"
    },
    "depth": {
        1: "superficial and light",
        2: "somewhat shallow with moments of insight",
        3: "a balance of surface-level events and deep introspection",
        4: "rich in profound thoughts and deep dives",
        5: "extremely contemplative and profound"
    },
    "scariness": {
        1: "easy-going and comforting",
        2: "mild tension with rare creepy moments",
        3: "a mix of safe spaces and eerie events",
        4: "dark, chilling, with constant suspense",
        5: "nightmarishly terrifying"
    },
    "romantic_intensity": {
        1: "completely platonic",
        2: "minor romantic subplots or hints",
        3: "equal mix of romance and other themes",
        4: "love is a driving force in the narrative",
        5: "overwhelmingly romantic and passionate"
    },
    "action_packed": {
        1: "tranquil and serene",
        2: "occasional energetic moments",
        3: "good balance of action and calm",
        4: "frequent adrenaline-pumping events",
        5: "non-stop action and thrills"
    },
    "fantasy_level": {
        1: "entirely realistic",
        2: "slight supernatural or unreal elements",
        3: "equal mix of real-world and fantastical events",
        4: "high fantasy with magical realms and creatures",
        5: "a world entirely shaped by imagination and magic"
    },
    "mysteriousness": {
        1: "straightforward and predictable",
        2: "occasional unexpected twists",
        3: "some enigmas and puzzles to solve",
        4: "plot filled with secrets and hidden truths",
        5: "deeply enigmatic, where nothing is as it seems"
    },
    "historical_setting": {
        1: "set in the present day",
        2: "slight historical elements or flashbacks",
        3: "equal mix of past and present events",
        4: "deeply rooted in a past era",
        5: "set in a bygone civilization or ancient world"
    },
    "humor_quotient": {
        1: "solemn and serious",
        2: "occasional light-hearted moments",
        3: "good balance of humor and other emotions",
        4: "consistently funny and comedic",
        5: "an absolute laugh riot from start to finish"
    }
}


#alignment stuff!!!!!!!!!!!

alignment_maker = """
Welcome to the Alignment Simulation Calibration. Your task is to design a rich simulation environment that adapts dynamically to user decisions while testing their alignment strategies. 
Ensure that this environment is based on the user's specified preferences. Here's a synthesis of the critical context:

- **Type of Organization**: {organization_type_description}
- **Research Climate**: {cooperation_level_description}
- **AI Capability**: {ai_capability_description}
- **Regulatory Landscape**: {regulation_intensity_description}
- **Public Perception**: {public_perception_description}

CRITICAL CALIBRATIONS:
- **Alignment Subarea Focus**: {alignment_subarea_description}
- **Specific User Conditions & Scenarios**: {themes}

This is not the simulation itself, but rather, a rich, succinct, synthetic description of the preferences specified above. Make sure the prompt integrates all the preferences mentioned. The essence of this synthesis will inform and shape the course of the actual alignment simulation.

Remember, this alignment simulation is not just a test but also an educational tool. The user should leave with a greater understanding of the intricacies and complexities of AI alignment. Ensure your decisions and scenarios foster this understanding.
"""

alignment_template = """
Your primary task is to generate alignment simulation segments that resonate with the user's preferences and challenge their alignment decision-making. 

**Critical Context**:

- **Simulation Preferences & Setup**: {preferences}
  
- **Simulation Progress Summary**: {alignment_progress_so_far}

- **Last Segment of Simulation**: {last_alignment_chunk}

- **User's Last Decision**: {user_last_decision}

Guidelines for crafting the next simulation segment:
1. Stay true to the preferences and setup. They provide the framework for your simulation segment.
2. Each segment should be ONE technically focused and interesting paragraph.
3. MAKE THE SITUATIONS AS PRACTICAL, REALISTIC, AND TECHNICALLY RIGOROUS AS POSSIBLE GIVEN THE STORY PARAMETERS. This is for training alignment researchers to make better decisions, not entertaining them. Do not make the story overly dramatic or sci-fi.
4. Use your specific knowledge of the AI alignment field to make these scenarios realistic and plausible.
4. Immerse the user in a second-person perspective, making them a REALISTIC character within the alignment scenario.
5. Highlight the nuances, dilemmas, and subtleties of technical alignment problems. It's essential for the user to feel the weight of their decisions.
6. Consequences are pivotal. The repercussions of the user's decisions should be evident, challenging them to reflect and adapt.

**CRITICAL OUTPUT**: Every segment must end with two distinct technical choices (phrased as decisions, not questions) for the user to determine their next steps. They should be marked as 'OPTION 1:' and 'OPTION 2:', pushing the simulation scenario forward while offering different potential paths.

Example of an OPTION: 'Initiate a public awareness campaign', NOT 'You decide to initiate a public awareness campaign'

Upcoming simulation segment with OPTION 1 and OPTION 2:
"""

alignment_summary_template = """
Given the previous progress summary:
{previous_summary}

And the new chunk of the alignment simulation:
{new_chunk}

Synthesize and produce an updated progress summary for the alignment simulation so far.
"""

alignment_title_prompt = """
Here is the skeleton for an interactive alignment simulation:

{story}

Your job is to generate a very short and straightforward and creative title for the alignment simulation given this information.

Do not make the title cheesy, corny, or generic.

Format your output without any quotation marks.

Your title (NO QUOTATION MARKS):
"""

alignment_illustrator = """
You are picking out phrases for an illustrator in an interactive AI alignment simulation.

Please offer four phrases that it would be suitable to illustrate for the chunk of the simulation story you will see.

Keep it abstract and straightforward. Always include language about AI and AI alignment!

Once you do this, append a three more phrases that explicitly include and are related to {style}. 

Return the full list of SIX or SEVEN phrases ONLY. The entire list should be no longer than 40 words in total. DONT FORGET TO INCLUDE STYLE RELATED PHRASES!

Example output: 'superintelligent AI, alignment researchers, neural networks. STYLE: trippy ethereal glow. Hyperrealistic 4K HD.'
"""
