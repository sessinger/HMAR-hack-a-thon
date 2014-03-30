HMAR-Hack-a-thon
================
#### Description

This project involved implementing a simple probabilistic model to construct a rudimentary song. The top node(s) S refer to the measure of the song, N refers to the beat within the measure and M refers to the sixteen note of the beat. A forth-order model was constructed such that sequences of 4 notes are chosen at a time. All 12 chromatic notes were included in the model and the key was set to A, although any key can be set easily. 


As shown in figure 1 the notes chosen for the beat nodes (N) are dependent on the notes chosen for the measure nodes (S) and the sixteenth (M) notes depend on the notes chosen for the beats, thus giving a hierarchical structure. For example, notes that are used in a beat node are given a greater weight when selecting the beat node's sixteenth node child. At this time the prior probabilities of the measure nodes (M) were set manually with the intent of performing inference from a song database in the future.  
