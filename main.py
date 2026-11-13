from dataclasses import dataclass
from drafter import *
from bakery import assert_equal



# list of popular NBA players
PLAYERS = [
    {"name": "Stephen Curry", "conference": "West", "role": "PG",
     "all_star": True, "foreign": False, "champion": True},
    {"name": "LeBron James", "conference": "West", "role": "SF",
     "all_star": True, "foreign": False, "champion": True},
    {"name": "Nikola Jokic", "conference": "West", "role": "C",
     "all_star": True, "foreign": True, "champion": True},
    {"name": "Shai Gilgeous-Alexander", "conference": "West", "role": "PG",
     "all_star": True, "foreign": True, "champion": True},
    {"name": "Luka Doncic", "conference": "West", "role": "PG",
     "all_star": True, "foreign": True, "champion": False},
    {"name": "Kevin Durant", "conference": "West", "role": "PF",
     "all_star": True, "foreign": False, "champion": True},
    {"name": "Anthony Edwards", "conference": "West", "role": "SG",
     "all_star": True, "foreign": False, "champion": False},
    {"name": "Victor Wembanyama", "conference": "West", "role": "C",
     "all_star": True, "foreign": True, "champion": False},
    {"name": "Devin Booker", "conference": "West", "role": "SG",
     "all_star": True, "foreign": False, "champion": False},
    {"name": "Kawhi Leonard", "conference": "West", "role": "SF",
     "all_star": True, "foreign": False, "champion": True},
    {"name": "Ja Morant", "conference": "West", "role": "PG",
     "all_star": True, "foreign": False, "champion": False},
    {"name": "Jamal Murray", "conference": "West", "role": "PG",
     "all_star": False, "foreign": True, "champion": True},
    {"name": "Domantas Sabonis", "conference": "West", "role": "C",
     "all_star": True, "foreign": True, "champion": False},
    {"name": "Chet Holmgren", "conference": "West", "role": "C",
     "all_star": False, "foreign": False, "champion": True},
    {"name": "Jalen Williams", "conference": "West", "role": "SF",
     "all_star": False, "foreign": False, "champion": True},
    {"name": "Jayson Tatum", "conference": "East", "role": "SF",
     "all_star": True, "foreign": False, "champion": True},
    {"name": "Giannis Antetokounmpo", "conference": "East", "role": "PF",
     "all_star": True, "foreign": True, "champion": True},
    {"name": "Jalen Brunson", "conference": "East", "role": "PG",
     "all_star": True, "foreign": False, "champion": True},
    {"name": "Joel Embiid", "conference": "East", "role": "C",
     "all_star": True, "foreign": True, "champion": False},
    {"name": "Donovan Mitchell", "conference": "East", "role": "SG",
     "all_star": True, "foreign": False, "champion": False},
    {"name": "Tyrese Haliburton", "conference": "East", "role": "PG",
     "all_star": True, "foreign": False, "champion": False},
    {"name": "Cade Cunningham", "conference": "East", "role": "PG",
     "all_star": False, "foreign": False, "champion": False},
    {"name": "Paolo Banchero", "conference": "East", "role": "PF",
     "all_star": True, "foreign": False, "champion": False},
    {"name": "Bam Adebayo", "conference": "East", "role": "C",
     "all_star": True, "foreign": False, "champion": False},
    {"name": "Jaylen Brown", "conference": "East", "role": "SF",
     "all_star": True, "foreign": False, "champion": True},
    {"name": "Evan Mobley", "conference": "East", "role": "PF",
     "all_star": False, "foreign": False, "champion": False},
    {"name": "Tyrese Maxey", "conference": "East", "role": "SG",
     "all_star": True, "foreign": False, "champion": False},
    {"name": "Scottie Barnes", "conference": "East", "role": "SF",
     "all_star": True, "foreign": True, "champion": False},
    {"name": "Trae Young", "conference": "East", "role": "PG",
     "all_star": True, "foreign": False, "champion": False},
    {"name": "LaMelo Ball", "conference": "East", "role": "PG",
     "all_star": True, "foreign": False, "champion": False},
]


@dataclass
class GameState:
    candidates: list
    asked_questions: list
    question: str
    target_name: str


