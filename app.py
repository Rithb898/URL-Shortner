from flask import Flask, render_template, request, jsonify, redirect
import random, string

app = Flask(__name__)

# In-memory database (for demo purposes)
url_db = {}

# Function to generate short URL
def generate_short_url():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/shorten', methods=['POST'])
def shorten_url():
    long_url = request.form.get('url')
    
    # Validate input
    if not long_url:
        return jsonify({'error': 'URL is required'}), 400
    
    # Generate short URL
    short_url = generate_short_url()
    
    # Save to "database"
    url_db[short_url] = long_url
    
    return jsonify({'result_url': request.host_url + short_url})

@app.route('/<short_url>')
def redirect_url(short_url):
    long_url = url_db.get(short_url)
    
    if long_url:
        return redirect(long_url)
    else:
        return jsonify({'error': 'Invalid short URL'}), 404

@app.route('/api/v1/shorten', methods=['POST'])
def api_shorten_url():
    data = request.get_json()
    long_url = data.get('url')
    
    if not long_url:
        return jsonify({'error': 'URL is required'}), 400
    
    short_url = generate_short_url()
    url_db[short_url] = long_url
    
    return jsonify({'result_url': request.host_url + short_url})


if __name__ == '__main__':
    app.run(debug=True)
