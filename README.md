
# MultiAgentAI-Research-Assistant

**MultiAgentAI-Research-Assistant** is a project designed to automate research workflows using multiple AI-powered tools. It includes capabilities for generating AI-driven use cases, conducting web searches, gathering industry insights, and organizing research resources. The frontend interface is powered by **Streamlit**, providing an intuitive and user-friendly experience.

---

## Key Features
### 1. **Streamlit Frontend (app.py)**
   - The **Streamlit-based frontend** offers a simple and interactive web interface for users to interact with all tools.
   - Provides:
     - Tabs to navigate between features like Use Case Generation, Web Search Results, and Research Tools.
     - Easy input/output visualization of results such as structured use cases and ranked web search results.

### 2. **Web Search Tool**
   - Automates web search queries, retrieves relevant results, and organizes them based on relevance scores.
   - Outputs include:
     - Titles, URLs, summaries, and scores for retrieved content.

### 3. **Industry Research Tool**
   - Focuses on industry-specific insights and trends.
   - Assists in understanding challenges, market innovations, and competitive strategies.

### 4. **Use Case Generator Tool**
   - Generates detailed use cases for AI applications across industries.
   - Outputs include:
     - **Case Description**: Concise summary.
     - **Objective**: The problem being addressed.
     - **AI Application**: Detailed explanation of AI's role.
     - **Cross-Functional Benefits**: Department-specific benefits like Operations, Finance, or Marketing.
     - **Reference Articles**: Links for additional reading.

### 5. **Resource Collector Tool**
   - Organizes research materials, online references, and datasets.
   - Simplifies large-scale data collection.

---

## Setup Instructions
### Prerequisites
Ensure the following are installed:
- **Python 3.10+**
- **pip** (Python package manager)

### Installation Steps
1. **Clone the repository**:
   ```bash
   git clone <repository_url>
   cd Research_MultiAgentAI
   ```
2. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3. **Set up Environment Variables**:
  - Create a .env file in the root directory.
  - Add sensitive credentials like API keys
   ```makefile
   
   API_KEY=your_api_key_here
   SECRET_KEY=your_secret_here
   ```
4. **Run the application**:
  - Launch the **Streamlit** app:
  ```bash
   streamlit run app.py
  ```
  - Open the provided localhost URL in your browser to access the interface.
