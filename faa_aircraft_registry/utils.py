"""
Utility functions that support modules within faa_aircraft_registry.
"""


def transform(dict_: dict, typed_dict: dict, substring_to_type: list = []) -> dict:
    """
    Convert values in input dictionary to typed values in object.

    Allows for recursive populating of dictionary types if provided in substring_to_type kwarg. The 
    format is as follows:

    substring_to_type: List[dict]
        substring: Text     - The prepended string to filter parameter names by
        field: Text         - The field that will be filled in dict_
        type: TypedDict     - The typeddict that will be created as field
    """

    for item in substring_to_type:
        # Initialize substring values to convert into dictionary type
        substring, field, type_ = [item.get(k)
                                   for k in ['substring', 'field', 'type']]
        substring = item['substring']
        field = item['field']
        type_ = item['type']

        # Find keys that match the substring and pull them into a new dictionary
        matching_keys = [key for key in dict_.keys() if substring in key]
        sub_dict = dict((s_key.strip(substring), dict_.pop(s_key))
                        for s_key in matching_keys)

        # Transform the dictionary into the dictionary type provided
        dict_[field] = transform(sub_dict, type_)

    fields = typed_dict.__annotations__
    return {name: fields[name](value) for name, value in dict_.items() if name in fields.keys()}
