
An effort to simplify the deployment management of high-complexity HLF (uses v2.5.6).

# Motivation
Due to its permissioned nature, HLF offers high customizability and high controllability. However, these features can also make the network really challenging to manage. So, this repository presents an effort to simplify the management process of HLF deployments for testing purpose.


# 디렉토리 구성
- deployment : docker 컨테이너 yaml 파일 관리
- channel-artifacts: genesis.block 저장용
- chaincode : chaincode 저장용. (참고로, 체인코드 폴더 안에서, go mod tidy 로 go module 로 되어 있어야 패키징됨.)
- configtx : genesis-block 정의용 설정 파일. 즉, 오더링 서비스 구성, 피어 조직 구성 등 설정.
- cryptogen : credentials 생성하는 프로필 
- organizations : credentials (private/pubkey, certificate, users, tls...)
- scripts : 기타 스크립트.
- caliper-benchmarks : Examples using Caliper for Benchmarking HLF

# Basic Flow
```bash
BINPATH=bins/bin-v2.5.6

# 1. credential 생성 (using cryptogen)
# 제일 먼저 참여 노드들의 신원 생성해야함 (MSP: 공개키,비밀키,인증서, TLS)
# 오더러 조직 (사용자+관리자 포함)
$BINPATH/cryptogen generate --config=./cryptogen/crypto-config-orderer.yaml --output="organizations"
# 피어 조직 (사용자+관리자 포함)
$BINPATH/cryptogen generate --config=./cryptogen/crypto-config-12-org.yaml --output="organizations"

# 2. Genesis Block 준비 + 환경설정: configtx/configtx.yaml 수정
# 오더링 서비스 설정 (e.g., 주소, 배치 크기), 컨소시엄 구성 설정 (Orgs, MSP), 채널 설정,
# Profile 설정 = {오더러 컨소시움, 피어(Application) 컨소시엄}
# Policy 는 'ANY Admins' 설정. MAJORITY 로 된 경우, 향후 config tx (배치 크기 변경 등) 할 때, signconfigtx 를 절반+1 까지 해야 하는 번거러움 발생하므로.

# 3. genesis block 생성 (from one of Profile in configtx.yaml). with 채널명
$BINPATH/configtxgen -profile ChannelUsingRaft  -configPath ./configtx  -outputBlock ./channel-artifacts/genesis.block -channelID mychannel


# 4. 피어, 오더러 도커 컨테이너 설정 파일 생성
cd deployment; 
vim bench-config.yaml 에서 peer, orderer 개수 조정.
# read bench-config.yaml and create orderer{Index}.yaml, peer0.org{Index}.yaml
./generate.py 

# 5. HLF 네트워크 시작 (로컬 or 분산)
# 주의: 이전 데이터 의존성 피하기 위해, 도커상 volume 맵핑된 데이터는 모두 삭제하기.  (또는, 따로 archiving)
# 분산 실험시에는, 원격 머신의 HLF volume 맵핑 경로 확인 (organizations + genesis.block)

# 5-1). 로컬 환경상 HLF 네트워크 생성
docker-compose -f orderers.yaml up -d
docker-compose -f peers.yaml up -d

# 5-2). 분산 환경상 HLF 네트워크 생성 (스웜 오버레이)
# swarm/*.yaml 모두 실행.
./swarm-deploy.py

# 6. 각 피어를 채널에 조인 시키기. (각자 수행)
./actions.py join

# 7. 체인 코드 설치, 승인, 배포
# 7-1. 체인코드 패키지를 각 피어에 대해 설치 (각자 수행)
./actions.py install
# 7-2. 체인코드 패키지를 각 피어들(orgs)로부터 승인 (각자 수행). Endorsement Policy 설정 가능
./actions.py approve 
# 7-3. 체인코드 트랜잭션 제출. 한 피어만 제출하면 됨 (한번만 수행). Endorsement Policy 설정 가능
./actions.py commit

# 8. 앵커피어 추가하는 트랜잭션 제출하기.
# 앵커 피어를 추가해야 cross-organizational 통신 가능. (즉, 서로 다른 조직간의 피어가 서로의 주소를 알게됨. 용도: Endorsement policy > 1 인 경우, 다른 조직 피어 주소를 알아야 하는데, 이때 앵커 피어 TX 를 제출해야지 endorsements 를 다른 조직 피어들로부터 확보 가능했음을 확인.)

# 9. batch size 변경 등

```


# Etc. Tips

```bash
# figuring out expired date of credentials
openssl x509 -noout -enddate -in peerOrganizations/org1.example.com/peers/peer0.org1.example.com/msp/signcerts/cert.pem
```