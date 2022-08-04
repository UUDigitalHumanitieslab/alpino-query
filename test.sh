#!/usr/bin/env bash
# Test the console script
check_error() {
    error=$1
    action=$2
    test=$3

    if [ $error -ne 0 ]
    then
        echo "ERROR: Difference in output of $action for $test"
        echo $test
        exit $error
    fi
}

for TEST in $(ls tests/data/*.txt)
do
    tokens=$(sed "1q;d" $TEST)
    attributes=$(sed "2q;d" $TEST)
    remove=$(sed "3q;d" $TEST)
    order=$(sed "4q;d" $TEST)
    
    # TEST MARK
    inputxml=$(cat ${TEST/.txt/.xml})
     (python -m alpino_query mark "$inputxml" "$tokens" "$attributes") > /tmp/output
    markedxml_path="${TEST/.txt/.marked.xml}"

    diff -B $markedxml_path /tmp/output
    check_error $? "MARK" $TEST

    # TEST SUBTREE
    markedxml=$(cat $markedxml_path)
     (python -m alpino_query subtree "$markedxml" "$remove") > /tmp/output
    subtreexml_path="${TEST/.txt/.subtree.xml}"

    diff -B $subtreexml_path /tmp/output
    check_error $? "SUBTREE" $TEST

    # TEST XPATH
    subtreexml=$(cat $subtreexml_path)
     (python -m alpino_query xpath "$subtreexml" "$order") > /tmp/output

    diff -B ${TEST/.txt/.xpath} /tmp/output
    check_error $? "XPATH" $TEST
done

echo "Succesfully checked console script!"
