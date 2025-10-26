# FitFindr API Demo Commands

## 🎯 Complete Demo Flow

### Step 1: Process User Query (with style preference)
```bash
curl -X POST "http://127.0.0.1:8000/query" \
  -F "style=vintage streetwear"
```

### Step 2: Scrape Pinterest for Items
```bash
curl -X POST "http://127.0.0.1:8000/scrape" \
  -H "Content-Type: application/json" \
  -d '{"keyword": "vintage streetwear", "max_items": 20}'
```

### Step 3: Get AI Recommendations
```bash
curl -X POST "http://127.0.0.1:8000/recommend" \
  -H "Content-Type: application/json" \
  -d '{"max_recommendations": 10}'
```

### Step 4: Record Feedback (like/dislike items)
```bash
curl -X POST "http://127.0.0.1:8000/feedback" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user_123",
    "item_id": "pinterest_1", 
    "feedback_type": "like"
  }'
```

### Step 5: Get AI Analysis
```bash
curl -X POST "http://127.0.0.1:8000/analyze" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "user_123"}'
```

## 🎨 Different Style Examples

### Vintage Streetwear
```bash
curl -X POST "http://127.0.0.1:8000/scrape" \
  -H "Content-Type: application/json" \
  -d '{"keyword": "vintage streetwear", "max_items": 15}'
```

### Minimalist Chic
```bash
curl -X POST "http://127.0.0.1:8000/scrape" \
  -H "Content-Type: application/json" \
  -d '{"keyword": "minimalist chic", "max_items": 15}'
```

### Bohemian Style
```bash
curl -X POST "http://127.0.0.1:8000/scrape" \
  -H "Content-Type: application/json" \
  -d '{"keyword": "bohemian fashion", "max_items": 15}'
```

## 📊 Get Analytics
```bash
curl -X GET "http://127.0.0.1:8000/analytics"
```

## 🔥 Get Trending Items
```bash
curl -X GET "http://127.0.0.1:8000/trending"
```

## 🎭 Get Available Styles
```bash
curl -X GET "http://127.0.0.1:8000/styles"
```
