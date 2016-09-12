Project 02: Distributed Computing
=================================

Please see the [distributed computing project] write-up.

[distributed computing project]: https://www3.nd.edu/~pbui/teaching/cse.20189.sp16/homework10.html

# Questions

#### 1. Describe the implementation of hulk.py. How does it crack passwords?
Hulk.py first parses command line arguments, then sets the appropriate variables. LENGTH is the desired password length, HASHES is teh path to the hashes file, and PREFIX defines a prefix for the candidate passwords. In order to track and store our passwords, we used sets. The hashes set contains all possible permutations of the alphabet given length LENGTH. The cracked set contains the passwords we have cracked. We filled cracked by using a for loop to iterate through all possible permutations. Inside the for loop, we create a possible password and check it with md5sum(). We then sort cracked, check if the length is correct, and print the password if so.

#### Explain how you tested hulk.py and verified that it works properly.
Testing hulk.py was simple, we just followed the examples given and verified the output.

#### Describe the implementation of fury.py. How does it:

##### Utilize hulk.py to crack passwords?
We used hulk.py command in this way:
    
    command = './hulk.py -l {}'.format(length) #aggregates all words

This line assigns the output of hulk.py to command, which we then check to see if it is already in the journal. If it isn't, we give it to the work queue.

##### Divide up the work among the different workers?
Thankfully, that's what work_queue is for. We just had to get the script working, work_queue took it from there.

##### Keep track of what has been attempted?
To keep track of previous attempts, we used the journal_dump_passwords script. We call this script and then dump the appropriate words into our passwords.txt.

##### Recover from failures?
If a worker fails, the master simply gives the task to a new worker. Same thing with journal and master.

#### Explain how you tested fury.py and verified that it works properly.
We ran our script, assigned a worker, and watched it go. We then catted it into deadpool and saw our netid on the leaderboard.

#### From your experience in this project and recalling your Discrete Math knowledge, what would make a password more difficult to brute-force: more complex alphabet or longer password? Explain.

A longer password would be more difficult. A 4 character password with 36 possible characters, (36^4), has many many more possible permutations than a 3 character password with an alphabet of 50 chaacters (50^3), for example.