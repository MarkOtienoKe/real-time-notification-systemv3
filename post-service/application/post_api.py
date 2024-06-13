from flask import Blueprint, request, jsonify
from .models import db, Post, Comment, Like
from . import producer
import json
post_api_blueprint = Blueprint('post_api', __name__)


def publish_kafka_event(event):
    producer.send('post-events', event)

@post_api_blueprint.route('/posts', methods=['POST'])
def create_post():
    data = request.get_json()
    #Fire create post event to kafka
    event = {
        'type': 'post_created',
        'user_id': data['user_id'],
        'msg_content': data['msg_content'],
    }
    publish_kafka_event(event)

    #save post to d
    new_post = Post(
        user_id=data['user_id'],
        msg_content=data['msg_content'],
    )
    db.session.add(new_post)
    db.session.commit()
    return jsonify({'message': 'Post created successfully'}), 201


@post_api_blueprint.route('/posts', methods=['GET'])
def get_posts():
    posts = Post.query.all()
    result = []
    for post in posts:
        post_data = {
            'id': post.id,
            'user_id': post.user_id,
            'msg_content': post.msg_content,
            'date_time_added': post.date_time_added,
            'date_time_modified': post.date_time_modified
        }
        result.append(post_data)
    return jsonify(result)


@post_api_blueprint.route('/posts/<post_id>', methods=['GET'])
def get_post(post_id):
    post = Post.query.get_or_404(post_id)
    post_data = {
        'id': post.id,
        'user_id': post.user_id,
        'msg_content': post.msg_content,
        'date_time_added': post.date_time_added,
        'date_time_modified': post.date_time_modified,
    }
    return jsonify(post_data)


@post_api_blueprint.route('/postComment', methods=['POST'])
def post_comment():
    data = request.get_json()
    new_post_comment = Comment(
        user_id=data['user_id'],
        post_id=data['post_id'],
        comment=data['comment'],
    )
    db.session.add(new_post_comment)
    db.session.commit()
    return jsonify({'message': 'Comment submitted successfully'}), 201


@post_api_blueprint.route('/likePost', methods=['POST'])
def like_post():
    data = request.get_json()
    new_post_like = Like(
        user_id=data['user_id'],
        post_id=data['post_id'],
        like=data['like'],
    )
    db.session.add(new_post_like)
    db.session.commit()
    return jsonify({'message': 'Like submitted successfully'}), 201
