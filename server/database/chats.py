from . import db

from datetime import datetime
from bson import ObjectId
from secrets import token_urlsafe
from html import escape

chats = db['chats']


def getChatHistory():
    chatHistory = list(chats.find({}, {"_id": 0}))
    return chatHistory

def postChat(message, user):
    success = chats.insert_one(
        {
            "chat": message,
            "creatorID": user,
        }
    )
    return True

def delete_comment(comment_id, user_id):
    comment = chats.find_one({"id", comment_id}, {"_id": False})
    if comment and comment['CreatorId'] == user_id:
        result = chats.delete_one({"id": comment_id})
        return result.deleted_count == 1
    else:
        return False
    
def delete_comments(board_id):
    chats.delete_many({"BoardId": board_id})
    
def get_comments(board_id):
    return list(chats.find({"BoardId": board_id}, {"_id": False}))
