import ChatApi
import Persister
from UserApi import UserApi
from MediaApi import MediaApi
from FollowerApi import FollowerApi
from ProjectApi import ProjectApi
from EventApi import EventApi
from NecessitiesRequestApi import NecessitiesRequestApi
from ChallengeApi import ChallengeApi
import os
from flask import Flask, render_template, request, redirect, jsonify
import json

app = Flask(__name__)
app.secret_key = os.urandom(24)

userApi = UserApi()
mediaApi = MediaApi()
followerApi = FollowerApi()
projectApi = ProjectApi()
eventApi = EventApi()
necessitiesRequestApi = NecessitiesRequestApi()
challengeApi = ChallengeApi()


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def route(path):
    return render_template('index.html')


@app.route('/test', methods=['POST'])
def testServer():
    return jsonify({"working": True})


# POST request to register a new user
# Fields:
#	name: string
#	email: string (must not be already in db)
#   password: string (unhashed)
# 	locationCity: string
# 	profilePhoto: string (base64 image)
# 	description: string
# 	organisation: string
@app.route('/register', methods=['POST'])
def registerUser():
    data = request.get_json()
    if data != None:
        return jsonify({"response": userApi.saveUser(
            data.get('name'),
            data.get('email'),
            data.get('password'),
            data.get('locationCity'),
            data.get('profilePhoto'),
            data.get('description'),
            data.get('organisation')
        )})
    return jsonify({"response": False, "msg": "Please make sure to send json data"})


# POST request to remove an existing user
# Fields:
#	id: int (must exist in db)
@app.route('/removeUser', methods=['POST'])
def removeUser():
    data = request.get_json()
    if data != None:
        return jsonify({"response": userApi.removeUser(data.get('id'))})
    return jsonify({"response": False, "msg": "Please make sure to send json data"})


# POST request to login a user
# Fields:
#	email: string (must exist in db)
#	password: string (unhashed)
@app.route('/login', methods=['POST'])
def loginUser():
    data = request.get_json()
    if data != None:
        return jsonify({"response": userApi.loginUser(data.get('email'), data.get('password'))})
    return jsonify({"response": False, "msg": "Please make sure to send json data"})


# POST request to login a user
# Fields:
#	email: string (must exist in db)
@app.route('/logout', methods=['POST'])
def logoutUser():
    data = request.get_json()
    if data != None:
        return jsonify({"response": userApi.logoutUser(data.get('id'))})
    return jsonify({"response": False, "msg": "Please make sure to send json data"})


@app.route('/storeChatMessages', methods=["POST"])
def storeChatMessages():
    messageObject = request.args.get('messageObject')
    owner = request.args.get('owner')
    user = request.args.get('user')
    ChatApi.storeChatMessages(owner, user, messageObject)


@app.route('/getChatMessages', methods=["GET"])
def getChatMessages():
    owner = request.args.get('owner')
    user = request.args.get('user')
    return ChatApi.storeChatMessages(owner, user)


@app.route('/storeMedia', methods=['POST'])
def storeMedia():
    data = request.get_json()
    if data != None:
        return jsonify({"response": mediaApi.storeMedia(data.get('project'), data.get('name'), data.get('media'))})
    return jsonify({"response": False, "msg": "Please make sure to send json data"})


@app.route('/removeMedia', methods=['POST'])
def removeMedia():
    data = request.get_json()
    if data != None:
        return jsonify({"response": mediaApi.removeMedia(data.get('id'))})
    return jsonify({"response": False, "msg": "Please make sure to send json data"})


@app.route('/addFollower', methods=['POST'])
def addFollower():
    data = request.get_json()
    if data != None:
        return jsonify(
            {"response": followerApi.addFollower(data.get('project'), data.get('user'), data.get('deviceId'))})
    return jsonify({"response": False, "msg": "Please make sure to send json data"})


@app.route('/removeFollower', methods=['POST'])
def removeFollower():
    data = request.get_json()
    if data != None:
        return jsonify({"response": followerApi.removeFollower(data.get('id'))})
    return jsonify({"response": False, "msg": "Please make sure to send json data"})


@app.route('/getFollowersForProject', methods=['POST'])
def getFollowersForProject():
    data = request.get_json()
    if data != None:
        return jsonify({"response": followerApi.getFollowersForProject(data.get('project'))})
    return jsonify({"response": False, "msg": "Please make sure to send json data"})


@app.route('/pushFollowers', methods=['POST'])
def pushFollowers():
    data = request.get_json()
    if data != None:
        return jsonify({"response": followerApi.pushFollowers(data.get('project'))})
    return jsonify({"response": False, "msg": "Please make sure to send json data"})


@app.route('/addProject', methods=['POST'])
def addProject():
    data = request.get_json()
    if data != None:
        return jsonify({"response": projectApi.addProject(data.get('title'), data.get('description'),
                                                          data.get('thumbnail'), data.get('creator'),
                                                          data.get('beginDate'), data.get('endDate'))})
    return jsonify({"response": False, "msg": "Please make sure to send json data"})


@app.route('/addEvent', methods=['POST'])
def addEvent():
    data = request.get_json()
    if data != None:
        return jsonify({"response": eventApi.addEvent(data.get('title'), data.get('description'), data.get('project'),
                                                      data.get('beginDate'), data.get('endDate'))})
    return jsonify({"response": False, "msg": "Please make sure to send json data"})


@app.route('/addLike', methods=['POST'])
def addLike():
    data = request.get_json()
    projectId = data.get('projectId')
    userId = data.get('userId')

    return jsonify({"response": projectApi.addLike(projectId, userId)})


@app.route('/removeLike', methods=['POST'])
def removeLike():
    id = request.args.get('id')
    return jsonify({"response": projectApi.removeLike(id)})


@app.route('/totalLikes', methods=['POST'])
def totalLikes():
    id = request.args.get('id')
    return jsonify({"response": projectApi.totalLikes(id)})


@app.route('/getAllProjects', methods=['POST'])
def getAllProjects():
    data = request.get_json()
    result = projectApi.getAllProjects()
    return jsonify({"response": result})


@app.route('/makeNecessityRequest', methods=['POST'])
def makeRequest():
    data = request.get_json()
    if data != None:
        return jsonify({"response": necessitiesRequestApi.makeRequest(data.get('owner'), data.get('title'), data.get('description'), data.get('necessity'), data.get('offered'), data.get('picture'))})
    return jsonify({"response": False, "msg": "Please make sure to send json data"})


@app.route('/getNecessityRequestById', methods=['POST'])
def getRequest():
    data = request.get_json()
    if data != None:
        return jsonify({"response": necessitiesRequestApi.getRequestById(data.get('id'))})
    return jsonify({"response": False, "msg": "Please make sure to send json data"})


@app.route('/getAllNecessityRequests', methods=['POST'])
def getAllRequests():
    data = request.get_json()
    if data != None:
        return jsonify({"response": necessitiesRequestApi.getAllRequests()})
    return jsonify({"response": False, "msg": "Please make sure to send json data"})

@app.route('/getAllChallenges', methods=['POST'])
def getAllChallenges():
    data = request.get_json()
    if data != None:
        return jsonify({"response": challengeApi.getAllChallenges()})
    return jsonify({"response": False, "msg": "Please make sure to send json data"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
