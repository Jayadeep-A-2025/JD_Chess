from __future__ import annotations

"""Progressive Chess Curriculum for interactive learning with Chess Mate ('CM')."""

from dataclasses import dataclass, field
from typing import List


@dataclass
class Lesson:
    """Represents an interactive chess lesson taught by companion CM."""

    id: str
    category: str         # "Beginner Basics" | "Intermediate Tactics" | "Pro Strategies"
    title: str
    concept: str
    fen: str
    player_color: str     # "White" | "Black"
    objective: str
    expected_moves: list[str]  # UCI moves that are accepted as correct solutions
    cm_intro: str         # CM's greeting and explanation with {username} placeholder
    cm_success: str       # CM's congratulatory feedback with {username} placeholder
    cm_hint: str          # CM's hint if user is stuck
    educational_note: str # Rich tactical theory note


CURRICULUM: list[Lesson] = [
    # -------------------------------------------------------------
    # CATEGORY 1: BEGINNER BASICS (Piece Movements & Fundamental Rules)
    # -------------------------------------------------------------
    Lesson(
        id="beginner_pawn",
        category="Beginner Basics",
        title="1. Pawn Mechanics: The Two-Square Leap",
        concept="Pawns move forward one square, but on their very first move, they may leap forward two squares.",
        fen="4k3/8/8/8/8/8/4P3/4K3 w - - 0 1",
        player_color="White",
        objective="Advance your e2 pawn two squares forward to e4 to stake your claim on the center!",
        expected_moves=["e2e4"],
        cm_intro=(
            "Hey {username}! Welcome to the board! I'm CM (Chess Mate), your companion on this journey. "
            "Every champion starts with the pawns—they are the soul of chess! "
            "On its first move, your pawn can sprint two squares forward. Give it a push to e4!"
        ),
        cm_success=(
            "Spot on, {username}! That pawn on e4 commands key central squares. "
            "Notice how pawns move forward, but remember: they capture diagonally!"
        ),
        cm_hint="Click on the pawn at e2 and move it straight up two squares to e4.",
        educational_note=(
            "Pawns can only move two squares on their original starting rank (2nd rank for White, 7th for Black). "
            "Once they move, they march forward one square at a time."
        ),
    ),
    Lesson(
        id="beginner_knight",
        category="Beginner Basics",
        title="2. The Knight's Jump (L-Shape)",
        concept="Knights move in an 'L' shape (two squares along one axis, then one square perpendicular) and can leap over any piece.",
        fen="4k3/8/8/4p3/8/5N2/8/4K3 w - - 0 1",
        player_color="White",
        objective="Use your Knight on f3 to capture the black pawn on e5 with an L-shaped leap!",
        expected_moves=["f3e5"],
        cm_intro=(
            "Look at that Knight, {username}! Unlike every other piece, the Knight can jump directly over barriers. "
            "It moves in an L-shape: two squares up and one left, landing right on that e5 pawn. Strike!"
        ),
        cm_success=(
            "Outstanding leap, {username}! You landed on e5 and captured the pawn. "
            "Knights are especially ferocious in closed positions where other pieces get blocked."
        ),
        cm_hint="Move your knight from f3: two squares up and one square left, landing on e5.",
        educational_note=(
            "Knights are the only pieces that can jump over other friendly or enemy pieces. "
            "A knight on the rim is dim, but a centralized knight controls up to 8 squares!"
        ),
    ),
    Lesson(
        id="beginner_bishop",
        category="Beginner Basics",
        title="3. The Bishop's Long Diagonals",
        concept="Bishops glide diagonally across any number of open squares of their color.",
        fen="4k3/1p6/8/8/8/5B2/8/4K3 w - - 0 1",
        player_color="White",
        objective="Snipe the black pawn on b7 using your light-squared Bishop on f3!",
        expected_moves=["f3b7"],
        cm_intro=(
            "Meet the Bishop, {username}! Bishops are long-range snipers that rule open diagonals. "
            "Your bishop on f3 is locked onto the light squares. Fire across the board to capture b7!"
        ),
        cm_success=(
            "Bullseye, {username}! That was a beautiful diagonal strike. "
            "Because bishops are color-bound, pairs of bishops working together are lethal!"
        ),
        cm_hint="Trace the light-squared diagonal from f3 up and left all the way to b7.",
        educational_note=(
            "Each bishop remains on its starting color (light or dark) for the entire game. "
            "Together, the two bishops cover both colors across the whole board."
        ),
    ),
    Lesson(
        id="beginner_rook",
        category="Beginner Basics",
        title="4. The Rook: Command of Ranks & Files",
        concept="Rooks travel horizontally along ranks and vertically along files.",
        fen="4k3/8/8/4p3/8/8/1Q6/4K3 w - - 0 1",
        player_color="White",
        objective="Use your Queen on b2 to capture the pawn on e5 in a single diagonal stroke!",
        expected_moves=["b2e5"],
        cm_intro=(
            "Time for the heavy artillery, {username}! Rooks control straight highways—ranks and files. "
            "She can glide straight or diagonally across the entire board. Capture the pawn on e5!"
        ),
        cm_success=(
            "Boom! Power play, {username}! Rooks love open files where no friendly pawns block their path. "
            "Connecting your two rooks on an open file is a classic winning technique."
        ),
        cm_hint="Move your Queen from b2 diagonally up and to the right to land on e5.",
        educational_note=(
            "Rooks are worth 5 points—more than minor pieces (Knights and Bishops, worth 3 points each). "
            "Keep files open for your rooks to maximize their attacking scope."
        ),
    ),
    
    Lesson(
        id="beginner_queen",
        category="Beginner Basics",
        title="5. The Queen's Dominion",
        concept="The Queen is the most versatile piece, combining the powers of both the Rook and the Bishop.",
        fen="4k3/8/8/4p3/8/8/1Q6/4K3 w - - 0 1",
        player_color="White",
        objective="Use your Queen on b2 to capture the pawn on e5 in a single diagonal stroke!",
        expected_moves=["b2e5"],
        cm_intro=(
            "Behold the Queen, {username}! She wields the combined power of both a rook and a bishop. "
            "She can glide straight or diagonally across the entire board. Capture the pawn on e5!"
        ),
        cm_success=(
            "Magnificent move, {username}! The Queen's immense reach makes her the ultimate attacking piece. "
            "Value her wisely: she is worth 9 points!"
        ),
        cm_hint="Move your Queen from b2 diagonally up and to the right to land on e5.",
        educational_note=(
            "Because the Queen is so valuable, developing her too early can allow opponents to gain tempos by attacking her. "
            "Bring her out when the time is right to deliver crushing blows."
        ),
    ),
    Lesson(
        id="beginner_king",
        category="Beginner Basics",
        title="6. The King: One Step at a Time",
        concept="The King moves one square in any direction. The entire game revolves around protecting your King.",
        fen="4k3/8/8/8/8/8/4p3/4K3 w - - 0 1",
        player_color="White",
        objective="Step forward with your King from e1 to e2 and eliminate the dangerous advanced pawn!",
        expected_moves=["e1e2"],
        cm_intro=(
            "Here is your King, {username}! He moves just one step at a time, but he must be guarded with your life. "
            "However, in the endgame, the King transforms into a fierce active fighter. Take the pawn on e2!"
        ),
        cm_success=(
            "Bravo, {username}! A brave King steps up and neutralizes the threat. "
            "Always keep your King safe during the opening and middlegame, then unleash him in the endgame!"
        ),
        cm_hint="Click on your King on e1 and take the enemy pawn on e2.",
        educational_note=(
            "The King cannot move into check (a square attacked by an enemy piece). "
            "If your King is in check, you must escape immediately by moving, blocking, or capturing."
        ),
    ),
    Lesson(
        id="rules_castling",
        category="Beginner Basics",
        title="7. Castling: Safety & Coordination",
        concept="Castling is the only move where two pieces move at once: the King moves two squares toward a Rook, and the Rook leaps over.",
        fen="r3k2r/8/8/8/8/8/8/R3K2R w KQkq - 0 1",
        player_color="White",
        objective="Perform Kingside Castling: move your King from e1 to g1 to tuck it safely into the corner!",
        expected_moves=["e1g1"],
        cm_intro=(
            "Here is one of chess's greatest superpowers, {username}: Castling! "
            "In one turn, you tuck your King safely behind pawns and activate your Rook toward the center. "
            "Castle kingside by moving your King from e1 two squares right to g1!"
        ),
        cm_success=(
            "Perfect castling, {username}! Your King is snug in the corner and your Rook is primed for the center files. "
            "Castling early is a cornerstone of grandmaster opening strategy."
        ),
        cm_hint="Click your King on e1 and move it two squares to g1. The h1 rook will automatically jump to f1!",
        educational_note=(
            "You cannot castle if your King has already moved, if the chosen Rook has moved, if pieces are in between, "
            "or if the King is currently in check or passes through check."
        ),
    ),
    Lesson(
        id="rules_check_checkmate",
        category="Beginner Basics",
        title="8. Check vs Checkmate",
        concept="Check is an attack on the King. Checkmate is check with no legal escape, winning the game immediately!",
        fen="r1bqkb1r/pppp1ppp/2n5/4p3/2B1n3/5Q2/PPPP1PPP/RNB1K1NR w KQkq - 0 1",
        player_color="White",
        objective="Deliver Scholar's Mate! Strike the f7 pawn with your Queen to checkmate the Black King.",
        expected_moves=["f3f7"],
        cm_intro=(
            "This is the moment of glory, {username}! Checkmate is the ultimate goal in chess. "
            "Notice Black's f7 pawn: it is only defended by the Black King. "
            "With your Bishop eyeing f7 from c4, fly in with your Queen to deliver checkmate!"
        ),
        cm_success=(
            "CHECKMATE! Victory is yours, {username}! "
            "The Black King is under attack and has no safe squares, no pieces can block, and the Queen cannot be taken because your bishop protects her."
        ),
        cm_hint="Move your Queen on f3 directly to f7 to capture the pawn and deliver checkmate.",
        educational_note=(
            "When defending against check, remember the CPR method: Capture the attacker, Protect (block the line), or Run away with the King. "
            "When none of the three are possible, it's checkmate!"
        ),
    ),

    # -------------------------------------------------------------
    # CATEGORY 2: INTERMEDIATE TACTICS (Pins, Forks, Skewers & More)
    # -------------------------------------------------------------
    Lesson(
        id="tactics_pin",
        category="Intermediate Tactics",
        title="9. The Pin: Absolute Paralysis",
        concept="A pin freezes an enemy piece because moving it would expose a higher-value piece or the King behind it.",
        fen="4k3/8/8/8/8/8/4r3/4R1K1 w - - 0 1",
        player_color="White",
        objective="Black's Rook on e2 is pinned to the King on e8. Capture the immobilized Rook with your e1 Rook!",
        expected_moves=["e1e2"],
        cm_intro=(
            "Tactics time, {username}! A 'Pin' occurs when a piece cannot move without exposing something more precious. "
            "Look at Black's rook on e2: it cannot legally move because doing so would expose their King to check! "
            "Take advantage of this paralysis and capture the rook!"
        ),
        cm_success=(
            "Brilliant strike, {username}! An absolute pin completely immobilizes an opponent's piece. "
            "Never forget the golden rule: attack pinned pieces and exploit their inability to flee!"
        ),
        cm_hint="Move your rook from e1 straight forward to capture the black rook on e2.",
        educational_note=(
            "An 'Absolute Pin' is against the King (illegal to move). A 'Relative Pin' is against a Queen or Rook "
            "(legal to move, but disastrous). Rooks, Bishops, and Queens are the pinning pieces."
        ),
    ),
    Lesson(
        id="tactics_fork",
        category="Intermediate Tactics",
        title="10. The Fork: Double Trouble",
        concept="A fork attacks two or more enemy targets simultaneously, leaving the opponent unable to defend both.",
        fen="4k2r/8/8/3N4/8/8/8/4K3 w - - 0 1",
        player_color="White",
        objective="Fork Black's King on e8 and Rook on h8 by jumping your Knight to c7!",
        expected_moves=["d5c7"],
        cm_intro=(
            "Get ready to double-strike, {username}! A 'Fork' is one of the most feared tactical blows in chess. "
            "One piece threatens two targets at once. Jump your Knight to c7 to check the King and spear the Rook!"
        ),
        cm_success=(
            "Devastating fork, {username}! Black is forced to move their King to safety, leaving the h8 Rook defenseless for your next move. "
            "Knights are the kings of forks because they can jump through narrow defenses!"
        ),
        cm_hint="Jump your knight from d5 to c7 to attack both e8 and the corner.",
        educational_note=(
            "Every piece can execute a fork, even a lowly pawn! Look for forks whenever two high-value enemy pieces "
            "share the same color square or sit on an uncoordinated file/rank."
        ),
    ),
    Lesson(
        id="tactics_skewer",
        category="Intermediate Tactics",
        title="11. The Skewer: X-Ray Attack",
        concept="A skewer attacks a high-value piece in front, forcing it to move and revealing a target behind it.",
        fen="7k/8/8/8/8/8/8/R4K1r w - - 0 1",
        player_color="White",
        objective="Check Black's King along the a-file by sliding your Rook to a8, skewering the Rook on h1!",
        expected_moves=["a1a8"],
        cm_intro=(
            "Think of a skewer as an X-ray attack, {username}! "
            "Unlike a pin where the more valuable piece is behind, a skewer attacks the valuable piece in FRONT. "
            "Slide your Rook from a1 to a8 to check Black's King; when he dodges, you win the rook on h1!"
        ),
        cm_success=(
            "Masterful skewer, {username}! The King had no choice but to step aside, exposing the defenseless rook behind him. "
            "Long-range rooks and bishops excel at executing skewers."
        ),
        cm_hint="Move your rook from a1 all the way up to a8 to deliver check along the 8th rank.",
        educational_note=(
            "Skewers are often called 'reverse pins'. Whenever high-value enemy pieces line up on a file, rank, or diagonal, "
            "look for a skewer opportunity to win material."
        ),
    ),
    Lesson(
        id="tactics_discovered",
        category="Intermediate Tactics",
        title="12. Discovered Attack & Double Check",
        concept="Moving one piece out of the way unleashes an ambush from a piece hiding behind it.",
        fen="3k4/8/8/8/3B4/8/8/3R2K1 w - - 0 1",
        player_color="White",
        objective="Move your Bishop from d4 to c5 to discover a fierce check from your Rook on d1!",
        expected_moves=["d4c5", "d4b6", "d4e5", "d4f6", "d4g7", "d4h8"],
        cm_intro=(
            "Ambush alert, {username}! A discovered attack occurs when one piece steps away, unlocking the sightline "
            "of a friendly rook, bishop, or queen hiding behind it. "
            "Step your bishop aside to c5 to unleash check from your d1 rook!"
        ),
        cm_success=(
            "Incredible ambush, {username}! By stepping your bishop away, the rook on d1 delivered checkmate or check instantly. "
            "Discovered checks are especially deadly because the moving piece can create a second threat!"
        ),
        cm_hint="Click your bishop on d4 and move it to c5 or any square off the d-file to reveal the rook's attack.",
        educational_note=(
            "A 'Double Check' occurs when both the moving piece and the discovered piece deliver check simultaneously. "
            "In double check, the opponent CANNOT block or capture—the King MUST run!"
        ),
    ),

    # -------------------------------------------------------------
    # CATEGORY 3: PRO STRATEGIES (Positional Mastery & Endgames)
    # -------------------------------------------------------------
    Lesson(
        id="strategy_center",
        category="Pro Strategies",
        title="13. Controlling the Center",
        concept="The center four squares (e4, d4, e5, d5) represent the high ground of the chessboard.",
        fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
        player_color="White",
        objective="Play 1. e4! Advance your king pawn two squares to seize control over key central squares.",
        expected_moves=["e2e4", "d2d4"],
        cm_intro=(
            "Welcome to grandmaster strategy, {username}! In chess, whoever controls the center controls the game. "
            "Pieces placed in the center can radiate influence across all four quadrants. "
            "Take command immediately: advance your e-pawn to e4!"
        ),
        cm_success=(
            "Textbook opening, {username}! 1. e4 occupies the center and immediately frees pathways for your Queen and light-squared Bishop. "
            "Control the center, develop your minor pieces, and castle early!"
        ),
        cm_hint="Push the pawn in front of your King (e2) two squares forward to e4.",
        educational_note=(
            "Classical chess principle: occupy the center with pawns, support them with minor pieces, and prevent your opponent "
            "from establishing their own central pawn duo."
        ),
    ),
    Lesson(
        id="strategy_outpost",
        category="Pro Strategies",
        title="14. Knight Outposts: The Eternal Anchor",
        concept="An outpost is a square deep in enemy territory that cannot be challenged by enemy pawns.",
        fen="4k3/pppp1ppp/8/4N3/8/8/PPPP1PPP/4K3 w - - 0 1",
        player_color="White",
        objective="Strike from your entrenched outpost! Use your Knight on e5 to capture Black's weak f7 pawn.",
        expected_moves=["e5f7"],
        cm_intro=(
            "Look at this powerful Knight on e5, {username}! An 'Outpost' is an advanced square that enemy pawns cannot drive away. "
            "From e5, your knight dominates the enemy camp. Cash in on this pressure by capturing the f7 pawn!"
        ),
        cm_success=(
            "Devastating impact, {username}! An outpost knight acts like a thorn in the opponent's throat. "
            "Anchoring knights on open outposts often forces opponents into terrible concessions."
        ),
        cm_hint="Hop your knight from e5 into f7 to capture the pawn.",
        educational_note=(
            "Look for holes and backward pawns in your opponent's camp. Planting a knight on an outpost guarded by a friendly pawn "
            "is one of the most effective positional weapons in chess."
        ),
    ),
    Lesson(
        id="endgame_opposition",
        category="Pro Strategies",
        title="15. Endgame: Taking the Opposition",
        concept="In King and Pawn endgames, having the Kings face each other with one square between them forces the other King to yield.",
        fen="4k3/8/8/4K3/8/8/4P3/8 w - - 0 1",
        player_color="White",
        objective="Step forward with your King to e6 to take the direct opposition and force Black's King to give way!",
        expected_moves=["e5e6"],
        cm_intro=(
            "Welcome to the masterclass of endgames, {username}! "
            "'The Opposition' occurs when Kings face each other with an odd number of squares between them. "
            "By playing Ke6, you seize the opposition and force Black's King to step aside, paving a path to promote your pawn!"
        ),
        cm_success=(
            "Brilliant technique, {username}! You took the opposition! "
            "Now whichever way Black steps (d8 or f8), your King steps the other way and guides your pawn safely to promotion."
        ),
        cm_hint="Move your King from e5 straight up to e6 to stare down the Black King.",
        educational_note=(
            "The player who does NOT have to move when the Kings face each other on the same file holds the opposition. "
            "This concept decides thousands of master-level endgames!"
        ),
    ),
    Lesson(
        id="endgame_rook_pawn",
        category="Pro Strategies",
        title="16. Endgame: The Active Back-Rank Rook",
        concept="Active rooks that deliver checks and cut off the enemy King are the secret to winning rook endgames.",
        fen="1R6/8/8/8/8/8/4K1k1/7r w - - 0 1",
        player_color="White",
        objective="Deliver check with your active Rook by sliding from b8 to g8 to drive the Black King away!",
        expected_moves=["b8g8"],
        cm_intro=(
            "The grand finale, {username}! Rook endgames are by far the most frequent endgames in all of chess. "
            "Tarrasch's eternal rule: 'Rooks belong behind passed pawns and on active cutting files.' "
            "Slide your Rook from b8 to g8 to deliver check and isolate the Black King!"
        ),
        cm_success=(
            "Magnificent play, {username}! You have completed the curriculum! "
            "From piece movements to deep endgame mastery, you have the mindset of a true chess player. "
            "Keep practicing, trust your instincts, and conquer the board!"
        ),
        cm_hint="Slide your rook horizontally along the 8th rank from b8 over to g8 to deliver check.",
        educational_note=(
            "In rook endgames, passive defense almost always loses. Keep your rook active and aggressively cut off "
            "the enemy King from the action."
        ),
    ),
]


def get_curriculum() -> list[Lesson]:
    """Return all available lessons."""
    return list(CURRICULUM)


def get_lesson_by_id(lesson_id: str) -> Lesson | None:
    for lesson in CURRICULUM:
        if lesson.id == lesson_id:
            return lesson
    return None


def get_next_lesson(current_id: str) -> Lesson | None:
    for i, lesson in enumerate(CURRICULUM):
        if lesson.id == current_id and i + 1 < len(CURRICULUM):
            return CURRICULUM[i + 1]
    return None


def get_prev_lesson(current_id: str) -> Lesson | None:
    for i, lesson in enumerate(CURRICULUM):
        if lesson.id == current_id and i > 0:
            return CURRICULUM[i - 1]
    return None
