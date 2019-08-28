#!/usr/bin/python
import os, sys, time, requests, thread, json
from flask import Flask, request
from threading import Thread


app = Flask(__name__)

ETCD_CMD_TEMPLATE = '/bin/etcd --data-dir /data --name %s --initial-advertise-peer-urls %s:2380 --listen-peer-urls http://0.0.0.0:2380 --listen-client-urls http://0.0.0.0:2379 --advertise-client-urls %s:2379 --initial-cluster %s --initial-cluster-state %s'
HOSTNAME = ''
STS_INDEX = 0
STS_NAME = ''
SERVICE_URL = ''
SERVICE_NAME = ''
#NAMESPACE_NAME = ''
UPDATE_INTERVAL = 5
#ETCD_READY = False
ETCD_NODE_NAME_LIST = []
ETCD_NODE_URL_LIST = []
ETCD_NODE_ID_LIST = []
ETCD_NODE_STATE_LIST = []
NODE_READINESS = False


def launch_etcd():
    global HOSTNAME      # Name of the pod, and in a StatefulSet we have HOSTNAME = '%s-%s'.format(STS_NAME, STS_INDEX)
    global STS_INDEX     # Index of this pod
    global STS_NAME      # Name of the StatefulSet
    global SERVICE_NAME  # Name of the Headless Service
    global SERVICE_URL
    global ETCD_NODE_NAME_LIST
    global ETCD_NODE_URL_LIST
    global ETCD_NODE_ID_LIST
    global ETCD_NODE_STATE_LIST
    global NODE_READINESS
    #global NAMESPACE_NAME

    #time.sleep(30)

    # Use localhost only in debug mode
    if len(sys.argv) > 2 and (sys.argv[1] == '--hostname' or sys.argv[1] == '-h'):
        HOSTNAME = sys.argv[2]
        #os.system("sed -i '1s/^/127.0.0.1 %s\\n/' /etc/hosts" % sys.argv[2])
    else:
        HOSTNAME = os.popen('hostname').read().strip()
    #HOSTNAME = 'etcd-ss-0'
    hostnameSplit = HOSTNAME.split('-')
    STS_INDEX = int(hostnameSplit[-1])
    STS_NAME = '-'.join(hostnameSplit[:-1])
    env = os.environ
    # Local debugging
    if len(sys.argv) > 2 and (sys.argv[1] == '--hostname' or sys.argv[1] == '-h'):
        with open('/etc/hosts', 'a+') as f:
            f.write('\n127.0.0.1 \t%s.%s\n' % (HOSTNAME, STS_NAME))
    # Let SERVICE_NAME = STS_NAME by default
    if 'SERVICE_NAME' in env:
        SERVICE_URL = '.'.join([HOSTNAME, env['SERVICE_NAME']])
        SERVICE_NAME = env['SERVICE_NAME']
    else:
        SERVICE_URL = '.'.join([HOSTNAME, STS_NAME])
        SERVICE_NAiME = STS_NAME
    #if 'NAMESPACE' in env:
    #    NAMESPACE_NAME = env['NAMESPACE']
    #else:
    #    NAMESPACE_NAME = 'default'
    
    with open('/etc/hosts', 'a+') as f:
        f.write('\n127.0.0.1 \t%s\n' % SERVICE_URL)
    
    SERVICE_URL = 'http://' + SERVICE_URL
    #SERVICE_URL = 'http://'
    #SERVICE_URL = 'http://' + HOSTNAME

    # Get the maximum number of pods
    if 'MAX_PODS_NUMBER' in env:
        maxPodsNumber = env['MAX_PODS_NUMBER']
    else:
        maxPodsNumber = 10
    print('Entrypoint initialized successfully.')
    print('* Hostname: %s\n* Index: %d\n* URL: %s\n* MaxPodsNumber: %d\n\n' % 
        (HOSTNAME, STS_INDEX, SERVICE_URL, maxPodsNumber)
    )

    # Limit the number of pods
    if STS_INDEX >= maxPodsNumber:
        print('The maximum number of pods is %d, and no pods should be added any more.' % maxPodsNumber)
        exit(1)

    accessFlag = False
    initialCluster = ''
    initialClusterState = ''
    # Try to access one of the existing node in the cluster
    for index in range(maxPodsNumber):
        if index == STS_INDEX:
            continue
        targetURL = 'http://%s-%d.%s:2378' % (STS_NAME, index, SERVICE_NAME)
        #targetURL = 'http://%s-%d:2378' % (STS_NAME, index)
        try:
            res = requests.get(url=targetURL + '/getClusterInfo', timeout=1)
        except Exception:
            print('Cannot connect to %s, the host may be unstarted or failed.' % targetURL)
            continue
        else:
            #print(res)
            receivedJson = json.loads(res.content)
            if (not 'state' in receivedJson) or (receivedJson['state'] != 'success'):
                print('Failed to get "success" feedback from %s, trying the next node.' % targetURL)
                continue
            print('Successfully got cluster information from %s' % targetURL)
            print('Current cluster information: %s' % res.content)
            # Fetch the cluster information from an existing node
            #receivedJson = json.loads(res)
            initialClusterNodeList = ['%s=%s:2380' % (HOSTNAME, SERVICE_URL)]
            for nodeID in receivedJson['list']:
                ETCD_NODE_NAME_LIST.append(receivedJson['list'][nodeID]['name'])
                ETCD_NODE_STATE_LIST.append(receivedJson['list'][nodeID]['state'])
                ETCD_NODE_URL_LIST.append(receivedJson['list'][nodeID]['url'])
                ETCD_NODE_ID_LIST.append(nodeID)
                initialClusterNodeList.append('%s=%s' % (ETCD_NODE_NAME_LIST[-1], ETCD_NODE_URL_LIST[-1]))

            # Send member add request to the existing node
            responseAdd = requests.get(url=targetURL + '/addMember', params={'name': HOSTNAME, 'url': (SERVICE_URL + ':2380')})
            resultAddMember = json.loads(responseAdd.content)
            print(responseAdd.content)
            print(resultAddMember)
            #resultAddMember = json.loads(requests.get(url=targetURL + '/addMember', params={'name': HOSTNAME, 'url': (SERVICE_URL + ':2380')}))
            #if (not 'state' in resultAddMember) or (resultAddMember['state'] != 'success'):
            #    print('Failed to add member, trying the next node.')
            #    continue
            #if resultAddMember['state'] == 'failure':
            #    print('The rubbish has fucking failed, trying the next one')
            #    continue

            # Generate the --initial-cluster parameter
            initialCluster = ','.join(initialClusterNodeList)
            print('Genereated --initial-cluster parameter: %s' % initialCluster)
            accessFlag = True
            initialClusterState = 'existing'
            break
    # Cannot access any of the nodes, which means a new cluster should be set up
    if not accessFlag:
        initialCluster = '%s=%s:2380' % (HOSTNAME, SERVICE_URL)
        initialClusterState = 'new'

    #ETCD_CMD = ETCD_CMD_TEMPLATE % (HOSTNAME, SERVICE_URL, SERVICE_URL, initialCluster, initialClusterState)
    ETCD_CMD = ETCD_CMD_TEMPLATE % (HOSTNAME, SERVICE_URL, SERVICE_URL, initialCluster, initialClusterState)
    print('Starting etcd with command:')
    print(ETCD_CMD)
    #os.system('nohup %s &' % ETCD_CMD)
    threadEtcd = Thread(target=launch_etcd_new_thread, args=(ETCD_CMD,))
    threadEtcd.start()
    while(1):
        try:
            response = requests.get(url='%s:2379/health' % SERVICE_URL, timeout=2)
        except Exception:
            print('Node not accessible yet.')
        else:
            receivedJson = json.loads(response.content)
            if response.ok and ('health' in receivedJson) and receivedJson['health']:
                print('Node is now ready.')
                break
            else:
                print('Node not ready yet.')
        time.sleep(UPDATE_INTERVAL)

    time.sleep(UPDATE_INTERVAL)
    get_cluster_member_list()
    NODE_READINESS = True


