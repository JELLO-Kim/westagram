import json, re

from json.decoder       import JSONDecodeError

from django.http        import JsonResponse
from django.views       import View
from django.db.models   import Q

from .models            import Posting, Comment, Like
from user.models        import User
from .utils             import login_decorator

class PostingView(View):
    @login_decorator
    def get(self, request):
        user            = request.user
        postings        = Posting.objects.filter(user_id=user.id)
        posting_list    = []
        for posting in postings :
            posting_info = {
                    'id'            : posting.id,
                    'name'          : User.objects.get(id=posting.user_id).name,
                    'image_url'     : posting.image_url,
                    'description'   : posting.description,
                    'create_at'     : posting.create_at,
                    }
            posting_list.append(posting_info)
        return JsonResponse({'result' : posting_list}, status=200)
    
    @login_decorator
    def post(self, request):
        try:
            data        = json.loads(request.body)
            user        = request.user

            Posting.objects.create(
                    user_id     = user.id,
                    image_url   = data['image_url'],
                    description = data.get('description', None)
                    )
            return JsonResponse({'message' : 'SUCCESS', 'image_url' : data['image_url'], 'description' : data.get('description', None), 'name' : user.name}, status=200)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)

        except User.DoesNotExist:
            return JsonResponse({'message' : 'INVALID_USER'}, status=400)
        
        except JSONDecodeError:
            return JsonResponse({'message' : 'NOTHING_INPUT'}, status=400)

class PostingDetailView(View):
    @login_decorator
    def get(self, request, user_id):
        try:
            user    = request.user
            posts   = Posting.objects.filter(user_id=user_id)

            if not user.id == user_id :
                return JsonResponse({'message' : 'INVALID_RIGHT'}, status=400)
            
            post_list = []
            for post in posts:
                post_info = {
                        'id' : post.id,
                        'image_url' : post.image_url,
                        'description' : post.description
                        }
                post_list.append(post_info)

            return JsonResponse({'result' : post_list}, status=200)
        
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)

    @login_decorator
    def put(self, request, posting_id):
        try:
            data        = json.loads(request.body)
            user        = request.user
            image_url   = data['image_url']
            description = data['description']
            user_id     = user.id

            post = Posting.objects.get(id=posting_id)

            if not user.name == post.user.name :
                return JsonResponse({'message' : 'INVALID_RIGHT'}, status=400)
            
            post.image_url      = image_url
            post.description    = description
            post.save()
            
            return JsonResponse({'result' : 'SUCCESS'}, status=200)

        except ValueError:
            return JsonResponse({'message' : 'VALUE_ERROR'}, status=400)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)
        except Posting.DoesNotExist:
            return JsonResponse({'message' : 'INVALID_POST'}, status=400)
    
    @login_decorator
    def patch(self, request,posting_id):
        try:
            data    = json.loads(request.body)
            user    = request.user
            post    = Posting.objects.get(id=posting_id)

            if not user.name == post.user.name :
                return JsonResponse({'message' : 'INVALID_RIGHT'}, status=400)
            
            post.description    = data.get('description', post.description)
            post.image_url      = data.get('image_url', post.image_url)
            post.save()

            return JsonResponse({'result' : 'SUCCESS_EDIT'}, status=200)


        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)
    @login_decorator
    def delete(self, request, posting_id):
        try:
            user        = request.user

            post = Posting.objects.get(id=posting_id)
            if not user.name == post.user.name:
                return JsonResponse({'message' : 'INVALID_USER'}, status=200)
            post.delete()

            return JsonResponse({'result' : 'SUCCESS'}, status=200)

        except ValueError:
            return JsonResponse({'message' : 'VALUE_ERROR'}, status=400)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)
        except Posting.DoesNotExist:
            return JsonResponse({'message' : 'INVALID_POST'}, status=400)

class CommentView(View):
    def get(self, request):
        comments = Comment.objects.all()
        comment_list = []
        for comment in comments:
            comment_info={
                    'id'    : comment.id,
                    'name' : comment.user.name,
                    'comment' : comment.comment,
                    'posting_id' : comment.posting_id,
                    }
            comment_list.append(comment_info)
        return JsonResponse({'result' : comment_list}, status=200)

    @login_decorator
    def post(self, request):
        try:
            data    = json.loads(request.body)
            comment = data['comment']
            user    = request.user

            Comment.objects.create(
                    comment     = comment,
                    user_id     = user.id,
                    posting_id  = data['posting_id'],
                    parent_id   = data.get('parent_id', None)
                    )
            return JsonResponse({'message' : 'SUCCESS'}, status=200)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)
        except Exception as e:
            return JsonResponse({'message' : e}, status=400)

