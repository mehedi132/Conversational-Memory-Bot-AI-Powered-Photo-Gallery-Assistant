from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get the current directory of this file (image_embedding.py)
current_dir = os.path.dirname(os.path.abspath(__file__))

# Move up TWO levels to reach the project root
project_root = os.path.abspath(os.path.join(current_dir, ".."))

# Construct the path to "config/api_key.txt"
data_path = os.path.join(project_root, "config", "api_key.txt")

def load_api_key():
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables. Please add it to your .env file.")
    return api_key

# Load API Key
api_key = load_api_key()

# Define the prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Answer the user's questions based on the conversation history."),
    MessagesPlaceholder(variable_name="history"),  # Placeholder for chat history
    ("human", "{input}")  # Placeholder for the current user input
])

# Initialize Gemini model
model = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=api_key,  # Replace with your actual key
    temperature=0.7
)

# Define the output parser
output_parser = StrOutputParser()

# Define the core chain
chain = prompt | model | output_parser

# Initialize memory to store chat history
memory = ConversationBufferMemory(
    return_messages=True  # Return messages as a list of HumanMessage/AIMessage objects
)

def get_session_history(session_id: str = "default_session") -> InMemoryChatMessageHistory:
    # Use the memory's chat_memory directly, ignoring session_id
    return memory.chat_memory

# Wrap the chain with RunnableWithMessageHistory
chatbot = RunnableWithMessageHistory(
    runnable=chain,
    get_session_history=get_session_history,
    input_messages_key="input",
    history_messages_key="history"
)



# Intent detection prompt

intent_prompt = PromptTemplate(
    input_variables=["input"],
    template="""You are an expert intent classifier tasked with analyzing a user input to determine whether they expect an image or text response. Given the input: "{input}", your goal is to interpret the words, context, and intent to classify the request as 'image' or 'text'. Follow these detailed guidelines:

1. **Explicit Visual Requests:**
   - If the user mentions 'image', 'picture', 'photo', 'diagram', 'chart', 'graph', 'map', 'sketch', 'drawing', or similar terms implying visual content, classify as 'image'.
   - Examples: "Show me a photo of a cat," "Draw a map of Europe," "Generate a chart of population growth."

2. **Explicit Textual Requests:**
   - If the user seeks information, explanations, descriptions, definitions, summaries, stories, or content naturally conveyed through words, classify as 'text'.
   - Examples: "Tell me about gravity," "Describe a sunset," "Summarize World War II."

3. **Verb Contextual Analysis:**
   - Analyze verbs like 'show', 'illustrate', 'depict', 'visualize', 'create', or 'make':
     - Paired with visual objects (e.g., "Show me a picture," "Illustrate with a diagram"), classify as 'image'.
     - Paired with processes or abstract ideas (e.g., "Show me how to code," "Illustrate how digestion works"), classify as 'text' unless a visual is specified.
   - Examples: "Show me a graph of sales" → 'image'; "Show me how photosynthesis works" → 'text'.

4. **Appearance-Focused Queries:**
   - If the user asks about visual traits (e.g., "What does a zebra look like?" "How does a galaxy appear?"), classify as 'image', as they likely expect a visual, even if unstated.
   - Examples: "What does a medieval castle look like?" → 'image'; "What does rain sound like?" → 'text'.

5. **Ambiguous or Unspecified Inputs:**
   - If intent is unclear or lacks indicators (e.g., "Help me," "What's this?"), default to 'text'—it's versatile and safer when uncertain. Single-word queries (e.g., "tiger", "apple") that do not specify a visual or appearance-focused intent should be classified as 'text', as they likely seek information or a description.
   - Examples: "tiger" → 'text'; "apple" → 'text'; "Surprise me" → 'text'; "Can you do something cool?" → 'text'.

6. **Non-Requests:**
   - For greetings, statements, or non-questions (e.g., "Hi there," "I love dogs," "Wow"), classify as 'text', assuming a conversational reply.
   - Examples: "Thanks!" → 'text'; "Cats are great" → 'text'.

7. **Mixed Requests:**
   - If both image and text are requested (e.g., "Explain gravity and draw a diagram"), prioritize 'image' if a visual is explicit; otherwise, default to 'text'.
   - Examples: "Tell me about stars and show a picture" → 'image'; "Explain coding and its benefits" → 'text'.

8. **Idiomatic or Figurative Language:**
   - Interpret phrases like "Paint a picture of the past" (description) or "Draw a conclusion" (deduction) as 'text' unless a literal visual is meant.
   - Examples: "Paint me a scene of war" → 'text'; "Paint me an image of war" → 'image'.

9. **Edge Cases:**
   - For ambiguous intent (e.g., "Make me laugh"), default to 'text' (e.g., a joke) unless a visual is specified (e.g., "Show a funny meme" → 'image').
   - For code-related queries (e.g., "What does this code look like running?"), classify as 'text' (output/explanation) unless a screenshot is requested.
   - Examples: "Make me happy" → 'text'; "Show me a happy picture" → 'image'; "What's this code's output?" → 'text'.

10. **Corner Cases:**
    - Empty input (""): classify as 'text' (e.g., "Please provide more details").
    - Nonsense (e.g., "xyz"): classify as 'text' (e.g., "I don't understand").
    - Questions about images without requesting one (e.g., "How are photos made?") → 'text'.

11. **Description of Visual Content:**
   - If the user requests a description, explanation, or analysis of an image, picture, or other visual content (e.g., "Describe the image," "Explain what's in the photo," "Analyze the chart"), classify as 'text', as the intent is to receive a textual response, not a visual.
   - Examples: "Describe the image" → 'text'; "What's happening in this picture?" → 'text'; "Explain the diagram" → 'text'.

**Output:**
Return ONLY 'image' or 'text' as plain text, reflecting the user's most likely intent based on the analysis.

Examples:
- "Draw a tiger" → 'image'
- "Tell me a tiger story" → 'text'
- "What does a tiger look like?" → 'image'
- "Explain tiger behavior" → 'text'
- "Show me how to draw" → 'text'
- "Show me a drawing" → 'image'
- "Paint a picture of love" → 'text'
- "Create an image of love" → 'image'
- "Hello" → 'text'
- "What's this?" → 'text'
- "Make me laugh with a picture" → 'image'
- "How does rain feel?" → 'text'
- "" → 'text'
- "xyz123" → 'text'
- "Describe and sketch a tree" → 'image'
- "tiger" → 'text'
- "apple" → 'text'
- "Describe the image" → 'text'
- "What's happening in this picture?" → 'text'
- "Explain the diagram" → 'text'
"""
)


