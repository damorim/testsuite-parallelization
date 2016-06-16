# Experimental script
#
TEST_PATH=$1

total_classes=0
total_methods=0
total_ignores=0

echo "Test Class, Test Methods, Ignored Tests"
for tc in `find "$TEST_PATH" -name *Test*.java`; do
    tests=`grep -w @Test $tc | wc -l`
    ignores=`grep -w @Ignore $tc | wc -l`
    echo $(basename $tc), $tests, $ignores

    total_classes=$(($total_classes + 1))
    total_methods=$(($total_methods + $tests))
    total_ignores=$(($total_ignores + $ignores))
done
echo "----------------------------------------------"
echo "$total_classes, $total_methods, $total_ignores"
