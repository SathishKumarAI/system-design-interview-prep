Replication is the process of having multiple copies of data in order to make sure that if a database goes down the data isn't lost.

Types:
[[Single Leader Replication]]
- All writes go to one dB, reads come from any dB
[[Multiple Leader Replication]]
- Writes can go to a small subset of leader databases reads can come from any dB
[[Leaderless replication]]
- writes go to all dB, reads come from all dB

Single leader replication is useful to ensure that there are no data conflicts, all writes will go to one node.

Leaderless and multileader replication is useful for increasing write [[throughput]] beyond just one dB node (at cost of potential write conflicts )
