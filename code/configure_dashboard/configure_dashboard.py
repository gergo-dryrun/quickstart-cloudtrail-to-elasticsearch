import json
import os
import requests
from collections import defaultdict


KIBANA_INDEX = '.kibana'
KIBANA_PATH = 'kibana_config'
ES_ENDPOINT = os.getenv('ES_ENDPOINT')


def discover_configs():

    configs = defaultdict(list)
    for dirname, subdir, files in os.walk(os.path.abspath(KIBANA_PATH)):
        if not len(files):
            continue
        doc_type = os.path.basename(dirname)
        for doc_setup in files:
            with open(os.path.join(dirname, doc_setup)) as fp:
                doc_setup_json = json.load(fp)
                configs[doc_type].append(doc_setup_json)
    return configs


def lambda_handler(event, context):
    doc_configs = discover_configs()
    for doc_config, doc_config_values in doc_configs.iteritems():
        URL_BASE = 'https://%s/%s/%s' % (ES_ENDPOINT, KIBANA_INDEX, doc_config)
        for config in doc_config_values:
            URL = '%s/%s' % (URL_BASE, config['title'])
            print 'Creating %s - %s at %s' % (doc_config, config['title'], URL)
            # resp = requests.put(URL, json.dumps(config))
            # print resp