# Create an intent detection chain
intent_chain = intent_prompt | model



# Function to process user input with intent detection
def process_input_langchain(user_input: str) -> str:
    # Step 1: Detect intent
    intent_response = intent_chain.invoke({"input": user_input})
    intent = intent_response.content.strip()  # Get the intent word (e.g., "conversation" or "images")
    return intent



image_match_with_text_prompt = PromptTemplate(
    input_variables=["image_data", "user_query"],
    template="""You are an expert assistant analyzing image descriptions and tags based on a user input query. Your input is a JSON string with exactly 10 unique image entries (indexed 0–9), each with:
- "path": a string (e.g., "img1.jpg"),
- "description": a string (e.g., "Two tigers in misty woods"),
- "tag": a list of strings (e.g., ["tiger", "forest"]).

**Important Context**:
- The input JSON is pre-sorted, with index 0 being the most relevant to the query and index 9 being the least relevant, based on prior similarity scoring (e.g., FAISS search). Your task is to respect this ranking while applying additional filtering and reasoning to ensure the best matches are selected.

**Your Task**:
1. **Analyze Input**:
   - Use the first 10 valid, unique entries (no duplicates by "path"). If the JSON is malformed or has fewer/more than 10 entries, process only the first 10 valid entries.
   - Consider both tags and descriptions for similarity to the user query: "{user_query}".

2. **Evaluate Similarity**:
   - **Step 1: Tag Matching**:
     - Prioritize exact tag matches (e.g., query "tiger" matches tag "tiger").
     - Allow synonymous tag matches (e.g., "woods" = "forest", "rain" = "storm", "bird" = "birds") using reasonable inference.
   - **Step 2: Description Matching**:
     - Look for thematic similarity in descriptions (e.g., "jungle cat" vs. "tiger in vines").
     - Infer specific details if relevant, such as colors (e.g., "golden"), counts (e.g., "two birds"), weather (e.g., "foggy"), or occasions (e.g., "dusk").
   - **Step 3: Respect Pre-Sorted Order**:
     - Start with the highest-ranked image (index 0) and proceed sequentially. Only skip an image if it has no tag or description similarity to the user query. Do not arbitrarily skip high-ranking images in favor of lower-ranking ones.

3. **Handle Edge Cases**:
   - **Vague Queries** (e.g., "animal"): Interpret broadly but prioritize relevance, favoring higher-ranked images.
   - **Empty Tags or Vague Descriptions** (e.g., "scene"): Rely on available data and query intent, but do not prioritize such images over those with clear matches.
   - **No Matches**: If no images match, return an empty result with the specified summary.

4. **Select Matches**:
   - Select 0–10 matching images, ensuring no duplicate "path" values.
   - Prioritize images with the strongest combined tag and description similarity to the user query, while respecting the pre-sorted order. For example, if images at indices 0, 1, and 2 match the query, they must be selected before considering images at indices 3–9.

5. **Return Format**:
   - Return a valid JSON object with:
     - "matched_images": a list of "path" strings (0–10 unique entries from input, ordered by relevance).
     - "summary": a 50-word narrative paragraph vividly describing shared traits—use rich imagery (e.g., "amber glow"), sensory details (e.g., "rustling leaves"), and specifics (colors, objects, counts, weather, occasions). Avoid generic phrasing.
     - "reasoning": a brief list of strings explaining why each matched image was selected (e.g., ["Exact tag match: tiger", "Description match: misty woods"]).
   - If no images match, return:
     - {{"matched_images": [], "summary": "No matching images surfaced from this vivid array of scenes.", "reasoning": ["No images matched the query criteria."]}}

**Output Constraints**:
- Output ONLY a valid JSON object (e.g., {{"matched_images": ["img1.jpg"], "summary": "...", "reasoning": ["..."]}}).
- Do not include additional text outside the JSON object.

**Examples**:
- User Query: "tigers in nature"
  - Input: [{{"path": "img1.jpg", "description": "Two golden tigers in woods", "tag": ["tiger", "forest"]}}, {{"path": "img2.jpg", "description": "Lion on plains", "tag": ["lion", "grass"]}}, ... (8 more)]
  - Output: {{"matched_images": ["img1.jpg"], "summary": "Two golden tigers roam misty woods, their amber coats aglow amidst towering trees. Leaves whisper underfoot as dappled sunlight filters through, painting a serene tableau of nature's wild heart, where the forest's quiet embrace cradles their majestic, untamed grace.", "reasoning": ["Exact tag match: tiger, forest; Description match: woods"]}}
- User Query: "sunny beach"
  - Input: [{{"path": "img1.jpg", "description": "Foggy hill", "tag": ["hill", "fog"]}}, ... (9 more, none beach-related)]
  - Output: {{"matched_images": [], "summary": "No matching images surfaced from this vivid array of scenes.", "reasoning": ["No images matched the query criteria."]}}
- User Query: "birds at dawn"
  - Input: [{{"path": "img1.jpg", "description": "Three red birds at sunrise", "tag": ["birds", "dawn"]}}, {{"path": "img2.jpg", "description": "Blue jay in morning mist", "tag": ["bird", "morning"]}}, ... (8 more)]
  - Output: {{"matched_images": ["img1.jpg", "img2.jpg"], "summary": "At dawn's tender blush, three red birds trill atop dew-kissed branches, while a blue jay soars through morning mist. Their vibrant plumes catch the first light, a soft chorus rising against a pastel sky, weaving nature's gentle awakening in serene harmony.", "reasoning": ["Exact tag match: birds, dawn; Description match: sunrise", "Synonymous tag match: bird, morning; Description match: morning mist"]}}

**Input JSON**: {image_data}
    """
)






