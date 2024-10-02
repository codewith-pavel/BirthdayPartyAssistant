import os
import json
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

from langchain import LLMChain
from langchain.llms import HuggingFacePipeline
from langchain.prompts import PromptTemplate
from transformers import pipeline, Pipeline

# Configure logging to output to both console and file
logging.basicConfig(
    level=logging.INFO,  # Set the logging level to INFO
    format="%(asctime)s [%(levelname)s] %(message)s",  # Define the log message format
    handlers=[
        logging.FileHandler("party_planning_assistant.log"),  # Log messages to a file
        logging.StreamHandler()  # Also output log messages to the console
    ]
)
logger = logging.getLogger(__name__)  # Create a logger for this module


class PartyPlanningAssistant:
    def __init__(self, user_id: str):
        """
        Initialize the PartyPlanningAssistant with user-specific data.
        """
        self.user_id = user_id
        self.data_file = f"party_plan_{self.user_id}.json"  # Define the filename for storing user data
        self.load_data()  # Load existing data or initialize default data

        # Initialize the GPT-2 model using HuggingFace's pipeline
        try:
            self.llm_pipeline: Pipeline = pipeline(
                "text-generation",
                model="distilbert/distilgpt2",  # Corrected model name for text generation
                max_length=300,  # Maximum length of generated text
                num_return_sequences=1,  # Number of sequences to generate
                truncation=True,  # Truncate sequences longer than max_length
                pad_token_id=50256  # Token ID for padding
            )
            logger.info("LLM pipeline initialized successfully.")  # Log successful initialization
        except Exception as e:
            logger.error(f"Failed to initialize LLM pipeline: {e}")  # Log any errors during initialization
            raise  # Raise the exception to halt execution

        # Define the prompt template for the language model
        self.prompt_template = PromptTemplate(
            input_variables=["user_input"],  # Define input variables for the prompt
            template=(
                "You are a helpful assistant specializing in birthday party planning. "
                "Based on the following details: {user_input}, please provide a detailed party plan with the following structure: "
                "1. **Themes**: Suggest three distinct themes for the party. "
                "2. **Venue Suggestions**: Provide three suitable venue options for the suggested themes. "
                "3. **Activities**: List three engaging activities for guests that align with the themes. "
                "Format your response with clear headings for each section and ensure it is informative and organized. "
                "Do not repeat the details; just provide the plan."
            )
        )

        # Create the LLMChain which connects the prompt template with the language model
        self.llm_chain = LLMChain(
            llm=HuggingFacePipeline(pipeline=self.llm_pipeline),  # Use the HuggingFace pipeline as the LLM
            prompt=self.prompt_template  # Attach the prompt template
        )
        logger.info("LLMChain created successfully.")  # Log successful creation of LLMChain

    def load_data(self):
        """
        Load user data from a JSON file. If the file doesn't exist, initialize default data.
        """
        if os.path.exists(self.data_file):  # Check if the data file exists
            try:
                with open(self.data_file, 'r') as file:
                    data = json.load(file)  # Load data from the JSON file
                # Extract data from the JSON structure or set defaults if keys are missing
                self.venues = data.get("venues", [])
                self.caterers = data.get("caterers", [])
                self.entertainment_options = data.get("entertainment", [])
                self.guests = data.get("guests", [])
                self.budget = data.get("budget", 0.0)
                self.user_preferences = data.get("preferences", {})
                self.event_timeline = data.get("event_timeline", [])
                self.photo_gallery = data.get("photo_gallery", [])
                self.checklist = data.get("checklist", [])
                logger.info(f"Data loaded successfully for user '{self.user_id}'.")  # Log successful data load
            except Exception as e:
                logger.error(f"Error loading data for user '{self.user_id}': {e}")  # Log any errors during data load
                self.initialize_default_data()  # Initialize default data if loading fails
        else:
            self.initialize_default_data()  # Initialize default data if file doesn't exist

    def initialize_default_data(self):
        """
        Initialize default data for a new user.
        """
        # Define default venues with name, capacity, and cost
        self.venues: List[Dict[str, Any]] = [
            {"name": "Banquet Hall A", "capacity": 100, "cost": 2000},
            {"name": "Garden Venue B", "capacity": 150, "cost": 3000},
            {"name": "Beachside Venue C", "capacity": 200, "cost": 5000}
        ]

        # Define default caterers with name and cost per person
        self.caterers: List[Dict[str, Any]] = [
            {"name": "Caterer X", "cost_per_person": 20},
            {"name": "Caterer Y", "cost_per_person": 25},
            {"name": "Caterer Z", "cost_per_person": 30}
        ]

        # Define default entertainment options with name and cost
        self.entertainment_options: List[Dict[str, Any]] = [
            {"name": "DJ Services", "cost": 800},
            {"name": "Live Band", "cost": 1500},
            {"name": "Magician", "cost": 500}
        ]

        self.guests: List[str] = []  # Initialize an empty guest list
        self.budget: float = 0.0  # Initialize budget to zero
        self.user_preferences: Dict[str, Any] = {}  # Initialize empty user preferences
        self.event_timeline: List[Dict[str, Any]] = []  # Initialize empty event timeline
        self.photo_gallery: List[str] = []  # Initialize empty photo gallery
        self.checklist: List[str] = []  # Initialize empty checklist
        logger.info(f"Initialized default data for user '{self.user_id}'.")  # Log initialization of default data

    def save_data(self):
        """
        Save user data to a JSON file.
        """
        # Prepare the data dictionary to be saved
        plan = {
            "budget": self.budget,
            "venues": self.venues,
            "caterers": self.caterers,
            "entertainment": self.entertainment_options,
            "guests": self.guests,
            "preferences": self.user_preferences,
            "event_timeline": self.event_timeline,
            "photo_gallery": self.photo_gallery,
            "checklist": self.checklist,
        }
        try:
            with open(self.data_file, 'w') as json_file:
                json.dump(plan, json_file, indent=4)  # Write data to the JSON file with indentation for readability
            logger.info(f"Data saved successfully for user '{self.user_id}'.")  # Log successful data save
        except Exception as e:
            logger.error(f"Failed to save data for user '{self.user_id}': {e}")  # Log any errors during data save

    def run(self, user_input: str) -> str:
        """
        Generate a party plan based on user input using the LLM.
        """
        user_input = user_input.strip()  # Remove leading and trailing whitespace
        if not user_input:
            return "I'm sorry, but it seems you haven't provided any details. Could you please describe the party you'd like to plan?"

        if len(user_input) > 1000:
            return "Your input seems quite lengthy. Please simplify your request to make it more concise."

        try:
            response = self.llm_chain.run(user_input)  # Generate a response using the LLM chain
            response_text = response if isinstance(response, str) else str(response)  # Ensure the response is a string
            if "I don't know" in response_text:
                return "I'm sorry, but I didn't understand that. Could you please provide more specific details about your party?"
            logger.info("Party plan generated successfully.")  # Log successful plan generation
            return response_text.strip()  # Return the generated plan
        except Exception as e:
            logger.error(f"Error during LLMChain invocation: {e}")  # Log any errors during LLM invocation
            return "An error occurred while generating the party plan. Please try again later."

    def update_preferences(self, key: str, value: Any) -> str:
        """
        Update user preferences.
        """
        self.user_preferences[key] = value  # Update the preference with the provided key and value
        self.save_data()  # Save the updated data
        logger.info(f"Preference '{key}' updated to '{value}'.")  # Log the update
        return f"Preference '{key}' updated to '{value}'."

    def get_preferences(self) -> Dict[str, Any]:
        """
        Retrieve user preferences.
        """
        return self.user_preferences  # Return the current user preferences

    def recommend_options(self, user_budget: float) -> Dict[str, List[Dict[str, Any]]]:
        """
        Recommend venues, caterers, and entertainment options based on the user's budget.
        """
        recommendations = {}

        # Recommend venues within budget
        available_venues = [venue for venue in self.venues if venue["cost"] <= user_budget]
        if available_venues:
            recommendations["venues"] = available_venues

        # Estimate catering cost based on number of guests, default to 10 if not set
        num_guests = len(self.guests) if self.guests else 10
        available_caterers = [
            caterer for caterer in self.caterers
            if caterer["cost_per_person"] * num_guests <= user_budget
        ]
        if available_caterers:
            recommendations["caterers"] = available_caterers

        # Recommend entertainment within budget
        available_entertainment = [ent for ent in self.entertainment_options if ent["cost"] <= user_budget]
        if available_entertainment:
            recommendations["entertainment"] = available_entertainment

        logger.info(f"Recommendations generated based on budget ${user_budget}.")  # Log the recommendation generation
        return recommendations  # Return the recommended options

    def book_service(self, service_type: str, details: str) -> str:
        """
        Book a service (venue, caterer, entertainment).
        """
        if service_type not in ["venue", "caterer", "entertainment"]:
            return "Invalid service type. Please choose from venue, caterer, or entertainment."

        if not details:
            return "Service details cannot be empty."

        # Placeholder for actual booking logic
        # Implement API calls or database operations as needed
        try:
            logger.info(f"Booked {service_type}: {details}.")  # Log the booking action
            self.save_data()  # Save the updated data after booking
            return f"{service_type.capitalize()} '{details}' has been booked successfully!"
        except Exception as e:
            logger.error(f"Error booking service '{service_type}': {e}")  # Log any errors during booking
            return "An error occurred while booking the service. Please try again later."

    def manage_guest_list(self, action: str, guest_info: Optional[str] = None) -> str:
        """
        Manage the guest list by adding, removing, listing, or viewing RSVPs.
        """
        if action == "add" and guest_info:
            if guest_info not in self.guests:
                self.guests.append(guest_info)  # Add the guest to the list
                self.save_data()  # Save the updated guest list
                logger.info(f"Guest '{guest_info}' added.")  # Log the addition
                return f"Guest '{guest_info}' added to the guest list."
            else:
                return f"Guest '{guest_info}' is already in the guest list."

        elif action == "remove" and guest_info:
            if guest_info in self.guests:
                self.guests.remove(guest_info)  # Remove the guest from the list
                self.save_data()  # Save the updated guest list
                logger.info(f"Guest '{guest_info}' removed.")  # Log the removal
                return f"Guest '{guest_info}' removed from the guest list."
            else:
                return f"Guest '{guest_info}' not found in the list."

        elif action == "list":
            guest_list = ", ".join(self.guests) if self.guests else "No guests in the list."
            logger.info("Guest list retrieved.")  # Log the retrieval of the guest list
            return f"Current guests: {guest_list}"

        elif action == "rsvp":
            if self.guests:
                rsvps = ", ".join([f"{guest} (Confirmed)" for guest in self.guests])
                logger.info("RSVPs retrieved.")  # Log the retrieval of RSVPs
                return f"RSVPs: {rsvps}"
            else:
                return "No guests in the list."

        else:
            return "Invalid action for guest management."

    def handle_user_requests(self, request_type: str, details: str) -> str:
        """
        Handle various user requests such as updating preferences or generating plans.
        """
        if request_type == "update":
            if ',' in details:
                key, value = details.split(',', 1)  # Split the details into key and value
                return self.update_preferences(key.strip(), value.strip())  # Update the preference
            else:
                return "Invalid format for updating preferences. Use 'key, value'."

        elif request_type == "preferences":
            prefs = self.get_preferences()  # Retrieve current preferences
            prefs_formatted = json.dumps(prefs, indent=2) if prefs else "No preferences set."
            logger.info("User preferences retrieved.")  # Log the retrieval
            return f"User Preferences:\n{prefs_formatted}"

        elif request_type == "plan":
            return self.run(details)  # Generate a party plan based on details

        else:
            return "Invalid request type."

    def adjust_plan(self, new_details: str) -> str:
        """
        Adjust the existing plan based on new details provided by the user.
        """
        logger.info("Adjusting the plan based on new details.")  # Log the adjustment action
        response = self.run(new_details)  # Generate an updated plan
        self.save_data()  # Save the updated plan
        return response  # Return the updated plan

    def set_budget(self, amount: float) -> str:
        """
        Set the user's budget.
        """
        if amount < 0:
            return "Budget cannot be negative."
        self.budget = amount  # Update the budget
        self.save_data()  # Save the updated budget
        logger.info(f"Budget set to ${amount}.")  # Log the budget update
        return f"Budget set to ${amount}."

    def get_budget(self) -> float:
        """
        Retrieve the user's current budget.
        """
        return self.budget  # Return the current budget

    def export_plan(self) -> str:
        """
        Export the party plan to a JSON file.
        """
        try:
            export_file = f'party_plan_{self.user_id}.json'  # Define the export filename
            with open(export_file, 'w') as json_file:
                json.dump({
                    "budget": self.budget,
                    "venues": self.venues,
                    "caterers": self.caterers,
                    "entertainment": self.entertainment_options,
                    "guests": self.guests,
                    "preferences": self.user_preferences,
                    "event_timeline": self.event_timeline,
                    "photo_gallery": self.photo_gallery,
                    "checklist": self.checklist,
                }, json_file, indent=4)  # Write the plan to the JSON file
            logger.info("Party plan exported successfully.")  # Log successful export
            return f"Party plan exported to '{export_file}'."
        except Exception as e:
            logger.error(f"Failed to export party plan: {e}")  # Log any errors during export
            return "An error occurred while exporting the party plan."

    def create_event_timeline(self, task: str, days_before: int) -> str:
        """
        Create a timeline task with a deadline.
        """
        try:
            if days_before < 0:
                return "Number of days before the event cannot be negative."
            deadline = datetime.now() + timedelta(days=days_before)  # Calculate the deadline date
            self.event_timeline.append({
                "task": task,
                "deadline": deadline.strftime("%Y-%m-%d")  # Format the deadline date
            })
            self.save_data()  # Save the updated timeline
            logger.info(f"Timeline task '{task}' created with deadline {deadline.strftime('%Y-%m-%d')}.")  # Log the timeline creation
            return f"Timeline task '{task}' created with a deadline of {deadline.strftime('%Y-%m-%d')}."
        except Exception as e:
            logger.error(f"Error creating event timeline: {e}")  # Log any errors during timeline creation
            return "An error occurred while creating the event timeline."

    def add_photo(self, photo_path: str) -> str:
        """
        Add a photo to the photo gallery.
        """
        try:
            if os.path.exists(photo_path) and os.path.isfile(photo_path):  # Check if the photo exists and is a file
                self.photo_gallery.append(photo_path)  # Add the photo path to the gallery
                self.save_data()  # Save the updated gallery
                logger.info(f"Photo '{photo_path}' added to the gallery.")  # Log the addition
                return f"Photo '{photo_path}' added to the gallery."
            else:
                logger.warning(f"Photo '{photo_path}' not found.")  # Log a warning if the photo is not found
                return f"Photo '{photo_path}' not found."
        except Exception as e:
            logger.error(f"Error adding photo '{photo_path}': {e}")  # Log any errors during photo addition
            return "An error occurred while adding the photo."

    def add_checklist_item(self, item: str) -> str:
        """
        Add an item to the checklist.
        """
        if not item:
            return "Checklist item cannot be empty."
        self.checklist.append(item)  # Add the item to the checklist
        self.save_data()  # Save the updated checklist
        logger.info(f"Checklist item '{item}' added.")  # Log the addition
        return f"Checklist item '{item}' added."

    def get_checklist(self) -> List[str]:
        """
        Retrieve the checklist items.
        """
        logger.info("Checklist retrieved.")  # Log the retrieval
        return self.checklist  # Return the current checklist


