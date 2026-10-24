# Agentic Support System

## Overview

The Agentic Support System is an intelligent multi-agent framework designed to provide automated customer support using advanced AI technologies. This system leverages machine learning models, retrieval-augmented generation (RAG), and orchestrator patterns to classify, retrieve, and respond to user queries effectively.

## Features

- **Multi-Agent Architecture**: Modular agents for classification, retrieval, and response generation
- **Retrieval-Augmented Generation (RAG)**: Enhanced responses using contextual document retrieval
- **Monitoring and Analytics**: Built-in logging, analytics, and performance tracking
- **Web UI**: User-friendly dashboard for interaction and monitoring
- **API Integration**: RESTful API for seamless integration with other systems
- **Containerized Deployment**: Docker and Docker Compose support for easy deployment
- **Evaluation Framework**: Comprehensive metrics and evaluation tools for model performance

## Project Structure

```
agentic-support-system/
├── api/                    # REST API endpoints
│   ├── main.py            # Main API application
│   └── __pycache__/
├── data/                   # Data storage and documentation
│   └── docs/
│       └── faq.txt        # FAQ documents for RAG
├── evaluation/             # Model evaluation and metrics
│   ├── dataset.json       # Evaluation dataset
│   ├── evaluator.py       # Evaluation scripts
│   └── metrics.py         # Performance metrics
├── monitoring/             # Monitoring and logging
│   ├── analytics.py       # Analytics tools
│   ├── logger.py          # Logging utilities
│   └── storage.json       # Monitoring data storage
├── orchestrator/           # Agent orchestration logic
│   ├── graph.py           # Orchestration graph
│   └── __pycache__/
├── services/               # Core agent services
│   ├── classifier/        # Query classification agent
│   │   ├── agent.py
│   │   └── __pycache__/
│   ├── responder/         # Response generation agent
│   │   ├── agent.py
│   │   └── __pycache__/
│   └── retriever/         # Document retrieval agent
│       ├── load_data.py   # Data loading utilities
│       ├── rag.py         # RAG implementation
│       └── __pycache__/
├── shared/                 # Shared utilities
│   ├── logger.py          # Shared logging
│   └── memory.py          # Memory management
├── ui/                     # User interface
│   ├── app.py             # Main UI application
│   └── dashboard.py       # Dashboard components
├── train.py                # Model training script
├── template.py             # Template utilities
├── requirements.txt        # Python dependencies
├── Dockerfile              # Docker container configuration
├── docker-compose.yml      # Multi-container orchestration
├── LICENSE                 # Project license
└── README.md               # This file
```

## Installation

### Prerequisites

- Python 3.8 or higher
- Docker and Docker Compose (for containerized deployment)
- Conda (recommended for environment management)

### Local Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd agentic-support-system
   ```

2. Create and activate a conda environment:
   ```bash
   conda create -n agent_env python=3.9
   conda activate agent_env
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. (Optional) Train the models:
   ```bash
   python train.py
   ```

### Docker Setup

1. Build and run with Docker Compose:
   ```bash
   docker-compose up --build
   ```

## Usage

### Running the API

Start the REST API server:
```bash
python api/main.py
```

The API will be available at `http://localhost:8000`

### Running the UI

Launch the web dashboard:
```bash
python ui/app.py
```

Access the dashboard at `http://localhost:5000`

### Training Models

Train the AI models:
```bash
python train.py
```

### Evaluation

Evaluate model performance:
```bash
python evaluation/evaluator.py
```

## API Endpoints

- `POST /classify` - Classify user queries
- `POST /retrieve` - Retrieve relevant documents
- `POST /respond` - Generate responses
- `GET /health` - Health check endpoint

## Configuration

The system can be configured through environment variables:

- `OPENAI_API_KEY` - API key for OpenAI services
- `DATABASE_URL` - Database connection string
- `LOG_LEVEL` - Logging level (DEBUG, INFO, WARNING, ERROR)

## Monitoring

The system includes comprehensive monitoring:

- Real-time analytics via `monitoring/analytics.py`
- Structured logging with `shared/logger.py`
- Performance metrics in `evaluation/metrics.py`

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with LangChain for agent orchestration
- Uses FAISS for efficient vector search
- Inspired by modern AI agent architectures.