QUESTIONS = [
    {
        "text": "Does the player play in the Western Conference?",
        "attribute": "conference",
        "value": "West"
    },
    {
        "text": "Does the player play in the Eastern Conference?",
        "attribute": "conference",
        "value": "East"
    },
    {
        "text": "Is the player a point guard (PG)?",
        "attribute": "role",
        "value": "PG"
    },
    {
        "text": "Is the player a shooting guard (SG)?",
        "attribute": "role",
        "value": "SG"
    },
    {
        "text": "Is the player a small forward (SF)?",
        "attribute": "role",
        "value": "SF"
    },
    {
        "text": "Is the player a power forward (PF)?",
        "attribute": "role",
        "value": "PF"
    },
    {
        "text": "Is the player a center (C)?",
        "attribute": "role",
        "value": "C"
    },
    {
        "text": "Was the player born outside the United States?",
        "attribute": "foreign",
        "value": True
    },
    {
        "text": "Has the player won an NBA championship?",
        "attribute": "champion",
        "value": True
    },
    {
        "text": "Has the player been an NBA All-Star?",
        "attribute": "all_star",
        "value": True
    },
]


def find_next_question(state):
    """Choose an attribute question that separates the candidates."""
    state.target_name = ""

    for question in QUESTIONS:
        if question["text"] not in state.asked_questions:
            yes_count = 0

            for player in state.candidates:
                if player[question["attribute"]] == question["value"]:
                    yes_count += 1

            
            if yes_count > 0 and yes_count < len(state.candidates):
                return question["text"]

    # If out of questions itll go down te players who have the same set of description
    state.target_name = state.candidates[0]["name"]
    return "Is your player " + state.target_name + "?"


def show_game(state):
    if len(state.candidates) == 1:
        return Page(state, [
            "I guessed it! Your player is "
            + state.candidates[0]["name"] + ".",
            Button("Play again", "index"),
            Button("Browse all players", "all_players")
        ])

    if len(state.candidates) == 0:
        return Page(state, [
            "I couldn't find that player in my list.",
            "Check your answers or add the player to the PLAYERS list.",
            Button("Play again", "index"),
            Button("Browse all players", "all_players")
        ])

    state.question = find_next_question(state)

    return Page(state, [
        "Pick a player from my list and answer each question.",
        state.question,
        Button("Yes", "answer", [Argument("answer", "yes")]),
        Button("No", "answer", [Argument("answer", "no")]),
        Button("Browse all players", "all_players")
    ])


@route
def index(state: GameState):
    """Start or restart the game."""
    state.candidates = PLAYERS[:]
    state.asked_questions = []
    state.question = ""
    state.target_name = ""
    return show_game(state)


@route
def answer(state: GameState, answer: str):
    """Use the answer to remove players who do not match."""
    if state.target_name != "":
        # Handle a question that asks about a specific player.
        if answer == "yes":
            state.candidates = [
                player for player in state.candidates
                if player["name"] == state.target_name
            ]
        else:
            state.candidates = [
                player for player in state.candidates
                if player["name"] != state.target_name
            ]

        state.target_name = ""

    else:
        # Handle a question about conference, role, or other attributes.
        for question in QUESTIONS:
            if question["text"] == state.question:
                remaining_players = []

                for player in state.candidates:
                    matches_question = (
                        player[question["attribute"]] == question["value"]
                    )

                    if answer == "yes" and matches_question:
                        remaining_players.append(player)
                    elif answer == "no" and not matches_question:
                        remaining_players.append(player)

                state.candidates = remaining_players
                state.asked_questions.append(question["text"])
                break

    return show_game(state)


@route
def all_players(state: GameState):
    """Show the directory of players in the game."""
    player_lines = []

    for player in PLAYERS:
        player_lines.append(
            player["name"] + " — " +
            player["role"] + " — " +
            player["conference"]
        )

    return Page(state, [
        "Player List",
        "\n".join(player_lines),
        Button("Back to game", "game"),
        Button("Start a new game", "index")
    ])


@route
def game(state: GameState):
    """Return to the current game without resetting it."""
    return show_game(state)


start_server(GameState(PLAYERS[:], [], "", ""))

conference_test_state = GameState(
    candidates=[
        {
            "name": "Test Player A",
            "conference": "West",
            "role": "PG",
            "all_star": True,
            "foreign": False,
            "champion": False
        },
        {
            "name": "Test Player B",
            "conference": "East",
            "role": "SG",
            "all_star": False,
            "foreign": True,
            "champion": True
        }
    ],
    asked_questions=[],
    question="",
    target_name=""
)

assert_equal(
    find_next_question(conference_test_state),
    "Does the player play in the Western Conference?"
)


# Test 2: If attributes cannot separate players, ask about one by name.
name_test_state = GameState(
    candidates=[
        {
            "name": "Test Player A",
            "conference": "West",
            "role": "PG",
            "all_star": True,
            "foreign": False,
            "champion": False
        },
        {
            "name": "Test Player B",
            "conference": "West",
            "role": "PG",
            "all_star": True,
            "foreign": False,
            "champion": False
        }
    ],
    asked_questions=[],
    question="",
    target_name=""
)

assert_equal(
    find_next_question(name_test_state),
    "Is your player Test Player A?"
)
