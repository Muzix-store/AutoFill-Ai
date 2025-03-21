# This module is meant for parsing Ai using interference API
# Input: Text query input Output: text response

import sys
from g4f.client import Client
#from g4f.Provider import Liaobots
from g4f.errors import ProviderNotWorkingError

def main():
    client = Client()
    query = str(input("Enter your query ~> "))
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a sales expert with over than 20 years of experience. Your task is to create selling description for an item. All data provided."
                },
                {
                    "role": "user",
                    "content": query
                }
            ],
            web_search=False,
            #provider=Liaobots
        )
        
        answer = response.choices[0].message.content
        print(answer)
        
    except ProviderNotWorkingError as e:
        print(f"Error: Provider not working - {e}")
        print("Try using a different provider or model.")
    except ConnectionError as e:
        print(f"Error: Connection issue - {e}")
        print("Check your internet connection and try again.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        print("Please check your inputs and try again.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
        sys.exit(0)
