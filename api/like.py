from flask.ext import restful
from authenticate import authenticate
from flask import request, abort, jsonify
import time
from itertools import permutations


import config
from models import Event
from models import User, Match

class Like(restful.Resource):
    method_decorators=[authenticate]

    def post(self):
        # Create DB Match entry
        dst_id = request.form.get('dst_user')
        session = config.session

        # Target already liked, trigger "match"
        match = session.query(Match).filter_by(
                match_from_id= dst_id,
                match_to_id= self.user.id).first()

        if match:
            participants = sorted([self.user.id, dst_id])
            base = {
                'type': 'match',
                'participants': '{}:{}'.format(participants)
            }

            for (dst, src) in permutations(participants):
                Event.create(base.update({
                    'dst': dst,
                    'src': src
                }))

            match.mutual = True
        else:
            match = Match(match_from_id= self.user.id, match_to_id= dst_id)
            session.add(match)

        session.commit()

        return jsonify(status="ok")
