"""
Views for the reviews app.

Purpose: Product reviews, ratings, review images, helpful votes.

Views only: parse request -> call serializer -> call service -> return
standard {success, message, data} / {success, message, errors} response.
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


# TODO: Implement reviews views here, using the standard WEBTECH API
# response envelope (see common/utils/responses.py).
