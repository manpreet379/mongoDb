from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from pymongo import MongoClient
from datetime import datetime

# Connect to local MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["contactdb"]
collection = db["messages"]

class ContactView(APIView):
    def post(self, request):
        data = request.data
        message = {
            "name": data.get("name"),
            "email": data.get("email"),
            "subject": data.get("subject"),
            "message": data.get("message"),
            "timestamp": datetime.utcnow()
        }
        result = collection.insert_one(message)
        return Response({"message": "Saved", "id": str(result.inserted_id)}, status=status.HTTP_201_CREATED)

class MessageListView(APIView):
    def get(self, request):
        messages = list(collection.find({}, {"_id": 0}))
        return Response(messages, status=status.HTTP_200_OK)
