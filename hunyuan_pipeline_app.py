from flask import Flask, request, jsonify, send_file
import base64
import os
import json
import tempfile
from PIL import Image
import io

app = Flask(__name__)

# Configure upload settings
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def decode_base64_image(base64_string):
    """Decode base64 image and save to temp file"""
    try:
        # Remove data URL prefix if present
        if 'data:image' in base64_string:
            base64_string = base64_string.split(',')[1]
        
        # Decode base64
        image_data = base64.b64decode(base64_string)
        
        # Create temp file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
        temp_file.write(image_data)
        temp_file.close()
        
        return temp_file.name
    except Exception as e:
        raise ValueError(f"Failed to decode image: {str(e)}")

def generate_3d_model(image_path, prompt=""):
    """
    Placeholder for your actual 3D generation function
    Replace this with your Hunyuan3D implementation
    """
    # This is where you'd call your 3D generation model
    print(f"Processing image: {image_path}")
    print(f"Prompt: {prompt}")
    
    # For testing, create a dummy GLB file
    output_path = os.path.join(OUTPUT_FOLDER, 'output.glb')
    with open(output_path, 'wb') as f:
        f.write(b'dummy glb content for testing')
    
    return output_path

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "hunyuan3d-api"})

@app.route('/generate', methods=['POST'])
def generate_3d():
    """Main endpoint for 3D generation"""
    try:
        # Parse JSON input
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        # Extract image and prompt
        image_base64 = data.get('image')
        prompt = data.get('prompt', '')
        
        if not image_base64:
            return jsonify({"error": "No image provided"}), 400
        
        # Decode and save image
        image_path = decode_base64_image(image_base64)
        
        # Generate 3D model
        output_path = generate_3d_model(image_path, prompt)
        
        # Read GLB file and encode to base64 for response
        with open(output_path, 'rb') as f:
            glb_data = f.read()
            glb_base64 = base64.b64encode(glb_data).decode('utf-8')
        
        # Clean up temp files
        os.unlink(image_path)
        
        return jsonify({
            "success": True,
            "glb_base64": glb_base64,
            "message": "3D model generated successfully"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/generate-file', methods=['POST'])
def generate_3d_file():
    """Alternative endpoint that returns GLB file directly"""
    try:
        data = request.get_json()
        image_base64 = data.get('image')
        prompt = data.get('prompt', '')
        
        if not image_base64:
            return jsonify({"error": "No image provided"}), 400
        
        # Process image
        image_path = decode_base64_image(image_base64)
        output_path = generate_3d_model(image_path, prompt)
        
        # Return GLB file directly
        return send_file(output_path, 
                        as_attachment=True, 
                        download_name='generated_model.glb',
                        mimetype='model/gltf-binary')
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("Starting Hunyuan3D API server...")
    print("Health check: http://localhost:8080/health")
    print("Generate endpoint: http://localhost:8080/generate")
    app.run(host='0.0.0.0', port=8080, debug=True)
