nactags are the building blocks to compose nacrules.

They can either appear in the "matching" / "not_matching" sections of a nacrule,
in which case they play the role of classifiers, or they could appear in the "apply_tags"
section of the of a nacrule, in which case they influence the result.

When the "type" field of nactag is "match", it can be used as the classfier of
a nacrule. "match" field specifies the attribute name and "values" field specifies
the list of attribute values to match on. When multiple values are specified,
its treated as an OR condition between those values.

When the "type" field of nactag is NOT "match", it can be used as the result of
a nacrule. "type" field identifies the action to take and the corresponding field
would provide any associated parameters to that action.'