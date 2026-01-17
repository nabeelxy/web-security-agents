# Lesson 3.2 - URLScan MCP Server

This lesson demonstrates how to build an MCP server that integrates with URLScan.io, a web scanning service that captures screenshots, DOM trees, and network activity. This is the most advanced MCP example, showing caching, multimodal analysis (vision + text), and real-world API integration.

## What You'll Learn

- How to integrate third-party APIs as MCP tools
- Implementing caching to avoid rate limits
- Using Gemini vision models to analyze screenshots
- Handling asynchronous operations (scan submissions take time)
- Error handling for external services
- Combining multiple data sources (screenshot + DOM + metadata)

## Key Concepts

### URLScan.io

URLScan.io is a free service that:
- Crawls websites with a headless browser
- Captures full-page screenshots
- Records HTTP requests and responses
- Extracts DOM tree
- Generates security verdicts
- Provides public search interface

**Perfect for:** Phishing detection, malware distribution sites, brand impersonation

### Multimodal Analysis

This example combines:
1. **Screenshot analysis** (vision model) → Detects visual phishing cues
2. **DOM analysis** (text parsing) → Finds suspicious scripts, hidden elements
3. **Metadata analysis** (API response) → Gets verdicts, technologies detected

### Caching Strategy

URLScan free tier: **50 scans/day, 1 scan every ~30 seconds**

To avoid limits, this server:
- Checks [../../data/urlscan_cache.csv](../../data/urlscan_cache.csv) before scanning
- Uses cached screenshots and DOM when available
- Only calls API for new domains (if API key is present)

See [../../data/README.md](../../data/README.md) for cache details.

## Prerequisites

```bash
pip install google-adk google-genai
```

## Environment Setup

### Option 1: Use Cached Data (Recommended for Workshop)

No API key needed! The workshop includes pre-cached scans:

```bash
# Just run the agent
adk web
```

The server will use cached data from [../../data/](../../data/) for example domains.

### Option 2: Enable Live Scanning

For live scanning of new domains, get an API key:

