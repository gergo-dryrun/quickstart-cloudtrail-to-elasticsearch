import json
import os
import requests
from collections import defaultdict

from aws_requests_auth.aws_auth import AWSRequestsAuth
import cfn_resource


KIBANA_INDEX = '.kibana'
KIBANA_PATH = 'kibana_config'
ES_ENDPOINT = os.getenv('ES_ENDPOINT')


auth = AWSRequestsAuth(aws_access_key=os.environ['AWS_ACCESS_KEY_ID'],
                       aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
                       aws_host=ES_ENDPOINT,
                       aws_region=os.environ['AWS_DEFAULT_REGION'],
                       aws_service='es',
                       aws_token=os.environ['AWS_SESSION_TOKEN'])

def discover_configs():

    configs = defaultdict(list)
    for dirname, subdir, files in os.walk(os.path.abspath(KIBANA_PATH)):
        if not len(files):
            continue
        doc_type = os.path.basename(dirname)
        for doc_setup in files:
            with open(os.path.join(dirname, doc_setup)) as fp:
                doc_setup_json = json.load(fp)
                doc_setup_json['_NAME_'] = doc_setup.split('.json')[0]
                configs[doc_type].append(doc_setup_json)
    return configs


handler = cfn_resource.Resource()


@handler.create
def create_resource(event, context):
    try:
        doc_configs = discover_configs()
        for doc_config, doc_config_values in doc_configs.iteritems():
            URL_BASE = 'https://%s/%s/%s' % (ES_ENDPOINT, KIBANA_INDEX, doc_config)
            for config in doc_config_values:
                URL = '%s/%s' % (URL_BASE, config['_NAME_'])
                print 'Creating %s - %s at %s' % (doc_config, config['_NAME_'], URL)
                resp = requests.put(URL, json.dumps(config), auth=auth)
                print 'Status code %s - %s' % (resp.status_code, resp.text)
        return {'Status': 'SUCCESS',
                'Reason': 'Nothing to do',
                'PhysicalResourceId': 'dummy_resource_id',
                'Data': {}
                }
    except Exception as e:
        return {'Status': 'FAILED',
                'Reason': str(e),
                'PhysicalResourceId': 'dummy_resource_id',
                'Data': {}
                }

@handler.update
def update_resource(event, context):
    return {'Status': 'SUCCESS',
            'Reason': 'Nothing to do',
            'Data': {}
            }


@handler.delete
def delete_resource(event, context):
    return {'Status': 'SUCCESS',
            'Reason': 'Nothing to do',
            'Data': {}
            }


if __name__ == '__main__':
    create_resource(None, None)
