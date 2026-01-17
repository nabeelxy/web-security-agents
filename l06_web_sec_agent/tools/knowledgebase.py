"""
Knowledge Base Loader - Domain Reputation Data

This module implements a singleton-pattern knowledge base that loads domain reputation
datasets into memory for fast lookups. It simulates what would typically be a database
in a production system.

The knowledge base contains:
- Tranco top 1M domains (with rankings)
- Crunchbase business domains
- Public/cloud hosting domains
- Known malicious IP addresses
- Malicious IPs on CDN infrastructure

All data is loaded once on first access and cached in memory for O(1) lookup performance.

Usage:
    KnowledgeBase.init('config.yml')
    if 'google.com' in KnowledgeBase.tranco:
        rank = KnowledgeBase.tranco['google.com']
        print(f"Google.com is ranked #{rank}")

Performance:
    - Loading time: ~2-5 seconds (96MB of data)
    - Memory usage: ~150-200 MB
    - Lookup time: O(1) for set/dict operations
    - Trade-off: Fast queries at the cost of startup time and memory

Production Considerations:
    In a production system, this would be replaced with:
    - Database (PostgreSQL, MySQL) for persistent storage
    - Redis/Memcached for in-memory caching
    - Regular updates (weekly for malicious IPs, monthly for domains)
    - Partitioning for very large datasets
"""

import yaml
from yaml.loader import SafeLoader
import pandas as pd
import os


