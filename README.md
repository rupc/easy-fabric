
- deployment : docker deploy 용 yaml 파일 관리
- channel-artifacts: genesis.block 저장용
- chaincode : chaincode 저장용. (체인코드 폴더 안에서, go mod tidy 로 go module 로 되어 있어야 패키징됨.)
- configtx : genesis-block 정의용 설정 파일. 즉, 오더링 서비스 구성, 피어 조직 구성 등 설정.
- cryptogen : credentials 생성하는 프로필 
- organizations : credentials (private/pubkey, certificate, users, tls...)
- caliper : 
- scripts : 기타 스크립트.

```bash
# Basic Flow

BINPATH=bins/bin-v2.5.6

# 1. credential 생성 (using cryptogen)
# genesis block 생성에는 Certficate 이 필요하므로.
$BINPATH/cryptogen generate --config=./cryptogen/crypto-config-orderer.yaml --output="organizations"

# 2. configtx/configtx.yaml 수정
# 오더링 서비스 설정 (e.g., 주소, 배치 크기), 컨소시엄 구성 설정 (Orgs, MSP), 채널 설정,
# Profile 설정 = {오더러 컨소시움, 피어(Application) 컨소시엄}
# Policy 는 'ANY Admins' 설정. MAJORITY 로 된 경우, 향후 config tx (배치 크기 변경 등) 할 때, signconfigtx 를 절반+1 까지 해야 하는 번거러움 발생하므로.

# 3. genesis block 생성 (from one of Profile in configtx.yaml). with 채널명
$BINPATH/configtxgen -profile ChannelUsingRaft  -configPath ./configtx  -outputBlock ./channel-artifacts/genesis.block -channelID mychannel


# 4. 도커 설정 파일 생성 & 오더러 & 피어 띄우기.
cd deployment; 
./generate.py
docker-compose -f orderers.yaml up -d
docker-compose -f peers.yaml up -d

# 5. 피어를 채널에 조인 시키기. 체인 코드 설치. 승인 & 커밋 (이떄 endorsemnet policy 설정)
./actions.py join
./actions.py install
./actions.py approve # Endorsement Policy 설정
./actions.py commit # Endorsement Policy 설정
```
