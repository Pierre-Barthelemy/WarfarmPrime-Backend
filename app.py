import threading
import time

from Data import Data
import uwsgidecorators
from extract import extract
from flask import Flask, jsonify
from flask.json import JSONEncoder
from flask_caching import Cache
from flask_restful import Api, Resource
from flask_restful.utils import cors
from mission import Mission, MissionValue
from relic import Relic


class MyJSONEncoder(JSONEncoder):
	def default(self, obj):
		if isinstance(obj, Relic):
			return {
				'Vaulted': obj.Vaulted,
				'Name': obj.Name,
				'Common': obj.Common,
				'Uncommon': obj.Uncommon,
				'Rare': obj.Rare
			}
		if isinstance(obj, MissionValue):
			return {
				'Name': obj.Name,
				'Main': obj.Main,
				'A': obj.A,
				'B': obj.B,
				'C': obj.C,
				'NoRotation': obj.No_rotation
			}
		if isinstance(obj, Mission):
			return {
				'Name': obj.Name,
				'Type': obj.Type,
				'RotationA': obj.Rotation_A,
				'RotationB': obj.Rotation_B,
				'RotationC': obj.Rotation_C
			}
		return super(MyJSONEncoder, self).default(obj)


config = {
	"DEBUG": False,          # some Flask specific configs
	"CACHE_TYPE": "simple",  # Flask-Caching related configs
	"CACHE_DEFAULT_TIMEOUT": 500
}

app = Flask(__name__)
app.json_encoder = MyJSONEncoder
app.config.from_mapping(config)
cache = Cache(app)
api = Api(app)

data = Data()
data.process_data(extract())


@uwsgidecorators.timer(600)
def run(num):
	data.process_data(extract())


class WarframeLootTable(Resource):

	@cors.crossdomain(origin='*')
	@cache.cached(timeout=60)
	def get(self):
		return jsonify(data.get_data())


api.add_resource(WarframeLootTable, '/')

if __name__ == '__main__':
	app.run()
