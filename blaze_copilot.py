#!/usr/bin/env python3
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add the BlazeQuery directory to the path
sys.path.append(str(Path(__file__).parent / "blaze_docs" / "BlazeQuery"))

from blaze_docs.BlazeQuery.query_blaze import BlazeQueryEngine
from conversation_history import ConversationHistory

# Load environment variables
load_dotenv()

class BlazeCopilot:
    def __init__(self):
        """
        Initialize the Blaze Inbox Copilot
        """
        print("Initializing Blaze Inbox Copilot...")
        
        try:
            self.query_engine = BlazeQueryEngine()
            self.conversation_history = ConversationHistory()
            print("Blaze Copilot initialized successfully!")
        except Exception as e:
            print(f"Error initializing Blaze Copilot: {e}")
            print("Make sure you have:")
            print("1. Run the scraper: python blaze_docs/scrape_blaze_docs.py")
            print("2. Created the vector database: python blaze_docs/BlazeQuery/create_vector_db.py")
            print("3. Set your GOOGLE_API_KEY in a .env file")
            sys.exit(1)
    
    def ask(self, query: str, show_details: bool = False) -> dict:
        """
        Ask a question to the Blaze Copilot
        """
        print(f"\nProcessing query: {query}")
        
        # Get response from query engine
        results = self.query_engine.query(query)
        
        # Extract key information
        ai_response = results["ai_response"]
        confidence = ai_response["confidence"]
        answer = ai_response["answer"]
        
        # Add to conversation history
        self.conversation_history.add_interaction(query, results, confidence)
        
        # Prepare response
        response = {
            "query": query,
            "answer": answer,
            "confidence": confidence,
            "sources": []
        }
        
        # Add source information
        for result in results["top_results"][:3]:  # Top 3 sources
            source = {
                "title": result["question"],
                "url": result["url"],
                "score": result["score"],
                "category": result["category"]
            }
            response["sources"].append(source)
        
        # Display response
        print(f"\n**Blaze Copilot Response:**")
        print(f"**Answer:** {answer}")
        print(f"**Confidence:** {confidence}%")
        
        if confidence < 50:
            print("**Low confidence warning:** This answer might not be accurate. Consider asking for clarification or checking the documentation directly.")
        
        if show_details and response["sources"]:
            print(f"\n**Sources:**")
            for i, source in enumerate(response["sources"], 1):
                print(f"{i}. {source['title']} (Score: {source['score']:.3f})")
                if source['url']:
                    print(f"   {source['url']}")
        
        return response
    
    def get_conversation_summary(self):
        """
        Get summary of current conversation session
        """
        summary = self.conversation_history.get_session_summary()
        
        print(f"\n**Session Summary:**")
        print(f"Total queries: {summary['total_queries']}")
        print(f"Average confidence: {summary['avg_confidence']}%")
        if summary['topics']:
            print(f"Main topics: {', '.join(summary['topics'])}")
        
        return summary
    
    def search_history(self, search_term: str):
        """
        Search through conversation history
        """
        matches = self.conversation_history.search_history(search_term)
        
        if matches:
            print(f"\n**Found {len(matches)} previous interactions about '{search_term}':**")
            for i, match in enumerate(matches, 1):
                print(f"{i}. Q: {match['query']}")
                print(f"   A: {match['response']['ai_response']['answer'][:100]}...")
                print(f"   Confidence: {match['confidence']}%")
                print(f"   Time: {match['timestamp']}")
                print()
        else:
            print(f"No previous interactions found for '{search_term}'")
        
        return matches
    
    def interactive_mode(self):
        """
        Run the copilot in interactive mode
        """
        print("\n**Welcome to Blaze Inbox Copilot!**")
        print("Ask me anything about Blaze's features, setup, or usage.")
        print("Commands:")
        print("  - Type your question normally")
        print("  - 'history <search_term>' - Search conversation history")
        print("  - 'summary' - Show session summary")
        print("  - 'quit' or 'exit' - Exit the copilot")
        print("  - 'help' - Show this help message")
        print("\n" + "="*50)
        
        while True:
            try:
                user_input = input("\nYou: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("\nThanks for using Blaze Copilot! Goodbye!")
                    break
                
                elif user_input.lower() == 'help':
                    print("\n**Help:**")
                    print("Just ask me questions about Blaze! For example:")
                    print("- 'How do I set up Discord analytics?'")
                    print("- 'How can I start a Twitter DM campaign?'")
                    print("- 'What are Topic Definitions?'")
                    print("- 'How do I update my billing information?'")
                    
                elif user_input.lower() == 'summary':
                    self.get_conversation_summary()
                
                elif user_input.lower().startswith('history '):
                    search_term = user_input[8:].strip()
                    if search_term:
                        self.search_history(search_term)
                    else:
                        print("Please provide a search term. Example: 'history discord'")
                
                else:
                    # Regular query
                    self.ask(user_input, show_details=True)
                    
            except KeyboardInterrupt:
                print("\n\nThanks for using Blaze Copilot! Goodbye!")
                break
            except Exception as e:
                print(f"\nError: {e}")
                print("Please try again or type 'help' for assistance.")


def main():
    """
    Main function to run the Blaze Copilot
    """
    import argparse
    
    parser = argparse.ArgumentParser(description="Blaze Inbox Copilot - AI Support Bot")
    parser.add_argument("--query", "-q", type=str, help="Ask a single question")
    parser.add_argument("--interactive", "-i", action="store_true", help="Run in interactive mode")
    parser.add_argument("--setup", action="store_true", help="Run setup (scraping and vector DB creation)")
    
    args = parser.parse_args()
    
    if args.setup:
        print("Setting up Blaze Copilot...")
        
        # Run scraper
        print("\n1. Scraping Blaze documentation...")
        try:
            from blaze_docs.scrape_blaze_docs import BlazeDocsScraper
            scraper = BlazeDocsScraper()
            scraper.scrape_all()
            print("Scraping completed!")
        except Exception as e:
            print(f"Scraping failed: {e}")
            return
        
        # Create vector database
        print("\n2. Creating vector database...")
        try:
            from blaze_docs.BlazeQuery.create_vector_db import BlazeVectorizer
            vectorizer = BlazeVectorizer("blaze_docs/scraped_content")
            vectorizer.create_database()
            print("Vector database created!")
        except Exception as e:
            print(f"Vector database creation failed: {e}")
            return
        
        print("\nSetup completed! You can now use the Blaze Copilot.")
        print("Run: python blaze_copilot.py --interactive")
        return
    
    # Initialize copilot
    copilot = BlazeCopilot()
    
    if args.query:
        # Single query mode
        copilot.ask(args.query, show_details=True)
    elif args.interactive:
        # Interactive mode
        copilot.interactive_mode()
    else:
        # Default to interactive mode
        copilot.interactive_mode()


if __name__ == "__main__":
    main() 