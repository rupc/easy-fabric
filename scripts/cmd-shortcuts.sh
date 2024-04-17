#!/usr/bin/bash

alias o1="docker logs orderer1.example.com"
alias o2="docker logs orderer2.example.com"
alias o3="docker logs orderer3.example.com"

alias p1="docker logs peer0.org1.example.com"
alias p2="docker logs peer0.org2.example.com"
alias p3="docker logs peer0.org3.example.com"
alias p4="docker logs peer0.org4.example.com"
alias p5="docker logs peer0.org5.example.com"
alias p6="docker logs peer0.org6.example.com"
alias p7="docker logs peer0.org7.example.com"
alias p8="docker logs peer0.org8.example.com"
alias p9="docker logs peer0.org9.example.com"
alias p10="docker logs peer0.org10.example.com"
alias p11="docker logs peer0.org11.example.com"

alias cw0="docker service logs -f caliper.org1.example.com"
function hlfdep {
    (
        cd /home/jyr/go/src/github.com/rupc/fabric-benchmarks/fabric-samples/bench-network/scripts;
        ansible-playbook -f 8 rollback-hlf.yaml -u root
        cd /home/jyr/go/src/github.com/rupc/fabric-benchmarks/fabric-samples/bench-network/deployment; 
        ./swarm-deploy.py
    )
}
alias caldep='(cd /home/jyr/go/src/github.com/rupc/fabric-benchmarks/fabric-samples/bench-network/caliper-benchmarks/swarm/; ./deploy-caliper.py)'
alias calbans='(cd /home/jyr/go/src/github.com/rupc/fabric-benchmarks/fabric-samples/bench-network/caliper-benchmarks/ansible/; ansible-playbook -f 8 sync-caliper.yaml -u root  --tags benchmarks)'
alias calans='(cd /home/jyr/go/src/github.com/rupc/fabric-benchmarks/fabric-samples/bench-network/caliper-benchmarks/ansible/; ansible-playbook -f 8 sync-caliper.yaml -u root)'
# The above aliases can be generated using the following loop:
# for i in {0...12};
# do
#     alias p{$i}="docker logs peer$i.org1.example.com"
# done

# The above aliases can be generated using the following loop:
# for i in {0...12};
# do
#     alias p{$i}="docker logs peer$i.org1.example.com"
# done

deploymentPath='/home/jyr/go/src/github.com/rupc/fabric-benchmarks/fabric-samples/bench-network/deployment/'

alias oc="(cd ${deploymentPath}; docker-compose -f orderers.yaml up -d;)"
alias pc="(cd ${deploymentPath}; docker-compose -f peers.yaml up -d;)"
