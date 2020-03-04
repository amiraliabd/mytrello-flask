from flask import Flask,request,redirect,Response,jsonify
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///trello.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Trello(db.Model):
    card_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    status = db.Column(db.String(20), nullable=False)


@app.route('/')
def home():
    if len(Trello.query.order_by(Trello.card_id).all()) == 0:
        return 'no card to show'
    ls=[]
    for obj in Trello.query.order_by(Trello.card_id).all():
        ls.append(
            {'card_id':obj.card_id, 'name':obj.name, 'status':obj.status }
        )
    return jsonify(ls)


@app.route('/add', methods=['POST'])
def add():
    data = request.get_json()
    new_card = Trello(card_id = data['card_id'], name = data['name'], status = data['status'])
    db.session.add(new_card)
    db.session.commit()
    return redirect('/')


@app.route('/delete', methods=['POST'])
def delete():
    data = request.get_json()
    object_to_delete = Trello.query.filter_by(card_id = data['card_id']).first()
    if object_to_delete == None:
        return Response(status=404)
    db.session.delete(object_to_delete)
    db.session.commit()
    return redirect('/')


@app.route('/update', methods=['POST'])
def update():
    data = request.get_json()
    object_to_update = Trello.query.filter_by(card_id=data['card_id']).first()
    if object_to_update == None:
        return Response(status=404)
    object_to_update.card_id = data['card_id']
    object_to_update.name = data['name']
    object_to_update.status = data['status']
    db.session.commit()
    return redirect('/')




if __name__ == '__main__':
    app.run(debug=True)
