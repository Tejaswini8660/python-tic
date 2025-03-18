from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Initialize game board
board = [['' for _ in range(3)] for _ in range(3)]
current_player = 'X'

def check_winner():
    """Checks if there's a winner"""
    for row in board:
        if row[0] == row[1] == row[2] and row[0] != '':
            return row[0]

    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != '':
            return board[0][col]

    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != '':
        return board[0][0]

    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != '':
        return board[0][2]

    return None

@app.route('/')
def index():
    """Home page with game board"""
    return render_template('index.html', board=board, current_player=current_player)

@app.route('/play', methods=['POST'])
def play():
    """Handle player moves"""
    global current_player

    data = request.json
    row, col = data['row'], data['col']

    if board[row][col] == '':
        board[row][col] = current_player
        winner = check_winner()
        
        if winner:
            return jsonify({'status': 'win', 'winner': winner})
        
        current_player = 'O' if current_player == 'X' else 'X'
        return jsonify({'status': 'success', 'next_player': current_player})
    
    return jsonify({'status': 'error', 'message': 'Cell already taken'})

@app.route('/reset', methods=['POST'])
def reset():
    """Reset the game board"""
    global board, current_player
    board = [['' for _ in range(3)] for _ in range(3)]
    current_player = 'X'
    return jsonify({'status': 'reset'})

if __name__ == '__main__':
    app.run(debug=True)
