from google.cloud import aiplatform
import vertexai
from vertexai.preview.generative_models import GenerativeModel
from daisy_executive_assistant.tools.auth import get_creds, get_project_id

def _init_vertex():
    """Initializes Vertex AI SDK."""
    project_id = get_project_id()
    if not project_id:
        return "Error: Could not determine Project ID from credentials.json."
    
    creds = get_creds()
    vertexai.init(project=project_id, location='us-central1', credentials=creds)
    return None

def get_vertex_model_response(prompt: str, model_name: str = "gemini-pro") -> str:
    """Generates a response using a specific Vertex AI model.
    Useful for using specialized models or testing prompts.
    """
    err = _init_vertex()
    if err: return err

    try:
        model = GenerativeModel(model_name)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating content: {e}"

def list_vertex_models() -> str:
    """Lists available foundation models in Vertex AI."""
    # This mimics a basic listing, as full Model Garden API is complex.
    # Returns a curated list of popular models.
    return "Available Vertex Models: gemini-pro, gemini-pro-vision, gemini-ultra, text-bison, chat-bison"
