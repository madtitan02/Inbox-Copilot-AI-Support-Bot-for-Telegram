#!/usr/bin/env python3
from flask import Flask, render_template, request, jsonify
import sys
from pathlib import Path
import json

# Add the BlazeQuery directory to the path
sys.path.append(str(Path(__file__).parent / "blaze_docs" / "BlazeQuery"))

from blaze_copilot import BlazeCopilot

app = Flask(__name__)

# Initialize the copilot
try:
    copilot = BlazeCopilot()
    print("Blaze Copilot web interface initialized!")
except Exception as e:
    print(f"Error initializing Blaze Copilot: {e}")
    copilot = None

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def query():
    """Handle query requests"""
    if not copilot:
        return jsonify({
            'error': 'Blaze Copilot not initialized. Please run setup first.',
            'success': False
        })
    
    try:
        data = request.get_json()
        user_query = data.get('query', '').strip()
        
        if not user_query:
            return jsonify({
                'error': 'Please provide a query',
                'success': False
            })
        
        # Get response from copilot
        response = copilot.ask(user_query, show_details=False)
        
        return jsonify({
            'success': True,
            'query': user_query,
            'answer': response['answer'],
            'confidence': response['confidence'],
            'sources': response['sources']
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Error processing query: {str(e)}',
            'success': False
        })

@app.route('/history')
def get_history():
    """Get conversation history"""
    if not copilot:
        return jsonify({
            'error': 'Blaze Copilot not initialized',
            'success': False
        })
    
    try:
        recent_interactions = copilot.conversation_history.get_recent_interactions(10)
        summary = copilot.conversation_history.get_session_summary()
        
        return jsonify({
            'success': True,
            'recent_interactions': recent_interactions,
            'summary': summary
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Error getting history: {str(e)}',
            'success': False
        })

@app.route('/search_history', methods=['POST'])
def search_history():
    """Search conversation history"""
    if not copilot:
        return jsonify({
            'error': 'Blaze Copilot not initialized',
            'success': False
        })
    
    try:
        data = request.get_json()
        search_term = data.get('search_term', '').strip()
        
        if not search_term:
            return jsonify({
                'error': 'Please provide a search term',
                'success': False
            })
        
        matches = copilot.search_history(search_term)
        
        return jsonify({
            'success': True,
            'search_term': search_term,
            'matches': matches
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Error searching history: {str(e)}',
            'success': False
        })

@app.route('/status')
def status():
    """Get system status"""
    return jsonify({
        'copilot_initialized': copilot is not None,
        'success': True
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 