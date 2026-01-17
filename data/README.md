# Data Cache Directory

This directory contains pre-fetched URLScan.io results and screenshots used by the workshop to avoid rate limiting during demos. The URLScan MCP server (L03.2) and capstone agent (L06) use this cached data when available.

## Overview

**Purpose:** Provide workshop participants with pre-cached scan results
**Why:** URLScan.io free tier has strict rate limits (50 scans/day)
**Benefit:** Run the workshop examples without hitting API quotas

## Directory Structure

```
data/
├── urlscan_cache.csv          # Maps domains to URLScan UUIDs
├── screenshots/               # PNG screenshots from URLScan
│   └── {uuid}.png
├── dom/                       # HTML DOM trees from URLScan
│   └── {uuid}.html
└── report/                    # Full URLScan JSON reports (if needed)
    └── {uuid}.json
```

## Files Explained

### urlscan_cache.csv

**Format:** CSV with header
```csv
url,uuid
coinbase-arena.com,019a4727-3608-7594-9078-7e80631e199a
carrtrucker.com,019a4725-63da-72b7-aa0f-eb2751031f55
reputationrescue.com,019a472a-039a-771e-b072-212b48d486fe
inslagarm.com,019a472b-434e-7237-b968-d1589a70ffaf
```

**Purpose:** Maps domain names to URLScan scan UUIDs
**Usage:** The URLScan MCP server checks this file before making API calls

**How it works:**
1. Agent requests scan for `paypal-login.com`
2. Server checks `urlscan_cache.csv` for the domain
3. If found, uses cached UUID instead of calling URLScan API
4. If not found, performs a real URLScan (if API key available)

### screenshots/ directory

**Contents:** PNG images captured by URLScan headless browser
**Naming:** `{uuid}.png` where UUID comes from URLScan scan result
**Size:** Varies (10 KB - 500 KB per screenshot)

**Example:**
- `019a4727-3608-7594-9078-7e80631e199a.png` → Screenshot of coinbase-arena.com

**Purpose:**
- Visual analysis by the Gemini vision model
- Detects phishing indicators (fake login forms, brand impersonation)
- Identifies suspicious UI elements (urgency banners, typos)

**How the agent uses screenshots:**
- Passed to `screenshot_analyzer.py` in L03.2
- Gemini vision model analyzes for phishing signals
- Combined with other intelligence for final assessment

### dom/ directory

**Contents:** HTML DOM trees from URLScan
**Naming:** `{uuid}.html` where UUID comes from URLScan scan result
**Size:** Varies (8 KB - 200 KB per file)

**Purpose:**
- Contains the rendered HTML of the scanned page
- Useful for detecting hidden scripts, iframes, redirects
- Can be parsed to extract links, forms, meta tags

**Not currently used by workshop agents but available for:**
- Advanced DOM analysis
- Extracting suspicious JavaScript
- Checking for obfuscation techniques
- Analyzing page structure

### report/ directory

**Contents:** Full URLScan JSON reports (optional)
**Currently:** Mostly empty (workshop uses screenshots/DOM mainly)
**Purpose:** Complete scan metadata if needed for advanced analysis

**Full reports contain:**
- Page metadata (title, links, cookies)
- Network requests (all HTTP calls)
- Technologies detected (frameworks, analytics)
- Geolocation of servers
- TLS certificate details
- Verdicts (malicious/suspicious/benign)

## How Caching Works

