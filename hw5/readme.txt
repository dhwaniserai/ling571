Readme for Ling 571 HW5
Author: Dhwani Serai (dserai)

Extended the example grammar(feat0) for better adaptability
Tried to mimic the HPSG format in Ling 566

1st issue: coverage of 'that'
Treated 'that' as a subordinating conjunction and added rules for SBP subordinating Phrase/predicate as an extension to VP transitive verbs

coverage of 'interesting' (adjective)
added it in VP expansions along with transitive verbs as an alternative to NP

2nd issue: ditransitive verbs and prepositions
added put as a ditransitive verb in the VP expansions and also introduced PP (prepositional phrases)

3rd change:
Added pronouns and reflexive pronouns in the NP expansion in the same way that PropN were getting expanded.
So basically we know that pronouns and reflexives can replace NP in certain scenarios so I have added those expansions
Reason: in place of 'Mary' we can have 'her' or 'herself'. The agreement remains the same in this case

4th issue:
handling questions. introduced QP (Question phrase) as an expansion to S
The issue is the questions are incomplete sentences so some part is going to be missing but it is still grammatical so I have added a bunch of expansions for QP
4.1 Introduced Q as a lexicon for 'what'
4.2 Introduced QVP of Question Verb Phrase to handle Verb Phrases with certain missing arguments
4.3 QPunc as the lexicon for '?'

5th issue: handling infinitives in sentences like What does Mary think John knows
Introduced infinitive as a type of verb (IFV) and added expansions for that in QVP

6th issue: handling Prepositional phrases (PP)
The problem was that many times PPs are optional so I have added a a bunch of expansions to cover all the optional cases like
VP -> V NP
VP -> V NP PP
VP -> V PP

7th issue: handling the difference between the verb 'reached' and 'walked'
for this I have added a new feature in AGR called TIME which can be long or short
walked does not have any requirement but reached has the AGR requirement of Time being long
Nom -> 'Saturday' has the Time feature as long but five minutes has the Time feature short
five minutes was getting counted as 2 different tokens so for the time being I have added another expansion in NP where NP-> Nom Nom to handle such time values