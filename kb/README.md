# Knowledge Base (kb/)

This directory contains domain reputation and threat intelligence data used by the capstone agent (L06) to make informed security assessments. These datasets enable the agent to distinguish legitimate domains from potentially malicious ones.

## Overview

**Total size:** ~96 MB
**Number of files:** 7
**Purpose:** Provide domain reputation context for web security analysis

The knowledge base is loaded by the `knowledgebase.py` singleton in [l06_web_sec_agent/tools/](../l06_web_sec_agent/tools/) and exposed as an MCP tool for the ReAct agent.

## Data Files

### 1. tranco.csv (15 MB, 1M domains)

**Source:** [Tranco Research-Oriented Top Sites Ranking](https://tranco-list.eu/)
**Last updated:** November 5, 2024
**Format:** One domain per line (no header)

```
google.com
microsoft.com
mail.ru
...
```

**Purpose:** Identify highly-ranked, legitimate domains
**Usage:** Domains in the top 10,000 are considered well-established and likely benign

**What is Tranco?**
- Research-oriented alternative to Alexa/Majestic rankings
- More stable than traditional rankings (less manipulation)
- Aggregates multiple sources (Alexa, Cisco Umbrella, Majestic, etc.)

**Security heuristic:**
- Top 1,000: Almost certainly legitimate
- Top 10,000: Highly likely to be legitimate
- Top 100,000: Established presence
- Not in list: Unknown, requires additional verification

---

### 2. crunchbase.csv (48 MB, 3M domains)

**Source:** Crunchbase business database (exported)
**Last updated:** November 5, 2024
**Format:** One domain per line (no header)

```
luxefitmodel.com
cresthire.com
landd-agency.co.uk
...
```

**Purpose:** Identify registered business domains
**Usage:** Domains associated with registered companies have more legitimacy

**What is Crunchbase?**
- Database of companies, investors, and business relationships
- Contains domains of startups, enterprises, and organizations
- Regularly updated with new business registrations

**Security heuristic:**
- If domain is in Crunchbase: Likely a real business
- If domain is NOT in Crunchbase: Could be legitimate (many businesses aren't listed) or malicious

---

### 3. public.csv (1.5 MB, 1.5M domains)

**Source:** Public/hosting/dynamic IP domains list
**Last updated:** November 5, 2024
**Format:** One domain per line (no header)

**Purpose:** Identify domains on public cloud/hosting infrastructure
**Usage:** Flag domains that might be temporarily hosted or on shared infrastructure

**Examples:**
- Cloud provider domains (AWS, GCP, Azure)
- Dynamic DNS providers (dyndns.org, no-ip.com)
- Free hosting services

**Security heuristic:**
- Public hosting: Higher risk (easy to set up, disposable)
- Dedicated hosting: More investment, potentially more legitimate

---

### 4. mal_ips.csv (1.3 MB, 96K IPs)

**Source:** Aggregated threat intelligence feeds
**Last updated:** November 5, 2024
**Format:** CSV with header

```
ip
13.248.197.209
216.218.185.162
...
```

**Purpose:** Identify known malicious IP addresses
**Usage:** Check if a domain resolves to a known bad IP

**Sources (typical aggregation):**
- Abuse.ch feeds
- Emerging Threats
- AlienVault OTX
- Spamhaus
- Other public threat feeds

**Security heuristic:**
- Domain resolves to IP in this list: HIGH RISK
- Domain doesn't resolve to malicious IP: Doesn't guarantee safety (IPs can change)

---

### 5. mal_ips_cdn.csv (617 KB, smaller subset)

**Source:** Malicious IPs filtered for CDN/cloud ranges
**Last updated:** November 5, 2024
**Format:** CSV with header

**Purpose:** Malicious IPs on CDN infrastructure
**Usage:** Higher confidence malicious IPs (removes false positives from shared hosting)

**Why separate file?**
- CDN IPs can be shared by many domains
- This list has higher-confidence malicious actors on CDN infrastructure
- Reduces false positives

---

### 6. GeoLite2-ASN-CSV.dat (6 MB)

**Source:** [MaxMind GeoLite2 ASN Database](https://dev.maxmind.com/geoip/geolite2-free-geolocation-data)
**Last updated:** November 5, 2024
**Format:** MaxMind CSV format

**Purpose:** Map IP addresses to Autonomous System Numbers (ASNs)
**Usage:** Identify the network operator/ISP hosting a domain

**What is ASN?**
- Autonomous System Number - unique identifier for a network
- Used to identify the organization operating the network
- Examples: AS15169 (Google), AS16509 (Amazon AWS)

**Security heuristic:**
- Legitimate ASNs (Google, Microsoft, AWS): Lower risk
- Suspicious ASNs (bulletproof hosting, known bad actors): Higher risk
- Residential/SOHO ASNs for business sites: Suspicious

---

### 7. GeoLite2-City-CSV.dat (22 MB)

**Source:** [MaxMind GeoLite2 City Database](https://dev.maxmind.com/geoip/geolite2-free-geolocation-data)
**Last updated:** November 5, 2024
**Format:** MaxMind CSV format

**Purpose:** Map IP addresses to geographic locations
**Usage:** Identify where a domain is hosted geographically

**Security heuristic:**
- Geographic mismatch: Domain claims to be US company but hosted in high-risk country
- Unexpected locations: Suspicious activity

---

## How the Agent Uses This Data

The capstone agent (L06) loads all these datasets into memory on startup and uses them to build a reputation score:

```python
# Simplified logic from knowledgebase.py
def get_domain_reputation(domain):
    score = 0

    # Check Tranco ranking
    if domain in tranco_top_10k:
        score += 50  # Highly trusted

    # Check if it's a registered business
    if domain in crunchbase:
        score += 20  # Business entity

    # Check if it's on public hosting
    if domain in public_hosting:
        score -= 10  # Slight risk

    # Check if IP is malicious
    ip = resolve(domain)
    if ip in malicious_ips:
        score -= 100  # Major red flag

    return reputation_category(score)
```

The agent combines this with:
- WHOIS data (registrar, age, ownership)
- VirusTotal threat intelligence
- URLScan screenshot analysis
- Historical threat reports (RAG)

## Updating the Data

These datasets should be refreshed periodically for production use:

### Tranco (monthly)
```bash
# Download latest Tranco list
curl https://tranco-list.eu/top-1m.csv.zip -o tranco.zip
unzip tranco.zip
mv top-1m.csv kb/tranco.csv
```

### Malicious IPs (weekly)
```bash
# Example: Abuse.ch Feodo Tracker
curl https://feodotracker.abuse.ch/downloads/ipblocklist.csv -o kb/mal_ips_new.csv
# Merge with existing, remove duplicates
```

### GeoLite2 (monthly)
```bash
# Requires MaxMind account (free)
# Download from: https://www.maxmind.com/en/accounts/current/geoip/downloads
```

## Data Privacy and Licensing

**Tranco:** Open research project, free to use
**Crunchbase:** Export may require Crunchbase license (check terms)
**GeoLite2:** Creative Commons Attribution-ShareAlike 4.0 License
**Malicious IP feeds:** Depends on source (most public feeds allow non-commercial use)

**Important:**
- For production use, verify you have appropriate licenses
- Some feeds prohibit commercial use without a license
- Consider using paid threat intelligence feeds for production

## Performance Considerations

Loading ~96 MB of data into memory:
- **Startup time:** ~2-5 seconds
- **Memory usage:** ~150-200 MB
- **Lookup speed:** O(1) for hash-based lookups (very fast)

For very large deployments:
- Consider using a database (PostgreSQL, Redis)
- Implement lazy loading (load datasets on first use)
- Use memory-mapped files for very large datasets

## Maintenance

The knowledge base singleton (`knowledgebase.py`) caches data:
- Data is loaded once on first access
- Subsequent calls use the cached data
- To refresh, restart the agent

## Security Considerations

**These datasets are not sufficient alone for security decisions:**

✅ **Use as one signal among many**
- Combine with WHOIS, TLS certificates, VirusTotal, URLScan
- No single indicator is definitive

❌ **Don't rely on these exclusively**
- False positives: Legitimate domains can be flagged
- False negatives: New threats won't be in the lists
- Data staleness: Threats evolve, data ages

**Production recommendations:**
- Refresh data regularly (weekly for IPs, monthly for domains)
- Use multiple threat feeds for redundancy
- Implement human review for high-stakes decisions
- Log all reputation checks for auditing

## Troubleshooting

**"File not found" errors**
- Ensure you're in the root workshop directory
- Check that kb/ folder contains all 7 files
- Verify file paths in `l06_web_sec_agent/tools/config.yml`

**"Out of memory" errors**
- The datasets are large (~96 MB)
- Ensure your system has at least 512 MB free RAM
- Consider using a database for constrained environments

**"Slow startup"**
- Loading 96 MB + parsing takes a few seconds
- This is normal and only happens once
- For faster startup, use smaller subsets during development

## Data Sources Summary

| File | Size | Records | Update Frequency | Purpose |
|------|------|---------|------------------|---------|
| tranco.csv | 15 MB | 1M | Monthly | Domain popularity |
| crunchbase.csv | 48 MB | 3M | Quarterly | Business domains |
| public.csv | 1.5 MB | 1.5M | Monthly | Hosting/cloud domains |
| mal_ips.csv | 1.3 MB | 96K | Weekly | Malicious IPs |
| mal_ips_cdn.csv | 617 KB | Subset | Weekly | High-confidence malicious IPs |
| GeoLite2-ASN-CSV.dat | 6 MB | Varies | Monthly | IP to ASN mapping |
| GeoLite2-City-CSV.dat | 22 MB | Varies | Monthly | IP to location mapping |

## Additional Resources

- [Tranco List](https://tranco-list.eu/)
- [MaxMind GeoLite2](https://dev.maxmind.com/geoip/geolite2-free-geolocation-data)
- [Abuse.ch Threat Feeds](https://abuse.ch/)
- [Crunchbase](https://www.crunchbase.com/)
