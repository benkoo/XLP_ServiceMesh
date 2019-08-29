#!/bin/bash
if [ -z ${AUTO_CLUSTER_DISCOVERY} ]; then
	/bin/start_cluster.py
else
	if [ -z ${CLIENT_URLS+x} ]; then
		CLIENT_URLS="http://0.0.0.0:4001,http://0.0.0.0:2379"
		echo "Using default CLIENT_URLS (${CLIENT_URLS})"
	else
		echo "Detected new CLIENT_URLS value of ${CLIENT_URLS}"
	fi

	if [ -z ${PEER_URLS+x} ]; then
		PEER_URLS="http://0.0.0.0:7001,http://0.0.0.0:2380"
		echo "Using default PEER_URLS (${PEER_URLS})"
	else
		echo "Detected new PEER_URLS value of ${PEER_URLS}"
	fi
	ETCD_CMD="/bin/etcd --data-dir=/data --listen-peer-urls=${PEER_URLS} --listen-client-urls=${CLIENT_URLS} ${LAUNCH_PARAMETERS}"
	echo -e "Launching etcd with ${ETCD_CMD}"
	echo "Begin etcd output:"
	echo "=============================================="
	exec $ETCD_CMD
fi
