SUBJECTS=("Algorithms" "Bukkit" "DiskLruCache" "FizzBuzzEnterpriseEdition"
"GCViewer" "Gaffer" "HanLP" "HdrHistogram" "Java-Chronicle"
"JavaVerbalExpressions" "OpenGrok" "OpenTripPlanner" "TrayNotification"
"YCSB" "ambrose" "android-maven-plugin" "android-volley"
"antlr4" "atmosphere" "aws-sdk-java" "blade"
"byte-buddy" "closure-compiler" "crawler4j"
"cucumber-jvm" "dex2jar" "disconf" "disunity" "druid")


for sub in ${SUBJECTS[@]}; do
    TARGET="./subjects/$sub"
    cnt_global=0
    for p in $(find $TARGET -name *.java); do
        cnt=$(grep -nr "import java.util.concurrent" $p | wc -l)
        cnt_global=$(($cnt_global + $cnt))
    done;
    echo $sub $cnt_global
done;