# Start etcd with a new thread, using nohup might trigger problems
def launch_etcd_new_thread(cmd):
    os.system(cmd)


# Launch the flask server at port 2378
def launch_flask():
    app.run('0.0.0.0', port=2378)


# Start constantly updating cluster info
def update_cluster_info():
    while(1):
        get_cluster_member_list()
        time.sleep(UPDATE_INTERVAL)


# Use 'etcdctl member list' to get information of all members
def get_cluster_member_list():
    global ETCD_NODE_ID_LIST
    global ETCD_NODE_NAME_LIST
    global ETCD_NODE_URL_LIST
    global ETCD_NODE_STATE_LIST
    print('Checking cluster state...')
    ETCD_NODE_ID_LIST = os.popen("etcdctl member list | awk '{print $1}' | tr ':' ' ' | tr '\\n' ' '").read().split()
    ETCD_NODE_NAME_LIST = os.popen("etcdctl member list | tr '=' ' ' | awk '{print $3}' | tr '\\n' ' '").read().split()
    ETCD_NODE_URL_LIST = os.popen("etcdctl member list | tr '=' ' ' | awk '{print $5}' | tr '\\n' ' '").read().split()
    ETCD_NODE_STATE_LIST = os.popen("etcdctl cluster-health | awk '{print $4}' | sed 's/the/ /' | tr '\\n' ' '").read().split()
    for index, item in enumerate(ETCD_NODE_ID_LIST):
        if len(item) == 27 and item[-10:-1] == 'unstarted':
            ETCD_NODE_STATE_LIST[index] = 'unstarted'
        print('Node ID: %s, name: %s, url: %s, state: %s' % (item, ETCD_NODE_NAME_LIST[index], ETCD_NODE_URL_LIST[index], ETCD_NODE_STATE_LIST[index]))


