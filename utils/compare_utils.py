from collections import defaultdict
from dataclasses import fields
from typing import List, Tuple, Any

from storage import ValidateFieldsForDb


def compare_tuple_lists(db_list: List[ValidateFieldsForDb], maked_list: List[ValidateFieldsForDb],
                        field_key: str = None, field_skip: str = None) -> Tuple[List[ValidateFieldsForDb], List
[ValidateFieldsForDb]] | Tuple[List[ValidateFieldsForDb], Any]:

    if len(db_list) == 0:
        return maked_list.copy(), []

    db_by_key = defaultdict(list)
    #  print(f"db_lenth = {len(db_list)}")
    #  print(f"db_list:\n{db_list[0]}\n{db_list[3]}\n{db_list[100]}")
    for item_db in db_list:
        key = getattr(item_db, field_key)
        #  print(f"key = {key}")
        db_by_key[key].append(item_db)

    completely_new = []
    partially_different = []

    for item_maked in maked_list:
        key = getattr(item_maked, field_key)
        if key not in db_by_key:
            completely_new.append(item_maked)
            continue

        exact_match_found = False
        for item_db in db_by_key[key]:
            all_fields_match = True
            for field in fields(item_db):
                field_name = field.name
                if field_name == field_skip or field_name == field_key:
                    continue
                if getattr(item_db, field_name) != getattr(item_maked, field_name):
                    all_fields_match = False
                    break

            if all_fields_match:
                exact_match_found = True
                break

        if not exact_match_found:
            partially_different.append(item_maked)

    return completely_new.copy(), partially_different.copy()
