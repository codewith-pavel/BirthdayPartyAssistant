# 🎉 Birthday Party Planning Assistant

A smart assistant built using the LangChain framework to help users plan birthday parties. The assistant can recommend venues, caterers, and entertainment options, and it can adjust plans based on user feedback.

## 📑 Table of Contents
1. [Features](#features)
2. [Technologies Used](#technologies-used)
3. [Installation](#installation)
4. [Usage](#usage)
5. [How It Works](#how-it-works)
6. [License](#license)

---

# 🛠️ Features

### 💰 Budget Management
- **Set and Track Budget**: Define your total budget for the party and monitor expenditures to stay within limits.
- **Budget Validation**: Ensures that budget inputs are valid and prevents negative budget values.

### 📍 Venue Recommendations
- **Personalized Suggestions**: Recommends suitable venues based on your budget, party size, and location preferences.
- **Cost Filtering**: Filters venue options to match your budget constraints, ensuring affordability.

### 🍽️ Catering Options
- **Diverse Caterer Listings**: Provides a curated list of caterers with varying cost-per-person rates to fit different budget ranges.
- **Cost Estimation**: Estimates total catering costs based on the number of guests and selected caterer, helping you make informed decisions.

### 🎉 Entertainment Suggestions
- **Variety of Entertainment**: Recommends a range of entertainment options such as DJ services, live bands, and magicians to suit different party themes and budgets.
- **Cost-Effective Choices**: Filters entertainment options to align with your financial plan.

### 👥 Guest List Management
- **Add and Remove Guests**: Easily manage your guest list by adding new guests or removing existing ones.
- **View Guest List**: Display the current list of invited guests.
- **RSVP Tracking**: View confirmed RSVPs to keep track of attendance.

### 🎨 Preferences Management
- **Update User Preferences**: Update your preferences for various aspects of the party, such as themes, colors, and specific requirements.
- **View Current Preferences**: Retrieve and display your current preferences for easy reference.

### 📅 Event Timeline Creation
- **Task Scheduling**: Create a timeline of tasks with deadlines leading up to the event, ensuring all preparations are on track.
- **Deadline Management**: Automatically calculates and assigns deadlines based on the number of days before the event.

### 📸 Photo Gallery Management
- **Add Photos**: Upload and manage photos related to party planning, such as venue images or decoration ideas.
- **Organize Gallery**: Maintain a curated gallery of photos for easy access and inspiration.

### ✅ Checklist Management
- **Add Checklist Items**: Create a comprehensive checklist of tasks to ensure nothing is overlooked during the planning process.
- **View and Track Progress**: Display all checklist items, allowing you to monitor progress and mark tasks as completed.

### 🔄 Dynamic Plan Adjustments
- **Real-Time Updates**: Adjust party plans based on new inputs or changes in your preferences, ensuring flexibility and adaptability.
- **Automated Revisions**: Automatically regenerates recommendations and plans to reflect any adjustments made by you.

### 💾 Data Persistence
- **Save and Load Plans**: Automatically saves all party planning data to a JSON file, enabling you to resume planning in future sessions without data loss.
- **Data Backup**: Ensures that all your data is securely stored and easily retrievable.

### 📜 Comprehensive Logging
- **Activity Tracking**: Logs all user actions and system events to a log file for monitoring and debugging purposes.
- **Error Reporting**: Provides detailed error messages and logs to help identify and resolve issues efficiently.

### 🖥️ User-Friendly Command-Line Interface
- **Interactive Menus**: Presents an intuitive menu-driven interface for easy navigation and interaction with the assistant.
- **Input Validation**: Ensures that all user inputs are valid, enhancing the overall user experience and preventing errors.

### 📤 Export Functionality
- **Export Party Plans**: Allows you to export your entire party plan to a JSON file, facilitating easy sharing and record-keeping.
- **Formatted Output**: Ensures that exported data is well-organized and formatted for readability.

---

# 🛠️ Technologies Used
- **Python**: Programming language used for developing the assistant.
- **LangChain**: Framework for building the AI assistant.
- **Docker**: Used for containerizing the application.
- **Hugging Face Transformers**: For language processing tasks.

---

# 🛠️ Installation

### 1. **Clone the Repository**
```bash
git clone https://github.com/your-username/birthday-party-assistant.git
cd birthday-party-assistant
```

### 2. **Install Dependencies**
Create a virtual environment and install the required libraries:
```bash
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

---

# 🚀 Usage

### **Running the Assistant Locally**

To run the assistant locally using Python, execute the following command:
```bash
python party_planning_assistant.py
```

### **Running the Assistant with Docker**

You can also run the application using Docker:

### 1. **Build the Docker Image**
   ```bash
   docker build -t birthday-party-assistant .
   ```

### 2. **Run the Docker Container**
   ```bash
   docker run -it birthday-party-assistant
   ```

---

# 💡 How It Works

The assistant interacts with users to gather information about their party requirements. It then processes this information to provide relevant recommendations and can execute bookings on behalf of the user. The use of LangChain allows for flexible integration with various APIs and services, enabling dynamic and intelligent responses based on user inputs.

---

# 📄 License

This project is licensed under the **Apache License 2.0** - see the [LICENSE](LICENSE) file for details.
