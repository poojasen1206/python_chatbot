from flask import Flask, render_template, request, jsonify
import requests


app = Flask(__name__)
API_URL = "base url"  
api_key = "your api key" 


headers = {
    'accept': 'application/json',
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}


def send_message(message, model="gpt-4o"):  # Replace "default_model" with the actual model name if needed
    """Send a message to the MyGenAssist API and get a response."""
    payload = {
        "messages": [{"role": "user", "content": message}],
        "model": model
    }
    
    response = requests.post(API_URL, json=payload, headers=headers)
    
    try:
        response_data = response.json()
    except ValueError:
        return "Error: Response is not in JSON format."

    if response.status_code == 200:
        message_content = response_data.get("choices")[0].get("message").get("content")
        return message_content
    else:
        return f"Error: {response.status_code} - {response_data}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json['message']
    bot_response = send_message(user_message)
    return jsonify({"response": bot_response})

if __name__ == "__main__":
    app.run(debug=True)