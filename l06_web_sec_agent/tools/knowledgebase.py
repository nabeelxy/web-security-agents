import yaml
from yaml.loader import SafeLoader
import pandas as pd
import os

'''
This simulates a database lookup of known benign/malicous knowledge.
In a production system, it would be stored in a database and one
would perform database lookups to fetch information.
'''
class KnowledgeBase:
    # Domains listed in a recent tranco list - in a production system,
    # we expect to profile and maintain latest tranco information
    tranco = dict()
    # Known public domains like rentable domains, web hosting domains,
    # CDNs, DDNSes, etc.
    public_doms = set()
    # A static snapshot of domains maintained by Crunchbase inc.
    crunchbase = set()
    # A static list of IP addresses known to hosting malicious domains recently
    known_mal_ips = set()
    # A static list of CDN IP addresses known to hosting maicious domains recently
    known_mal_cdn_ips = set()

    initialized = False

    @staticmethod
    def init(cfg_file):
        if KnowledgeBase.initialized:
            return
        with open(cfg_file) as cfgfile:
            cfg = yaml.load(cfgfile, Loader = SafeLoader)

        if cfg == None:
            raise Exception("Unable to load configuration file")

        tranco_filename = cfg.get("tranco_filename", None)
        crunchbase_filename = cfg.get("crunchbase_filename", None)
        public_filename = cfg.get("public_filename", None)
        malip_filename = cfg.get("malip_filename", None)
        malip_cdn_filename = cfg.get("malip_cdn_filename", None)

        if tranco_filename == None or\
            crunchbase_filename == None or\
            public_filename == None or malip_filename == None or\
            malip_cdn_filename == None:
            raise Exception("Invalid knowledge filename")

        KnowledgeBase.tranco = KnowledgeBase.load_ranked_file(os.path.join(os.path.dirname(__file__), tranco_filename))
        KnowledgeBase.crunchbase = KnowledgeBase.load_file(os.path.join(os.path.dirname(__file__), crunchbase_filename))
        KnowledgeBase.public_doms = KnowledgeBase.load_file(os.path.join(os.path.dirname(__file__), public_filename))
        KnowledgeBase.malip = KnowledgeBase.load_file(os.path.join(os.path.dirname(__file__), malip_filename), 'ip')
        KnowledgeBase.malip_cdn = KnowledgeBase.load_file(os.path.join(os.path.dirname(__file__), malip_cdn_filename), 'ip')
        KnowledgeBase.initialized = True

    @staticmethod
    def load_file(filename, column='domain'):
        df = pd.read_csv(filename, header = None)
        df.columns = [column]
        return set(df[column].unique())
    
    @staticmethod
    def load_ranked_file(filename, column='domain'):
        df = pd.read_csv(filename, header = None)
        df.columns = [column]
        d = dict()
        for index, row in df.iterrows():
            d[row[column]] = index + 1
        return d