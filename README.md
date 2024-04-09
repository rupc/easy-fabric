
- deployment : docker deploy 용 yaml 파일 관리
- channel-artifacts: genesis.block 저장용
- chaincode : chaincode 저장용. (체인코드 폴더 안에서, go mod tidy 로 go module 로 되어 있어야 패키징됨.)
- configtx : genesis-block 정의용 설정 파일. 즉, 오더링 서비스 구성, 피어 조직 구성 등 설정.
- cryptogen : credentials 생성하는 프로필 
- organizations : credentials (private/pubkey, certificate, users, tls...)
- scripts : 기타 스크립트.

```bash
# Basic Flow

# 1. genesis block 생성
../bin/configtxgen -profile ChannelUsingRaft  -configPath ./configtx  -outputBlock ./channel-artifacts/genesis.block -channelID mychannel

# 2. credential 생성 (using cryptogen)
../bin/cryptogen generate --config=./cryptogen/crypto-config-orderer.yaml --output="organizations"

# 3. 도커 설정 파일 자동 생성
cd deployment; 
./generate.py

# 4. 오더러 & 피어 띄우기.
docker-compose -f orderers.yaml up -d
docker-compose -f peers.yaml up -d

# 5. 피어를 채널에 조인 시키기. 체인 코드 설치. 승인 & 커밋 (이떄 endorsemnet policy 설정)
./actions.py join
./actions.py install
./actions.py approve
./actions.py commit
```