similar_image_by_image_prompt = PromptTemplate(
    input_variables=["user_input", "image_data"],
    template="""You are an expert assistant analyzing image descriptions and tags against a user query provided as a JSON object: {user_input}, containing:
- "description": a string (e.g., "Three tigers in misty woods"),
- "tag": a list of strings (e.g., ["tiger", "forest"]).
Your input data is a JSON string with exactly 10 unique image objects (by "path"), each with:
- "path": a string (e.g., "img1.jpg"),
- "description": a string (e.g., "Tiger in dense forest"),
- "tag": a list of strings (e.g., ["tiger", "woods"]).

**Important Context**:
- The input JSON is pre-sorted, with index 0 being the most relevant to the query and index 9 being the least relevant, based on prior similarity scoring (e.g., FAISS search). Your task is to respect this ranking while applying additional filtering and reasoning to ensure the best matches are selected.

**Your Task**:
1. **Analyze Input**:
   - Use the first 10 valid, unique entries (no duplicates by "path"). If the JSON is malformed or has fewer/more than 10 entries, process only the first 10 valid entries.
   - Compare the query's tags and description to each image's tags and description for similarity.

2. **Evaluate Similarity**:
   - **Step 1: Tag Matching**:
     - Prioritize exact tag matches (e.g., query tag "tiger" matches image tag "tiger").
     - Allow synonymous tag matches (e.g., "woods" = "forest", "rain" = "storm", "bird" = "birds") using reasonable inference.
   - **Step 2: Description Matching**:
     - Look for thematic similarity in descriptions (e.g., "jungle cat" vs. "tiger in vines").
     - Infer specific details if relevant, such as colors (e.g., "golden"), counts (e.g., "two birds"), weather (e.g., "foggy"), or occasions (e.g., "dusk").
   - **Step 3: Respect Pre-Sorted Order**:
     - Start with the highest-ranked image (index 0) and proceed sequentially. Only skip an image if it has no tag or description similarity to the query. Do not arbitrarily skip high-ranking images in favor of lower-ranking ones.

3. **Handle Edge Cases**:
   - **Vague Queries** (e.g., {{"description": "animal", "tag": ["nature"]}}): Interpret broadly but prioritize relevance, favoring higher-ranked images.
   - **Empty Tags or Vague Descriptions** (e.g., "scene"): Rely on available data and query intent, but do not prioritize such images over those with clear matches.
   - **No Matches**: If no images match, return an empty result with the specified summary.

4. **Select Matches**:
   - Select 0–10 matching images, ensuring no duplicate "path" values.
   - Prioritize images with the strongest combined tag and description similarity, while respecting the pre-sorted order. For example, if images at indices 0, 1, and 2 match the query, they must be selected before considering images at indices 3–9.

5. **Return Format**:
   - Return a valid JSON object with:
     - "matched_images": a list of "path" strings (0–10 unique entries from input, ordered by relevance).
     - "summary": a 50-word narrative paragraph vividly describing shared traits—use rich imagery (e.g., "amber glow"), sensory details (e.g., "rustling leaves"), and specifics (colors, objects, counts, weather, occasions). Avoid generic phrasing.
     - "reasoning": a brief list of strings explaining why each matched image was selected (e.g., ["Exact tag match: tiger", "Description match: misty woods"]).
   - If no images match, return:
     - {{"matched_images": [], "summary": "No matching images surfaced from this vivid array of scenes.", "reasoning": ["No images matched the query criteria."]}}

**Output Constraints**:
- Output ONLY a valid JSON object (e.g., {{"matched_images": ["img1.jpg"], "summary": "...", "reasoning": ["..."]}}).
- Do not include additional text outside the JSON object.

**Examples**:
- Query: {{"description": "tigers in nature", "tag": ["tiger", "nature"]}}
  - Input: [{{"path": "img1.jpg", "description": "Two golden tigers in woods", "tag": ["tiger", "forest"]}}, {{"path": "img2.jpg", "description": "Lion on plains", "tag": ["lion", "grass"]}}, ... (8 more)]
  - Output: {{"matched_images": ["img1.jpg"], "summary": "Two golden tigers roam misty woods, their amber coats aglow amidst towering trees. Leaves whisper underfoot as dappled sunlight filters through, painting a serene tableau of nature's wild heart, where the forest's quiet embrace cradles their majestic, untamed grace.", "reasoning": ["Exact tag match: tiger; Synonymous tag match: forest = nature; Description match: woods"]}}
- Query: {{"description": "sunny beach", "tag": ["beach", "sun"]}}
  - Input: [{{"path": "img1.jpg", "description": "Foggy hill", "tag": ["hill", "fog"]}}, ... (9 more, none beach-related)]
  - Output: {{"matched_images": [], "summary": "No matching images surfaced from this vivid array of scenes.", "reasoning": ["No images matched the query criteria."]}}
- Query: {{"description": "birds at dawn", "tag": ["birds", "morning"]}}
  - Input: [{{"path": "img1.jpg", "description": "Three red birds at sunrise", "tag": ["birds", "dawn"]}}, {{"path": "img2.jpg", "description": "Blue jay in morning mist", "tag": ["bird", "morning"]}}, ... (8 more)]
  - Output: {{"matched_images": ["img1.jpg", "img2.jpg"], "summary": "At dawn's tender blush, three red birds trill atop dew-kissed branches, while a blue jay soars through morning mist. Their vibrant plumes catch the first light, a soft chorus rising against a pastel sky, weaving nature's gentle awakening in serene harmony.", "reasoning": ["Exact tag match: birds; Synonymous tag match: dawn = morning; Description match: sunrise", "Synonymous tag match: bird = birds, morning; Description match: morning mist"]}}

Input JSON: {image_data}
    """
)




