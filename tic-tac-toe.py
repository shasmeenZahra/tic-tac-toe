import streamlit as st  # Importing Streamlit for the UI
import numpy as np  # Importing NumPy for handling the game board as a matrix

# Title and subheading
st.title("Tic-Tac-Toe 🎮")  # Display the main title
st.subheader("Play against AI or with a friend!")  # Small description of the game

# Initialize the game state variables in Streamlit session
if "board" not in st.session_state:
    st.session_state.board = np.full((3, 3), "", dtype=str)  # Create a 3x3 empty board
if "player_turn" not in st.session_state:
    st.session_state.player_turn = "X"  # Set first player to "X"
if "winner" not in st.session_state:
    st.session_state.winner = None  # No winner at the start
if "game_mode" not in st.session_state:
    st.session_state.game_mode = "Two Player"  # Default mode is two-player

# Function to check for a winner
def check_winner():
    """
    Checks if there is a winner or if the game ends in a draw.
    Returns 'X', 'O', 'Draw', or None (if the game is still ongoing).
    """
    board = st.session_state.board  # Get the current board state

    # Check rows and columns for a winner
    for i in range(3):
        if all(board[i, :] == board[i, 0]) and board[i, 0] != "":
            return board[i, 0]  # Winner found in a row
        if all(board[:, i] == board[0, i]) and board[0, i] != "":
            return board[0, i]  # Winner found in a column

    # Check diagonals
    if all(board.diagonal() == board[0, 0]) and board[0, 0] != "":
        return board[0, 0]  # Winner found in the main diagonal
    if all(np.fliplr(board).diagonal() == board[0, 2]) and board[0, 2] != "":
        return board[0, 2]  # Winner found in the anti-diagonal

    # Check for a draw (no empty cells left)
    if "" not in board:
        return "Draw"

    return None  # No winner yet, game continues

# Function for AI Move (random move)
def ai_move():
    """
    AI selects a random empty cell to place 'O'.
    """
    empty_cells = np.argwhere(st.session_state.board == "")  # Find all empty positions
    if len(empty_cells) > 0:
        row, col = empty_cells[np.random.choice(len(empty_cells))]  # Pick a random empty cell
        st.session_state.board[row, col] = "O"  # AI places "O" in the selected cell

# Sidebar options for game mode selection
st.sidebar.header("Game Settings")  # Sidebar header
game_mode = st.sidebar.radio("Select Mode:", ["Two Player", "Play Against AI"])  # Select between AI or two-player mode

# If game mode changes, reset the game
if game_mode != st.session_state.game_mode:
    st.session_state.game_mode = game_mode  # Update game mode
    st.session_state.board = np.full((3, 3), "", dtype=str)  # Reset the board
    st.session_state.player_turn = "X"  # Start with "X"
    st.session_state.winner = None  # Reset winner

# Display the Tic-Tac-Toe board
cols = st.columns(3)  # Create 3 columns for the grid
for i in range(3):
    for j in range(3):
        with cols[j]:  # Place each button in its respective column
            if st.button(st.session_state.board[i, j] or " ", key=f"{i}{j}"):  # If button is clicked
                if st.session_state.board[i, j] == "" and st.session_state.winner is None:  # Ensure cell is empty and game isn't over
                    st.session_state.board[i, j] = st.session_state.player_turn  # Mark the player's move
                    st.session_state.winner = check_winner()  # Check if this move wins the game

                    # Switch turns if no winner yet
                    if not st.session_state.winner:
                        st.session_state.player_turn = "O" if st.session_state.player_turn == "X" else "X"

                    # If playing against AI and it's "O"'s turn
                    if st.session_state.game_mode == "Play Against AI" and st.session_state.player_turn == "O" and not st.session_state.winner:
                        ai_move()  # AI makes a move
                        st.session_state.winner = check_winner()  # Check for a winner after AI move
                        st.session_state.player_turn = "X"  # Return turn to "X"

# Display winner or draw message
if st.session_state.winner:
    if st.session_state.winner == "Draw":
        st.success("It's a Draw! 🤝")  # Show draw message
    else:
        st.success(f"Player {st.session_state.winner} Wins! 🎉")  # Announce winner

# Button to restart the game
if st.button("Restart Game 🔄"):
    st.session_state.board = np.full((3, 3), "", dtype=str)  # Reset the board
    st.session_state.player_turn = "X"  # Reset player turn to "X"
    st.session_state.winner = None  # Reset winner
