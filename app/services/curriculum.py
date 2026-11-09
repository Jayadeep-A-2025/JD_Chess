from __future__ import annotations

"""Progressive Chess Curriculum for interactive learning with Chess Mate ('CM').

Contains foundational training modules and an extensive 20-lesson structured
curriculum spanning Chess Fundamentals, Opening Principles, Tactical Skills,
Tactical Combinations, Defensive Techniques, Endgames, and Advanced Calculation.
"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class Lesson:
    """Represents an interactive chess lesson taught by companion CM."""

    id: str
    category: str         # Category title for navigation and grouping
    title: str
    concept: str
    fen: str
    player_color: str     # "White" | "Black"
    objective: str
    expected_moves: list[str]  # UCI moves accepted as correct solutions
    cm_intro: str         # CM's greeting and challenge description
    cm_success: str       # CM's congratulatory feedback
    cm_hint: str          # CM's quick hint
    educational_note: str # Grandmaster theory note
    # Enhanced interactive learning fields
    hints: list[str] = field(default_factory=list)      # Progressive 3-tier hints
    guided_move: str = ""                                # Primary demonstration move (UCI)
    theory_detail: str = ""                              # In-depth tactical theory breakdown
    feedback_correct: str = ""                           # Why the solution succeeds strategically
    feedback_incorrect: str = ""                         # Guidance when an alternative move is played


# =============================================================================
# CURRICULUM DEFINITION (36 Lessons: 16 Core Foundations + 20 Advanced Modules)
# =============================================================================

CURRICULUM: list[Lesson] = [
    # -------------------------------------------------------------------------
    # ORIGINAL FOUNDATION 1: BEGINNER BASICS
    # -------------------------------------------------------------------------
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
        hints=[
            "Look at the white pawn standing proudly on e2.",
            "Remember that on its initial turn, a pawn can advance either 1 or 2 squares.",
            "Click on e2 and select e4 to execute the opening leap!",
        ],
        guided_move="e2e4",
        theory_detail="Pawns dictate the terrain of the battlefield. Advancing central pawns opens diagonals for bishops and the queen.",
        feedback_correct="e2-e4 is the single most popular opening move in grandmaster chess history!",
        feedback_incorrect="That move doesn't stake a claim on the center. Try pushing the e2 pawn two squares forward to e4!",
    ),
    Lesson(
        id="beginner_knight",
        category="Beginner Basics",
        title="2. The Knight's Jump (L-Shape)",
        concept="Knights move in an 'L' shape (two squares along one axis, then one perpendicular) and can leap over any piece.",
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
        hints=[
            "Identify the target: Black's unprotected pawn on e5.",
            "Knights count 2 squares in one direction and 1 to the side.",
            "Move f3 to e5 to capture the pawn!",
        ],
        guided_move="f3e5",
        theory_detail="A centralized knight controls up to 8 squares, whereas a cornered knight controls only 2.",
        feedback_correct="The knight safely eliminates the black central pawn while establishing a dominant outpost.",
        feedback_incorrect="That move missed the target. Hop the knight from f3 directly to e5 to capture the pawn!",
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
        hints=[
            "Trace the diagonal from f3 up and left towards b7.",
            "No pieces obstruct the diagonal between f3 and b7.",
            "Select the Bishop on f3 and capture the pawn on b7!",
        ],
        guided_move="f3b7",
        theory_detail="Bishops thrive on open boards where pawns do not obstruct their long diagonals.",
        feedback_correct="Capturing b7 tears apart Black's queenside pawn structure.",
        feedback_incorrect="Bishops only glide along diagonals. Follow the long diagonal from f3 up to b7!",
    ),
    Lesson(
        id="beginner_rook",
        category="Beginner Basics",
        title="4. The Rook: Command of Ranks & Files",
        concept="Rooks travel horizontally along ranks and vertically along files.",
        fen="4k3/8/8/4p3/8/8/1R6/4K3 w - - 0 1",
        player_color="White",
        objective="Use your Rook on b2 to capture the pawn on e5 along the 2nd and 5th files!",
        expected_moves=["b2b5", "b2e2"],
        cm_intro=(
            "Time for the heavy artillery, {username}! Rooks control straight highways—ranks and files. "
            "Glide straight along files or ranks to dominate open lines. Advance your rook!"
        ),
        cm_success=(
            "Boom! Power play, {username}! Rooks love open files where no friendly pawns block their path. "
            "Connecting your two rooks on an open file is a classic winning technique."
        ),
        cm_hint="Slide your Rook straight up or across the board.",
        educational_note=(
            "Rooks are worth 5 points—more than minor pieces (Knights and Bishops, worth 3 points each). "
            "Keep files open for your rooks to maximize their attacking scope."
        ),
        hints=[
            "Rooks travel in straight cardinal directions.",
            "Look for an open highway to advance your rook.",
            "Slide the rook from b2 up to b5!",
        ],
        guided_move="b2b5",
        theory_detail="Rooks belong on open files (files with no pawns) or semi-open files.",
        feedback_correct="An active rook cuts off enemy territory and exerts immense pressure.",
        feedback_incorrect="Rooks cannot travel diagonally. Advance straight along ranks or files!",
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
        hints=[
            "The Queen can move diagonally like a bishop or straight like a rook.",
            "The black pawn on e5 sits on the same diagonal as b2.",
            "Take the pawn on e5 with your Queen!",
        ],
        guided_move="b2e5",
        theory_detail="Worth 9 points, the Queen is the strongest attacker on the board.",
        feedback_correct="The Queen sweeps across the board and claims central dominance.",
        feedback_incorrect="The queen can capture e5 directly along the diagonal. Select b2 and click e5!",
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
        hints=[
            "The King moves exactly one square in any direction.",
            "The pawn on e2 is undefended and directly adjacent to your King.",
            "Move e1 to e2 to capture the pawn!",
        ],
        guided_move="e1e2",
        theory_detail="In endgames, an active centralized King is equivalent to a minor piece in attacking and defending value.",
        feedback_correct="Capturing the pawn stops Black's promotion threat in its tracks.",
        feedback_incorrect="Take the threatening pawn right in front of your King: e1 to e2!",
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
        hints=[
            "Castling is initiated by moving the King two squares toward the corner.",
            "Select e1 and click g1.",
            "The h1 rook will automatically hop over to f1!",
        ],
        guided_move="e1g1",
        theory_detail="Castling achieves two goals simultaneously: protects the king behind a wall of pawns and activates the rook toward central files.",
        feedback_correct="Castling early prevents devastating tactical attacks down the open center.",
        feedback_incorrect="Castle by moving your King on e1 two squares right to g1!",
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
        hints=[
            "Observe the f7 square: guarded by the Bishop on c4 and attacked by the Queen on f3.",
            "Black has left the f7 vulnerability undefended.",
            "Play Queen to f7 to deliver immediate checkmate!",
        ],
        guided_move="f3f7",
        theory_detail="The f7 (and f2 for White) square is the weakest square on the board because only the king defends it initially.",
        feedback_correct="Checkmate! The Black King has no legal escape squares and the attacking Queen is guarded by the Bishop.",
        feedback_incorrect="Look for the killing checkmate on the f7 pawn with your queen!",
    ),

    # -------------------------------------------------------------------------
    # ORIGINAL FOUNDATION 2: INTERMEDIATE TACTICS
    # -------------------------------------------------------------------------
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
        hints=[
            "Notice Black's Rook on e2 sits directly between your e1 Rook and Black's King.",
            "Because moving the e2 Rook would put the King in check, it cannot legally move.",
            "Capture e2 with your e1 Rook!",
        ],
        guided_move="e1e2",
        theory_detail="Pinned pieces cannot protect other squares or escape attacks.",
        feedback_correct="The pinned piece was helpless, winning a whole rook!",
        feedback_incorrect="Take advantage of the pinned rook on e2: capture it with e1xe2!",
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
        hints=[
            "Look for a square where your Knight can simultaneously attack e8 and a8/h8.",
            "c7 attacks the King on e8 while threatening the Rook on a8 or h8.",
            "Jump the knight from d5 to c7!",
        ],
        guided_move="d5c7",
        theory_detail="Because the King must respond to check, the second attacked piece is won for free.",
        feedback_correct="Double attack! The King must flee, allowing White to pick up the rook.",
        feedback_incorrect="Look for a square that attacks both king on e8 and rook in the corner: Nc7!",
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
        hints=[
            "Observe the line of the 8th rank: King is on h8, your rook can deliver check on a8.",
            "When the King moves off the 8th rank, the h1 rook is exposed.",
            "Play Rook from a1 to a8!",
        ],
        guided_move="a1a8",
        theory_detail="Skewers exploit collinear targets where the front piece is too valuable to be sacrificed.",
        feedback_correct="The check forces Black's king aside, leaving the rear piece vulnerable.",
        feedback_incorrect="Deliver check along the 8th rank with your rook: Ra8+!",
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
        hints=[
            "Your Bishop on d4 blocks your Rook on d1 from checking the King on d8.",
            "Move the Bishop off the d-file.",
            "Step the Bishop to c5 to unmask the Rook's check!",
        ],
        guided_move="d4c5",
        theory_detail="Discovered attacks are devastating because the moving piece can threaten a second target while the masked piece delivers check.",
        feedback_correct="Discovered check unleashed! The Black King is under fire while the Bishop controls escape avenues.",
        feedback_incorrect="Move the bishop off the d-file to unmask your rook's check on the black king!",
    ),

    # -------------------------------------------------------------------------
    # ORIGINAL FOUNDATION 3: PRO STRATEGIES
    # -------------------------------------------------------------------------
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
        hints=[
            "The center squares are d4, e4, d5, and e5.",
            "Pushing the king pawn two squares immediately stakes a claim on d5 and f5.",
            "Push e2 to e4!",
        ],
        guided_move="e2e4",
        theory_detail="Controlling the center restricts opponent piece mobility while maximizing your own army's speed and coordination.",
        feedback_correct="1. e4 establishes ideal center control and activates lines for your queen and bishop.",
        feedback_incorrect="Stake your claim in the center: advance the e-pawn two squares to e4!",
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
        hints=[
            "The knight on e5 is stationed on an advanced square that cannot be kicked by enemy pawns.",
            "The pawn on f7 is vulnerable to attack.",
            "Capture f7 with your knight from e5!",
        ],
        guided_move="e5f7",
        theory_detail="Knights on outposts in enemy territory paralyze opponent coordination and generate tactical breakthroughs.",
        feedback_correct="The outpost knight strikes cleanly, winning material and shattering defenses.",
        feedback_incorrect="Strike the vulnerable f7 square using your dominant e5 knight!",
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
        hints=[
            "Direct opposition occurs when two kings face each other on the same file separated by 1 square.",
            "Step forward with your King.",
            "Move e5 to e6 to force Black's king to give ground!",
        ],
        guided_move="e5e6",
        theory_detail="Taking the opposition forces the opponent king to step aside, allowing your king to outflank and shepherd the passed pawn.",
        feedback_correct="Ke6 seizes the opposition! Black must yield, ensuring unstoppable pawn promotion.",
        feedback_incorrect="Step forward directly opposite the Black King: Ke6!",
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
        hints=[
            "Find an active checking square that drives the enemy king away from the defense.",
            "Slide horizontally across the 8th rank.",
            "Move b8 to g8 to deliver check!",
        ],
        guided_move="b8g8",
        theory_detail="Active rooks dictate the tempo of endgames. A single active rook easily outplays a passive defender.",
        feedback_correct="Rg8+ forces Black's king into the corner, securing a decisive winning advantage.",
        feedback_incorrect="Deliver check along the 8th rank with Rg8+ to cut off the Black King!",
    ),

    # -------------------------------------------------------------------------
    # 20 NEW COMPREHENSIVE CURRICULUM MODULES
    # -------------------------------------------------------------------------

    # --- CHESS FUNDAMENTALS ---
    Lesson(
        id="curr_coords",
        category="Chess Fundamentals",
        title="17. Understanding Board Coordinates",
        concept="Every square is uniquely designated by its file letter (a-h) and rank number (1-8).",
        fen="4k3/8/8/8/8/8/8/R3K2R w KQ - 0 1",
        player_color="White",
        objective="Centralize your queenside Rook by moving it from a1 to d1 along the first rank!",
        expected_moves=["a1d1"],
        cm_intro=(
            "Coordinates are the GPS of chess, {username}! "
            "Files run vertically from 'a' to 'h', and ranks run horizontally from '1' to '8'. "
            "Navigate your Rook on a1 to the central 'd1' square!"
        ),
        cm_success=(
            "Precision navigation, {username}! d1 is a vital central coordinate. "
            "Mastering algebraic notation allows you to read grandmaster games and communicate tactics effortlessly!"
        ),
        cm_hint="Slide the a1 rook horizontally along rank 1 to column d.",
        educational_note="Every square has an algebraic name: letter first for the file, then number for the rank.",
        hints=[
            "Files are letters a through h from left to right; ranks are numbers 1 through 8 from bottom to top.",
            "Locate the d-file and the 1st rank.",
            "Click on the a1 rook and move it to d1!",
        ],
        guided_move="a1d1",
        theory_detail="Algebraic notation was formalized in the 19th century and is the universal language of chess literature and digital engines.",
        feedback_correct="1. Rd1 successfully centralizes the rook on the primary central file.",
        feedback_incorrect="Navigate along rank 1 to the d-file: select the rook on a1 and click d1!",
    ),
    Lesson(
        id="curr_piece_moves",
        category="Chess Fundamentals",
        title="18. How Every Chess Piece Moves",
        concept="Centralized pieces control vastly more squares than pieces stuck on the edges of the board.",
        fen="4k3/8/8/8/8/5N2/8/4K3 w - - 0 1",
        player_color="White",
        objective="Centralize your Knight by hopping from f3 into the heart of the board on d4!",
        expected_moves=["f3d4"],
        cm_intro=(
            "Mobility is king, {username}! A piece's strength depends on how many squares it touches. "
            "On the edge, a knight is crippled; in the center, it commands 8 squares! "
            "Leap your f3 Knight straight into the central powerhouse on d4!"
        ),
        cm_success=(
            "Supreme mobility, {username}! From d4, your Knight radiates influence over 8 key squares. "
            "Centralization is the golden rule of piece activity!"
        ),
        cm_hint="Hop your knight from f3: two squares left and one square up to d4.",
        educational_note="A knight on the rim is dim! In the center, a knight attacks up to 8 squares; in the corner, only 2.",
        hints=[
            "Look for the central square d4.",
            "The knight on f3 can jump two squares left and one up.",
            "Move f3 to d4 to maximize piece influence!",
        ],
        guided_move="f3d4",
        theory_detail="Piece efficiency is measured by mobility: a centralized knight commands 8 squares, creating four times more tactical threats than a corner knight.",
        feedback_correct="Nd4 controls c6, e6, b5, f5, and covers both wings of the board.",
        feedback_incorrect="Jump your knight towards the center: two squares left and one up to d4!",
    ),
    Lesson(
        id="curr_piece_values",
        category="Chess Fundamentals",
        title="19. Chess Piece Values & Exchanges",
        concept="Pawn=1, Knight/Bishop=3, Rook=5, Queen=9. Never trade a higher-value piece for a lesser one!",
        fen="4k3/8/8/8/3r4/8/1Q6/4K3 w - - 0 1",
        player_color="White",
        objective="Black's Rook (5 pts) is completely undefended! Capture it with your Queen on b2!",
        expected_moves=["b2d4"],
        cm_intro=(
            "Let's talk economics, {username}! Knowing piece values prevents catastrophic trades. "
            "Rooks are worth 5 points—far more than minor pieces. "
            "Notice Black left their Rook on d4 unguarded. Cash in with your Queen!"
        ),
        cm_success=(
            "Profitable trade, {username}! You claimed a full Rook for free (+5 points). "
            "Always calculate the material balance before capturing!"
        ),
        cm_hint="Move your Queen on b2 along the rank/diagonal to capture the d4 rook.",
        educational_note="Material hierarchy: Pawn=1, Knight/Bishop=3, Rook=5, Queen=9. Trading a minor piece for a rook is winning the 'Exchange'.",
        hints=[
            "Inspect Black's pieces to spot undefended targets.",
            "The Rook on d4 has no friendly pieces protecting it.",
            "Capture d4 with your Queen from b2!",
        ],
        guided_move="b2d4",
        theory_detail="Material advantage is the most reliable path to victory. Even a single pawn lead can be converted into a decisive queen in the endgame.",
        feedback_correct="Qxd4 wins 5 full points of material with zero counterplay.",
        feedback_incorrect="Take the undefended rook! Move your Queen from b2 to capture on d4.",
    ),

    # --- OPENING PRINCIPLES ---
    Lesson(
        id="curr_center_control",
        category="Opening Principles",
        title="20. Controlling the Centre",
        concept="Opening with 1. d4 immediately controls the central e5 and c5 squares while freeing the queen's bishop.",
        fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
        player_color="White",
        objective="Play 1. d4! Advance your queen's pawn two squares to claim the central territory.",
        expected_moves=["d2d4"],
        cm_intro=(
            "Time to build a grandmaster opening repertoire, {username}! "
            "1. d4 is a cornerstone of world champions like Kasparov and Carlsen. "
            "Push your d-pawn two squares to d4 to seize central terrain!"
        ),
        cm_success=(
            "Majestic opening, {username}! 1. d4 controls e5 and c5 and is solidly protected by your Queen. "
            "Center dominance is the foundation of every winning strategy."
        ),
        cm_hint="Select the pawn in front of your Queen (d2) and push it forward two squares to d4.",
        educational_note="1. d4 leads to rich strategic battles where central control and piece maneuvering take precedence over wild tactical gambits.",
        hints=[
            "Find the queen's pawn on d2.",
            "Push it two squares forward into the center.",
            "Play d2 to d4!",
        ],
        guided_move="d2d4",
        theory_detail="Unlike 1. e4 which leaves the pawn undefended, 1. d4 is inherently protected by the white queen on d1 from the very first move.",
        feedback_correct="1. d4 takes direct control of e5 and c5, laying the groundwork for a classical Queens Gambit.",
        feedback_incorrect="Claim the center with your Queen's pawn: push d2 forward to d4!",
    ),
    Lesson(
        id="curr_piece_dev",
        category="Opening Principles",
        title="21. Developing Your Pieces",
        concept="Develop minor pieces towards the center before moving pawns or heavy artillery.",
        fen="rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2",
        player_color="White",
        objective="Develop your kingside Knight to f3, attacking Black's e5 pawn and preparing kingside castling!",
        expected_moves=["g1f3"],
        cm_intro=(
            "Don't move the same piece twice in the opening, {username}! "
            "Grandmasters prioritize developing minor pieces to active squares. "
            "Bring your Knight from g1 out to f3 to pressure e5 and clear the back rank!"
        ),
        cm_success=(
            "Flawless development, {username}! 2. Nf3 develops a piece with tempo by immediately attacking Black's e5 pawn. "
            "Developing with threats is the secret to seizing the initiative!"
        ),
        cm_hint="Hop your knight on g1 to f3.",
        educational_note="Developing with a threat forces the opponent to respond defensively rather than pursuing their own active plans.",
        hints=[
            "Observe the kingside knight sleeping on g1.",
            "Hop it forward and toward the center to attack e5.",
            "Move g1 to f3!",
        ],
        guided_move="g1f3",
        theory_detail="Nf3 accomplishes three key opening objectives: attacks e5, controls d4, and vacates the g1 square for kingside castling.",
        feedback_correct="2. Nf3 develops with tempo, creating immediate tactical pressure.",
        feedback_incorrect="Develop your kingside knight towards the center: move g1 to f3!",
    ),
    Lesson(
        id="curr_castling_safety",
        category="Opening Principles",
        title="22. Protecting Your King & Castling",
        concept="A king in the center is an easy target. Castle within the first 7-10 moves to ensure safety.",
        fen="rnbqk2r/pppp1ppp/5n2/2b1p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 4 4",
        player_color="White",
        objective="Castle kingside! Move your King from e1 to g1 to tuck it behind an impregnable wall of pawns.",
        expected_moves=["e1g1"],
        cm_intro=(
            "Never leave your King stranded in the center highway, {username}! "
            "Both your bishop and knight are developed. The runway is clear! "
            "Castle kingside to secure your King and activate your rook!"
        ),
        cm_success=(
            "Safety first, {username}! Your King is cozy behind the f2-g2-h2 pawn shield, and your Rook is ready to strike down the f and e files."
        ),
        cm_hint="Click your King on e1 and move it two squares right to g1.",
        educational_note="Many beginners lose games by launching premature attacks while leaving their own King stranded in the center.",
        hints=[
            "Both minor pieces between the king and h1 rook have been developed.",
            "Click on the King at e1 and select g1.",
            "Execute kingside castling!",
        ],
        guided_move="e1g1",
        theory_detail="Castling removes the king from the dangerous e-file where central pawn exchanges frequently open devastating lines of fire.",
        feedback_correct="Castling immediately secures king safety while activating the h1 rook.",
        feedback_incorrect="Tuck your King safely into the corner: move e1 to g1 to castle!",
    ),

    # --- TACTICAL SKILLS ---
    Lesson(
        id="curr_forks",
        category="Tactical Skills",
        title="23. Understanding Forks",
        concept="A fork occurs when one piece attacks two or more enemy pieces at the same time.",
        fen="r3k3/2q5/8/3N4/8/8/8/4K3 w - - 0 1",
        player_color="White",
        objective="Hop your Knight into c7 to deliver a devastating royal fork against the King on e8 and Queen on c7!",
        expected_moves=["d5c7"],
        cm_intro=(
            "Time for fireworks, {username}! A Royal Fork attacks both the enemy King and Queen. "
            "Because the King MUST get out of check, the Queen is doomed! "
            "Spring the trap: leap your Knight from d5 to c7!"
        ),
        cm_success=(
            "Check and mate for the Queen, {username}! Black must move the King, leaving their prized Queen ripe for harvest next turn. "
            "Knights are natural fork machines!"
        ),
        cm_hint="Hop your knight from d5 to c7.",
        educational_note="Because knights move in an L-shape and leap over pieces, knight forks cannot be blocked—the King must run or capture.",
        hints=[
            "Observe the c7 square: it is in jumping distance of d5 and attacks both e8 and the black queen.",
            "A check forces Black's king to respond immediately.",
            "Play Knight from d5 to c7!",
        ],
        guided_move="d5c7",
        theory_detail="A royal fork is the single most decisive minor piece tactic in chess, winning the queen by force.",
        feedback_correct="1. Nxc7+ checks the king while simultaneously attacking the queen. Unstoppable material gain!",
        feedback_incorrect="Fork the King and Queen together: leap your knight from d5 to c7!",
    ),
    Lesson(
        id="curr_pins",
        category="Tactical Skills",
        title="24. Understanding Pins",
        concept="A pinned piece cannot move without breaking the rules of chess. Strike the pinned target!",
        fen="4k3/4b3/8/8/8/8/8/4R1K1 w - - 0 1",
        player_color="White",
        objective="Black's Bishop on e7 is pinned to the King on e8! Capture it with your Rook on e1!",
        expected_moves=["e1e7"],
        cm_intro=(
            "Notice the paralysis, {username}! Black's Bishop on e7 sits directly in front of the Black King on e8. "
            "It CANNOT step aside because doing so would expose their King to check! "
            "Pounce on the frozen piece: take the Bishop on e7!"
        ),
        cm_success=(
            "Clinical execution, {username}! The pinned Bishop was completely paralyzed and could not escape or fight back. "
            "Always search for pinned pieces in your games!"
        ),
        cm_hint="Move your rook straight up the e-file to capture the e7 bishop.",
        educational_note="Remember: The pinned piece is not a real defender! It cannot move to protect other pieces.",
        hints=[
            "The Bishop on e7 is pinned along the e-file.",
            "It cannot capture anything or run away.",
            "Take the bishop: e1 captures e7!",
        ],
        guided_move="e1e7",
        theory_detail="Absolute pins are enforcers of passivity. Pinned defenders cannot fulfill any other tactical responsibilities.",
        feedback_correct="Rxe7+ captures the immobilized bishop with check.",
        feedback_incorrect="Attack the pinned piece along the e-file: e1 captures e7!",
    ),
    Lesson(
        id="curr_skewers",
        category="Tactical Skills",
        title="25. Understanding Skewers",
        concept="A skewer attacks a high-value piece in front, forcing it to dodge and exposing the piece behind it.",
        fen="k7/8/8/8/8/8/r7/R3K3 w - - 0 1",
        player_color="White",
        objective="Capture Black's Rook on a2 using your Rook on a1 to eliminate the dangerous counterplay!",
        expected_moves=["a1a2"],
        cm_intro=(
            "Skewers are often called 'reverse pins', {username}! "
            "When high-value enemy pieces line up along an open file, long-range pieces slice through them. "
            "Strike along the a-file and capture the a2 rook!"
        ),
        cm_success=(
            "Devastating accuracy, {username}! You claimed the rook cleanly. "
            "Skewers frequently decide endgames when rooks and kings line up on edges!"
        ),
        cm_hint="Capture the rook on a2 with your a1 rook.",
        educational_note="Skewers are most lethal when the King is attacked first: the King is forced to move, yielding whatever sits behind it.",
        hints=[
            "Both rooks are aligned on the a-file.",
            "Take Black's rook on a2 immediately.",
            "Play a1 captures a2!",
        ],
        guided_move="a1a2",
        theory_detail="Rooks and bishops dominate linear files and diagonals to skewer exposed opposing pieces.",
        feedback_correct="1. Rxa2 claims the full rook with zero complications.",
        feedback_incorrect="Capture Black's rook directly on a2 with your a1 rook!",
    ),
    Lesson(
        id="curr_discovered",
        category="Tactical Skills",
        title="26. Discovered Attacks",
        concept="Move one piece out of the way to uncover an ambush check from a heavy piece behind it.",
        fen="3k4/8/2q5/8/3B4/8/8/3R2K1 w - - 0 1",
        player_color="White",
        objective="Move your Bishop from d4 to b6 to uncover check from the d1 Rook while skewering the Queen!",
        expected_moves=["d4b6", "d4c5", "d4e5", "d4f6", "d4g7", "d4h8"],
        cm_intro=(
            "Get ready for an ambush, {username}! "
            "Your Rook on d1 is aiming straight at the Black King on d8, but your own Bishop on d4 blocks the view. "
            "Step your bishop to b6: it discovers check from the rook AND attacks Black's queen on c6!"
        ),
        cm_success=(
            "Tactical brilliance, {username}! Discovered checks are devastating because the moving piece can create a second threat "
            "while the uncovered piece delivers check. Black must answer the check, losing their Queen!"
        ),
        cm_hint="Move your bishop from d4 to b6 to uncover the rook check and spear the queen.",
        educational_note="In discovered checks, the opponent must respond to the check first, leaving the piece moved by you free to wreak havoc.",
        hints=[
            "Moving the bishop away uncovers the d1 rook's attack on the d8 king.",
            "Choose a square where the bishop also creates an attack, such as b6.",
            "Play Bishop to b6!",
        ],
        guided_move="d4b6",
        theory_detail="Discovered check gives you two moves in one: the check paralyzes the opponent while the unmasking piece captures or forks.",
        feedback_correct="Bxb6+ creates a double threat: the king must flee check, and the black queen is won on the next move.",
        feedback_incorrect="Move the bishop away from the d-file to unleash your rook's check!",
    ),

    # --- TACTICAL COMBINATIONS ---
    Lesson(
        id="curr_double_attack",
        category="Tactical Combinations",
        title="27. Double Attacks",
        concept="Create two simultaneous threats with one move. The opponent can only parry one, guaranteeing a win.",
        fen="4k3/1b6/8/8/8/8/8/3QK3 w - - 0 1",
        player_color="White",
        objective="Slide your Queen to a4 to deliver check to the King on e8 while attacking the undefended Bishop on b7!",
        expected_moves=["d1a4"],
        cm_intro=(
            "Double attacks overwhelm your opponent's defensive bandwidth, {username}! "
            "Notice Black's bishop on b7 is loose (undefended). "
            "Fly your Queen to a4: check the King on e8 and attack the bishop on b7 simultaneously!"
        ),
        cm_success=(
            "Masterclass, {username}! Black is forced to respond to check, allowing you to scoop up the b7 bishop next turn. "
            "Always search for loose pieces—they fall to double attacks!"
        ),
        cm_hint="Move your Queen from d1 diagonally to a4.",
        educational_note="GM John Nunn's famous rule: LPDO ('Loose Pieces Drop Off'). Always scan for undefended enemy pieces.",
        hints=[
            "Look for a square that attacks both the e8 king and the b7 bishop.",
            "The a4 square checks the king along the diagonal and eyes b7.",
            "Play Queen to a4!",
        ],
        guided_move="d1a4",
        theory_detail="Double attacks force the opponent into triage: the higher-priority threat must be answered, surrendering the secondary objective.",
        feedback_correct="1. Qa4+ checks the king and wins the loose b7 bishop on the following move.",
        feedback_incorrect="Find the checking square that simultaneously attacks the loose b7 bishop: Qa4+!",
    ),
    Lesson(
        id="curr_remove_defender",
        category="Tactical Combinations",
        title="28. Removing the Defender",
        concept="Identify which enemy piece protects a vital target, then eliminate or deflect that defender.",
        fen="4k3/8/5n2/8/4b3/5B2/8/4K3 w - - 0 1",
        player_color="White",
        objective="Black's Bishop on e4 is guarded by the f6 Knight. Capture the Bishop directly to trade down favorably!",
        expected_moves=["f3e4"],
        cm_intro=(
            "When an enemy target is defended, ask yourself: can I eliminate or remove the guard? "
            "Here, Black's e4 bishop is contested. Strike into e4 with your bishop to win material!"
        ),
        cm_success=(
            "Direct and clean, {username}! Eliminating contested defenders clarifies the position and leads to simplified winning endgames."
        ),
        cm_hint="Capture the e4 bishop with your f3 bishop.",
        educational_note="Removing the defender can be done by capturing the defender, chasing it away with a pawn, or deflecting it.",
        hints=[
            "The bishop on f3 can capture directly on e4.",
            "Take the enemy bishop.",
            "Play f3 captures e4!",
        ],
        guided_move="f3e4",
        theory_detail="Identifying key defenders is the basis of master-level tactical calculation.",
        feedback_correct="Bxe4 captures the active black bishop and neutralizes black's counterplay.",
        feedback_incorrect="Eliminate the contested piece: capture the bishop on e4 with Bxe4!",
    ),
    Lesson(
        id="curr_deflection",
        category="Tactical Combinations",
        title="29. Deflection Tactics",
        concept="Force an opponent's key piece away from the critical square or file it is guarding.",
        fen="3r2k1/5ppp/8/8/8/8/4QPPP/6K1 w - - 0 1",
        player_color="White",
        objective="Invade with your Queen to e7 to attack the defending rook and paralyze Black's back rank!",
        expected_moves=["e2e7"],
        cm_intro=(
            "Deflection forces a defender to abandon its post, {username}! "
            "Black's Rook on d8 is desperately holding the back rank together. "
            "Infiltrate with your Queen to e7 to attack the rook and dismantle their camp!"
        ),
        cm_success=(
            "Sensational infiltration, {username}! Queen on e7 paralyzes Black and threatens back rank devastation. "
            "Deflection turns strong defenses into ruins!"
        ),
        cm_hint="Advance your Queen from e2 forward to e7.",
        educational_note="Deflection tactics are common in attacking back-rank mate positions and tactical endgames.",
        hints=[
            "Invade deep into Black's camp along the e-file.",
            "The e7 square directly attacks the d8 rook and targets f7.",
            "Move Queen to e7!",
        ],
        guided_move="e2e7",
        theory_detail="Deflection exploits piece overload: when a single piece has too many defensive tasks, forcing it away breaks the dam.",
        feedback_correct="Qe7 penetrates the 7th rank, creating unstoppable mating threats.",
        feedback_incorrect="Invade on the 7th rank to deflect the black rook: play Qe7!",
    ),

    # --- DEFENSIVE SKILLS ---
    Lesson(
        id="curr_defend_piece",
        category="Defensive Skills",
        title="30. Defending Attacked Pieces",
        concept="When an opponent attacks your piece, don't panic! Defend, retreat, or counter-attack.",
        fen="4k3/8/8/8/4p3/5N2/8/4K3 w - - 0 1",
        player_color="White",
        objective="Black's e4 pawn is attacking your Knight on f3! Hop the Knight to safety on the central d4 square!",
        expected_moves=["f3d4"],
        cm_intro=(
            "Defense is an art, {username}! Good players know how to attack, but great champions know how to defend. "
            "Black's pawn on e4 has just attacked your f3 Knight. "
            "Jump your Knight to the safe, dominant central square on d4!"
        ),
        cm_success=(
            "Calm and collected, {username}! Instead of losing material, your Knight retreated to an even more commanding central square on d4. "
            "A retreat can often be an upgrade in piece placement!"
        ),
        cm_hint="Move your knight from f3 to the safe d4 square.",
        educational_note="When a piece is attacked, evaluate the three responses: Retreat, Protect, or Counter-attack.",
        hints=[
            "The knight on f3 is threatened by the e4 pawn.",
            "Look for a safe central square that is not attacked.",
            "Move the Knight from f3 to d4!",
        ],
        guided_move="f3d4",
        theory_detail="Defensive retreats to active central squares neutralize enemy initiative while preserving material balance.",
        feedback_correct="Nd4 escapes the pawn fork and cements a dominant central blockader.",
        feedback_incorrect="Escape the pawn attack by jumping your knight to the safe d4 center square!",
    ),
    Lesson(
        id="curr_escape_attack",
        category="Defensive Skills",
        title="31. Escaping Attacks and Finding Safe Squares",
        concept="Identify which squares are covered by the enemy and steer your high-value pieces to absolute safety.",
        fen="3r4/4k3/8/8/3Q4/8/8/4K3 w - - 0 1",
        player_color="White",
        objective="Black's Rook on d8 attacks your Queen on d4! Escape with check by moving the Queen to e5!",
        expected_moves=["d4e5"],
        cm_intro=(
            "Under fire, {username}! Black's Rook on d8 is skewering your Queen down the d-file. "
            "Queens must never be surrendered lightly! "
            "Evacuate your Queen to e5: escape the attack AND deliver a powerful check to the Black King!"
        ),
        cm_success=(
            "Brilliant tactical defense, {username}! You escaped the rook's crosshairs and countered with check. "
            "Escaping with tempo is the ultimate defensive counterpunch!"
        ),
        cm_hint="Move your Queen from d4 to e5 with check.",
        educational_note="When fleeing an attack, always look for squares that deliver check or create an even stronger counter-threat.",
        hints=[
            "The d-file is contested by the d8 rook.",
            "Step off the d-file to e5.",
            "Move Queen to e5 with check!",
        ],
        guided_move="d4e5",
        theory_detail="Escaping with check gains a critical tempo, allowing you to reposition your forces before the opponent can consolidate.",
        feedback_correct="1. Qe5+ escapes the rook's attack while delivering check to the enemy king.",
        feedback_incorrect="Escape with check! Step the Queen to e5 where it cannot be captured.",
    ),
    Lesson(
        id="curr_counter_threat",
        category="Defensive Skills",
        title="32. Recognising and Responding to Threats",
        concept="Preventing back-rank mate: Step your King to f1 to eliminate back-rank vulnerabilities.",
        fen="6k1/5ppp/8/8/8/8/4rPPP/6K1 w - - 0 1",
        player_color="White",
        objective="Black's Rook threatens back rank mate! Move your King from g1 to f1 to attack the rook and escape danger!",
        expected_moves=["g1f1"],
        cm_intro=(
            "Danger alert, {username}! Black's Rook on e2 is menacing. "
            "Recognize the threat: step your King boldly to f1! "
            "This defends against back-rank mate AND attacks the intruding rook!"
        ),
        cm_success=(
            "Iron defense, {username}! By stepping to f1, your King neutralizes the checkmate threat and drives Black's rook backwards. "
            "Active kings in the endgame are ferocious defenders!"
        ),
        cm_hint="Step your king from g1 to f1 to confront the rook.",
        educational_note="In endgames, an active King should walk towards threats rather than retreating to passive corner squares.",
        hints=[
            "Black's rook is invading on e2.",
            "Step your King forward to f1.",
            "Play King from g1 to f1!",
        ],
        guided_move="g1f1",
        theory_detail="Proactive king activation in endgames turns potential defensive liabilities into active piece hunters.",
        feedback_correct="1. Kf1 steps out of any back rank traps while threatening to capture Black's rook.",
        feedback_incorrect="Step your King forward to f1 to neutralize the back-rank threat!",
    ),

    # --- ENDGAMES ---
    Lesson(
        id="curr_kp_endgame",
        category="Endgames",
        title="33. Basic King and Pawn Endgames",
        concept="The player whose King forces the other to yield holds the opposition and can escort pawns to promotion.",
        fen="8/8/4k3/8/4P3/8/4K3/8 w - - 0 1",
        player_color="White",
        objective="Step forward with your King from e2 to e3 to seize the opposition and support your passed pawn!",
        expected_moves=["e2e3"],
        cm_intro=(
            "Welcome to the purest stage of chess, {username}: The King & Pawn endgame! "
            "With few pieces on the board, precision is life or death. "
            "Move your King to e3: seize the direct opposition and prepare to escort your pawn to glory!"
        ),
        cm_success=(
            "Textbook grandmaster technique, {username}! Ke3 seizes the opposition. "
            "From here, your King leads the way, paving an unstoppable highway to the 8th rank!"
        ),
        cm_hint="Step your King from e2 up to e3.",
        educational_note="King in front of the pawn: In king and pawn endgames, placing your King ahead of your pawn is the fundamental winning rule.",
        hints=[
            "Keep your king in close coordination with your passed pawn.",
            "Step forward into e3.",
            "Move King to e3!",
        ],
        guided_move="e2e3",
        theory_detail="Without piece clutter, king placement determines the outcome of the entire game. The king must act as the blocker and escort.",
        feedback_correct="1. Ke3 takes the opposition, ensuring the pawn cannot be blockaded.",
        feedback_incorrect="Take the opposition! Advance your King to e3 directly supporting the e4 pawn.",
    ),
    Lesson(
        id="curr_pawn_promotion",
        category="Endgames",
        title="34. Understanding Pawn Promotion",
        concept="A pawn that reaches the opposite end of the board (8th rank for White) promotes to any piece, usually a Queen!",
        fen="8/4P1k1/8/8/8/8/8/4K3 w - - 0 1",
        player_color="White",
        objective="Push your e7 pawn to e8 and promote it to a Queen to deliver a winning blow!",
        expected_moves=["e7e8q", "e7e8r"],
        cm_intro=(
            "The crowning moment, {username}! "
            "Every humble pawn dreams of marching across the board to be crowned Queen. "
            "Push your e7 pawn straight to e8 and claim your Queen!"
        ),
        cm_success=(
            "QUEEN DELIVERED! Victory is at hand, {username}! "
            "A promoted Queen completely transforms the board and guarantees a swift checkmate. "
            "Passed pawns must be pushed!"
        ),
        cm_hint="Push the pawn on e7 forward to e8 and choose Queen.",
        educational_note="Pawn promotion: When a pawn reaches the 8th rank, it immediately transforms into a Queen, Rook, Bishop, or Knight. You do not need a captured piece to promote!",
        hints=[
            "The pawn on e7 is only one step away from the final rank.",
            "Move it from e7 to e8.",
            "Promote to a Queen!",
        ],
        guided_move="e7e8q",
        theory_detail="Pawn promotion is the ultimate prize in chess. Creating and pushing passed pawns is the central theme of grandmaster endgame play.",
        feedback_correct="1. e8=Q+ promotes with check, concluding the endgame with decisive material advantage.",
        feedback_incorrect="Push the pawn all the way to the 8th rank: e7 to e8 to promote!",
    ),

    # --- ADVANCED BEGINNER ---
    Lesson(
        id="curr_backrank_mate",
        category="Advanced Beginner",
        title="35. Common Checkmate Patterns",
        concept="When an enemy King is trapped behind its own pawns, a rook or queen on the back rank delivers mate!",
        fen="6k1/5ppp/8/8/8/8/8/R3K3 w - - 0 1",
        player_color="White",
        objective="Deliver the classic Back-Rank Checkmate! Slide your Rook from a1 to a8!",
        expected_moves=["a1a8"],
        cm_intro=(
            "Behold the most famous checkmate pattern in chess history, {username}: The Back-Rank Mate! "
            "Notice Black's King is imprisoned behind its own f7-g7-h7 pawns. "
            "Fire your Rook from a1 all the way to a8 to deliver instant checkmate!"
        ),
        cm_success=(
            "CHECKMATE! Down goes the King, {username}! "
            "Because Black's pawns blocked the escape squares, your solitary Rook was enough to end the game. "
            "Always give your King a flight square ('luft') to prevent this!"
        ),
        cm_hint="Slide your Rook all the way from a1 up to a8.",
        educational_note="Luft (German for 'air'): Pushing a pawn (like h3 or g3) creates a breathing hole so your King cannot be back-rank mated.",
        hints=[
            "Black's King on g8 has nowhere to step forward due to its own pawns.",
            "The 8th rank is wide open for an invasion.",
            "Move Rook from a1 all the way to a8!",
        ],
        guided_move="a1a8",
        theory_detail="Back-rank checkmates occur when the defending king is trapped by its own unmoved pawns, leaving no escape along the back rank.",
        feedback_correct="1. Ra8# is pure checkmate. The black king cannot escape its own defensive wall.",
        feedback_incorrect="Deliver checkmate along the back rank: slide the rook from a1 to a8!",
    ),
    Lesson(
        id="curr_calculation",
        category="Advanced Beginner",
        title="36. Basic Calculation & Planning",
        concept="Calculate move by move: Checks, Captures, and Threats lead to forced victories.",
        fen="r1bqk2r/pppp1ppp/2n5/4p3/2B1n3/5Q2/PPPP1PPP/RNB1K1NR w KQkq - 0 1",
        player_color="White",
        objective="Calculate the killing blow! Queen takes f7 delivering Scholar's Checkmate!",
        expected_moves=["f3f7"],
        cm_intro=(
            "The final exam, {username}! Calculation means visualizing moves before playing them. "
            "Look at checks, captures, and threats. "
            "Your Bishop on c4 and Queen on f3 team up against f7. Execute the forced checkmate!"
        ),
        cm_success=(
            "MAGNIFICENT CHECKMATE, {username}! You calculated the forcing sequence and delivered the final blow! "
            "You have conquered the 36-lesson JD Chess Grandmaster Curriculum. The board is yours!"
        ),
        cm_hint="Strike f7 with your Queen to deliver checkmate.",
        educational_note="Always calculate using C-C-T: 1. Checks, 2. Captures, 3. Threats. Forcing moves are the heart of tactical calculation.",
        hints=[
            "Scan for the most forcing move on the board.",
            "f7 is defended only by the Black King and attacked twice by you.",
            "Queen takes f7 delivers checkmate!",
        ],
        guided_move="f3f7",
        theory_detail="Calculation is chess's superpower. Forcing moves (checks and captures) drastically reduce opponent choices, making victory predictable.",
        feedback_correct="Qxf7# delivers unstoppable checkmate. The complete curriculum has been mastered!",
        feedback_incorrect="Find the most forcing checkmate on f7 with your queen: Qxf7#",
    ),
]


def get_curriculum() -> list[Lesson]:
    """Return all available lessons in the structured curriculum."""
    return list(CURRICULUM)


def get_lesson_by_id(lesson_id: str) -> Lesson | None:
    """Find a specific lesson by its unique string ID."""
    for lesson in CURRICULUM:
        if lesson.id == lesson_id:
            return lesson
    return None


def get_next_lesson(current_id: str) -> Lesson | None:
    """Retrieve the lesson following current_id in the progression path."""
    for i, lesson in enumerate(CURRICULUM):
        if lesson.id == current_id and i + 1 < len(CURRICULUM):
            return CURRICULUM[i + 1]
    return None


def get_prev_lesson(current_id: str) -> Lesson | None:
    """Retrieve the lesson preceding current_id in the progression path."""
    for i, lesson in enumerate(CURRICULUM):
        if lesson.id == current_id and i > 0:
            return CURRICULUM[i - 1]
    return None