1. Sign up at [urlscan.io](https://urlscan.io/)
2. Go to Settings → API
3. Copy your API key
4. Set environment variable:

```bash
URLSCAN_API_KEY=your_api_key_here
```

Add to [../../.env](../../.env):
```bash
URLSCAN_API_KEY=your_urlscan_api_key_here
```

## Functionalities Supported

The MCP server exposes these tools:

### 1. `scan_url`
Scans a URL and returns comprehensive analysis including:
- URLScan verdict (malicious/suspicious/benign)
- Screenshot analysis (visual phishing indicators)
- Technologies detected
- Links to full report

**Input:** Domain name (e.g., `paypal-login.com`)
**Output:** JSON with scan results + vision analysis

### 2. `fetch_screenshot`
Retrieves the screenshot for a previously scanned URL.

**Input:** Domain name or URLScan UUID
**Output:** Base64-encoded PNG image

### 3. `fetch_dom`
Retrieves the HTML DOM tree for a scanned page.

**Input:** Domain name or URLScan UUID
**Output:** HTML string

## Running the Agent

### Start the MCP Server + Web UI

```bash
adk web
```

Visit http://localhost:8080

### Example Queries

Try these queries with the agent:

**Using cached examples:**
```
Is coinbase-arena.com legitimate?
Analyze paypal-login.com for phishing indicators
What does carrtrucker.com look like?
```

**General analysis (if you have API key):**
```
Scan example-phishing-site.com and tell me if it's safe
What visual elements does suspicious-domain.com have?
```

## Code Walkthrough

### server.py - MCP Server

The server exposes URLScan functionality as MCP tools:

```python
@mcp_server.tool()
def scan_url(url: str):
    """Scan a URL using URLScan.io and analyze screenshot"""
    # 1. Check cache first
    # 2. If not cached, call URLScan API
    # 3. Wait for scan to complete
    # 4. Download screenshot
    # 5. Analyze screenshot with vision model
    # 6. Return comprehensive results
```

### urlscan.py - URLScan Client

The largest file in the workshop (213 lines) implements:

- **Cache management** - Read/write to `urlscan_cache.csv`
- **Scan submission** - POST to URLScan API
- **Result polling** - Wait for scan completion (can take 30-60 seconds)
- **Data retrieval** - Download screenshot, DOM, metadata
- **Error handling** - Rate limits, timeouts, API failures

**Key functions:**
- `scan_url(domain)` - Main entry point
- `_check_cache(domain)` - Look up cached results
- `_submit_scan(url)` - Submit new scan to URLScan
- `_wait_for_scan(uuid)` - Poll until ready
- `_download_screenshot(uuid)` - Save PNG to cache

### screenshot_analyzer.py - Vision Analysis

Uses Gemini's vision capabilities to detect phishing:

```python
def analyze_screenshot(image_path, domain):
    """Analyze screenshot for phishing indicators using vision model"""

    prompt = f"""
    You are a security analyst examining a screenshot of {domain}.
    Look for:
    - Login forms (credential harvesting)
    - Brand impersonation (logos, colors)
    - Urgency tactics (warnings, countdowns)
    - Suspicious UI elements
    - Typos or poor design quality

    Provide a security assessment.
    """

    # Send image + prompt to gemini-2.0-flash
    response = model.generate_content([prompt, image])
    return response.text
```

**Why vision models are powerful for phishing detection:**
- Detect visual brand impersonation (fake PayPal/bank logos)
- Identify suspicious UI patterns (fake urgency banners)
- Catch details that DOM analysis misses (images, CSS, layout)

## How Caching Works

Sequence diagram:

```
Agent asks: "Is coinbase-arena.com safe?"
    ↓
MCP Server receives: scan_url("coinbase-arena.com")
    ↓
urlscan.py checks: data/urlscan_cache.csv
    ↓
Cache HIT! UUID: 019a4727-3608-7594-9078-7e80631e199a
    ↓
Load: data/screenshots/019a4727...png
Load: data/dom/019a4727...html
    ↓
screenshot_analyzer.py analyzes image
    ↓
Return: {verdict: "suspicious", analysis: "..."}
```

If cache MISS and API key present:
```
Submit scan → Wait 30-60s → Download results → Cache for next time
```

## Pre-Cached Domains

The workshop includes these pre-scanned domains:

| Domain | Type | Visual Indicators |
|--------|------|-------------------|
| coinbase-arena.com | Phishing | Fake Coinbase login page |
| carrtrucker.com | Suspicious | Unknown service, poor design |
| reputationrescue.info | Suspicious | Typosquatting attempt |
| inslagarm.com | Suspicious | Random/generated domain |

See [../../data/README.md](../../data/README.md) for details.

## Common Issues

**"URLScan API key not found"**
- For workshop demos, you don't need an API key (use cached examples)
- For live scanning, set `URLSCAN_API_KEY` environment variable
- Verify the key is correct (check urlscan.io settings)

**"Scan timeout"**
- URLScan can take 30-60 seconds per scan
- The server waits up to 2 minutes before timing out
- Some sites fail to scan (errors, timeouts, JavaScript issues)

**"Rate limit exceeded"**
- Free tier: 50 scans/day
- Use cached examples during workshop
- Wait 24 hours for quota reset
- Consider paid tier for production

**"Screenshot analysis failed"**
- Ensure `GOOGLE_API_KEY` is set (for vision model)
- Check that screenshot file exists and is valid PNG
- Vision model requires Gemini 2.0+ (supports multimodal)

**"Cache not found"**
- Ensure you're running from the workshop root directory
- Check that `data/urlscan_cache.csv` exists
- Verify the domain is spelled exactly as in the cache

## Comparison with Previous MCP Lessons

| Lesson | Transport | Complexity | External API | Caching |
|--------|-----------|------------|--------------|---------|
| L03.0 | STDIO | Low | No | No |
| L03.0 (HTTP) | HTTP | Low | No | No |
| L03.1 | STDIO | Medium | Yes (VT) | No |
| **L03.2** | **STDIO** | **High** | **Yes (URLScan)** | **Yes** |

## Production Considerations

For production deployment:

1. **Implement proper async/await** - Don't block for 60 seconds
2. **Add retry logic** - URLScan can be flaky
3. **Set up webhooks** - Don't poll, get notified when scans complete
4. **Cache aggressively** - Scans rarely change for static pages
5. **Use private scans** - Public scans are visible to everyone
6. **Monitor costs** - Vision API calls add up
7. **Add rate limiting** - Protect against abuse
8. **Implement cache TTL** - Refresh stale scans after 7 days

## Next Steps

- **L04** - Learn about RAG for historical threat intelligence
- Experiment with analyzing your own domains (if you have API key)
- Try modifying the screenshot analysis prompt for different use cases
- Compare vision model analysis with DOM parsing

## Additional Resources

- [URLScan.io API Documentation](https://urlscan.io/docs/api/)
- [URLScan.io Search](https://urlscan.io/search/) - Browse public scans
- [Gemini Vision Documentation](https://ai.google.dev/gemini-api/docs/vision)
- [MCP Specification](https://spec.modelcontextprotocol.io/)
