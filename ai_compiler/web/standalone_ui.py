#!/usr/bin/env python3
"""
Standalone AI Compiler Web UI
Run this file directly: python standalone_ui.py
"""

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from datetime import datetime
import uvicorn

app = FastAPI()

# Simple pipeline simulator
class SimplePipeline:
    def run(self, prompt, quality):
        # Parse keywords
        prompt_lower = prompt.lower()
        
        if "crm" in prompt_lower:
            app_name = "CRM_System"
            tables = ["users", "contacts", "deals"]
            endpoints = ["/api/auth/login", "/api/contacts", "/api/deals"]
        elif "ecommerce" in prompt_lower or "shop" in prompt_lower:
            app_name = "EcommercePlatform"
            tables = ["products", "carts", "orders"]
            endpoints = ["/api/products", "/api/cart", "/api/checkout"]
        elif "todo" in prompt_lower or "task" in prompt_lower:
            app_name = "TodoApp"
            tables = ["users", "tasks"]
            endpoints = ["/api/tasks", "/api/tasks/{id}"]
        else:
            app_name = "GeneratedApp"
            tables = ["users"]
            endpoints = ["/api/users"]
        
        return {
            "success": True,
            "config": {
                "app_name": app_name,
                "version": "1.0.0",
                "database": {"tables": [{"name": t, "fields": ["id", "created_at"]} for t in tables]},
                "api": {"endpoints": [{"path": e, "methods": ["GET", "POST"]} for e in endpoints]},
                "ui": {"pages": ["/dashboard", "/profile"]},
                "auth": {"roles": ["admin", "user"]},
                "business_logic": []
            },
            "metrics": {"total_time_seconds": 0.5, "repair_attempts": 0}
        }

pipeline = SimplePipeline()

class GenRequest(BaseModel):
    prompt: str
    quality: str = "balanced"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>AI Compiler</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0;
            padding: 20px;
            min-height: 100vh;
        }
        .container {
            max-width: 1000px;
            margin: 0 auto;
        }
        .card {
            background: white;
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 20px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        }
        h1 {
            color: white;
            text-align: center;
            margin-bottom: 30px;
        }
        textarea {
            width: 100%;
            padding: 10px;
            border: 2px solid #ddd;
            border-radius: 10px;
            font-size: 16px;
        }
        button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 10px;
            font-size: 16px;
            cursor: pointer;
            width: 100%;
            margin-top: 10px;
        }
        button:hover {
            transform: translateY(-2px);
        }
        .result {
            margin-top: 20px;
            padding: 15px;
            background: #f5f5f5;
            border-radius: 10px;
            overflow-x: auto;
        }
        pre {
            background: #1e1e1e;
            color: #d4d4d4;
            padding: 15px;
            border-radius: 10px;
            overflow-x: auto;
        }
        .loading {
            text-align: center;
            display: none;
        }
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 20px auto;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🤖 AI Compiler - Generate Apps from Text</h1>
        
        <div class="card">
            <h2>📝 Describe Your App</h2>
            <textarea id="prompt" rows="4" placeholder="Example: Build a CRM with login, contacts, and dashboard..."></textarea>
            
            <div style="margin: 10px 0;">
                <strong>Quick Examples:</strong><br>
                <button class="example" style="width: auto; margin: 5px;" data-prompt="Build a CRM with login, contacts, dashboard">CRM</button>
                <button class="example" style="width: auto; margin: 5px;" data-prompt="Create an e-commerce platform with products and cart">E-commerce</button>
                <button class="example" style="width: auto; margin: 5px;" data-prompt="Build a todo app with tasks">Todo App</button>
            </div>
            
            <button id="generate">🚀 Generate Application</button>
            
            <div id="loading" class="loading">
                <div class="spinner"></div>
                <p>Generating your application... (5-stage pipeline)</p>
            </div>
        </div>
        
        <div id="resultCard" class="card" style="display: none;">
            <h2>✅ Generated Configuration</h2>
            <div id="result"></div>
        </div>
    </div>
    
    <script>
        document.querySelectorAll('.example').forEach(btn => {
            btn.addEventListener('click', () => {
                document.getElementById('prompt').value = btn.dataset.prompt;
            });
        });
        
        document.getElementById('generate').addEventListener('click', async () => {
            const prompt = document.getElementById('prompt').value;
            if (!prompt) {
                alert('Please enter a prompt');
                return;
            }
            
            document.getElementById('loading').style.display = 'block';
            document.getElementById('generate').disabled = true;
            document.getElementById('resultCard').style.display = 'none';
            
            try {
                const response = await fetch('/api/generate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ prompt, quality: 'balanced' })
                });
                const result = await response.json();
                
                if (result.success) {
                    document.getElementById('result').innerHTML = `<pre>${JSON.stringify(result.config, null, 2)}</pre>`;
                    document.getElementById('resultCard').style.display = 'block';
                } else {
                    alert('Error: ' + result.error);
                }
            } catch (error) {
                alert('Error: ' + error.message);
            } finally {
                document.getElementById('loading').style.display = 'none';
                document.getElementById('generate').disabled = false;
            }
        });
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def root():
    return HTMLResponse(HTML_TEMPLATE)

@app.post("/api/generate")
async def generate(req: GenRequest):
    result = pipeline.run(req.prompt, req.quality)
    return result

if __name__ == "__main__":
    print("\n" + "="*50)
    print("🚀 AI Compiler Web UI Starting...")
    print("="*50)
    print("\n📍 Open your browser: http://localhost:8000")
    print("💡 Try: 'Build a CRM with login and contacts'")
    print("⚡ Press Ctrl+C to stop\n")
    print("="*50 + "\n")
    uvicorn.run(app, host="127.0.0.1", port=8000)
