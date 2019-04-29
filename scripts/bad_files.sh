declare -a bad_files=(
  "07000029.wav" "07030018.wav" "07030027.wav"
  "07030042.wav" "07030052.wav" "07030053.wav"
  "07036140.wav" "07040003.wav" "07040029.wav"
  "07040170.wav" "07042134.wav" "07042253.wav"
  "07043325.wav" "07049110.wav" "07050001.wav"
  "07050065.wav" "07050193.wav" "07050197.wav"
  "07050205.wav" "07050211.wav" "07052022.wav"
  "07053101.wav" "07055254.wav" "07060021.wav"
  "07060027.wav" "07060102.wav" "07062063.wav"
  "07063055.wav" "07063056.wav")

for i in "${bad_files[@]}" ; do
    curl -O http://bbcsfx.acropolis.org.uk/assets/$i
done
