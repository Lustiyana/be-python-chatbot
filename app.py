from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime
from flask_cors import CORS

cred = credentials.Certificate("./chatbot-c0517-firebase-adminsdk-87jwd-c7d2916881.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://chatbot-c0517-default-rtdb.asia-southeast1.firebasedatabase.app'
})

ref = db.reference('/chats')


app = Flask(__name__)
cors = CORS(app)

posts = []

@app.route('/api/message/admin', methods=['POST'])
def message_admin():
    # Disini selain ngirim ke firebase tapi ngirim juga pesannya ke wa

    data = request.form
    message = data.get('message')
    existing_key = request.args.get('key')
    timestamp_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    new_data = {
        'message': message,
        'updated_at': timestamp_now,
        'role': 'admin'
    }


    messages_ref = ref.child(existing_key).child('messages')
    messages_ref.push(new_data)

    return jsonify({'message': 'Post created successfully!'}), 201


@app.route('/api/message', methods=['POST'])
def create_post():
    data = request.form
    message = data.get('message')
    phone_number = data.get('phone_number')
    timestamp_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    get_data = ref.get()
    phone_numbers = []

    new_data = {
        'message': message,
        'updated_at': timestamp_now,
        'role': 'user'
    }


    if get_data is not "": 
        for key, value in get_data.items():
            phone_number_item = value.get('phone_number')
            if phone_number_item:
                phone_numbers.append({'phone_number': phone_number_item, 'key': key})

    phone_number_keys = [entry['key'] for entry in phone_numbers]

    if phone_number in [entry['phone_number'] for entry in phone_numbers]:
        existing_key = phone_numbers[[entry['phone_number'] for entry in phone_numbers].index(phone_number)]['key']

        messages_ref = ref.child(existing_key).child('messages')
        
        messages_ref.push(new_data)

    else:
        uid_message = ref.push({'phone_number': phone_number})
        messages_ref = uid_message.child('messages')

        messages_ref.push(new_data)

    return jsonify({'message': 'Post created successfully!'}), 201


if __name__ == '__main__':
    app.run(debug=True)
