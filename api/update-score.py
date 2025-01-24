from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/update-score', methods=['POST'])
def update_score():
    data = request.json
    username = data.get('username')
    points = data.get('points')
    
    if not username or points is None:
        return jsonify({"error": "البيانات غير كاملة"}), 400
    
    return jsonify({"message": f"تم تحديث نقاط {username} إلى {points}"}), 200

if __name__ == '__main__':
    app.run(debug=True)