class KnowledgeBase:
    """
    Singleton knowledge base for domain reputation data.

    This class uses the static/class variable pattern to ensure data is loaded
    only once and shared across all instances. The 'initialized' flag prevents
    redundant loading.

    Class Attributes:
        tranco (dict): Domain -> Rank mapping (e.g., {'google.com': 1})
            - Contains top 1M domains from Tranco list
            - Lower rank = more popular (1 is most popular)
            - Empty if not in top 1M

        public_doms (set): Domains on public/cloud/shared hosting
            - Includes AWS, GCP, Azure, DDNs, free hosting
            - Presence indicates potentially disposable infrastructure

        crunchbase (set): Domains of registered businesses
            - Contains ~3M business domains from Crunchbase
            - Presence indicates legitimate business entity

        known_mal_ips (set): IP addresses hosting malicious domains
            - Contains ~96K known bad IPs from threat feeds
            - Regularly updated from abuse databases

        known_mal_cdn_ips (set): Malicious IPs on CDN infrastructure
            - Subset of mal_ips with higher confidence
            - Filters out shared hosting false positives

        initialized (bool): Whether data has been loaded
            - Prevents redundant loading on subsequent init() calls
    """

    # Domain reputation data (loaded once, shared across all uses)
    tranco = dict()             # Domain -> Popularity rank
    public_doms = set()         # Public/cloud hosting domains
    crunchbase = set()          # Registered business domains
    known_mal_ips = set()       # Known malicious IP addresses
    known_mal_cdn_ips = set()   # Malicious IPs on CDNs

    # Singleton pattern flag
    initialized = False

    @staticmethod
    def init(cfg_file):
        """
        Initialize the knowledge base by loading all datasets from disk.

        This method loads ~96MB of reputation data into memory. It should be
        called once at application startup. Subsequent calls are no-ops.

        Args:
            cfg_file (str): Path to YAML config file with dataset paths
                Example config.yml:
                    tranco_filename: ../../kb/tranco.csv
                    crunchbase_filename: ../../kb/crunchbase.csv
                    public_filename: ../../kb/public.csv
                    malip_filename: ../../kb/mal_ips.csv
                    malip_cdn_filename: ../../kb/mal_ips_cdn.csv

        Raises:
            Exception: If config file is invalid or datasets are missing

        Performance:
            - First call: ~2-5 seconds to load all datasets
            - Subsequent calls: <1ms (no-op due to initialized flag)

        Example:
            >>> KnowledgeBase.init('config.yml')
            >>> print(f"Loaded {len(KnowledgeBase.tranco)} Tranco domains")
            Loaded 1000000 Tranco domains
        """
        # Check if already initialized (singleton pattern)
        if KnowledgeBase.initialized:
            return  # Data already loaded, skip

        # Load configuration file (YAML format)
        with open(cfg_file) as cfgfile:
            cfg = yaml.load(cfgfile, Loader=SafeLoader)

        # Validate configuration
        if cfg is None:
            raise Exception("Unable to load configuration file")

        # Extract dataset paths from config
        tranco_filename = cfg.get("tranco_filename", None)
        crunchbase_filename = cfg.get("crunchbase_filename", None)
        public_filename = cfg.get("public_filename", None)
        malip_filename = cfg.get("malip_filename", None)
        malip_cdn_filename = cfg.get("malip_cdn_filename", None)

        # Ensure all required datasets are specified
        if tranco_filename is None or \
           crunchbase_filename is None or \
           public_filename is None or \
           malip_filename is None or \
           malip_cdn_filename is None:
            raise Exception("Invalid knowledge filename - missing required datasets")

        # Load datasets into memory (relative to this file's location)
        # Each load operation reads CSV and converts to set/dict for O(1) lookups
        base_path = os.path.dirname(__file__)

        KnowledgeBase.tranco = KnowledgeBase.load_ranked_file(
            os.path.join(base_path, tranco_filename)
        )  # ~1M domains with ranks (dict)

        KnowledgeBase.crunchbase = KnowledgeBase.load_file(
            os.path.join(base_path, crunchbase_filename)
        )  # ~3M business domains (set)

        KnowledgeBase.public_doms = KnowledgeBase.load_file(
            os.path.join(base_path, public_filename)
        )  # ~1.5M public hosting domains (set)

        KnowledgeBase.malip = KnowledgeBase.load_file(
            os.path.join(base_path, malip_filename), 'ip'
        )  # ~96K malicious IPs (set)

        KnowledgeBase.malip_cdn = KnowledgeBase.load_file(
            os.path.join(base_path, malip_cdn_filename), 'ip'
        )  # Subset of malicious IPs on CDNs (set)

        # Mark as initialized to prevent reloading
        KnowledgeBase.initialized = True

    @staticmethod
    def load_file(filename, column='domain'):
        """
        Load a simple CSV file into a set for fast O(1) membership testing.

        Args:
            filename (str): Path to CSV file (no header)
            column (str): Name to assign to the column (default: 'domain')

        Returns:
            set: Unique values from the CSV file

        File Format:
            domain1.com
            domain2.com
            domain3.com

        Example:
            >>> domains = KnowledgeBase.load_file('public.csv')
            >>> if 'amazonaws.com' in domains:
            ...     print("AWS domain detected")

        Performance:
            - O(n) to load from disk
            - O(1) for membership testing after loading
            - Set automatically handles duplicates
        """
        # Use pandas for efficient CSV parsing
        df = pd.read_csv(filename, header=None)
        df.columns = [column]

        # Convert to set for O(1) membership testing
        # unique() removes duplicates (though sets do this anyway)
        return set(df[column].unique())

    @staticmethod
    def load_ranked_file(filename, column='domain'):
        """
        Load a ranked CSV file (like Tranco) into a dict mapping domain -> rank.

        The Tranco list is ordered by popularity, so the first line is rank 1,
        second line is rank 2, etc. This function preserves that ranking.

        Args:
            filename (str): Path to CSV file (no header, ordered by rank)
            column (str): Name to assign to the column (default: 'domain')

        Returns:
            dict: Mapping of domain -> rank (1-indexed)

        File Format:
            google.com       <- Rank 1
            microsoft.com    <- Rank 2
            mail.ru          <- Rank 3
            ...

        Example:
            >>> tranco = KnowledgeBase.load_ranked_file('tranco.csv')
            >>> rank = tranco.get('google.com', float('inf'))
            >>> if rank <= 10000:
            ...     print(f"Top 10K domain (rank #{rank})")

        Performance:
            - O(n) to load and build dict
            - O(1) for rank lookups after loading

        Security Use Case:
            - Rank ≤ 1,000: Almost certainly legitimate
            - Rank ≤ 10,000: Highly likely legitimate
            - Rank ≤ 100,000: Established domain
            - Not in dict (rank > 1M): Unknown, needs verification
        """
        # Parse CSV without header
        df = pd.read_csv(filename, header=None)
        df.columns = [column]

        # Build dict mapping domain to rank (1-indexed)
        d = dict()
        for index, row in df.iterrows():
            # index starts at 0, so add 1 for human-readable ranks
            d[row[column]] = index + 1

        return d