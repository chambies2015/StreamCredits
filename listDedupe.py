import GetFollowList
import GetSubList

# Not sure this is needed if Twitch doesn't count Subscribers as Followers too.
def dedupe(list1, list2):
    # Convert list1 to a set for efficient lookups
    set1 = set(list1)

    # Create a new list with items from list2 that are not in set1
    updated_list2 = [item for item in list2 if item not in set1]

    return updated_list2