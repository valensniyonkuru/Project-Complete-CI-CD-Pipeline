from flask import Flask, jsonify, render_template_string
import os
import socket
from datetime import datetime

app = Flask(__name__)

# HTML template for the landing page with enhanced styling and dynamic content injection
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CI/CD Pipeline Demo</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
        }
        .container {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
            border: 1px solid rgba(255, 255, 255, 0.18);
            max-width: 600px;
            text-align: center;
        }
        h1 {
            font-size: 2.5em;
            margin-bottom: 20px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }
        .emoji {
            font-size: 4em;
            margin: 20px 0;
            animation: bounce 2s infinite;
        }
        @keyframes bounce {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-20px); }
        }
        .info {
            background: rgba(255, 255, 255, 0.2);
            border-radius: 10px;
            padding: 20px;
            margin-top: 30px;
            text-align: left;
        }
        .info-item {
            margin: 10px 0;
            display: flex;
            justify-content: space-between;
        }
        .label {
            font-weight: bold;
        }
        .endpoints {
            margin-top: 20px;
        }
        .endpoint {
            background: rgba(255, 255, 255, 0.1);
            padding: 10px;
            border-radius: 5px;
            margin: 5px 0;
            font-family: 'Courier New', monospace;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 CI/CD Pipeline Demo</h1>
        <div class="emoji">✅</div>
        <p style="font-size: 1.2em; margin: 20px 0;">
            Deployed successfully via Jenkins!
        </p>
        <div class="info">
            <div class="info-item">
                <span class="label">Hostname:</span>
                <span>{{ hostname }}</span>
            </div>
            <div class="info-item">
                <span class="label">Version:</span>
                <span>{{ version }}</span>
            </div>
            <div class="info-item">
                <span class="label">Timestamp:</span>
                <span>{{ timestamp }}</span>
            </div>
        </div>
        <div class="endpoints">
            <h3>Available Endpoints:</h3>
            <div class="endpoint">GET /</div>
            <div class="endpoint">GET /health</div>
            <div class="endpoint">GET /info</div>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    """Main landing page"""
    return render_template_string(
        HTML_TEMPLATE,
        hostname=socket.gethostname(),
        version=os.environ.get('APP_VERSION', '1.0.0'),
        timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )

@app.route('/health')
def health():
    """Health check endpoint for monitoring"""
    return jsonify({
        'status': 'healthy',
        'service': 'cicd-demo-app',
        'timestamp': datetime.now().isoformat()
    }), 200

@app.route('/info')
def info():
    """Application information endpoint"""
    return jsonify({
        'application': 'CI/CD Pipeline Demo',
        'version': os.environ.get('APP_VERSION', '1.0.0'),
        'hostname': socket.gethostname(),
        'environment': os.environ.get('ENVIRONMENT', 'production'),
        'python_version': os.sys.version,
        'endpoints': {
            'home': '/',
            'health': '/health',
            'info': '/info'
        }
    }), 200

if __name__ == '__main__':
    # Get port from environment or use default
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
