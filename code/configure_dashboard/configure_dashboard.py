import json
import os
import requests
from collections import defaultdict

import cfn_resource


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


def send_response(event, context, responseStatus, responseData=None):
    response_body = {
        'Status': responseStatus,
        'Reason': "See the details in CloudWatch Log Stream: " + context.logStreamName,
        'PhysicalResourceId': context.logStreamName,
        'StackId': event.StackId,
        'RequestId': event.RequestId,
        'LogicalResourceId': event.LogicalResourceId,
        'Data': responseData
        }
    print 'Response body %s' % response_body


handler = cfn_resource.Resource()


@handler.create
def create_resource():
    doc_configs = discover_configs()
    for doc_config, doc_config_values in doc_configs.iteritems():
        URL_BASE = 'https://%s/%s/%s' % (ES_ENDPOINT, KIBANA_INDEX, doc_config)
        for config in doc_config_values:
            URL = '%s/%s' % (URL_BASE, config['title'])
            print 'Creating %s - %s at %s' % (doc_config, config['title'], URL)
            resp = requests.put(URL, json.dumps(config))
            print resp
    return {'Status': 'SUCCESS',
            'Reason': 'Nothing to do',
            'Data': {}
            }

@handler.update
def update_resource():
    return {'Status': 'SUCCESS',
            'Reason': 'Nothing to do',
            'Data': {}
            }


@handler.delete
def delete_resource():
    return {'Status': 'SUCCESS',
            'Reason': 'Nothing to do',
            'Data': {}
            }


if __name__ == '__main__':
    create_resource(None, None)
