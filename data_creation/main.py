import json, secrets
import pandas as pd
import os


def main():
    
    if not os.path.exists("./data"):
        os.makedirs("./data")
    
    # University data
    univ_df = pd.read_excel("./excels/universities.xlsx")
    UNI_COL_NAME = "University Name"
    UNI_COL_NAME_SHORT = "Short Name"
    
    # Team data
    team_df = pd.read_excel("./excels/teams.xlsx")
    TEAM_COL_NAME = "TeamName"
    TEAM_COL_UNI = "University"
    
    # Replace Group Participants with your Group
    GROUP_ID = "3"
    
    # create groups.json
    groups = [
        {
            "id": GROUP_ID,
            "icpc_id": "100",
            "name": "The ICPC Greece Regional Competition"
        }
    ]
    
    groups_path = "./data/groups.json"
    with open(groups_path, 'w') as f:
        json.dump(groups, f, indent=4)
    
    print("Groups Ready!")
    
    # create organizations.json
    orgs = []
    
    for index, row in univ_df.iterrows():
        
        if not row[UNI_COL_NAME] or not row[UNI_COL_NAME_SHORT]:
            print(f"Skipping uni row with index {index}!")
            continue
        
        uni_name = row[UNI_COL_NAME_SHORT]
        uni_formal_name = row[UNI_COL_NAME]
        
        org = {
            "id": uni_name,
            "icpc_id": str(200+index+1),
            "name": uni_name,
            "formal_name": uni_formal_name,
            "country": "GRC"
        }
        
        orgs.append(org)
    
    orgs_path = "./data/organizations.json"
    with open(orgs_path, 'w') as f:
        json.dump(orgs, f, indent=4)
    
    print("Universities Ready!")
    
    # create teams.json
    teams = []
    
    for index, row in team_df.iterrows():
        
        if not row[TEAM_COL_UNI] or not row[TEAM_COL_NAME]:
            print(f"Skipping team row with index {index}!")
            continue
        
        team_uni = row[TEAM_COL_UNI]
        team_name = row[TEAM_COL_NAME]
        
        team = {
            "id": str(index+1),
            "icpc_id": str(100+index+1),
            "group_ids": [GROUP_ID],
            "name": team_name,
            "organization_id": team_uni
        }
        
        teams.append(team)
    
    teams_path = "./data/teams.json"
    with open(teams_path, 'w') as f:
        json.dump(teams, f, indent=4)
    
    print("Teams Ready!")
    
    # create accounts.yaml
    accounts = []
    users = []
    passwords = []
    
    for index, row in team_df.iterrows():
        
        if not row[TEAM_COL_UNI] or not row[TEAM_COL_NAME]:
            print(f"Skipping team row with index {index}!")
            users.append("-")
            passwords.append("-")
            continue
        
        team_uni = row[TEAM_COL_UNI]
        team_name = row[TEAM_COL_NAME]
        
        password_length = 8
        
        username = team_name + "-ACC"
        password = secrets.token_urlsafe(password_length)
        
        users.append(username)
        passwords.append(password)
        
        account = {
            "id": team_name,
            "username": username,
            "password": password,
            "type": "team",
            "team_id": str(index+1)
        }
        
        accounts.append(account)
    
    accounts_path = "./data/accounts.json"
    with open(accounts_path, 'w') as f:
        json.dump(accounts, f, indent=4)
    
    print("Accounts Ready!")
    
    # Save username and passwords on the team df
    team_df['username'] = users
    team_df['password'] = passwords
    
    path = "./data/team_accounts.xlsx"
    team_df.to_excel(path, index=False)


if __name__ == "__main__":
    main()
