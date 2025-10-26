# FitFindr Backend API

AI-powered fashion recommendation system backend built with FastAPI.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Virtual environment (recommended)

### Installation

1. **Activate virtual environment:**
   ```bash
   # Windows
   ..\venv\Scripts\Activate.ps1
   
   # macOS/Linux
   source ../venv/bin/activate
   ```

2. **Install dependencies:**
   ```bash
   pip install fastapi uvicorn python-multipart requests beautifulsoup4
   ```

3. **Start the server:**
   ```bash
   python start_server.py
   # OR
   python -m uvicorn main:app --reload
   ```

4. **Access the API:**
   - Base URL: `http://127.0.0.1:8000`
   - API Documentation: `http://127.0.0.1:8000/docs`
   - Interactive API: `http://127.0.0.1:8000/redoc`

## 📚 API Endpoints

### Core Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API information and available endpoints |
| `/query` | POST | Process user style and image |
| `/scrape` | POST | Scrape Pinterest for fashion items |
| `/recommend` | POST | Generate outfit recommendations |
| `/feedback` | POST | Record user feedback |
| `/analyze` | POST | Get AI analysis and explanations |

### Additional Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/styles` | GET | Get available style options |
| `/trending` | GET | Get trending items |
| `/user/{user_id}/feedback` | GET | Get user's feedback summary |
| `/analytics` | GET | Get overall analytics |

## 🔧 Usage Examples

### 1. Process User Query
```bash
curl -X POST "http://127.0.0.1:8000/query" \
  -F "style=vintage streetwear" \
  -F "image=@user_photo.jpg"
```

### 2. Scrape Pinterest Items
```bash
curl -X POST "http://127.0.0.1:8000/scrape" \
  -H "Content-Type: application/json" \
  -d '{"keyword": "vintage streetwear", "max_items": 20}'
```

### 3. Get Recommendations
```bash
curl -X POST "http://127.0.0.1:8000/recommend" \
  -H "Content-Type: application/json" \
  -d '{"max_recommendations": 10}'
```

### 4. Record Feedback
```bash
curl -X POST "http://127.0.0.1:8000/feedback" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user_123",
    "item_id": "item_456", 
    "feedback_type": "like"
  }'
```

## 🏗️ Architecture

### Core Modules

- **`queryhandler.py`** - Processes user queries and coordinates modules
- **`scraper.py`** - Pinterest web scraping functionality
- **`analyzer.py`** - AI analysis using Gemini API
- **`recommender.py`** - Recommendation engine with scoring
- **`feedback.py`** - User feedback management
- **`shapedetector.py`** - Body shape detection and styling tips
- **`storage.py`** - JSON data persistence

### Data Structure

```
backend/
├── main.py                 # FastAPI application
├── core/                   # Core modules
│   ├── queryhandler.py
│   ├── scraper.py
│   ├── analyzer.py
│   ├── recommender.py
│   ├── feedback.py
│   ├── shapedetector.py
│   └── storage.py
├── data/                   # JSON data storage
│   ├── users.json
│   ├── items.json
│   ├── recommendations.json
│   └── feedback.json
└── requirements.txt        # Dependencies
```

## 🤖 AI Integration

### Gemini API Setup

1. **Get API Key:**
   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key

2. **Set Environment Variable:**
   ```bash
   # Windows
   set GEMINI_API_KEY=your_api_key_here
   
   # macOS/Linux
   export GEMINI_API_KEY=your_api_key_here
   ```

3. **Features:**
   - Body shape detection from images
   - Outfit compatibility scoring
   - Personalized style explanations
   - AI-powered recommendations

## 📊 Data Flow

1. **User Query** → Process style + image → Body shape analysis
2. **Scraping** → Pinterest items → Filter by style
3. **Recommendation** → Score items → Generate outfit combinations
4. **Feedback** → Record likes/dislikes → Improve future recommendations
5. **Analysis** → AI explanations → Personalized insights

## 🧪 Testing

### Run Test Suite
```bash
python test_server.py
```

### Manual Testing
1. Open `http://127.0.0.1:8000/docs` in your browser
2. Use the interactive API documentation
3. Test endpoints with sample data

## 🔧 Development

### Project Structure
- **Modular Design**: Each core module handles specific functionality
- **JSON Storage**: Simple file-based data persistence
- **Mock Data**: Fallback data for demo purposes
- **Error Handling**: Comprehensive error handling and logging

### Key Features
- **CORS Enabled**: Ready for frontend integration
- **Input Validation**: Robust input validation
- **Logging**: Activity logging for debugging
- **Mock Data**: Works without external APIs for demo

## 🚀 Deployment

### Local Development
```bash
python start_server.py
```

### Production Deployment
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## 📝 API Response Format

### Success Response
```json
{
  "message": "Operation completed successfully",
  "data": { ... },
  "status": "success"
}
```

### Error Response
```json
{
  "detail": "Error description",
  "status_code": 400
}
```

## 🔍 Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed
2. **Port Conflicts**: Change port if 8000 is occupied
3. **CORS Issues**: Check frontend URL configuration
4. **API Key Errors**: Verify Gemini API key is set correctly

### Debug Mode
```bash
python -m uvicorn main:app --reload --log-level debug
```

## 📈 Performance

- **Response Time**: < 2 seconds for most operations
- **Concurrent Users**: Supports multiple simultaneous requests
- **Memory Usage**: Optimized for minimal memory footprint
- **Scalability**: Ready for horizontal scaling

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is part of the FitFindr hackathon project.
