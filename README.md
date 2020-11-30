# 15-112-Term-Project
1.Project Proposal [15 pts]

1.1 Project Description [2.5 pts]:
Election Simulator: An interactive election simulator showcasing different types of single-winner voting methods visually.Each voter and candidate will be characterized by  a point on a 2-D grid, and the closer a candidate is to a voter,the more likely it is that the voter will vote for that candidate.

1.2 Competitive Analysis [2.5 pts]:
Similar project : 
https://www.youtube.com/watch?v=yhO6jfHPFQU&t=572s

Similarities:
 both are voting systems simulations, both use a 2-D grid format and distance as a measure of likelihood to vote for each candidate.

Differences: 
The primer project was coded with Unity, my project will implement simpler graphics w/o external modules.
The primer project uses distance as an absolute measure ,whereas my project will use the votes calculated from the distance as a jumping off point to generate many trials ,each tweaked randomly according to some margin of error to find out the probability of each candidate winning.
The primer project has implemented plurality, instant run-off and approval voting whereas my project will have approval, plurality,two-round and ranked-pair voting.
