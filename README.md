Thi is a CLI tool to sort integers that accepts the following arguments:

  - `-n int`: An integer for the value N, which will be output length.
  - `--input-file string`: A string representing a path to an input file.
  - `--output-file string`: A string representing a path to an output file.

The input file will contain one number per line. The valid number is anything
that is a valid unsigned 64-bit integer. The goal is to read the
input file, get N largest numbers, sort them in descending order, and output
the result to the output file, one number per line.


Program complies with the following requirements:

  1. Exit with the following custom errors when using wrong arguments:
    - The input file does not exist: `ERROR: input file does not exist.`
    - The input file is not readable: `ERROR: input file is not readable.`
    - The integer N argument is less than or equal to zero: `ERROR: Number of top results must be bigger than 0.`
    - The integer N argument is over the upper limit: `ERROR: The maximum number of top results must be less or equal than 30000000.`
  2. The program ignores and warns about invalid lines in the following format: `WARN: Invalid line <line>.`
  3. Invalid lines are all lines that do not contain an unsigned 64-bit integer, for example:
    - Multiple numbers on the same line: 12345 890
    - Not unsigned 64-bit integers: `1234helo` or `12345.01`
  4. The program handles big files with tens of millions of lines efficiently.
  5. Avoid using third-party libraries and stick with the standard ones.
