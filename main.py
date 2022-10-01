import json
import os
import sys
from typing import List
import boto3

ec2 = boto3.client("ec2")


def scan_sgr(ports=[], excluded_tags=None, cidr=[]) -> List:
    security_group_rules = ec2.describe_security_group_rules()["SecurityGroupRules"]

    sg_rule_result = []
    for sg_rule in security_group_rules:
        if (
            sg_rule["FromPort"] in ports
            and excluded_tags not in sg_rule["Tags"]
            and sg_rule["CidrIpv4"] in cidr
        ):
            sg_rule_result.append(sg_rule)

    return sg_rule_result


def revoke_sgr(sg_rules):
    revoked_result = []
    for revoke in sg_rules:
        result = ec2.revoke_security_group_ingress(
            SecurityGroupRuleIds=[revoke["SecurityGroupRuleId"]],
            GroupId=revoke["GroupId"],
        )
        revoked_result.append(result)
        print(result)
    return revoked_result    


if __name__ == "__main__":
    ports = json.loads(os.environ["PORTS"])
    cidr = json.loads(os.environ["CIDR"])
    excluded_tags = None
    if os.getenv("EXCLUDED_TAGS_KEY") and os.getenv("EXCLUDED_TAGS_VALUE"):
        excluded_tags = dict(
            Key=os.getenv("EXCLUDED_TAGS_KEY"),
            Value=os.getenv("EXCLUDED_TAGS_VALUE"),
        )
    print("Information Summary")
    print("tags excluded: ", excluded_tags)
    print("ports scanned: ", ports)
    print("cidr scanned: ", cidr)
    read_only = sys.argv[1] == "True"
    result = scan_sgr(
        ports=ports,
        excluded_tags=excluded_tags,
        cidr=cidr,
    )

    print("----- Scanning Result -------")
    if result:
        print("List of Loose Security Groups: ")
        print(result)
        if not read_only:
            print("------- Revoke Result -------")
            revoke_sgr(result)
    else:
        print("No loose security groups rules found")
