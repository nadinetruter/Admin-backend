from flask import Response, request
from database.models import SignUp, Admin
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from mongoengine.errors import FieldDoesNotExist, NotUniqueError, DoesNotExist, ValidationError, InvalidQueryError
from resources.errors import SchemaValidationError, AdminAlreadyExistsError, InternalServerError, UpdatingAdminError, DeletingAdminError, AdminNotExistsError


#these classes are created so that the admin can update/delete/send data to their profile
class AdminApi(Resource):
  #get objects
  #convert them to json
  #return response object
  #define type of response (application/json)
  # status 200 = success
  @jwt_required
  def get(self):
    sign = Admin.objects().to_json()
    return Response(sign, mimetype="application/json", status=200)


  # ** is the spread operator
  # it spreads the dict object out, neat viewing format
  # save object and return it as an id in Response
  @jwt_required
  def post(self):
      try:
          user_id = get_jwt_identity()
          body = request.get_json()
          user = SignUp.objects.get(id=user_id)
          admin =  Admin(**body, added_by=user)
          admin.save()
          user.update(push__movies=movie)
          user.save()
          id = movie.id
          return {'id': str(id)}, 200

      except (FieldDoesNotExist, ValidationError):
          raise SchemaValidationError
      except NotUniqueError:
          raise AdminAlreadyExistsError
      except Exception as e:
            raise InternalServerError



class AdminsApi(Resource):
  # updating an object
  # call the id of the object
  # use spread operator to pass the value to update funtion
  @jwt_required
  def put(self, id):
      try:
          user_id = get_jwt_identity()
          admin = Admin.objects.get(id=id, added_by=user_id)
          body = request.get_json()
          Admin.objects.get(id=id).update(**body)
          return '', 200
      except InvalidQueryError:
          raise SchemaValidationError
      except DoesNotExist:
          raise UpdatingAdminError
      except Exception:
          raise InternalServerError

  #get id matching object that wants to be deleted
  # deletes object
  @jwt_required
  def delete(self, id):
      try:
          user_id = get_jwt_identity()
          admin = Admin.objects.get(id=id, added_by=user_id)
          admin.delete()
          return '', 200
      except DoesNotExist:
          raise DeletingAdminError
      except Exception:
          raise InternalServerError

  # get only one document from server
  @jwt_required
  def get(self, id):
      try:
          admin = Admin.objects.get(id=id).to_json()
          return Response(Admin, mimetype="application/json", status=200)
      except DoesNotExist:
          raise AdminNotExistsError
      except Exception:
          raise InternalServerError
