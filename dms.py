# %%
# libraries
import pandas as pd
import numpy as np
from pymongo import MongoClient

# %%
git = pd.read_csv('gitData.csv')
# create a new column of project types for gitData, which contains only pytorch and tensorflow 
regx = r'({})'.format('|'.join(['pytorch', 'audio', 'text', 'vision', 'serve', 'torchrec','elastic', 'xla']))
git['project_type'] = git['project_name'].str.replace(regx, "pytorch").fillna(git['project_name'])

print("finish read data")

# new collection for git data
# let's connect to the localhost
client = MongoClient()

# let's create a database 
db = client.github
gitData = db.gitData

# print connection
print("""
Database
==========
{}

Collection
==========
{}
""".format(db, gitData), flush=True
)

# %%
# import the git data to mongo compass
#%%time 
##
##
# import the git data to mongo compass
#%%time 
##
# slow loading of data
d_gitcommit = {}
#pass data
for i in git.index:
    d_gitcommit = {
        "Commit": {
            "hash":git.loc[i, "hash"],
            "Msg":{
                "msg":git.loc[i, 'msg'],
                "Author":{
                    "Author_name": git.loc[i, 'author_name'],
                    "Author_date": git.loc[i, 'author_date'],
                    "Author_timezone": git.loc[i, 'author_timezone'].astype(str)
                }
            },
            "Committer":{
                "Committer_name": git.loc[i, 'committer_name'],
                "Committer_date": git.loc[i, 'committer_date'],
                "Committer_timezone": git.loc[i, 'committer_timezone'].astype(str)
            }
        },
        "Branch":{
            "Branches": git.loc[i, 'branches'],
            "In_main_branch": git.loc[i, 'in_main_branch'].astype(str),
            "Merge": git.loc[i, 'merge'].astype(str),
            "Parents":git.loc[i, 'parents']
        },
        "Project_name": {
            "Project_type" : git.loc[i, 'project_type'],
            "Project_name": git.loc[i, 'project_name']
            },
        "File":{
            "Filename": git.loc[i, 'filename'],
            "Change_type": git.loc[i, 'change_type'],
            "Commit_change":{
                "Deletions": git.loc[i, 'deletions'].astype(str),
                "Insertions": git.loc[i, 'insertions'].astype(str),
                "Files": git.loc[i, 'files'].astype(str),
                "Lines":git.loc[i, 'lines'].astype(str)
            }
        },
        "Code_change":{
            "Path":{
                "old_path":git.loc[i, 'old_path'],
                "new_path": git.loc[i, 'new_path']
            },
            "Diff":{
                "Diff": git.loc[i, 'diff'],
                "Diff_parse":{
                    "Diff_parsed":git.loc[i, 'diff_parsed'],
                    "Deleted_lines":git.loc[i, 'deleted_lines'].astype(str)
                }
            },
            "Source_code":{
                "Source_code":git.loc[i, 'source_code'],
                "Source_code_before":git.loc[i, 'source_code_before']
            }
        },
        "Nloc":git.loc[i, 'nloc'],
        "Complexity":git.loc[i, 'complexity'],
        "Token_count":git.loc[i, 'token_count']
        
     }
    gitData.insert_one(d_gitcommit)

print("finish data insert")
print("start data clensing")

###############################################################################
# %%
# data cleaning
# clean the NA values into null
# get key names

# key_list_issue = []
# for i in d_gitissue.keys():
#     try:
#         for b in d_gitissue.get(str(i)).keys():
#             key_list_issue.append(str(i) + '.' + str(b))
#     except:
#         key_list_issue.append(i)

# # get key names
# key_list_comment = []
# for i in d_comment.keys():
#     try:
#         for b in d_comment.get(str(i)).keys():
#             key_list_comment.append(str(i) + '.' + str(b))
#     except:
#         key_list_comment.append(i)

# get key names
key_list_commit = []
for i in d_gitcommit.keys():
    try:
        for b in d_gitcommit.get(str(i)).keys():
            key_list_commit.append(str(i) + '.' + str(b))
    except:
        key_list_commit.append(i)

# # unset NaN fields
# for i in key_list_issue:
#     update = gitIssues.update_many({str(i):np.nan},{"$unset": {str(i):""}})
#     print("""
#     Key: {}
#     Matched: {}
#     Modified: {}
#     ------------
#     """.format(i, update.matched_count, update.modified_count), flush=True)
# print("finish data cleasing for issue")
# # unset NaN fields
# for i in key_list_comment:
#     update = IssueComment.update_many({str(i):np.nan},{"$unset": {str(i):""}})
#     print("""
#     Key: {}
#     Matched: {}
#     Modified: {}
#     ------------
#     """.format(i, update.matched_count, update.modified_count), flush=True)
# print("finish data cleasing for comment")
# unset NaN fields
for i in key_list_commit:
    update = gitData.update_many({str(i):np.nan},{"$unset": {str(i):""}})
    print("""
    Key: {}
    Matched: {}
    Modified: {}
    ------------
    """.format(i, update.matched_count, update.modified_count), flush=True)

print("finish data cleansing")