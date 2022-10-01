# sg-scan-removal

## Pre-Requisite
1. python 
2. pipenv
3. AWS
## Installation 
```
1. pipenv install
2. Setup Environment -> check .env.example
2. python main.py False
```
## Usage Guide
```
Format Script: 
python main.py [ReadOnly]
ReadOnly only suport string: 
- True
- False
```
ReadOnly -> True: Will scan only without revoking the access

ReadOnly -> False: Will try to revoke the access


### example:
```
Script: 
python main.py False

Result: 
Information Summary
tags excluded:  {'Key': 'specified_tag', 'Value': 'True'}
ports scanned:  [21, 31, 30]
cidr scanned:  ['0.0.0.0/0']
----- Scanning Result -------
No loose security groups rules found
```


# Note
https://aws.amazon.com/blogs/security/how-to-continuously-audit-and-limit-security-groups-with-aws-firewall-manager/

AWS already have high level solution for auditing security groups. 