gallery_image_match_with_text_prompt = PromptTemplate(
    input_variables=["user_query", "image_metadata"],
    template="""You are an expert assistant tasked with analyzing image metadata to deliver a detailed, narrative response based on a user-provided query, while also accurately answering direct questions about the presence of specific elements. Your input includes:
- User query: "{user_query}" (this can be any type of query, such as a question, a description, a request, or any other form of inquiry, including direct questions like "Is a cycle in the image?").
- Image metadata: a single JSON object containing:
  - "tags": a list of strings tagging the image (e.g., ["birds", "red", "rain"]),
  - "description": a string describing the image content (e.g., "A pair of red birds perched on a branch in the rain").

Your task is to:
1. **Analyze Metadata**: Examine the tags and description of the provided image in the context of the user query.
2. **Handle Direct Questions**: If the query is a direct question (e.g., "Is a cycle in the image?" or "Does the image contain birds?"), first provide a concise, accurate answer (e.g., "Yes, a cycle is present" or "No, a cycle is not present") based solely on the tags and description. Look for exact matches or synonyms (e.g., "bicycle" for "cycle") in the tags or description.
3. **Assess Metadata Relevance**: Assess how well the image's metadata matches or relates to the query, considering:
   - Exact or synonymous matches in tags (e.g., "storm" vs. "rain", "bicycle" vs. "cycle").
   - Descriptive themes (e.g., "sunset" might imply "evening").
   - Inferred details like colors, object counts, weather, occasions, or settings, even if not explicitly mentioned.
4. **Craft a Narrative Response**: Regardless of the query type, craft a vivid, narrative-style response (at least 50 words) addressing the query, weaving in:
   - Specific details: colors (e.g., "crimson"), objects (e.g., "three deer"), counts, weather (e.g., "misty dawn"), occasions (e.g., "festive gathering").
   - Sensory richness: sights, sounds, or moods (e.g., "whispering winds").
   - For direct questions, include the concise answer within the narrative or as a prefix to it.
5. **Return JSON Output**: Return a valid JSON object with:
   - "answer": a string containing your response, which includes the concise answer (if applicable) followed by the detailed narrative.
6. **Handle Corner Cases**:
   - If metadata is malformed, empty, or insufficient (e.g., vague tags like ["nature"] for a specific query), return:
     - {{"answer": "Insufficient information to fully address the query amidst the sparse or unclear metadata."}}
   - If the query is vague (e.g., "scene"), interpret broadly but stay grounded in the data provided by the tags and description.
7. **Output Format**: Output ONLY a valid JSON object (e.g., {{"answer": "..."}}). No plain text or invalid JSON.

Examples:
- Query: "Is a cycle in the image?"
  - Metadata: {{ "tags": ["bicycle", "park"], "description": "A red bicycle leaning against a tree in a park"}}
  - Output: {{"answer": "Yes, a cycle is present. Amidst the serene expanse of a sunlit park, a crimson bicycle leans lazily against a gnarled tree, its metal frame glinting in the golden rays. The gentle rustle of leaves whispers through the air, mingling with the distant laughter of unseen picnickers, painting a scene of tranquil leisure."}}
- Query: "red birds in nature"
  - Metadata: {{ "tags": ["birds", "red", "forest"], "description": "Two red birds on a green branch"}}
  - Output: {{"answer": "In this serene scene, two crimson birds perch gracefully on a vibrant green branch, nestled within a whispering forest. Their vivid feathers gleam under dappled sunlight, a symphony of nature's hues unfolding amidst rustling leaves and the faint trill of distant companions."}}
- Query: "sunny beach party"
  - Metadata: {{ "tags": ["hill", "cloud"], "description": "A cloudy hill"}}
  - Output: {{"answer": "Insufficient information to fully address the query amidst the sparse or unclear metadata."}}
- Query: "Is a cycle in the image?"
  - Metadata: {{ "tags": ["birds", "red"], "description": "Two red birds on a branch"}}
  - Output: {{"answer": "No, a cycle is not present. Instead, the scene unveils two crimson birds perched delicately on a slender branch, their scarlet feathers glowing against a backdrop of verdant leaves. The air hums with the soft trill of their song, a melody woven into the fabric of a tranquil forest."}}

Input metadata: {image_metadata}
    """
)

