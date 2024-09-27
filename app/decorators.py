import functools
import time


from flask import  jsonify, request

from app.config import Config
import aiohttp
import asyncio

def validate_uploaded_document(func):
    """
    Validate uploaded document if it is exists, valid, and its mimetype is `application/pdf` which located on the body of request and its name is `document`
    """

    @functools.wraps(func)
    def validate(*args, **kwrgs):
        if "document" not in request.files:
            return {"message": "Request does not contain proper document."}, 422

        file = request.files.get("document")
        file_mimetype = file.mimetype

        if file_mimetype != "application/pdf":
            return {"message": f"{file_mimetype} extension is not supported."}, 422
        return func(*args, **kwrgs)

    return validate


def timing_decorator(func):
    """
    Count function execution time

    Returns:
    - Prints the execution time on in terminal in seconds.
    """

    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Execution time: {end_time - start_time} seconds")
        return result

    return wrapper


def handle_exceptions(func):
    @functools.wraps(func)
    def wrapper(*args, **kwrgs):
        try:
            return func(*args, **kwrgs)
        except Exception as e:
            if Config.DEBUG:
                return jsonify({"message": f"Service Exception Message: {str(e)}"}), 500

            # TODO: Build error page.
            return jsonify({"message": "Service Exception."}), 500

    return wrapper




async def fetch_summarization(session, paragraph):
    start_time = time.time()
    async with session.post("http://127.0.0.1:5000/summarized_text", json={"paragraph": paragraph}) as response:
        if response.status == 200:
            data = await response.json()
            end_time = time.time()
            print(f"Summarization fetched in {end_time - start_time:.2f} seconds")
            return data['summarization']
        else:
            raise ValueError("Failed to generate summarization")

async def fetch_image(session, subtitle):
    start_time = time.time()
    async with session.post("http://127.0.0.1:5000/generate-summarization-image", json={"summary": subtitle}) as response:
        if response.status == 201:
            data = await response.json()
            end_time = time.time()
            print(f"Image fetched in {end_time - start_time:.2f} seconds")
            return data['url']
        else:
            raise ValueError("Failed to generate image")

async def generate_summarization(paragraph):
    async with aiohttp.ClientSession() as session:
        return await fetch_summarization(session, paragraph)

async def generate_image(subtitle):
    async with aiohttp.ClientSession() as session:
        return fetch_image(session, subtitle)

async def generate_summarizations_and_images(paragraphs, subtitles , main_title ):
    summarizations = await asyncio.gather(*(generate_summarization(p) for p in paragraphs))
    
    if len(summarizations) != len(subtitles):
        raise ValueError("The number of subtitles must match the number of paragraphs.")
    async with aiohttp.ClientSession() as session:
        subtitles.append(main_title)
        tasks = [asyncio.ensure_future(fetch_image(session , s)) for s in subtitles]
        images = await asyncio.gather(*tasks)      
    return summarizations, images

