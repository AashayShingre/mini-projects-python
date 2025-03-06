## Build your own compression tool

https://codingchallenges.fyi/challenges/challenge-huffman

It uses `bitarray` module to convert string of 0s and 1s into actually binary


### To run the app

`python -m app.compress [<json_file1> ...]` 


### To run tests 

`pytest`

If you just want to test the cases from the challenge, run 

`pytest test_compress.py`


----


Note: The tools reads the file in text mode only for compression. 
[TODO: Change it to byte mode, and look for repeatitions of bytes]