def display_menu():
    """
    Display the main menu options to the user.
    """
    print("\nPlease choose an option from the menu below:")
    print("1. Set Budget")
    print("2. Recommend Options")
    print("3. Book Service")
    print("4. Manage Guest List")
    print("5. Update/View Preferences")
    print("6. Export Plan")
    print("7. Create Event Timeline")
    print("8. Add Photo")
    print("9. Add/View Checklist")
    print("10. Adjust Plan")
    print("11. Exit")


def start_interaction():
    """
    Start the interaction loop with the user.
    """
    print("Welcome to the Birthday Party Planning Assistant!")  # Greet the user

    # Simple user identification mechanism
    user_id = input("Please enter your user ID (or type 'new' to create a new user): ").strip()
    if user_id.lower() == 'new':
        user_id = input("Enter a new user ID: ").strip()
        if not user_id:
            print("User ID cannot be empty. Exiting.")
            return
    elif not user_id:
        print("User ID cannot be empty. Exiting.")
        return

    assistant = PartyPlanningAssistant(user_id=user_id)  # Initialize the assistant with the user ID

    while True:
        display_menu()  # Show the menu options
        choice = input("Enter the number corresponding to your choice: ").strip()  # Get user's choice

        if choice == "1":
            # Set Budget
            try:
                amount_input = input("Enter your budget amount: ").strip()
                amount = float(amount_input)  # Convert input to float
                response = assistant.set_budget(amount)  # Set the budget
                print(response)
            except ValueError:
                print("Invalid budget amount. Please enter a numeric value.")

        elif choice == "2":
            # Recommend Options
            budget = assistant.get_budget()  # Retrieve the current budget
            if budget <= 0:
                print("Please set a valid budget first using the 'Set Budget' option.")
            else:
                recommendations = assistant.recommend_options(budget)  # Get recommendations based on budget
                if not recommendations:
                    print("No available options within your budget.")
                else:
                    print("\nRecommendations:")
                    for category, options in recommendations.items():
                        print(f"\n{category.capitalize()}:")
                        for option in options:
                            cost = option.get('cost') or option.get('cost_per_person', 'N/A')  # Get cost information
                            cost_info = f"Cost: ${cost}" if isinstance(cost, (int, float)) else f"{cost}"
                            print(f"- {option['name']} ({cost_info})")  # Display each recommended option

        elif choice == "3":
            # Book Service
            service_type = input("Enter the service type (venue/caterer/entertainment): ").strip().lower()
            if service_type not in ["venue", "caterer", "entertainment"]:
                print("Invalid service type. Please choose from venue, caterer, or entertainment.")
                continue
            details = input("Enter the details of the service (e.g., name): ").strip()
            if not details:
                print("Service details cannot be empty.")
                continue
            response = assistant.book_service(service_type, details)  # Book the selected service
            print(response)

        elif choice == "4":
            # Manage Guest List
            print("\nGuest List Management:")
            print("a. Add Guest")
            print("b. Remove Guest")
            print("c. List Guests")
            print("d. View RSVPs")
            guest_action = input("Choose an action (a/b/c/d): ").strip().lower()
            if guest_action == "a":
                guest_info = input("Enter the guest name to add: ").strip()
                if not guest_info:
                    print("Guest name cannot be empty.")
                    continue
                response = assistant.manage_guest_list("add", guest_info)  # Add a guest
                print(response)
            elif guest_action == "b":
                guest_info = input("Enter the guest name to remove: ").strip()
                if not guest_info:
                    print("Guest name cannot be empty.")
                    continue
                response = assistant.manage_guest_list("remove", guest_info)  # Remove a guest
                print(response)
            elif guest_action == "c":
                response = assistant.manage_guest_list("list")  # List all guests
                print(response)
            elif guest_action == "d":
                response = assistant.manage_guest_list("rsvp")  # View RSVPs
                print(response)
            else:
                print("Invalid action. Please choose a, b, c, or d.")

        elif choice == "5":
            # Update/View Preferences
            print("\nPreferences Management:")
            print("a. Update Preferences")
            print("b. View Preferences")
            pref_action = input("Choose an action (a/b): ").strip().lower()
            if pref_action == "a":
                details = input("Enter the preference to update in 'key, value' format: ").strip()
                response = assistant.handle_user_requests("update", details)  # Update a preference
                print(response)
            elif pref_action == "b":
                preferences = assistant.handle_user_requests("preferences", "")  # View preferences
                print(preferences)
            else:
                print("Invalid action. Please choose a or b.")

        elif choice == "6":
            # Export Plan
            export_response = assistant.export_plan()  # Export the current party plan
            print(export_response)

        elif choice == "7":
            # Create Event Timeline
            task = input("Enter the task for the timeline: ").strip()
            if not task:
                print("Task cannot be empty.")
                continue
            try:
                days_before_input = input("Enter the number of days before the event for the deadline: ").strip()
                days_before = int(days_before_input)  # Convert input to integer
                response = assistant.create_event_timeline(task, days_before)  # Create a timeline task
                print(response)
            except ValueError:
                print("Invalid number of days. Please enter an integer.")

        elif choice == "8":
            # Add Photo
            photo_path = input("Enter the photo path to add: ").strip()
            response = assistant.add_photo(photo_path)  # Add a photo to the gallery
            print(response)

        elif choice == "9":
            # Add/View Checklist
            print("\nChecklist Management:")
            print("a. Add Checklist Item")
            print("b. View Checklist")
            checklist_action = input("Choose an action (a/b): ").strip().lower()
            if checklist_action == "a":
                item = input("Enter the checklist item: ").strip()
                if not item:
                    print("Checklist item cannot be empty.")
                    continue
                response = assistant.add_checklist_item(item)  # Add a checklist item
                print(response)
            elif checklist_action == "b":
                checklist = assistant.get_checklist()  # Retrieve the checklist
                if not checklist:
                    print("No checklist items.")
                else:
                    print("\nChecklist Items:")
                    for idx, item in enumerate(checklist, start=1):
                        print(f"{idx}. {item}")  # Display each checklist item
            else:
                print("Invalid action. Please choose a or b.")

        elif choice == "10":
            # Adjust Plan
            new_details = input("Enter the new details to adjust the plan: ").strip()
            if not new_details:
                print("Adjustment details cannot be empty.")
                continue
            adjustment_response = assistant.adjust_plan(new_details)  # Adjust the existing plan
            print(adjustment_response)

        elif choice == "11":
            # Exit
            print("Thank you for using the Birthday Party Assistant. Goodbye!")  # Farewell message
            break  # Exit the loop and end the program

        else:
            print("Invalid choice. Please enter a number between 1 and 11.")  # Handle invalid menu choices


if __name__ == "__main__":
    start_interaction()  # Start the assistant when the script is run