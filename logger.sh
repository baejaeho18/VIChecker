#!/bin/sh

# 입력된 매개변수를 변수로 저장
start_date="$1"
end_date="$2"
output_file="$3"

# git log 명령을 실행하여 JSON 파일로 저장
git log --since="$start_date" --until="$end_date" --pretty=format:'{%n  ^^^^commitHash^^^^: ^^^^%H^^^^,  %n  ^^^^parent^^^^: ^^^^%P^^^^,  %n  ^^^^subject^^^^: ^^^^%s^^^^,  %n  ^^^^sanitized_subject_line^^^^: ^^^^%f^^^^,  %n  ^^^^commit_notes^^^^: ^^^^%N^^^^,  %n  ^^^^body^^^^: ^^^^%b^^^^,  %n  ^^^^author_name^^^^: ^^^^%aN^^^^,  ^^^^committer_name^^^^: ^^^^%cN^^^^,%n    ^^^^date^^^^: ^^^^%cD^^^^%n},' |
  sed 's/"/\\"/g' |
  sed 's/\^^^^/"/g' |
  sed "$ s/,$//" |
  sed -e ':a' -e 'N' -e '$!ba' -e 's/\n/ /g' |
  tr -d '\r\n' |
  tr -d '	' |
  tr -d '	' |
  awk 'BEGIN { print("[") } { print($0) } END { print("]") }' > "$output_file"
