# TelcoResQ: AI-Powered Survey Insight Engine

An AI-powered survey analysis system specifically designed for telecom network resilience insights. The system processes qualitative survey data, extracts meaningful themes, and provides natural language querying capabilities.

## Quick Start

### Prerequisites
- Docker and Docker Compose installed
- OpenAI API key

### Running the Application

1. **Clone and navigate to the project:**
   ```bash
   cd TelcoResQ
   ```

2. **Build the Docker container:**
   ```bash
   docker-compose build
   ```

3. **Run the application:**
   ```bash
   docker-compose up
   ```

4. **Access the application:**
   Open [http://localhost:8501](http://localhost:8501) in your browser

### Alternative: Local Development

If you prefer to run locally without Docker:

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set Python path:**
   ```bash
   export PYTHONPATH=/path/to/TelcoResQ
   ```

3. **Run the application:**
   ```bash
   streamlit run telcoresq/app/main.py
   ```

## 📊 What This Project Does

TelcoResQ is designed to analyze telecom resilience survey data using AI. It provides:

- **Data Processing**: Upload and clean CSV/JSON survey data
- **Sentiment Analysis**: Analyze sentiment of survey responses with justifications
- **Theme Extraction**: Automatically identify and categorize themes from responses
- **Natural Language Queries**: Ask questions about your data in plain English
- **Vector Search**: Find similar responses using semantic similarity
- **Executive Summaries**: Generate comprehensive summaries of survey insights
- **Interactive Visualizations**: Charts and graphs for sentiment and theme analysis

## Project Structure

```
TelcoResQ/
├── telcoresq/                    # Main application package
│   ├── app/                      # Streamlit application
│   │   ├── main.py              # Main Streamlit app entry point
│   │   ├── components/          # UI components and visualizations
│   │   ├── services/            # Core business logic
│   │   │   ├── ai_services.py   # OpenAI API integrations
│   │   │   ├── data_processing.py # Data cleaning and preprocessing
│   │   │   ├── database.py      # Database operations
│   │   │   └── vector_store.py  # FAISS vector search
│   │   └── utils/               # Utility functions
│   ├── config/                  # Configuration files
│   │   ├── settings.py          # Application settings
│   │   └── prompts.py           # AI prompt templates
│   └── data/                    # Data storage
│       ├── raw/                 # Raw uploaded data
│       ├── processed/           # Processed data
│       └── sample/              # Sample datasets
├── docker-compose.yml           # Docker orchestration
├── Dockerfile                   # Docker container definition
└── requirements.txt             # Python dependencies
```

## Dataset

The application works with survey data in CSV or JSON format. Sample data is included in `telcoresq/data/sample/`.

### Expected Data Format
- **CSV**: Text responses in columns (typically open-ended survey questions)
- **JSON**: Structured survey responses
- **Required**: At least one text column for analysis

### Sample Dataset
A sample telecom resilience survey dataset is provided at:
```
telcoresq/data/sample/sample_telecom_resilience_survey.csv
```

## AI Models & Services

### OpenAI Integration
- **GPT-4**: Used for sentiment analysis, theme extraction, and natural language queries
- **Embeddings**: Text embeddings for semantic search and similarity matching
- **API Key Required**: Set your OpenAI API key in the application sidebar

### Vector Search (FAISS)
- **Purpose**: Semantic similarity search for finding related responses
- **Implementation**: FAISS index for efficient similarity queries
- **Storage**: Indexes are saved locally for reuse

### Natural Language Processing
- **Sentiment Analysis**: Categorizes responses as positive, negative, or neutral
- **Theme Extraction**: Identifies recurring themes and topics
- **Query Processing**: Converts natural language questions into searchable queries

## Key Features

### Dashboard
- File upload and data preview
- Data preprocessing and cleaning
- Embedding generation and vector store creation
- Sentiment analysis with visualizations
- Theme extraction and categorization

### Query Interface
- Natural language question answering
- Semantic search across responses
- Context-aware answer generation
- Source response highlighting

### Reports
- Export functionality for insights
- Executive summary generation
- Data visualization exports

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the project root:
```env
OPENAI_API_KEY=your_openai_api_key_here
```

### Application Settings
Key settings can be modified in `telcoresq/config/settings.py`:
- Model configurations
- API endpoints
- Processing parameters

## Development

### Adding New Features
1. **Services**: Add new AI services in `telcoresq/app/services/`
2. **Components**: Create new UI components in `telcoresq/app/components/`
3. **Configuration**: Update settings in `telcoresq/config/`

### Testing
Run tests from the project root:
```bash
python -m pytest tests/
```

## Performance Considerations

- **Large Datasets**: Processing time scales with dataset size
- **API Costs**: OpenAI API usage incurs costs based on token usage
- **Memory**: Vector search requires sufficient RAM for large datasets
- **Caching**: FAISS indexes are cached for improved performance

## Troubleshooting

### Common Issues
1. **Module Import Errors**: Use Docker or set PYTHONPATH correctly
2. **Port Conflicts**: Ensure port 8501 is available
3. **API Key Issues**: Verify OpenAI API key is valid and has sufficient credits
4. **Memory Issues**: Reduce dataset size or increase system resources

### Logs
Check Docker logs for debugging:
```bash
docker-compose logs
```
