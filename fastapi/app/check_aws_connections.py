# check_aws_connections.py

import os
import json
import boto3
from botocore.exceptions import BotoCoreError, ClientError

def check_amazon_lex():
    """
    Amazon Lexへのアクセスを確認し、ボット情報を取得します。
    """
    try:
        lex_client = boto3.client(
            'lexv2-models',
            region_name=os.getenv('AWS_REGION'),
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            aws_session_token=os.getenv('AWS_SESSION_TOKEN')  # 必要な場合
        )
        
        # ボットの詳細情報を取得（最新バージョン）
        response = lex_client.describe_bot(
            botId=os.getenv('LEX_BOT_ID')
            # botVersion パラメータを除外
        )
        bot_name = response.get('botName', 'Unknown')
        return {"status": "success", "service": "Amazon Lex", "message": f"ボット名: {bot_name}"}
    except ClientError as e:
        return {"status": "error", "service": "Amazon Lex", "message": str(e)}
    except BotoCoreError as e:
        return {"status": "error", "service": "Amazon Lex", "message": str(e)}

def check_amazon_bedrock():
    """
    Amazon Bedrockへのアクセスを確認し、モデル情報を取得します。
    """
    try:
        bedrock_client = boto3.client(
            'bedrock-runtime',
            region_name=os.getenv('AWS_REGION'),
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            aws_session_token=os.getenv('AWS_SESSION_TOKEN')  # 必要な場合
        )
        
        # Bedrockモデルに対してテストリクエストを送信
        test_body = json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 100,
            "messages": [
                {"role": "user", "content": "テスト"}
            ]
        })
        
        response = bedrock_client.invoke_model(
            body=test_body,
            modelId=os.getenv('BEDROCK_MODEL_ID'),
            accept='application/json',
            contentType='application/json'
        )
        
        response_body = response.get('body').read()
        response_json = json.loads(response_body)
        
        # Bedrockからの完全なレスポンスをログに出力
        print("Bedrock Response:", json.dumps(response_json, indent=4, ensure_ascii=False))
        
        # 'content' フィールドを確認
        if 'content' in response_json:
            # 'content' はリスト形式なので、最初の要素の 'text' を取得
            content = response_json['content']
            if isinstance(content, list) and len(content) > 0:
                text_response = content[0].get('text', '')
                return {"status": "success", "service": "Amazon Bedrock", "message": f"応答内容: {text_response}"}
            else:
                return {"status": "error", "service": "Amazon Bedrock", "message": "応答の 'content' フィールドが空です。"}
        elif 'error' in response_json:
            # エラーが含まれている場合
            return {"status": "error", "service": "Amazon Bedrock", "message": response_json['error']['message']}
        else:
            return {
                "status": "error",
                "service": "Amazon Bedrock",
                "message": "応答に 'completion' も 'content' も含まれていません。",
                "response": response_json  # 追加: レスポンス全体を返す
            }
    except ClientError as e:
        return {"status": "error", "service": "Amazon Bedrock", "message": str(e)}
    except BotoCoreError as e:
        return {"status": "error", "service": "Amazon Bedrock", "message": str(e)}
    except json.JSONDecodeError:
        return {"status": "error", "service": "Amazon Bedrock", "message": "応答の解析に失敗しました。"}



def check_amazon_dynamodb():
    """
    Amazon DynamoDBへのアクセスを確認します。
    """
    try:
        dynamodb_client = boto3.client(
            'dynamodb',
            region_name=os.getenv('AWS_REGION'),
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
        )
        
        # テーブルの存在を確認
        table_name = os.getenv('DYNAMODB_TABLE_NAME')
        response = dynamodb_client.describe_table(TableName=table_name)
        table_status = response['Table']['TableStatus']
        return {"status": "success", "service": "Amazon DynamoDB", "message": f"テーブル名: {table_name}, 状態: {table_status}"}
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            return {"status": "error", "service": "Amazon DynamoDB", "message": f"テーブル '{os.getenv('DYNAMODB_TABLE_NAME')}' が存在しません。"}
        else:
            return {"status": "error", "service": "Amazon DynamoDB", "message": str(e)}
    except BotoCoreError as e:
        return {"status": "error", "service": "Amazon DynamoDB", "message": str(e)}
