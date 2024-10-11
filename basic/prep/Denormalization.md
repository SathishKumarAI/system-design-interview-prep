#### Denormalization

Denormalization attempts to improve read performance at the expense of some write performance. Redundant copies of the data are written in multiple tables to avoid expensive joins. Some RDBMS such as [[PostgreSQL]] and Oracle support [[Materialized_view]] which handle the work of storing redundant information and keeping redundant copies consistent.

Once data becomes distributed with techniques such as [[system design primer?tab=readme ov file#federation]] and [[system design primer?tab=readme ov file#sharding]], managing joins across data centers further increases complexity. Denormalization might circumvent the need for such complex joins.

In most systems, reads can heavily outnumber writes 100:1 or even 1000:1. A read resulting in a complex database join can be very expensive, spending a significant amount of time on disk operations.

##### Disadvantage(s): denormalization
- Data is duplicated.
- Constraints can help redundant copies of information stay in sync, which increases complexity of the database design.
- A denormalized database under heavy write load might perform worse than its normalized counterpart.

###### Source(s) and further reading: denormalization
- [Denormalization](https://github.com/SathishKumar9866/system-design-interview-prep/blob/backlinks_test/Denormalization.md)