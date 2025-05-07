from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from pymongo import MongoClient
from .serializers import ContactSerializer, MessageSerializer
from datetime import datetime


client = MongoClient("mongodb://localhost:27017/")
db = client["contactdb"]
collection = db["messages"]

class ContactView(APIView):
    def post(self, request):
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            message = serializer.validated_data
            message["timestamp"] = datetime.utcnow()
            result = collection.insert_one(message)
            return Response({"message": "Saved", "id": str(result.inserted_id)}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class MessageListView(APIView):
     def get(self, request):
        raw_data = list(collection.find({}, {"_id": 0}))
        serializer = MessageSerializer(raw_data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
