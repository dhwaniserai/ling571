Ling 571 HW6 Readme.txt
Author: Dhwani Serai (dserai)

This was an interesting homework. At first all the lamda functions were very confusing and the notations in nltk were also kind of different from the slides. By the end of it I do feel that I understand lambda reductions better.

Handling different scenarios in this homework:
1. Added the interpretation of verb forms of 'eat' and 'drink' as a transitive and intransitive verb to account for sentences like 'John eats' and 'John eats a sandwich'
Side note: In this homework I have not accounted for Agreement and Tense because I feel that both of those features are related to syntax and not semantics. They don't contribute anything semantically. 

2. Added Coordination rule in the grammar to account for 'or' conjunction. The coordination rules added by me in the grammar account for coordination between Verb Phrases and Nouns.

3. Negation: I have added two forms of negation in the grammar. One is the negative auxillary construction of verbs (does not eat, does not drink, etc.) Here 'does' is a semantically empty construction. It just aids in the unification of verbs. 
For negation of nouns I tried to use a single rule (NDet) but that did not work for words like 'nobody'. So for 'nobody' I had to add a special NP rule to account for an implied negation of determiner and person.
Nobody is semantically supposed to be 'there exists no person'
For common nouns like student where the negated phrase will be 'no student' no just directly acts like a negated determiner

4. In the sentences where negation and coordination both are used the interpretation of my grammar depends on the location of negation. Like if the negation is in the start of the sentence 'no student eats a bagel' the negation applies to the whole sentence because using the First Order Logic the negation first gets attached to 'no student existing' and then the next elements are reduced with that so it negates the whole thing.

But in the case of 'Jack does not eat or drink' the negation gets attached to the event eating and it never combines with the other verb so the semantics only represent the negation of the first verb. Had it been a sentence like  'Jack does not eat sandwich or bagel or drink' the semantic representation would've been like 'there is an event of eating (which is negated) where the eater is Jack and Jack eats sandwich or bagel; or there is an event of drinking where Jack is the drinker'

5. There is also one more slight glitch in the grammar where if there are two seperate events like 'eating' and 'drinking' the grammar represents them with the same symbol 'e' but once the number of predicates increase like 'eating a sandwich or drinking a soda' the events are still represented by the same symbol but the sandwich(x) and soda(y) which are two different symbols which could've been the same. 
I also feel that even though they are different they do not make much of a difference but if they would've been the same it would be better. 