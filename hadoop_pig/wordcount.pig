
-- Word Count Example in Apache Pig

-- Step 1: Load each line from the input file
lines = LOAD 'data/wordcount_input.txt' AS (line:chararray);

-- Step 2: Tokenize each line into words
words = FOREACH lines GENERATE FLATTEN(TOKENIZE(line)) AS word;

-- Step 3: Group the data by each word
grouped = GROUP words BY word;

-- Step 4: Count the number of occurrences of each word
word_counts = FOREACH grouped GENERATE group AS word, COUNT(words) AS count;

-- Step 5: Store the result to an output directory in HDFS
STORE word_counts INTO 'output/wordcount_pig';
