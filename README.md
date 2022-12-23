# 포맷프리(NxFs) 방식 블랙박스 영상복구 도구

포맷프리(NxFS) 방식 블랙박스 영상복구 도구는 BoB 11기 삼청이 팀에서 진행한 프로젝트 입니다. 

NxFS 파일시스템 분석 및 복구를 진행하는 NxFS Analyzer 파일과 파일시스템 슬랙 영역, 손상된 영상, 영상 자체의 슬랙 영역을 복구해주는 File Restore 파일로 구성되어 있습니다.

NxFS Analyzer 파일은 NxFS 파일시스템을 대상으로 할당/미할당/슬랙 영역을 분석 및 분리하여 각 데이터에 대한 오프셋과 함께 복구 결과가 제공됩니다.

File Restore 파일은 파일시스템 슬랙 영역, 손상된 영상, 영상 자체의 슬랙 영역을 복구하여 오프셋과 함께 복구 결과가 제공됩니다.

직접 테스트 했을 때 복구에 성공한 제품은 Carmore CM-3000, CM-3300, URIVE A5 입니다.

Releases Tab에서 바이너리 파일 확인하실 수 있습니다.

## 도구 사용 매뉴얼
* https://drive.google.com/file/d/1Kvhkj-pzKKQJy1b0jq67cFaff4pAIwq-/view?usp=sharing

## CLI 명령어
* NxFS Analyzer: newcore.py 이용하여 도구 사용 가능. (python newcore.py -h)
* File Restore: 추가 예정

## 프로젝트 팀원
* 이찬우 ([@RokLcw](https://github.com/RokLcw))
* 오주연 ([@juyeonoh](https://github.com/juyeonoh))
* 이정인 ([@jeong0000](https://github.com/jeong0000))
* 박수영 ([@swimminq](https://github.com/swimminq))
* 고서정 ([@revibk16](https://github.com/revibk16))
* PL: 문현지 ([@hyunjm95](https://github.com/hyunjm95))
* 멘토: 최원영 ([@fl0ckfl0ck](https://github.com/fl0ckfl0ck))
* 멘토: 윤상혁 ([@trudy85](https://github.com/trudy85))
