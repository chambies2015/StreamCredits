import GetFollowList
import GetSubList
import rollingCredits
import Credentials
import listDedupe

if __name__ == "__main__":
    subList = GetSubList.getSubList()
    followList = GetFollowList.get_followers()
    subList = sorted(subList, key=str.lower)
    dedupedFollowList = listDedupe.dedupe(subList,followList)
    followList = sorted(dedupedFollowList, key=str.lower)


    rollingCredits.rolling_credits(Credentials.filePath, subList, followList)