image_analysis_prompt = PromptTemplate(
    input_variables=["user_query"],
    template="""You are an advanced vision assistant with exceptional image analysis skills, tasked with interpreting up to 10 unique images (no duplicates by path, if provided) based on a user query: "{user_query}". For each image:
1. Analyze meticulously to identify:
   - Objects present (e.g., "three deer", "a crimson car"), including counts if discernible.
   - Dominant colors (e.g., "golden hues", "deep azure").
   - A detailed scene description (e.g., "mist veils a forest at dawn").
   - Scene type (e.g., landscape, portrait, action, still life).
   - Movement or dynamic elements (e.g., "waves crashing", "birds soaring"), if visible.
   - Inferred details: weather (e.g., "rainy dusk"), occasion (e.g., "festive dusk"), mood (e.g., "serene").
2. Craft a 50-word, narrative response addressing the query in natural, beautiful language, weaving:
   - Sensory details: colors, textures, sounds (e.g., "whispering winds").
   - Specific elements: objects, counts, weather, or occasion relevant to the query.
3. Handle corner cases:
   - If multiple images (up to 10), focus on the most relevant ones; ignore duplicates (by path, if available).
   - If no image is attached or analysis fails (e.g., corrupted data), return: "Unable to analyze the image due to missing or unreadable content."
   - If the query is vague (e.g., "what's here?"), describe the scene broadly but vividly.
   - If the query can't be answered (e.g., "smell of rain" from visuals), return: "The query exceeds visual analysis; insufficient data to respond fully."
4. Return ONLY plain text (50 words max), not JSON or structured data.

Examples:
- Query: "What animals are in the image?"
  - Image: Three deer in a snowy field
  - Output: "Three graceful deer stand poised in a snow-draped field, their tawny coats stark against the glistening white. Frost clings to their antlers as a chilly breeze ripples through, painting a serene winter tableau under a pale, overcast sky."
- Query: "Describe the weather"
  - Image: Ocean waves under a stormy sky
  - Output: "Dark storm clouds churn above a restless ocean, where slate-gray waves crash with wild fervor. The air hums with the scent of rain, as jagged lightning briefly illuminates the tempestuous scene unfolding beneath a brooding, windswept sky."
- Query: "What's the mood?"
  - Image: A lone tree in fog
  - Output: "A lone tree emerges from swirling fog, its gnarled branches draped in muted grays. Silence reigns in this ethereal haze, casting a melancholic yet tranquil mood over the misty landscape, where time seems to pause in quiet reflection."
- Query: "Who's in the room?"
  - Image: Empty desert
  - Output: "The query exceeds visual analysis; this vast desert, with golden sands stretching under a blazing sun, holds no rooms or figures, only the whisper of wind across endless dunes."

Attached image(s) metadata or context: {{image_context}} (if provided; otherwise, assume single image analysis).
    """
)


# Define the prompt template


basic_text_prompt = PromptTemplate(
    input_variables=["input_text"],
    template="""
You are a helpful AI assistant. Your task is to generate a response based on the following input text. Please provide a clear, concise, and accurate response in plain text format. Do not include any JSON, markdown, or other formatting in your response—just return the plain text answer.

Input text: {input_text}

Response:
"""
)