def generate_response(objects, question):
    """
    Generates a response based on detected objects and the user's question
    
    Args:
        objects: List of detected object names
        question: User's question about the image
    
    Returns:
        String response addressing the user's question
    """
    if not objects:
        return "I couldn't detect any objects in this image."
    
    # Basic processing - convert objects to a readable list with confidence levels
    object_list = ", ".join(objects[:10])  # Limit to top 10 objects
    
    # Check question types and provide appropriate responses
    question_lower = question.lower()
    
    if "what" in question_lower and ("see" in question_lower or "in this image" in question_lower or "in the image" in question_lower):
        return f"I can see the following objects in this image: {object_list}"
    
    elif "is there" in question_lower or "are there" in question_lower:
        # Check if any of the objects user is asking about are in our detected list
        words = question_lower.split()
        for word in words:
            if word in [obj.lower() for obj in objects]:
                return f"Yes, I can see {word} in the image."
        return f"I don't see what you're asking about specifically, but I do see: {object_list}"
    
    elif "how many" in question_lower:
        return f"I can identify about {len(objects)} distinct elements in this image, including {object_list}"
    
    elif "describe" in question_lower:
        return f"This image contains {object_list}. What would you like to know specifically about these objects?"
    
    else:
        # Generic response for other questions
        return f"You asked: '{question}'\nI detected these objects in the image: {object_list}"