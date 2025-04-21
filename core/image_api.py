import os
import base64
from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2

# Clarifai API settings
USER_ID = 'rpzauwrxgmyw'
PAT = '9f78c9efeae84556be358e71a4b6f3a4'
APP_ID = 'neuroai'
WORKFLOW_ID = 'general-image-recognition-workflow-z9qzgo'

def detect_objects(image_source):
    """
    Detects objects in an image using Clarifai API via gRPC
    
    Args:
        image_source: Can be a URL or local file path
    
    Returns:
        List of detected object names or None if detection fails
    """
    try:
        # Setup the Clarifai gRPC client
        channel = ClarifaiChannel.get_grpc_channel()
        stub = service_pb2_grpc.V2Stub(channel)
        metadata = (('authorization', 'Key ' + PAT),)
        user_data_object = resources_pb2.UserAppIDSet(user_id=USER_ID, app_id=APP_ID)
        
        # Determine if the image_source is a URL or local file
        if image_source.startswith(('http://', 'https://')):
            # Process URL-based image
            input_object = resources_pb2.Input(
                data=resources_pb2.Data(
                    image=resources_pb2.Image(
                        url=image_source
                    )
                )
            )
        else:
            # Process local file
            with open(image_source, 'rb') as f:
                file_bytes = f.read()
            
            input_object = resources_pb2.Input(
                data=resources_pb2.Data(
                    image=resources_pb2.Image(
                        base64=file_bytes
                    )
                )
            )
        
        # Make the API request using the workflow
        workflow_response = stub.PostWorkflowResults(
            service_pb2.PostWorkflowResultsRequest(
                user_app_id=user_data_object,
                workflow_id=WORKFLOW_ID,
                inputs=[input_object]
            ),
            metadata=metadata
        )
        
        # Check if the request was successful
        if workflow_response.status.code != status_code_pb2.SUCCESS:
            print(f"Error from Clarifai API: {workflow_response.status.description}")
            return None
        
        # Process results
        results = workflow_response.results[0]
        detected_objects = []
        
        # Extract concepts from each model output
        for output in results.outputs:
            for concept in output.data.concepts:
                # Only add concepts with confidence > 0.5
                if concept.value > 0.5:
                    detected_objects.append({
                        'name': concept.name,
                        'confidence': concept.value
                    })
        
        # Extract just the names for backward compatibility
        object_names = [obj['name'] for obj in detected_objects]
        return object_names
    
    except Exception as e:
        print(f"Exception during object detection: {e}")
        return None