from flask import Blueprint, request,  redirect, url_for, render_template
from app.validators import validate_uploaded_document
from app.connectors import connect_document_intelligence_service
import json
from flask_jwt_extended import decode_token
from jwt import ExpiredSignatureError, InvalidTokenError
import json

mind_map_bp = Blueprint("mind_map", __name__)

# Middleware to check JWT token before every request to the mind_map page
@mind_map_bp.before_request
def check_token():
    if request.endpoint == 'mind_map.func':  # Use your actual endpoint
        token = request.cookies.get('access_token_cookie')
        if not token:
            return redirect(url_for('authentication.signin'))
        try:
            # Manually decode the token
            decoded_token = decode_token(token)
            user_identity = decoded_token.get('sub')  # Get the user identity
            if not user_identity:
                return redirect(url_for('authentication.signin'))
        except (ExpiredSignatureError, InvalidTokenError) as e:
            # Redirect to signin if token is expired or invalid
            return redirect(url_for('authentication.signin'))
        
@mind_map_bp.route('/generate-mind-map', methods=['POST'])
@validate_uploaded_document
def generat_new_mind_map():
    document = request.files.get("document")
    #to display file name after uploading
    file_name = document.filename
    # generate_new_mind_map
    document_analysis_client = connect_document_intelligence_service()
    poller = document_analysis_client.begin_analyze_document(
        "prebuilt-layout", document=document
    )
    result = poller.result()

    # Convert paragraphs to a list of dictionaries
    paragraphs = [p.to_dict() for p in result.paragraphs]

    # Create a dictionary to map section headings to their paragraphs
    paragraphs_dict = {}
    current_section_heading = None

    for paragraph in result.paragraphs:
        if paragraph.role == "title":
            # There should only be one title
            main_title = paragraph.content
        elif paragraph.role == "sectionHeading":
            # Save paragraphs for the previous section heading if it exists
            if (
                current_section_heading
                and current_section_heading not in paragraphs_dict
            ):
                paragraphs_dict[current_section_heading] = []
            # Update the current section heading
            current_section_heading = paragraph.content
            if current_section_heading not in paragraphs_dict:
                paragraphs_dict[current_section_heading] = []
        elif paragraph.role is None and current_section_heading:
            # Append paragraphs to the current section heading
            paragraphs_dict[current_section_heading].append(paragraph.content)
    output = {
        "mainTitle": main_title if "main_title" in locals() else "",
        "picture": None,
        "subtitles": [
            {
                "subtitle": section_heading,
                "paragraphs": paragraphs_dict.get(section_heading, []),
                "picutre" : None,
                "summarization": None
            }
            for section_heading in paragraphs_dict
        ],
    }
    

    #save structure in structure_output.json file
    with open("structured_output.json", "w") as f:
        json.dump(output, f)
    return render_template('mindMap.html', output=output,file_name=file_name)


@mind_map_bp.route("/mindMap")
def func():
    # TODO: paragraphs should be singlular and key value pair insted of key array pair
    output = {
            "mainTitle": "The Future of Artificial Intelligence",
            "subtitles": [
                {
                    "paragraphs": [
                        "The continued advancements in machine learning techniques will heavily shape the future of artificial intelligence. As computing power and data availability increase, we can expect to see even more sophisticated models emerge that can tackle increasingly complex problems. This could lead to breakthroughs in natural language processing, computer vision, and predictive analytics, allowing AI systems to understand and interact with the world in more human-like ways. With further progress in deep learning, reinforcement learning, and other cutting-edge machine learning approaches, the capabilities of AI will continue to expand, enabling it to become an indispensable tool across a wide range of industries and applications."
                    ],
                    "subtitle": "Advancements in Machine Learning:",
                },
                {
                    "paragraphs": [
                        "The future of AI will also be defined by its deeper integration with other emerging technologies. As AI becomes more embedded in internet-connected devices, the Internet of Things, and advanced robotics, it will enable a new generation of smart and autonomous systems. This convergence of AI with technologies like 5G, edge computing, and quantum computing could lead to unprecedented levels of speed, efficiency, and intelligence in areas like autonomous vehicles, smart cities, and personalized healthcare. Additionally, the fusion of AI with biotechnology, nanotechnology, and neurotechnology could pave the way for transformative breakthroughs in fields like human-machine interfaces, neural implants, and synthetic biology."
                    ],
                    "subtitle": "Integration with Emerging Technologies:",
                },
                {
                    "paragraphs": [
                        "As AI becomes more powerful and ubiquitous, the ethical implications of its development and deployment will become increasingly crucial. Questions around privacy, bias, transparency, and the societal impact of AI-driven decision-making will need to be carefully addressed. Policymakers, researchers, and industry leaders will have to work together to establish robust ethical frameworks and governance structures to ensure that AI is developed and used in a responsible and accountable manner, benefiting humanity as a whole."
                    ],
                    "subtitle": "Ethical Considerations:",
                },
                {
                    "paragraphs": [
                        "The future of AI may also involve the democratization of the technology, making it more accessible and usable by a wider range of individuals and organizations. As AI tools and platforms become more user- friendly and affordable, they could empower small businesses, entrepreneurs, and even individual citizens to leverage the power of AI in their daily lives and problem-solving efforts. This democratization could lead to a surge of innovation and the emergence of AI-driven solutions tailored to local and niche needs, fostering greater inclusivity and diversity in the AI ecosystem."
                    ],
                    "subtitle": "Democratization of AI :",
                },
                {
                    "paragraphs": [
                        "One of the most ambitious and intriguing aspects of the AI\u0027s future is the potential development of Artificial General Intelligence (AGI) - AI systems that possess human-level or even superhuman cognitive abilities across a wide range of domains. While the path to AGI remains uncertain and fraught with challenges, continued advancements in areas like deep learning, neuroscience, and computing could bring us closer to this transformative milestone. The emergence of AGI could fundamentally reshape our world, opening up new frontiers in science, technology, and human development, but also raising profound questions about the implications for society, the economy, and the very nature of intelligence itself."
                    ],
                    "subtitle": "Artificial General Intelligence:",
                },
            ],
        }
    
    #save structure in structure_output.json file
    with open("structure_output.json", "w") as f:
        json.dump(output, f)

    return render_template("mindMap.html", output=output)