# Return the list of names of all nodes in the etcd cluster
@app.route('/getClusterInfo', methods=['GET'])
def get_cluster_info():
    print('Getting cluster info!=================================')
    print(ETCD_NODE_ID_LIST)
    resultJson = {'state': 'success', 'list': {}}
    for nodeIndex, nodeID in enumerate(ETCD_NODE_ID_LIST):
        #print('===== Adding %s to clusterinfo' % nodeID)
        resultJson['list'][nodeID] = {'name': ETCD_NODE_ID_LIST[nodeIndex], 'url': ETCD_NODE_URL_LIST[nodeIndex], 'state': ETCD_NODE_STATE_LIST[nodeIndex]}
        #resultJson['list'][nodeID]['name'] = ETCD_NODE_ID_LIST[nodeIndex]
        #resultJson['list'][nodeID]['url'] = ETCD_NODE_URL_LIST[nodeIndex]
        #resultJson['list'][nodeID]['state'] = ETCD_NODE_STATE_LIST[nodeIndex]
    return json.dumps(resultJson)


# Check the state of this node
@app.route('/', methods=['GET', 'POST'])
def node_check():
    return json.dumps("{'state': 'success'}")


# Request to add a new node
@app.route('/addMember', methods=['GET'])
def add_member_to_cluster():
    memberName = request.args.get('name')
    memberURL = request.args.get('url')
    ADD_MEMBER_CMD = 'etcdctl member add %s %s' % (memberName, memberURL)
    result = os.system(ADD_MEMBER_CMD)
    result = 0 #============================================================================
    if result == 0:
        return json.dumps("{'state': 'success'}")
    else:
        return json.dumps("{'state': 'failure'}")


@app.route('/readiness', methods=['GET', 'POST'])
def readiness_probe():
    if NODE_READINESS:
        return 'OK', 200
    else:
        return 'Not Ready', 500


@app.route('/liveness', methods=['GET', 'POST'])
def liveness_probe():
    try:
        response = requests.get(url='%s:2379/health' % SERVICE_URL, timeout=2)
    except Exception:
        return 'Unhealthy', 500
    else:
        receivedJson = json.loads(response.content)
        if response.ok and ('health' in receivedJson) and receivedJson['health']:
            return 'Healthy', 200
        else:
            return 'Unhealthy', 500


if __name__ == '__main__':
    launch_etcd()
    threadCheck = Thread(target=update_cluster_info, args=())
    threadCheck.start()
    launch_flask()

