from flask import Blueprint, request, jsonify, render_template
from app.validators import validate_text_is_not_empty, validate_text_regenerating_input
from app.connectors import connect_open_ai_service, connect_open_ai_chatbot, connect_language_services
from app.decorators import handle_exceptions

from typing import Dict
import json
import os

summarization_bp = Blueprint("summarization", __name__)

@summarization_bp.route("/generate-summarization-image", methods=["POST"])
@handle_exceptions
@validate_text_is_not_empty("summary")
def generate_summarization_image() -> Dict[str, str]:
    """
    Generates an Image that describes summarized text using DallE-3 model.

    Returns:
    - A JSON object containing:
    - "message": A success message.
    - "url": The URL of the generated image.
    """
    # Retrieve 'summary' and 'mainTitle' from the request body
    summary = request.get_json().get('summary')
    maintitle = request.get_json().get('mainTitle')

# Neutral and professional prompt structure
    prompt = (
        f"Create an educational, professional, and neutral illustration of the concept '{summary}' "
        f"within the broader context of '{maintitle}'. "
        "The image should focus on abstract, educational elements, and avoid sensitive content."
    )
    client = connect_open_ai_service()

    result = client.images.generate(model="dall-e-3", prompt=prompt, n=1)

    url = json.loads(result.model_dump_json())["data"][0]["url"]

    return {
        "message": "Image generated successfully.",
        "url": url,
    }, 201

@summarization_bp.route("/regenerate-summarization-content", methods=['POST'])
@handle_exceptions
@validate_text_regenerating_input
def regenerate_summarization_content():
    """
    Regenerate and summarize summarized content using OpenAI

    This function uses OpenAI chatbot to regenerate and summarize summarized text
    by building new prompt, the inject the prompt into chatbot.
    """
    text = request.get_json().get("text")

    client = connect_open_ai_chatbot()
    
    n_tokens = text.split(' ')

    prompt = (
        f"You are a genius chat bot, regenerate and summarize this text for me \n{text}"
    )

    response = client.completions.create(
        model=os.getenv("OPEN_AI_CHAT_DEBLOYMENT_NAME"),
        prompt=prompt,
        temperature=1,
        max_tokens=n_tokens,
        top_p=0.5,
        frequency_penalty=0,
        presence_penalty=0,
        best_of=1,
        stop=None,
    )

    return {
        "message": "Text summarized successfully.",
        "text": response.choices[0].text,
    }

@summarization_bp.route("/summarized_text", methods=["POST"])
def summarized_text():
    paragraph = request.json.get("paragraph")   
    if not paragraph:
        return jsonify({'error': 'Invalid data'}), 400
    if len(paragraph.split()) < 35 or paragraph==None:
        return (
            jsonify({"error": "Invalid input: paragraph must be more that 35 words"}),
            422,
        )  
    text_analytics_client = connect_language_services()
    summarized_texts = []
    poller = text_analytics_client.begin_abstract_summary([paragraph])
    abstract_summary_results = poller.result()
    for result in abstract_summary_results:
        if result.kind == "AbstractiveSummarization":
            [summarized_texts.append(summary.text) for summary in result.summaries]
        elif result.is_error is True:
            print(
                "...Is an error with code '{}' and message '{}'".format(
                    result.error.code, result.error.message
                )
            )
    return jsonify({'summarization': summarized_texts[0]}), 200

