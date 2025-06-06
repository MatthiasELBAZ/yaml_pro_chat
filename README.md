# Lynk.ai Feature Creator

A specialized agent for generating Lynk.ai feature YAML files based on natural language descriptions.

## Features

- Create four types of Lynk features: Metric, First-Last, Formula, and Field
- Conversational UI for interactive feature creation
- Guideline-based YAML generation
- Automatic YAML validation
- Git integration for committing generated features to a repository

## Architecture

- **Backend**: Python with FastAPI, LangGraph, and LangChain
- **Frontend**: Simple HTML/CSS/JavaScript chat interface
- **Deployment**: Docker and Docker Compose

## Requirements

- Docker and Docker Compose
- Git (for the commit feature)
- API Keys:
  - OpenAI API Key (for the language model)
  - Tavily API Key (for documentation search)

## Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd lynk-feature-creator
   ```

2. Create a `.env` file with your API keys:
   ```
   OPENAI_API_KEY=your_openai_api_key
   TAVILY_API_KEY=your_tavily_api_key
   ```

3. Build and run the application with Docker Compose:
   ```bash
   docker-compose up --build
   ```

4. Access the application:
   - Frontend: http://localhost
   - Backend API: http://localhost:8000
   - API documentation: http://localhost:8000/docs

## How to Run Backend and Frontend Separately

During development, you may want to run the backend and frontend servers separately for easier debugging and faster iteration.

### Running the Backend

1. Make sure you have the required environment variables set (through a `.env` file or directly in your shell):
   ```bash
   export OPENAI_API_KEY=your_openai_api_key
   export TAVILY_API_KEY=your_tavily_api_key
   ```

2. Navigate to the `src` directory and run the FastAPI server:
   ```bash
   cd src
   python main.py
   ```

3. The backend server will start on http://0.0.0.0:8000 with auto-reload enabled for development.

### Running the Frontend

1. In a separate terminal, navigate to the `frontend` directory:
   ```bash
   cd frontend
   ```

2. Start a simple HTTP server to serve the frontend files:
   ```bash
   python -m http.server 8081
   ```

3. Access the frontend in your browser at http://localhost:8081

### Testing the Application

1. Open the frontend in your browser (http://localhost:8081)
2. Enter a feature request in the chat input, for example: "I would like to create a metric feature on asset my_asset"
3. The frontend will communicate with the backend, and you'll receive a response from the agent


 cd src && python main.py
 cd frontend && python -m http.server 8081

## Usage

1. Open the chat interface in your browser
2. Describe the feature you want to create, for example:
   - "I would like to create a metric feature on asset my_asset"
   - "I would like to create a formula feature with SQL..."
3. The agent will ask follow-up questions if any information is missing
4. Once all information is provided, the agent will generate and display the YAML code
5. The agent will ask if you want to save the YAML to a file
6. If you agree, it will save the file to the `features` directory
7. The agent will then ask if you want to commit the file to Git
8. If you agree, it will commit the file to your Git repository

## Git Integration

The application includes Git integration that allows you to:

1. Save generated YAML files to the `features` directory
2. Commit those files to your Git repository directly from the chat interface

This feature is useful for incorporating feature creation into your development workflow. Make sure you have Git installed and that you're running the application in a Git repository.

## Development

To run the application for development without Docker:

1. Install the dependencies:
   ```bash
   pip install -e .
   ```

2. Set the environment variables:
   ```bash
   export OPENAI_API_KEY=your_openai_api_key
   export TAVILY_API_KEY=your_tavily_api_key
   ```

3. Run the backend:
   ```bash
   python src/main.py
   ```

4. Serve the frontend (optional, using any static file server):
   ```bash
   cd frontend && python -m http.server 80
   ```

## License

[MIT License](LICENSE) 