class CommentDetailView(View):
    # ?????? ???????????? ????????? ??????
    def get(self, request, posting_id):
        try:
            comments = Comment.objects.filter(posting_id=posting_id)
            comment_list = []
            for comment in comments:
                comment_detail = {
                        'name' : comment.user.name,
                        'comment' : comment.comment,
                        'posting_id' : comment.posting.id
                        }
                comment_list.append(comment_detail)
            if not comment_list:
                return JsonResponse({'result' : '????????????'}, status=200)

            return JsonResponse({'result' : comment_list}, status=200)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)

    # ?????? ???????????? ?????? ????????? ?????? ???????????? ??????
    def get(self, request, posting_id, comment_id):
        try:
            comments = Comment.objects.filter(parent_id=comment_id)
            comment_list = []
            for comment in comments:
                comment_detail = {
                        'user' : comment.user.name,
                        'comment' : comment.comment,
                        'Up_comment' : comment.parent_id
                        }
                comment_list.append(comment_detail)
            if not comment_list:
                return JsonResponse({'result' : 'NO_COMMENT'}, status=200)

            return JsonResponse({'result' : comment_list}, status=200)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)


    @login_decorator
    def put(self, request, posting_id, comment_id):
        try:
            data    = json.loads(request.body)
            user    = request.user
            comment = Comment.objects.get(id=comment_id)

            if user.id != comment.user_id:
                return JsonResponse({'message' : 'INVALID_RIGHT'}, status=400)

            comment.comment=data['comment']
            comment.save()
            return JsonResponse({'result' : 'SUCCESS_EDIT'}, status=200)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)


    @login_decorator
    def delete(self, request, posting_id, comment_id):
        try:
            user    = request.user
            comment = Comment.objects.filter(id=comment_id, posting_id=posting_id)
            comment.delete()

            return JsonResponse({'result' : 'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)
        except Comment.DoesNotExist:
            return JsonResponse({'message' : 'NO_EXISTING_COMMENT'}, status=400)

class LikeView(View):
    def get(self, request):
            like_list =[]
            for post in posts:
                like_info = {
                    'posting_id' : post.id,
                    'user_id' : post.user_id
                    }
                like_list.append(like_info)

            return JsonResponse({'result' : like_list}, status=200)

    @login_decorator
    def post(self, request):
        try:
            data        = json.loads(request.body)
            posting     = data['posting_id']
            user        = request.user
            post        = Posting.objects.get(id=posting)

            # Posting??? MtoM?????? ???????????? ????????????!
            post.like_user.add(User.objects.get(id=user.id))
            # Like model??? import????????? ????????? ?????? ??????
            #Like.objects.create(user_id=user.id, posting_id=posting)

            return JsonResponse({'result' : 'SUCCESS'}, status=200)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)

class LikeDetailView(View):
    def get(self, request, posting_id):
        try:
            posts       = Like.objects.filter(posting_id=posting_id)
            if not Posting.objects.filter(id=posting_id).exists():
                return JsonResponse({'message' : 'INVALID_POST'}, status=400)

            posting_like =[]
            for post in posts:
                posting_like_info = {
                    'posting_id' : post.id,
                    'user_id' : post.user_id
                    }
                posting_like.append(posting_like_info)

            # ????????? ?????? ????????? ?????? ??????
            if not posting_like:
                return JsonResponse({'result' : 'NONE_HEART'}, status=200)

            return JsonResponse({'result' : len(posting_like)}, status=200)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)

    @login_decorator
    def delete(self, request, posting_id):
        try:
            user        = request.user
            like        = Like.objects.get(user_id=user.id, posting_id=posting_id)

            like.delete()
            return JsonResponse({'result' : 'SUCCESS'}, status=200)

        except ValueError:
            return JsonResponse({'message' : 'VALUE_ERROR'}, status=400)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)
        except Like.DoesNotExist:
            return JsonResponse({'message' : 'INVALID_LIKE'}, status=400)
