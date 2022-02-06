import boto3

rds = boto3.client('rds')

def get_tags_for_db(db):
    """
    get instance list
    """
    instance_arn = db['DBInstanceArn']
    instance_tags = rds.list_tags_for_resource(ResourceName=instance_arn)
    return instance_tags['TagList']

def start_db_instances(target_tag):
    """
    start instances
    """
    try:
        dbs = rds.describe_db_instances()
    except Exception as e:
        print(e)
        return { 'status': 2 }

    for db in dbs['DBInstances']:
        db_tags = get_tags_for_db(db)
        tag = next(iter(filter(lambda tag: tag['Key'] == target_tag and tag['Value'] == 'true', db_tags)), None)

        if tag and db['DBInstanceStatus'] == 'stopped':
            response = rds.start_db_instance(DBInstanceIdentifier=db["DBInstanceIdentifier"])
            print(db['DBInstanceIdentifier'])

def lambda_handler(event, context):
    target_tag = "autostart"
    start_db_instances(target_tag)
    return { 'status': 0 }