The caching mechanism is implemented in [l03_2_urlscan_mcp/urlscan.py:1-213](../l03_2_urlscan_mcp/urlscan.py#L1-L213):

```python
# Simplified caching logic
def scan_url(domain):
    # 1. Check cache first
    if domain in urlscan_cache:
        uuid = get_cached_uuid(domain)
        return load_cached_result(uuid)

    # 2. If not cached, call API
    if URLSCAN_API_KEY:
        result = urlscan_api.scan(domain)
        cache_result(domain, result.uuid)
        return result
    else:
        return "No cached data and no API key"
```

## Pre-Cached Domains

The workshop includes pre-cached scans for:

| Domain | Type | Purpose |
|--------|------|---------|
| coinbase-arena.com | Phishing | Brand impersonation example |
| carrtrucker.com | Suspicious | Unknown/new domain |
| reputationrescue.info | Suspicious | Typosquatting example |
| inslagarm.com | Suspicious | Random/generated domain |

These were selected to demonstrate different threat categories during the workshop.

## Adding Your Own Cached Scans

To cache additional domains for your workshop:

### 1. Perform URLScan (requires API key)

```bash
cd l03_2_urlscan_mcp
python -c "
from urlscan import scan_url
result = scan_url('example.com')
print(f'UUID: {result.uuid}')
"
```

### 2. Files are automatically saved

The URLScan wrapper automatically:
- Downloads screenshot to `data/screenshots/{uuid}.png`
- Downloads DOM to `data/dom/{uuid}.html`
- Adds entry to `data/urlscan_cache.csv`

### 3. Commit to version control (optional)

```bash
git add data/urlscan_cache.csv
git add data/screenshots/{uuid}.png
git add data/dom/{uuid}.html
git commit -m "Add cached scan for example.com"
```

## Rate Limit Strategy

**URLScan.io Free Tier Limits:**
- 50 scans per day
- 1 scan every ~30 seconds (rate limit)
- Public scans are visible to all users

**Workshop Strategy:**
1. **Pre-cache common examples** → Avoid hitting limits during workshop
2. **Graceful fallback** → Return "no scan available" if no cache + no API key
3. **Encourage participants to use cache** → Don't scan every domain during testing

**For production:**
- Consider URLScan.io paid tier (higher limits)
- Implement request throttling (respect rate limits)
- Cache aggressively (scans don't change for static sites)
- Use alternative screenshot services (Puppeteer, Playwright)

## Cache Freshness

**Important:** Cached scans can become stale

**Considerations:**
- Malicious sites can change content after being reported
- Domains can be taken down or parked
- Screenshots represent a point-in-time view

**Recommendations:**
- For workshop demos: Cache is fine (examples are illustrative)
- For production: Set cache TTL (e.g., 7 days) and refresh
- For critical decisions: Always perform fresh scans

## Clearing the Cache

To start fresh:

```bash
# Remove cache file
rm data/urlscan_cache.csv

# Remove screenshots
rm data/screenshots/*

# Remove DOM files
rm data/dom/*

# Create empty cache (optional)
echo "url,uuid" > data/urlscan_cache.csv
```

## Privacy and Ethics

**URLScan.io scans are public by default:**
- Anyone can see what you've scanned
- Scans are indexed and searchable
- Don't scan internal/private URLs

**Workshop Considerations:**
- Pre-cached scans are already public
- Participants should only scan public websites
- Avoid scanning domains you don't own without permission

**For production:**
- Use URLScan private scans (paid tier)
- Implement proper authorization checks
- Respect robots.txt and terms of service

## Storage Considerations

**Current usage:** ~1.5 MB (5 domains cached)
**Estimated at scale:** ~300 KB per domain (screenshot + DOM)

**For 100 cached domains:**
- ~30 MB total
- Acceptable for version control if compressed

**For 1000+ cached domains:**
- Consider external storage (S3, GCS)
- Don't commit to Git (use Git LFS or external hosting)
- Implement cache pruning (remove old scans)

## Troubleshooting

**"Screenshot not found"**
- Check that UUID in `urlscan_cache.csv` matches screenshot filename
- Verify screenshot file exists in `data/screenshots/`
- Try deleting cache entry and re-scanning

**"DOM file empty or corrupted"**
- URLScan sometimes fails to capture DOM (page errors, timeouts)
- Delete the cached entry and re-scan
- Check URLScan.io website for scan errors

**"Cache not being used"**
- Ensure `urlscan_cache.csv` exists in `data/` folder
- Check that domain is spelled exactly the same (case-sensitive)
- Verify the URLScan server is loading the cache file correctly

**"URLScan API quota exceeded"**
- This is why we have the cache!
- Use only cached domains during workshop
- Wait 24 hours for quota to reset
- Consider upgrading to paid tier

## Example: Analyzing a Cached Screenshot

```python
from l03_2_urlscan_mcp import screenshot_analyzer

# Load cached screenshot
screenshot_path = "data/screenshots/019a4727-3608-7594-9078-7e80631e199a.png"

# Analyze with Gemini vision
analysis = screenshot_analyzer.analyze(screenshot_path)

print(analysis)
# Output: "This appears to be a phishing page impersonating Coinbase.
#          The domain 'coinbase-arena.com' is suspicious. The page
#          requests login credentials..."
```

## Integration with L03.2 and L06

**L03.2 (URLScan MCP Server):**
- Implements the caching logic
- Checks cache before calling API
- Saves new scans to cache automatically

**L06 (Capstone Agent):**
- Uses URLScan MCP server as a tool
- Benefits from cached results
- Combines screenshot analysis with other intelligence

## Maintaining the Cache

For workshop instructors:

1. **Before workshop:**
   - Pre-scan example domains
   - Verify screenshots are high quality
   - Test that cache loading works

2. **During workshop:**
   - Stick to cached examples
   - Only demonstrate live scans if quota allows
   - Have backup examples if API is down

3. **After workshop:**
   - Consider caching participant discoveries
   - Share interesting findings with the community
   - Update cache with new phishing examples

## Additional Resources

- [URLScan.io API Documentation](https://urlscan.io/docs/api/)
- [URLScan.io Search Interface](https://urlscan.io/search/)
- [L03.2 URLScan MCP Server](../l03_2_urlscan_mcp/)
- [Screenshot Analyzer Code](../l03_2_urlscan_mcp/screenshot_analyzer.py)
