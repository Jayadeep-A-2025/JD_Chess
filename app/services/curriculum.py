from __future__ import annotations

"""JD Chess Learning Academy — Complete Progressive 7-Level Curriculum.

Structured chess curriculum transforming players from absolute beginner to
advanced competitive level across 7 comprehensive tiers:
  Level 1: Beginner Foundations (Lessons 1 - 6)
  Level 2: Chess Tactics (Lessons 7 - 12)
  Level 3: Opening Mastery (Lessons 13 - 18)
  Level 4: Middlegame Strategy (Lessons 19 - 24)
  Level 5: Advanced Calculation (Lessons 25 - 30)
  Level 6: Endgame Mastery (Lessons 31 - 36)
  Level 7: Competitive Chess (Lessons 37 - 42)

Every lesson is fully interactive with Concept, Guided Practice with Progressive Hints,
Interactive Challenge, Threat Detection, Why Mistakes Fail, Real Master Game Application,
and Conceptual Assessment Quizzes.
"""

from dataclasses import dataclass, field
from typing import Any, List


@dataclass
class Lesson:
    """Represents an interactive chess lesson taught by companion CM."""

    id: str
    category: str         # Subcategory / Category title for navigation and test compatibility
    title: str
    concept: str
    fen: str
    player_color: str     # "White" | "Black"
    objective: str
    expected_moves: list[str]  # UCI moves accepted as correct solutions
    cm_intro: str         # CM greeting and challenge description
    cm_success: str       # CM congratulatory feedback
    cm_hint: str          # CM quick hint
    educational_note: str # Grandmaster theory note
    # Academy progressive learning enhancements
    level_number: int = 1                                # 1 to 7
    level_name: str = "Beginner Foundations"             # Level title
    difficulty: str = "Beginner"                         # "Beginner" | "Intermediate" | "Advanced"
    topic: str = "fundamentals"                          # Topic tag for weakness tracking
    opponent_threat: str = ""                            # What is the opponent threatening?
    hints: list[str] = field(default_factory=list)       # Progressive 3-tier hints
    guided_move: str = ""                                # Primary demonstration move (UCI)
    theory_detail: str = ""                              # In-depth tactical / strategic theory
    feedback_correct: str = ""                           # Why the solution succeeds strategically
    feedback_incorrect: str = ""                         # Guidance when an alternative move is played
    why_mistakes_fail: dict[str, str] = field(default_factory=dict)  # Move-specific failure explanations
    real_application: str = ""                           # Historical master game or tournament context
    assessment_question: str = ""                        # Conceptual assessment check
    assessment_options: list[str] = field(default_factory=list)      # Multiple choice options
    assessment_answer_index: int = 0                     # Correct option index (0-based)
    assessment_explanation: str = ""                     # Explanation of the assessment answer


# =============================================================================
# ACADEMY LEVELS METADATA
# =============================================================================

ACADEMY_LEVELS = [
    {
        "level_number": 1,
        "name": "Beginner Foundations",
        "description": "Board coordinates, piece movement rules, king safety, captures, check, and checkmate.",
        "difficulty": "Beginner",
        "icon": "🌱",
    },
    {
        "level_number": 2,
        "name": "Chess Tactics",
        "description": "Forks, pins, skewers, discovered attacks, deflections, and removing defenders.",
        "difficulty": "Intermediate",
        "icon": "⚡",
    },
    {
        "level_number": 3,
        "name": "Opening Mastery",
        "description": "Center control, rapid minor piece development, king shelter, and common opening traps.",
        "difficulty": "Beginner",
        "icon": "🏰",
    },
    {
        "level_number": 4,
        "name": "Middlegame Strategy",
        "description": "Knight outposts, pawn structures, open files, good vs bad bishops, and seizing initiative.",
        "difficulty": "Intermediate",
        "icon": "⚔️",
    },
    {
        "level_number": 5,
        "name": "Advanced Calculation",
        "description": "Checks, captures, threats (C-C-T), candidate moves, clearance sacrifices, and desperado.",
        "difficulty": "Advanced",
        "icon": "🧠",
    },
    {
        "level_number": 6,
        "name": "Endgame Mastery",
        "description": "Direct opposition, passed pawns, the Lucena bridge, Philidor defense, and zugzwang.",
        "difficulty": "Intermediate",
        "icon": "👑",
    },
    {
        "level_number": 7,
        "name": "Competitive Chess",
        "description": "Positional sacrifices, punishing mistakes, tournament prophylaxis, and converting wins.",
        "difficulty": "Advanced",
        "icon": "🏆",
    },
]


# =============================================================================
# CURRICULUM DEFINITION (42 Comprehensive Academy Lessons Across 7 Levels)
# =============================================================================

CURRICULUM: list[Lesson] = [
    # -------------------------------------------------------------------------
    # LEVEL 1: BEGINNER FOUNDATIONS (Lessons 1 - 6)
    # -------------------------------------------------------------------------
    Lesson(
        id="beginner_pawn",
        category="Beginner Basics",
        level_number=1,
        level_name="Beginner Foundations",
        difficulty="Beginner",
        topic="pawn_mechanics",
        title="1. Pawn Mechanics: Center Advance & Two-Square Leap",
        concept="Pawns move forward one square, but on their very first move, they may leap forward two squares. Pawns capture diagonally.",
        fen="4k3/8/8/8/8/8/4P3/4K3 w - - 0 1",
        player_color="White",
        objective="Advance your e2 pawn two squares forward to e4 to stake your claim on the center!",
        expected_moves=["e2e4"],
        guided_move="e2e4",
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
            "Locate your pawn standing on square e2.",
            "Pawns on their starting rank can advance either 1 or 2 squares forward.",
            "Click e2 and push the pawn forward two squares to e4!",
        ],
        theory_detail="Central pawn advances directly contest d5 and f5, creating space to develop your Knights and Bishops.",
        feedback_correct="1. e4 seizes central space and opens lines for both your Queen and Light-Squared Bishop.",
        feedback_incorrect="Push your pawn forward two squares to e4: e2e4!",
        opponent_threat="Without a white central pawn advance, Black will play e5 and claim undisputed central dominance.",
        why_mistakes_fail={"e2e3": "e2e3 is too passive; advancing two squares to e4 claims far more central space."},
        real_application="1. e4 is the most popular opening move in chess history, championed by World Champions Bobby Fischer and Garry Kasparov.",
        assessment_question="On its initial starting square, how many squares forward can a pawn legally move?",
        assessment_options=["Only 1 square", "1 or 2 squares forward", "Diagonally forward 2 squares", "Any number of squares"],
        assessment_answer_index=1,
        assessment_explanation="Pawns on their original home rank have the special option to advance either 1 or 2 squares forward.",
    ),
    Lesson(
        id="curr_coords",
        category="Chess Fundamentals",
        level_number=1,
        level_name="Beginner Foundations",
        difficulty="Beginner",
        topic="coordinates",
        title="2. Board Coordinates & Square Vision",
        concept="The chessboard is an 8x8 grid. Files are vertical columns (a-h); ranks are horizontal rows (1-8).",
        fen="4k3/8/8/8/8/8/8/R3K3 w - - 0 1",
        player_color="White",
        objective="Centralize your Rook by sliding along rank 1 from a1 over to the central d-file on d1!",
        expected_moves=["a1d1"],
        guided_move="a1d1",
        cm_intro=(
            "Welcome to board vision, {username}! Every square has an address: a letter for the column (file a to h) "
            "and a number for the row (rank 1 to 8). Slide your Rook from a1 over to the d-file on d1!"
        ),
        cm_success=(
            "Excellent navigation, {username}! You moved to d1. "
            "Files and ranks are the universal coordinate system of every grandmaster."
        ),
        cm_hint="Click on the Rook at a1 and slide horizontally to the d1 square.",
        educational_note="Files are vertical lines lettered a to h from White's left to right. Ranks are horizontal lines numbered 1 to 8.",
        hints=[
            "Files are letters a through h from left to right; ranks are numbers 1 through 8 from bottom to top.",
            "Locate the d-file on the 1st rank.",
            "Click on the a1 rook and move it horizontally to d1!",
        ],
        theory_detail="Rooks thrive on central open files. Placing a rook on d1 exerts immediate central influence.",
        feedback_correct="1. Rd1 centralizes the heavy piece on the d-file, demonstrating precise board coordinate navigation.",
        feedback_incorrect="Slide along rank 1 to the d-file: select the rook on a1 and click d1!",
        opponent_threat="Without central piece coordination, the opponent King will march unchecked into the center.",
        why_mistakes_fail={"a1b1": "b1 is on the flank; d1 commands the central Queen-file."},
        real_application="Grandmasters memorize board coordinates so thoroughly that they can play entire games blindfolded without seeing the board.",
        assessment_question="Which file on the chessboard is the central 'Queen file'?",
        assessment_options=["The e-file", "The d-file", "The c-file", "The f-file"],
        assessment_answer_index=1,
        assessment_explanation="The d-file is the central Queen file, while the e-file is the central King file.",
    ),
    Lesson(
        id="curr_piece_moves",
        category="Chess Fundamentals",
        level_number=1,
        level_name="Beginner Foundations",
        difficulty="Beginner",
        topic="piece_movement",
        title="3. Piece Navigation: The Knight's Central Jump",
        concept="Knights move in an L-shape (2 squares one way, 1 square perpendicular). They can leap directly over any intervening piece.",
        fen="4k3/8/8/8/8/5N2/8/4K3 w - - 0 1",
        player_color="White",
        objective="Centralize your Knight by hopping from f3 into the heart of the board on d4!",
        expected_moves=["f3d4"],
        guided_move="f3d4",
        cm_intro=(
            "Mobility is king, {username}! A piece's strength depends on how many squares it touches. "
            "On the edge, a knight is crippled; in the center, it commands 8 squares! "
            "Hop your knight from f3 into the central outpost on d4!"
        ),
        cm_success=(
            "Dominant leap, {username}! From d4, your Knight radiates power in all directions, controlling 8 critical squares!"
        ),
        cm_hint="Hop the knight from f3 to d4 (two squares left, one square up).",
        educational_note="Centralized knights control up to 8 squares. A knight placed on the rim or corner controls only 2 to 4 squares.",
        hints=[
            "Count two squares left from f3 (to d3) and one square up to d4.",
            "d4 is one of the four golden central squares.",
            "Select the f3 knight and leap to d4!",
        ],
        theory_detail="The Knight is the only piece on the board whose movement cannot be obstructed by intervening pieces.",
        feedback_correct="1. Nd4 places the knight on an active central square commanding 8 distinct destination squares.",
        feedback_incorrect="Hop your knight from f3 into the center: Nd4!",
        opponent_threat="A passive knight placed on the rim (h4) controls only 4 squares and cannot influence central play.",
        why_mistakes_fail={"f3h4": "A knight on the rim is dim! On h4 the knight controls only 4 squares instead of 8 in the center."},
        real_application="Siegbert Tarrasch coined the famous chess proverb: 'A knight on the rim is grim' to emphasize central knight placement.",
        assessment_question="How many squares does a centrally placed knight on d4 or e4 attack?",
        assessment_options=["4 squares", "6 squares", "8 squares", "10 squares"],
        assessment_answer_index=2,
        assessment_explanation="A centrally placed knight commands its maximum possible radius of 8 distinct destination squares.",
    ),
    Lesson(
        id="beginner_king",
        category="Beginner Basics",
        level_number=1,
        level_name="Beginner Foundations",
        difficulty="Beginner",
        topic="king_safety",
        title="4. King Safety: Castling Kingside",
        concept="Castling is a dual move that shields your King behind a wall of pawns while activating your Rook toward the center.",
        fen="r1bqk2r/pppp1ppp/2n2n2/4p3/1bB1P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 4 4",
        player_color="White",
        objective="Tuck your King safely into the corner and activate your Rook by castling kingside (O-O)!",
        expected_moves=["e1g1"],
        guided_move="e1g1",
        cm_intro=(
            "Protect the crown, {username}! An uncastled King in the center is an easy target for enemy attacks. "
            "Castle kingside: your King leaps two squares to g1, and your Rook jumps over to f1. Make the move!"
        ),
        cm_success=(
            "Safety first, {username}! Your King is safely sheltered behind the f2, g2, and h2 pawns, and your Rook is mobilized!"
        ),
        cm_hint="Click your King on e1 and move it two squares to the right to g1.",
        educational_note=(
            "Castling requires that neither the King nor the Rook has moved, no pieces stand between them, "
            "and the King does not castle out of, through, or into check."
        ),
        hints=[
            "Castling is executed by moving the King two squares toward the Rook.",
            "The King moves from e1 to g1.",
            "Click on e1, then click g1 to castle kingside!",
        ],
        theory_detail="Early castling within the first 7-10 moves drastically reduces tactical vulnerabilities down the central e-file.",
        feedback_correct="1. O-O safely secures the King and connects the rooks for rapid middlegame coordination.",
        feedback_incorrect="Move the King two squares to the right to castle kingside: e1 to g1!",
        opponent_threat="Black's Bishop on b4 and Knight on f6 are preparing central attacks against an uncastled King.",
        why_mistakes_fail={"d1e2": "Qe2 blocks the King's escape and delays king safety while the e-file is opening up."},
        real_application="Castling in the opening reduces King vulnerability by over 80% in competitive master play.",
        assessment_question="Can you castle if your King is currently in check?",
        assessment_options=["Yes, anytime", "No, you cannot castle out of check", "Only if castling queenside", "Only with Queen permission"],
        assessment_answer_index=1,
        assessment_explanation="By FIDE rules, you cannot castle while your King is in check, nor through a square attacked by enemy pieces.",
    ),
    Lesson(
        id="beginner_captures",
        category="Beginner Basics",
        level_number=1,
        level_name="Beginner Foundations",
        difficulty="Beginner",
        topic="captures",
        title="5. Capturing & Defending Material",
        concept="Captures occur when a piece lands on an opponent's square. Always count attackers versus defenders before capturing.",
        fen="r1bqkbnr/pppp1ppp/2n5/4p3/3P4/5N2/PPP1PPPP/RNBQKB1R w KQkq - 2 3",
        player_color="White",
        objective="Capture Black's undefended or weakly defended e5 pawn using your d4 central pawn!",
        expected_moves=["d4e5", "f3e5"],
        guided_move="d4e5",
        cm_intro=(
            "Time to strike, {username}! Look at Black's e5 pawn: it is under pressure from both your d4 pawn and f3 knight. "
            "Capture the pawn on e5 with your d4 pawn to win central material!"
        ),
        cm_success=(
            "Clean capture, {username}! You claimed Black's central pawn and opened up lines for your pieces!"
        ),
        cm_hint="Click on your pawn at d4 and capture Black's pawn on e5 diagonally.",
        educational_note="Before capturing, count the number of attackers and defenders. If you have more attackers, the trade is in your favor.",
        hints=[
            "White has two attackers on e5: the d4 pawn and the f3 knight.",
            "Pawns capture diagonally one square forward.",
            "Take the e5 pawn using d4: dxe5!",
        ],
        theory_detail="Pawn exchanges in the center dictate which files open up for heavy piece penetration.",
        feedback_correct="1. dxe5 cleanly captures central material and breaks Black's central presence.",
        feedback_incorrect="Take Black's pawn on e5 with your pawn or knight: d4xe5 or f3xe5!",
        opponent_threat="If White does not resolve the tension, Black could play exd4 or push e4, disrupting White's knight.",
        why_mistakes_fail={"f1c4": "Ignoring the tension allows Black to capture exd4 or push e4, kicking White's knight away."},
        real_application="Counting attackers vs defenders is the fundamental arithmetic underlying all tactical calculation in chess.",
        assessment_question="If an opponent piece is attacked by 2 of your pieces and defended by only 1 enemy piece, who wins the exchange?",
        assessment_options=["The defender wins", "You win material (net +1 piece)", "It is an equal trade", "No captures can happen"],
        assessment_answer_index=1,
        assessment_explanation="When you have more attackers than the opponent has defenders, you win net material after all captures conclude.",
    ),
    Lesson(
        id="rules_check_checkmate",
        category="Advanced Beginner",
        level_number=1,
        level_name="Beginner Foundations",
        difficulty="Beginner",
        topic="checkmate",
        title="6. Check vs Checkmate: Scholar's Mating Net",
        concept="Check attacks the King. Checkmate is check with no escape: you cannot Capture the attacker, Protect (block), or Run away (CPR).",
        fen="r1bqkb1r/pppp1ppp/2n5/4p3/2B1n3/5Q2/PPPP1PPP/RNB1K1NR w KQkq - 0 1",
        player_color="White",
        objective="Deliver unstoppable checkmate! Strike Black's weak f7 square with your Queen supported by the c4 Bishop!",
        expected_moves=["f3f7"],
        guided_move="f3f7",
        cm_intro=(
            "The ultimate goal of chess, {username}! The game ends not by capturing the King, but by trapping him with Checkmate! "
            "Notice Black's f7 pawn: only the Black King defends it. Your Queen on f3 and Bishop on c4 form a deadly battery. "
            "Deliver the Scholar's Checkmate with Qxf7#!"
        ),
        cm_success=(
            "CHECKMATE, {username}! That is game over! The Black King cannot capture your Queen because your Bishop on c4 protects her. "
            "The King cannot run, and no piece can block. Outstanding!"
        ),
        cm_hint="Click your Queen on f3 and capture the f7 pawn directly next to the Black King.",
        educational_note=(
            "The CPR mnemonic helps in check: C = Capture the checking piece, P = Protect (block) the line of check, "
            "R = Run away with the King. When none of the three works, it is Checkmate."
        ),
        hints=[
            "Look for a move that delivers check to the Black King.",
            "f7 is defended only by Black's King and attacked twice by you.",
            "Move your Queen from f3 and capture on f7!",
        ],
        theory_detail="f7 is the weakest square in Black's starting position because only the King defends it.",
        feedback_correct="Qxf7# delivers Scholar's Mate. The Queen is protected by the Bishop, giving Black no legal response.",
        feedback_incorrect="Strike f7 with your Queen to deliver instant checkmate: Qxf7#",
        opponent_threat="Black's Knight on e4 attacks White's Queen on f3; ignoring it without delivering mate would lose the Queen.",
        why_mistakes_fail={"f3e4": "Qxe4 captures a knight but lets the enemy King escape; Qxf7# ends the game instantly on the spot!"},
        real_application="The weak f7 (and f2) square is the target of numerous classical mating patterns, including Scholar's Mate and Fried Liver Attack.",
        assessment_question="What are the three fundamental ways to escape a check (CPR)?",
        assessment_options=["Castle, Pass, Resign", "Capture the checking piece, Protect (block) the check, Run away with the King", "Call arbiter, Pause clock, Reset", "Sacrifice a pawn, Trade queens, Move rook"],
        assessment_answer_index=1,
        assessment_explanation="The three legal responses to check are CPR: Capture the attacking piece, Protect by blocking the check line, or Run away with the King.",
    ),

    # -------------------------------------------------------------------------
    # LEVEL 2: CHESS TACTICS (Lessons 7 - 12)
    # -------------------------------------------------------------------------
    Lesson(
        id="tactics_fork",
        category="Intermediate Tactics",
        level_number=2,
        level_name="Chess Tactics",
        difficulty="Intermediate",
        topic="forks",
        title="7. The Royal Knight Fork: Double Attack",
        concept="A fork attacks two or more enemy targets at the same time with a single piece. The opponent can only save one piece.",
        fen="r3k2r/ppp2ppp/8/3N4/8/8/PPPP1PPP/R3K2R w KQkq - 0 1",
        player_color="White",
        objective="Jump your Knight to c7 to deliver check to the King while simultaneously attacking the undefended Rook on a8!",
        expected_moves=["d5c7"],
        guided_move="d5c7",
        cm_intro=(
            "Welcome to the tactical arena, {username}! A fork is one of the most deadly weapons in chess. "
            "Your Knight on d5 can jump to c7, attacking BOTH the Black King on e8 and the Rook on a8 at once! "
            "Execute the fork!"
        ),
        cm_success=(
            "Brutal fork, {username}! Black must respond to check by moving the King, leaving the corner Rook ripe for the taking!"
        ),
        cm_hint="Hop your knight from d5 into c7 to attack both the King and the corner Rook.",
        educational_note=(
            "Every piece can deliver a fork, but Knights are notorious for forks because they jump over obstacles and "
            "attack heavy pieces without entering their line of fire."
        ),
        hints=[
            "Find a square where your Knight attacks both e8 and a8 at once.",
            "c7 is in range of both the enemy King and the corner Rook.",
            "Jump the knight from d5 to c7!",
        ],
        theory_detail="Because the King must respond to check, the second attacked piece is won for free with zero compensation.",
        feedback_correct="1. Nc7+ forks King and Rook. The King must step aside, allowing White to capture the a8 Rook.",
        feedback_incorrect="Jump your knight to c7 to fork the King and Rook: Nc7+!",
        opponent_threat="If White hesitates, Black will castle kingside or play 0-0-0, removing their King from the fork danger zone.",
        why_mistakes_fail={"d5e3": "Passive retreat forfeits the decisive fork Nc7+ which wins a full rook."},
        real_application="Knight forks are the single most frequent tactical blunder at amateur and club level chess.",
        assessment_question="Why are Knights particularly lethal at executing forks against Queens and Rooks?",
        assessment_options=["Knights move faster", "Knights can attack heavy pieces without being attacked back along ranks, files, or diagonals", "Knights cannot be captured", "Knights have higher point value"],
        assessment_answer_index=1,
        assessment_explanation="Because Knights move in an L-shape, they can attack Queens and Rooks from squares where those pieces cannot attack back.",
    ),
    Lesson(
        id="tactics_pin",
        category="Tactical Skills",
        level_number=2,
        level_name="Chess Tactics",
        difficulty="Intermediate",
        topic="pins",
        title="8. The Absolute Pin: Total Paralysis",
        concept="An absolute pin occurs when a piece shields its King from attack. Moving the pinned piece is strictly illegal.",
        fen="4k3/4r3/8/8/8/8/4R3/4K3 w - - 0 1",
        player_color="White",
        objective="Exploit the pinned Rook on e7! Capture Black's immobilized Rook with your active Rook on e2!",
        expected_moves=["e2e7"],
        guided_move="e2e7",
        cm_intro=(
            "Feel the power of the pin, {username}! Black's Rook on e7 cannot move because doing so would expose the Black King to check. "
            "A pinned piece loses all its defensive capability. Cash in on the pin by capturing on e7!"
        ),
        cm_success=(
            "Decisive execution, {username}! Black's immobilized Rook was powerless to resist. You eliminated their key piece!"
        ),
        cm_hint="Capture Black's pinned rook on e7 with your rook on e2.",
        educational_note=(
            "An Absolute Pin pins a piece to the King (making moving illegal). A Relative Pin pins a piece to a Queen or Rook "
            "(moving is legal but loses material)."
        ),
        hints=[
            "Observe the open e-file: White Rook on e2, Black Rook on e7, Black King on e8.",
            "The Black Rook cannot flee because it shields its King.",
            "Capture on e7 with your rook: Rxe7+!",
        ],
        theory_detail="Absolute pins are enforcers of passivity. Pinned defenders cannot fulfill any other tactical responsibilities.",
        feedback_correct="1. Rxe7+ captures the immobilized rook with check, converting the pin into an overwhelming material victory.",
        feedback_incorrect="Capture Black's pinned rook on e7 with your e2 rook: Rxe7+!",
        opponent_threat="If White does not trade or exploit the pin, Black might play Kd8 to unpin their Rook.",
        why_mistakes_fail={"e1d2": "Moving the King allows Black to trade rooks on Black's terms or unpin with Kd8."},
        real_application="Grandmaster Aaron Nimzowitsch famously observed: 'The pinned piece is an optical illusion of a defender.'",
        assessment_question="What makes an 'Absolute Pin' different from a 'Relative Pin'?",
        assessment_options=["An absolute pin involves a Queen", "In an absolute pin, moving the piece is strictly illegal by chess rules because it exposes the King", "A relative pin cannot be broken", "An absolute pin only happens on the rank"],
        assessment_answer_index=1,
        assessment_explanation="An absolute pin is aligned against the King, making it strictly illegal to move the pinned piece under chess rules.",
    ),
    Lesson(
        id="tactics_skewer",
        category="Intermediate Tactics",
        level_number=2,
        level_name="Chess Tactics",
        difficulty="Intermediate",
        topic="skewers",
        title="9. The Skewer: X-Ray Attack on Rank 8",
        concept="A skewer attacks a high-value piece in front (like the King), forcing it to move and revealing a target behind it on the same line.",
        fen="3k3r/8/8/8/8/8/5K2/R7 w - - 0 1",
        player_color="White",
        objective="Deliver check along the 8th rank by sliding your Rook to a8, skewering Black's King and the Rook on h8!",
        expected_moves=["a1a8"],
        guided_move="a1a8",
        cm_intro=(
            "Think of a skewer as an X-ray attack, {username}! "
            "Unlike a pin where the more valuable piece is behind, a skewer attacks the valuable piece in FRONT. "
            "Slide your Rook from a1 to a8 to check Black's King; when he dodges, you win the rook on h8!"
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
            "Observe the line of the 8th rank: King is on d8, your rook can deliver check on a8.",
            "When the King moves off the 8th rank, the h8 rook is exposed.",
            "Play Rook from a1 to a8!",
        ],
        theory_detail="Skewers exploit collinear targets where the front piece is too valuable to be sacrificed.",
        feedback_correct="Ra8+ skewers the king, forcing a retreat and leaving the rook on h8 undefended.",
        feedback_incorrect="Deliver check along the 8th rank with your rook: Ra8+!",
        opponent_threat="Black's Rook on h8 threatens to give checks down the h-file (Rh2+) and pick up pawns.",
        why_mistakes_fail={"a1d1": "Rd1+ checks the King but allows it to step to c7 or e7 without skewering the h8 Rook."},
        real_application="Skewers are often called 'reverse pins'. Rooks and Bishops are the premier skewer weapons in master play.",
        assessment_question="In a skewer, which piece sits in front facing the attack?",
        assessment_options=["The less valuable piece", "The more valuable piece", "The pawn", "Any undefended piece"],
        assessment_answer_index=1,
        assessment_explanation="In a skewer, the more valuable piece stands in front, forcing it to dodge and revealing the target behind it.",
    ),
    Lesson(
        id="tactics_discovered",
        category="Intermediate Tactics",
        level_number=2,
        level_name="Chess Tactics",
        difficulty="Intermediate",
        topic="discovered_attacks",
        title="10. Discovered Attack with Check",
        concept="A discovered attack happens when moving one piece unmasks a hidden attack from a piece standing behind it.",
        fen="3k4/8/2q5/8/3B4/8/8/3R2K1 w - - 0 1",
        player_color="White",
        objective="Move your Bishop from d4 to b6 to uncover check from the d1 Rook while skewering the Queen!",
        expected_moves=["d4b6", "d4c5", "d4e5", "d4f6", "d4g7", "d4h8"],
        guided_move="d4b6",
        cm_intro=(
            "Get ready for an ambush, {username}! "
            "Your Rook on d1 is aiming straight at the Black King on d8, but your own Bishop on d4 blocks the view. "
            "Step your bishop to b6: it discovers check from the rook AND attacks Black's queen on c6!"
        ),
        cm_success=(
            "Devastating ambush, {username}! Because the King was checked by the rook, Black was forced to deal with check, "
            "leaving you free to capture their Queen on the next move!"
        ),
        cm_hint="Move your bishop on d4 away to b6 to uncover check from the rook on d1.",
        educational_note=(
            "Discovered checks are among the most lethal weapons in chess because the moving piece can land anywhere "
            "with impunity while the opponent is forced to answer the check."
        ),
        hints=[
            "The d1 rook and Black King on d8 share the d-file.",
            "Move the d4 bishop to b6 with double check/double attack.",
            "Play Bishop to b6: Bb6+!",
        ],
        theory_detail="Because check requires immediate resolution, discovered attacks allow the uncovering piece to make threats with complete immunity.",
        feedback_correct="Bb6+ unmasks check from the rook while targeting the queen on c6.",
        feedback_incorrect="Move your bishop out of the d-file to unleash check: Bb6+!",
        opponent_threat="Black's Queen on c6 dominates the center and threatens counter-checks against White's King.",
        why_mistakes_fail={"d1d2": "Passive rook move relinquishes the devastating discovered check from the d-file."},
        real_application="Discovered checks and double checks are lethal because the opponent must respond to the check, leaving the second target defenseless.",
        assessment_question="Why is a Double Check (discovered check where both pieces give check) so devastating?",
        assessment_options=["The opponent loses two turns", "The King MUST move; blocking or capturing one checking piece is impossible", "The game ends in a draw", "Pawns can promote immediately"],
        assessment_answer_index=1,
        assessment_explanation="In a double check, capturing or blocking one checking piece leaves the King in check from the second, so the King MUST run.",
    ),
    Lesson(
        id="curr_deflection",
        category="Tactical Combinations",
        level_number=2,
        level_name="Chess Tactics",
        difficulty="Intermediate",
        topic="deflection",
        title="11. Deflection: Removing the Key Guard",
        concept="Deflection lures an enemy piece away from an essential duty, such as guarding the back rank or protecting a piece.",
        fen="1k1r4/ppp5/8/8/8/8/4QPPP/3R2K1 w - - 0 1",
        player_color="White",
        objective="Deflect Black's defensive Rook by sacrificing or trading down the d-file to crush Black's back rank!",
        expected_moves=["d1d8"],
        guided_move="d1d8",
        cm_intro=(
            "Look at Black's back rank, {username}! Black's King is trapped behind pawns on a7, b7, c7. "
            "Their only guard is the Rook on d8. Strike directly by playing Rxd8+ to crush the back rank!"
        ),
        cm_success=(
            "Decisive blow, {username}! You eliminated Black's back-rank defender and forced immediate capitulation!"
        ),
        cm_hint="Take Black's rook on d8 with your rook on d1.",
        educational_note="Overloaded defenders and deflection tactics account for over 30% of tactical victories in tournament play.",
        hints=[
            "White has a rook on d1 and queen on e2 targeting the back rank.",
            "Black's only defender is the rook on d8.",
            "Take the rook with check: Rxd8#!",
        ],
        theory_detail="Deflection strips away the glue holding a defensive fortress together, leaving key squares defenseless.",
        feedback_correct="1. Rxd8# delivers back-rank checkmate, exploiting the trapped King.",
        feedback_incorrect="Take the defending rook directly: Rxd8#!",
        opponent_threat="Black threatens Rd6 or c6 to consolidate back-rank security.",
        why_mistakes_fail={"e2e7": "Qe7 allows Black Rdc8, maintaining defender contact and defending the back rank."},
        real_application="Deflection combinations frequently appear in grandmaster play when an overloaded defender is pulled away from king safety.",
        assessment_question="What is an 'overloaded' piece in chess tactics?",
        assessment_options=["A piece that has moved too many times", "A piece tasked with defending two critical squares or pieces at the same time", "A queen that is trapped", "A pawn that cannot advance"],
        assessment_answer_index=1,
        assessment_explanation="An overloaded piece has two defensive responsibilities at once; deflecting it from one task breaks the position.",
    ),
    Lesson(
        id="curr_remove_defender",
        category="Tactical Combinations",
        level_number=2,
        level_name="Chess Tactics",
        difficulty="Intermediate",
        topic="removing_defender",
        title="12. Removing the Defender & Tactical Conversion",
        concept="When a target is defended, identify the defending piece and eliminate, distract, or pin it to win material.",
        fen="r1b1k2r/pppp1ppp/2n2n2/4p3/1b2P3/2NP1N2/PPP2PPP/R1BQKB1R w KQkq - 1 5",
        player_color="White",
        objective="Question Black's pinning Bishop on b4 by playing a2-a3 to force a retreat or capture!",
        expected_moves=["a2a3", "d1e2"],
        guided_move="a2a3",
        cm_intro=(
            "Put the question to the bishop, {username}! Black's bishop on b4 is pinning your knight on c3. "
            "Push a2-a3 to challenge the bishop immediately: Black must either retreat or exchange!"
        ),
        cm_success=(
            "Excellent probe, {username}! By playing a3, you broke the pin's psychological pressure and seized queenside space!"
        ),
        cm_hint="Push your a-pawn forward one square to a3 to attack the bishop.",
        educational_note="Never suffer pins passively. Challenge pinned pieces with pawn jabs or unpinning maneuvers.",
        hints=[
            "Look at the bishop on b4 pinning your c3 knight.",
            "Pawns can harass enemy minor pieces with minimal risk.",
            "Advance the a2 pawn to a3!",
        ],
        theory_detail="Challenging pins forces opponents to make immediate decisions before they can organize secondary attackers.",
        feedback_correct="1. a3 puts the question to the pinning bishop, resolving the pressure favorably.",
        feedback_incorrect="Challenge the bishop on b4 with your pawn: a2a3!",
        opponent_threat="Black's pin on c3 threatens Nd4 or Bxc3+ ruining White's pawn structure.",
        why_mistakes_fail={"c1d2": "Bd2 is passive; a3 immediately puts the question to the bishop to force resolution."},
        real_application="Capablanca's rule: 'First remove the foundation, then the roof falls by itself.'",
        assessment_question="What are the three ways to remove a defending piece in chess?",
        assessment_options=["Capture it, chase it away (attack it), or deflect/pin it", "Castle, check, promote", "Sacrifice queen, resign, offer draw", "Wait, advance pawns, double rooks"],
        assessment_answer_index=0,
        assessment_explanation="Defenders can be captured directly, driven away with pawn jabs or threats, or pinned/deflected from their post.",
    ),

    # -------------------------------------------------------------------------
    # LEVEL 3: OPENING MASTERY (Lessons 13 - 18)
    # -------------------------------------------------------------------------
    Lesson(
        id="curr_center_control",
        category="Opening Principles",
        level_number=3,
        level_name="Opening Mastery",
        difficulty="Beginner",
        topic="center_control",
        title="13. Classical Center Control: Pawn Occupation",
        concept="The center squares (e4, d4, e5, d5) are the high ground of the board. Whoever controls the center controls the game's flow.",
        fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
        player_color="White",
        objective="Occupy the center on move 1 by advancing your d-pawn to d4 (or e-pawn to e4)!",
        expected_moves=["d2d4", "e2e4"],
        guided_move="d2d4",
        cm_intro=(
            "Welcome to the opening masterclass, {username}! In the opening, you must immediately fight for the center squares (e4, d4, e5, d5). "
            "Push your queen's pawn to d4 to establish early control of the board!"
        ),
        cm_success=(
            "Flawless move, {username}! 1.d4 claims central territory, controls e5 and c5, and liberates your dark-squared bishop!"
        ),
        cm_hint="Push your d2 pawn forward two squares to d4.",
        educational_note="Every opening system revolves around either directly occupying the center with pawns or controlling it with pieces.",
        hints=[
            "Focus on the four central squares: d4, e4, d5, and e5.",
            "Move your Queen's pawn straight forward two squares.",
            "Play d2 to d4!",
        ],
        theory_detail="Classical center theory states that pawns on d4 and e4 restrict opposing knights and provide natural anchors.",
        feedback_correct="1.d4 stakes an immediate claim in the center and immediately activates your queen and bishop diagonals.",
        feedback_incorrect="Stake your claim in the center: push d2 to d4!",
        opponent_threat="If you play passively on the flanks (like a3 or h3), Black will seize the central squares e5 and d5.",
        why_mistakes_fail={"a2a3": "1.a3 is a flank pawn push that does nothing to control e4 or d4 and leaves the initiative to Black."},
        real_application="World Champion Wilhelm Steinitz established that all sound opening play stems from central dominance.",
        assessment_question="Why are center squares (d4, e4, d5, e5) more important than flank squares (a4, h4)?",
        assessment_options=["Pieces in the center command more squares and can quickly swing to either flank", "Pawns are worth more points in the center", "Kings can only castle through the center", "No pieces can cross the center"],
        assessment_answer_index=0,
        assessment_explanation="Pieces centralized on d4/e4 touch twice as many squares and can rapidly mobilize toward either wing.",
    ),
    Lesson(
        id="curr_piece_dev",
        category="Opening Principles",
        level_number=3,
        level_name="Opening Mastery",
        difficulty="Beginner",
        topic="development",
        title="14. Rapid Piece Development & Coordination",
        concept="In the opening, bring out your minor pieces (Knights and Bishops) rapidly. Knights belong toward the center; avoid moving the same piece twice.",
        fen="rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2",
        player_color="White",
        objective="Develop your King's Knight to f3, attacking Black's e5 pawn with tempo!",
        expected_moves=["g1f3", "b1c3", "f1c4"],
        guided_move="g1f3",
        cm_intro=(
            "Development with threats, {username}! Don't just move pieces aimlessly. "
            "Develop your King's Knight from g1 to f3: you bring a minor piece into action, prepare kingside castling, "
            "AND attack Black's e5 pawn simultaneously!"
        ),
        cm_success=(
            "Textbook development, {username}! 2.Nf3 coordinates piece activity with immediate pressure against e5!"
        ),
        cm_hint="Hop your knight from g1 to f3.",
        educational_note="A 'tempo' is a unit of time (one move). Developing with a threat forces the opponent to respond, gaining you a tempo.",
        hints=[
            "Minor pieces (knights and bishops) must be brought into play.",
            "f3 is the most natural home for White's King's Knight.",
            "Play Knight from g1 to f3: Nf3!",
        ],
        theory_detail="Developing with threats forces the opponent to react defensively, keeping the initiative firmly in your hands.",
        feedback_correct="2. Nf3 develops toward the center with tempo by attacking Black's e5 pawn.",
        feedback_incorrect="Develop your King's Knight to f3: g1f3!",
        opponent_threat="Black's e5 pawn stakes central space; 2.Nf3 develops with tempo by attacking e5 immediately.",
        why_mistakes_fail={"d1h5": "Early queen raids violate opening principles and expose the Queen to tempo attacks from Nc6 and Nf6."},
        real_application="Paul Morphy destroyed opponents in the 1850s simply by developing all his pieces while opponents moved pawns.",
        assessment_question="Why should you generally develop Knights before Bishops in classical openings?",
        assessment_options=["Knights are worth more points", "Knights almost always belong on f3/c3, whereas Bishops have multiple candidate diagonals depending on the position", "Bishops cannot jump over pawns", "Rules require knights first"],
        assessment_answer_index=1,
        assessment_explanation="Knights have obvious natural squares (f3/c3), whereas Bishops are best placed after seeing the opponent's structure.",
    ),
    Lesson(
        id="curr_castling_safety",
        category="Opening Principles",
        level_number=3,
        level_name="Opening Mastery",
        difficulty="Beginner",
        topic="king_safety",
        title="15. King Safety: Timing the Castle",
        concept="Do not delay castling. An uncastled King in the center is a magnet for pawn sacrifices and central line openings.",
        fen="r1bqk2r/pppp1ppp/2n2n2/2b1p3/2B1P3/3P1N2/PPP2PPP/RNBQK2R w KQkq - 1 5",
        player_color="White",
        objective="Complete your opening development by castling kingside (O-O) before launching central action!",
        expected_moves=["e1g1"],
        guided_move="e1g1",
        cm_intro=(
            "Don't leave your King in the danger zone, {username}! Both sides have developed pieces toward the center. "
            "Before launching any pawn breaks, secure your King with kingside castling: e1 to g1!"
        ),
        cm_success=(
            "Safe and sound, {username}! Your King is tucked into safety and your f1 Rook is ready to join the central fight!"
        ),
        cm_hint="Move your king two squares to the right to castle: e1g1.",
        educational_note="A king in the center past move 10 is vulnerable to central breakthroughs like d4 or e5 blasting open the files.",
        hints=[
            "The way between e1 King and h1 Rook is completely clear.",
            "Castling moves the King two squares toward the corner.",
            "Play King from e1 to g1!",
        ],
        theory_detail="Castling completes development phase 1, connecting both rooks along the back rank.",
        feedback_correct="1. O-O safeguards the King and transitions your army into active middlegame play.",
        feedback_incorrect="Castle kingside to secure the King: e1g1!",
        opponent_threat="Black is fully developed and ready to play d6, Bg4, and Nd4 with mounting pressure against White's center.",
        why_mistakes_fail={"h2h3": "h3 is an unnecessary pawn move when the King is still in the central crosshairs; castle first!"},
        real_application="In the famous Opera Game (1858), Morphy sacrificed pieces to blast open lines against the uncastled enemy King.",
        assessment_question="What is the primary danger of leaving your King in the center past move 10?",
        assessment_options=["The King gets lonely", "Central pawn breaks (d4/d5 or e4/e5) open files straight to the exposed King", "Castling becomes illegal", "Opponent pawns become queens"],
        assessment_answer_index=1,
        assessment_explanation="If files in the center open up, opposing rooks and queens will deliver devastating checks and pins against the central King.",
    ),
    Lesson(
        id="opening_traps",
        category="Opening Principles",
        level_number=3,
        level_name="Opening Mastery",
        difficulty="Intermediate",
        topic="opening_traps",
        title="16. Punishing Opening Mistakes & Traps",
        concept="Recognize premature attacks and punish them. When an opponent brings out their Queen too early, develop with threats!",
        fen="r1bqkbnr/pppp1ppp/2n5/4p3/2B1P3/5Q2/PPPP1PPP/RNB1K1NR b KQkq - 3 3",
        player_color="Black",
        objective="Neutralize White's premature Scholar's Mate attempt by developing your Knight to f6, blocking the mating diagonal!",
        expected_moves=["g8f6", "d8f6", "d8e7"],
        guided_move="g8f6",
        cm_intro=(
            "Alert, {username}! White rolled out their Queen on move 3 aiming for Qxf7# Scholar's Checkmate! "
            "Don't panic—punish premature queen attacks! Jump your King's Knight to f6: "
            "you block the diagonal, develop a piece, and prepare to harass their exposed Queen!"
        ),
        cm_success=(
            "Clinical defense, {username}! 3...Nf6 blocks the mating diagonal, develops a minor piece, and leaves White's early Queen awkward!"
        ),
        cm_hint="Move your Knight from g8 to f6 to block the Queen's view of f7.",
        educational_note="Premature Queen attacks violate opening principles. Defend with natural developing moves that leave the Queen exposed to tempo hits.",
        hints=[
            "White's Queen on f3 and Bishop on c4 both target f7.",
            "You can block the attack by placing a piece on f6.",
            "Play Knight from g8 to f6: Nf6!",
        ],
        theory_detail="3...Nf6 develops Black's Kingside pieces while White wastes valuable opening tempos with an exposed queen.",
        feedback_correct="3... Nf6 cleanly parries the checkmate threat while developing Black's minor piece toward the center.",
        feedback_incorrect="Block the attack on f7 by developing your knight: g8f6!",
        opponent_threat="White threatens instant checkmate with Qxf7#! Black must neutralize the mating threat while developing.",
        why_mistakes_fail={"g7g6": "g6 defends f7 but weakens dark squares around the King; Nf6 develops a piece toward the center and blocks f7 naturally."},
        real_application="Defending against Scholar's Mate with 3...Nf6 leaves White's early Queen awkward and targets White for counterattack.",
        assessment_question="How should you react when an opponent launches an aggressive early Queen raid in the opening?",
        assessment_options=["Panic and move your King", "Develop your minor pieces calmly while defending threats and harassing the exposed Queen", "Resign", "Push all edge pawns"],
        assessment_answer_index=1,
        assessment_explanation="Early Queen attacks are premature. Calm development with tempo attacks on the Queen leaves the attacker behind in development.",
    ),
    Lesson(
        id="opening_italian",
        category="Opening Principles",
        level_number=3,
        level_name="Opening Mastery",
        difficulty="Intermediate",
        topic="opening_plans",
        title="17. Italian Game: Harmonic Piece Placement",
        concept="The Italian Game (1.e4 e5 2.Nf3 Nc6 3.Bc4) aims at the weak f7 square while preparing rapid castling and pawn center expansion.",
        fen="r1bqk1nr/pppp1ppp/2n5/2b1p3/2B1P3/2P2N2/PP1P1PPP/RNBQK2R b KQkq - 0 4",
        player_color="Black",
        objective="Counter White's c3-d4 center expansion plan by striking White's e4 pawn with 4...Nf6!",
        expected_moves=["g8f6"],
        guided_move="g8f6",
        cm_intro=(
            "Welcome to grandmaster theory, {username}! White played 4.c3, intending to build a massive center with 5.d4! "
            "How does Black counter? Counterattack! Jump your Knight to f6: develop with a direct threat against White's e4 pawn!"
        ),
        cm_success=(
            "Precision play, {username}! 4...Nf6 follows the golden rule: counterattack the center when the opponent builds a pawn wall!"
        ),
        cm_hint="Develop your Knight from g8 to f6 to attack White's e4 pawn.",
        educational_note="In classical e4-e5 openings, attacking the opposing center pawn immediately dampens the opponent's attacking ambition.",
        hints=[
            "White's e4 pawn is currently undefended.",
            "Develop your King's Knight to attack e4.",
            "Play Knight to f6: Nf6!",
        ],
        theory_detail="4...Nf6 is the Main Line Italian Game. Black demands White solve the problem of e4 before expanding with d4.",
        feedback_correct="4... Nf6 challenges White's center and prepares Black's own castling.",
        feedback_incorrect="Develop your knight to f6 to attack e4: g8f6!",
        opponent_threat="White played 4.c3 preparing a big pawn center with 5.d4 attacking Black's bishop on c5.",
        why_mistakes_fail={"d7d6": "Passive d6 lets White play d4 with tempo; 4...Nf6 counterattacks White's e4 pawn directly!"},
        real_application="The Italian Game is over 500 years old and remains a top weapon of Magnus Carlsen and Ding Liren.",
        assessment_question="In the Italian Game with 4.c3, what is White's primary strategic plan?",
        assessment_options=["To play d4 and establish a broad two-pawn center", "To trade Queens immediately", "To trap Black's king", "To castle queenside"],
        assessment_answer_index=0,
        assessment_explanation="The move 4.c3 supports the d2-d4 pawn push, aiming to build a dominant pawn duo on e4 and d4.",
    ),
    Lesson(
        id="opening_asymmetric",
        category="Opening Principles",
        level_number=3,
        level_name="Opening Mastery",
        difficulty="Intermediate",
        topic="opening_plans",
        title="18. Asymmetric Warfare: The Sicilian Defense",
        concept="1...c5 creates an immediate dynamic asymmetry. Black fights for central control from the flank and aims for an open c-file.",
        fen="rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1",
        player_color="Black",
        objective="Launch the fighting Sicilian Defense by advancing your c-pawn two squares to c5!",
        expected_moves=["c7c5"],
        guided_move="c7c5",
        cm_intro=(
            "Ready for dynamic combat, {username}? Instead of copying White with 1...e5, the Sicilian Defense plays 1...c5! "
            "You control the critical d4 central square from the flank, preparing an asymmetric battle for the full point!"
        ),
        cm_success=(
            "Fabulous! 1...c5 is the weapon of World Champions Fischer and Kasparov. You are playing for the win from move 1!"
        ),
        cm_hint="Push your c7 pawn forward two squares to c5.",
        educational_note="The Sicilian Defense is statistically Black's highest-scoring response to 1.e4 in grandmaster databases.",
        hints=[
            "Locate the c-file pawn on c7.",
            "On its first move, the c-pawn can leap two squares.",
            "Push c7 to c5!",
        ],
        theory_detail="By exchanging a flank c-pawn for White's central d-pawn later, Black acquires two central pawns against White's one.",
        feedback_correct="1... c5 initiates the Sicilian Defense, fighting for central control and asymmetric counterplay.",
        feedback_incorrect="Play the Sicilian Defense: c7c5!",
        opponent_threat="White wants to establish e4 and d4 unopposed; 1...c5 prevents White from dominating the center comfortably.",
        why_mistakes_fail={"a7a6": "a6 gives White a free hand to play 2.d4 and seize full central space."},
        real_application="The Sicilian Defense is Black's highest-scoring response to 1.e4 in grandmaster history.",
        assessment_question="What is Black's strategic asset in the Open Sicilian after White plays d4 and Black plays cxd4?",
        assessment_options=["Black gets two central pawns (e and d) against White's one (e-pawn) and an open c-file", "Black checkmates White on move 5", "Black wins White's queen", "Black gets three knights"],
        assessment_answer_index=0,
        assessment_explanation="Trading the c-pawn for White's d-pawn gives Black two center pawns against White's one and a half-open c-file for rook pressure.",
    ),

    # -------------------------------------------------------------------------
    # LEVEL 4: MIDDLEGAME STRATEGY (Lessons 19 - 24)
    # -------------------------------------------------------------------------
    Lesson(
        id="strategy_outpost",
        category="Middlegame Strategy",
        level_number=4,
        level_name="Middlegame Strategy",
        difficulty="Intermediate",
        topic="outposts",
        title="19. Knight Outposts: The Eternal Anchor",
        concept="An outpost is a square deep in enemy territory that cannot be challenged by enemy pawns. An entrenched knight dominates the board.",
        fen="4k3/pppp1ppp/8/4N3/8/8/PPPP1PPP/4K3 w - - 0 1",
        player_color="White",
        objective="Strike from your entrenched outpost! Use your Knight on e5 to capture Black's weak f7 pawn.",
        expected_moves=["e5f7"],
        guided_move="e5f7",
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
            "e5 is an eternal outpost: no black pawns on d or f can ever kick it.",
            "f7 is a vulnerable target in Black's camp.",
            "Jump from e5 to f7 to claim the pawn!",
        ],
        theory_detail="Outposts on the 5th and 6th ranks paralyze enemy coordination and serve as jumping pads for tactical strikes.",
        feedback_correct="1. Nxf7 demonstrates the destructive conversion power of an unassailable knight outpost.",
        feedback_incorrect="Strike from the outpost: take the f7 pawn with your e5 knight!",
        opponent_threat="Black wants to organize d6 or f6 to contest White's active knight.",
        why_mistakes_fail={"e5d3": "Retreating from e5 relieves all pressure on Black's weak squares; strike f7 directly!"},
        real_application="Anatoly Karpov's mastery of knight outposts on d5 and e5 suffocated world-class grandmasters.",
        assessment_question="What makes a square a true 'outpost' for a knight?",
        assessment_options=["It is defended by our own piece and cannot be attacked by an enemy pawn", "It is on the edge of the board", "It has a rook on it", "It is near our King"],
        assessment_answer_index=0,
        assessment_explanation="A true outpost is an advanced square that cannot be challenged by enemy pawns, ideally supported by friendly pawns.",
    ),
    Lesson(
        id="strategy_pawn_structure",
        category="Middlegame Strategy",
        level_number=4,
        level_name="Middlegame Strategy",
        difficulty="Intermediate",
        topic="pawn_structures",
        title="20. Pawn Structure: Targets & Weaknesses",
        concept="Pawns cannot move backward. Every pawn push creates permanent holes behind it. Target isolated, doubled, and backward pawns.",
        fen="4k3/1p3ppp/p1p5/8/4P3/8/PPP2PPP/4K3 w - - 0 1",
        player_color="White",
        objective="Centralize your King toward the endgame center with 1.Ke2, preparing to exploit Black's weak c6 and b7 pawns!",
        expected_moves=["e1e2"],
        guided_move="e1e2",
        cm_intro=(
            "Look at Black's pawn structure, {username}! The pawns on a6, b7, and c6 are disconnected and backward. "
            "In endgames, the King transforms into an attacking piece! Step your King forward to e2 to prepare the invasion!"
        ),
        cm_success=(
            "Grandmaster technique, {username}! 1.Ke2 mobilizes the King to support pawn breaks while Black's weaknesses sit exposed!"
        ),
        cm_hint="Advance your King one square forward to e2.",
        educational_note="In the endgame, the King is worth approximately 4 points of fighting power. Always centralize the King!",
        hints=[
            "With Queens off the board, King safety is no longer endangered in the center.",
            "e2 is the natural first step toward centralizing the King.",
            "Play King to e2: Ke2!",
        ],
        theory_detail="Pawn weaknesses persist indefinitely because pawns cannot retreat to repair damaged squares.",
        feedback_correct="1. Ke2 centralizes the King, preparing an active endgame invasion against Black's structural flaws.",
        feedback_incorrect="Centralize your King: e1 to e2!",
        opponent_threat="Black wants to activate their King to d7 and c7 to defend the weak queenside pawns.",
        why_mistakes_fail={"a2a4": "Premature flank pawn pushes create unnecessary targets; centralize your King first in the endgame!"},
        real_application="Philidor famously declared: 'Pawns are the soul of chess.' Structure dictates plans.",
        assessment_question="What is an 'isolated pawn' in chess terminology?",
        assessment_options=["A pawn with no friendly pawns on adjacent files to defend it", "A pawn that has reached the 7th rank", "A pawn in check", "A pawn on the h-file"],
        assessment_answer_index=0,
        assessment_explanation="An isolated pawn has no friendly pawns on the neighboring files, making it a chronic target for enemy piece attack.",
    ),
    Lesson(
        id="strategy_open_files",
        category="Middlegame Strategy",
        level_number=4,
        level_name="Middlegame Strategy",
        difficulty="Intermediate",
        topic="piece_activity",
        title="21. Rooks on Open Files & the 7th Rank",
        concept="Rooks need open files to unleash their power. Infiltrating the 7th rank attacks base pawns and restricts the enemy King.",
        fen="3r2k1/5ppp/8/8/8/8/4RPPP/4R1K1 w - - 0 1",
        player_color="White",
        objective="Penetrate Black's back rank using your doubled rooks on the open e-file to deliver back-rank checkmate!",
        expected_moves=["e2e8"],
        guided_move="e2e8",
        cm_intro=(
            "Battery unleashed, {username}! You have doubled rooks on the open e-file. "
            "An open file is an open highway into the opponent's territory. Strike e8 with your lead rook!"
        ),
        cm_success=(
            "Checkmate, {username}! Doubled rooks on open files are devastating. Black had no escape from the e-file invasion!"
        ),
        cm_hint="Capture on e8 with your e2 rook.",
        educational_note="Alekhine's Gun is the ultimate open-file battery: two rooks backed up by a Queen down a completely open file.",
        hints=[
            "White has doubled rooks on e1 and e2.",
            "e8 is defended once by Black's rook but attacked twice by White.",
            "Play Re2 takes e8: Re8+!",
        ],
        theory_detail="Controlling an open file guarantees penetration into the enemy back rank and 7th rank.",
        feedback_correct="1. Rxe8+ Rxe8 2. Rxe8# delivers forced checkmate down the open file.",
        feedback_incorrect="Invade down the e-file: e2 takes e8!",
        opponent_threat="Black's rook controls d8; doubling rooks on e-file delivers back-rank checkmate!",
        why_mistakes_fail={"e1a1": "Abandoning the open e-file gives Black total control of the center."},
        real_application="Reuben Fine called rooks on the 7th rank 'the blind pigs'—they devour everything in sight.",
        assessment_question="Why is a Rook on the 7th rank (or 2nd rank for Black) so devastating?",
        assessment_options=["It attacks unadvanced pawns from behind and cuts off the opponent King", "It turns into a Queen", "It can jump over pieces", "It gains extra points"],
        assessment_answer_index=0,
        assessment_explanation="On the 7th rank, the Rook attacks the base of enemy pawn chains horizontally while cutting the enemy King off from the center.",
    ),
    Lesson(
        id="strategy_good_bad_bishop",
        category="Middlegame Strategy",
        level_number=4,
        level_name="Middlegame Strategy",
        difficulty="Intermediate",
        topic="positional_advantage",
        title="22. Good vs Bad Bishops: Color Complex Control",
        concept="A 'bad bishop' is blocked by its own pawns fixed on the same color squares. A 'good bishop' roams freely around pawn chains.",
        fen="4k3/8/4p3/3b4/8/2B5/4PPPP/4K3 w - - 0 1",
        player_color="White",
        objective="Centralize your light-squared Bishop to the active e5 square, dominating the board's key long diagonal!",
        expected_moves=["c3e5", "g2g3"],
        guided_move="c3e5",
        cm_intro=(
            "Color complex mastery, {username}! Notice how White's pawns are on light and dark squares, but Black's e6 pawn is fixed on dark. "
            "Place your Bishop on e5: it cuts across the board, dominates the center, and prevents Black's King from advancing!"
        ),
        cm_success=(
            "Superb diagonal dominance, {username}! From e5, your Bishop commands both wings and restricts the enemy King!"
        ),
        cm_hint="Slide your bishop from c3 to the central e5 square.",
        educational_note="Place your pawns on the opposite color of your bishop so your bishop retains open diagonals and mobility.",
        hints=[
            "e5 is an active central post for your light-squared bishop.",
            "It cuts across both sides of the board.",
            "Move c3 to e5: Be5!",
        ],
        theory_detail="A good bishop controls open diagonals across the whole board, acting like a long-range laser.",
        feedback_correct="1. Be5 centralizes the bishop with maximum diagonal influence.",
        feedback_incorrect="Centralize your bishop along the long diagonal: Be5!",
        opponent_threat="Black's bishop on d5 threatens g2 and controls the central diagonal.",
        why_mistakes_fail={"f2f3": "Fixing pawns on dark squares restricts your own dark-squared bishop."},
        real_application="Capablanca's rule: Place your pawns on the OPPOSITE color of your bishop so they do not obstruct each other.",
        assessment_question="If your only bishop moves on light squares, what color squares should you generally place your pawns on?",
        assessment_options=["Dark squares", "Light squares", "Only on the edge", "Pawn color does not matter"],
        assessment_answer_index=0,
        assessment_explanation="Placing pawns on dark squares keeps light diagonals open for your light-squared bishop and covers the squares your bishop cannot touch.",
    ),
    Lesson(
        id="strategy_initiative",
        category="Middlegame Strategy",
        level_number=4,
        level_name="Middlegame Strategy",
        difficulty="Intermediate",
        topic="initiative",
        title="23. Seizing the Initiative: Active Defense",
        concept="The initiative is the ability to make threats that the opponent must answer. When under fire, defend actively, not passively.",
        fen="r1b1k2r/pppp1ppp/2n5/4p3/2B1P2q/8/PPPP1bPP/RNBQK1NR w KQkq - 0 6",
        player_color="White",
        objective="Step your King to f1 to escape check while trapping Black's overextended Bishop on f2!",
        expected_moves=["e1f1"],
        guided_move="e1f1",
        cm_intro=(
            "Under attack, {username}! Black launched an aggressive raid with Qh4 and Bxf2+. "
            "Don't panic! Step your King to f1: you escape check, defend g2, AND leave Black's f2 bishop trapped with nowhere to run!"
        ),
        cm_success=(
            "Cool-headed defense, {username}! You stepped to f1. Black's bishop on f2 is now stranded in enemy territory and will be captured!"
        ),
        cm_hint="Move your King from e1 to f1.",
        educational_note="When the opponent attacks prematurely, calm King moves often leave the attacking pieces stranded and overextended.",
        hints=[
            "The King has two legal moves: e2 or f1.",
            "Ke2 walks into dangerous central checks.",
            "Step the King to f1: Kf1!",
        ],
        theory_detail="Overextended attackers quickly become trapped targets once their initial check is parried cleanly.",
        feedback_correct="1. Kf1 steps out of check and traps Black's overextended bishop on f2.",
        feedback_incorrect="Escape check by moving your King to f1: e1f1!",
        opponent_threat="Black's Queen and Bishop deliver check on f2, threatening White's King.",
        why_mistakes_fail={"e1e2": "Ke2 steps directly into Nd4+ winning White's Queen; Kf1 shelters the King while Black's f2 bishop is trapped!"},
        real_application="Garry Kasparov was renowned for sacrificing pawns just to retain the initiative and dictate the game.",
        assessment_question="Why is holding the initiative an enormous psychological and practical advantage in chess?",
        assessment_options=["It forces the opponent to solve difficult problems every turn while you dictate the action", "You get extra time on the clock", "You can skip moves", "It doubles piece value"],
        assessment_answer_index=0,
        assessment_explanation="The player with the initiative dictates the tempo and forces the defender into stressful, accurate problem-solving on every move.",
    ),
    Lesson(
        id="strategy_prophylaxis",
        category="Middlegame Strategy",
        level_number=4,
        level_name="Middlegame Strategy",
        difficulty="Intermediate",
        topic="prophylaxis",
        title="24. Prophylaxis: Stopping Counterplay in Advance",
        concept="Prophylaxis means anticipating the opponent's intentions and preventing their plan before they can execute it.",
        fen="r1bqkb1r/pp3ppp/2n2n2/2p1p3/2B1P3/2N2N2/PPPP2PP/R1BQK2R w KQkq - 2 7",
        player_color="White",
        objective="Solidify your center and prevent Black's Ng4 incursion by playing the prophylactic 1.d3!",
        expected_moves=["d2d3", "a2a3"],
        guided_move="d2d3",
        cm_intro=(
            "Think ahead like a master, {username}! Black is contemplating Ng4, targeting f2 and e3. "
            "Play prophylactic move 1.d3: you solidify e4, open the c1 Bishop's diagonal, and safeguard the f2 square in advance!"
        ),
        cm_success=(
            "Masterly prophylaxis, {username}! You squashed Black's active ideas before they even appeared on the board."
        ),
        cm_hint="Push your d2 pawn to d3 to solidify your center.",
        educational_note="World Champion Tigran Petrosian made prophylaxis his trademark: first eliminate opponent dreams, then conquer.",
        hints=[
            "Support the e4 pawn from behind.",
            "Open the c1 bishop's diagonal.",
            "Push d2 to d3: d3!",
        ],
        theory_detail="Prophylactic moves eliminate opponent counterplay before launching your own offensive operations.",
        feedback_correct="1. d3 secures the center and prevents tactical opponent leaps.",
        feedback_incorrect="Solidify your center with d2d3!",
        opponent_threat="Black plans Ng4 or Nd4, exploiting pins and invading White's camp.",
        why_mistakes_fail={"f3g5": "Premature attack on f7 allows Black d5!, seizing central space and neutralizing the threat."},
        real_application="Tigran Petrosian, 9th World Champion, was the ultimate master of prophylaxis, destroying attacks before opponents even conceived them.",
        assessment_question="What question should you ask yourself on EVERY single move in chess?",
        assessment_options=["What is my opponent threatening with their last move?", "Can I sacrifice my Queen?", "How fast can I move?", "Which piece looks prettiest?"],
        assessment_answer_index=0,
        assessment_explanation="Asking 'What is my opponent threatening?' prevents over 90% of tactical blunders before making your move.",
    ),

    # -------------------------------------------------------------------------
    # LEVEL 5: ADVANCED CALCULATION (Lessons 25 - 30)
    # -------------------------------------------------------------------------
    Lesson(
        id="curr_calculation",
        category="Advanced Calculation",
        level_number=5,
        level_name="Advanced Calculation",
        difficulty="Advanced",
        topic="calculation",
        title="25. The C-C-T Method: Checks, Captures, Threats",
        concept="Calculation must be disciplined. Start every calculation tree by scanning for Checks, then Captures, then Threats.",
        fen="r1bqk2r/pppp1ppp/2n5/4p3/2B1n3/5Q2/PPPP1PPP/RNB1K1NR w KQkq - 0 1",
        player_color="White",
        objective="Apply the C-C-T formula: Checks come first! Calculate the forced checkmate on f7 with your Queen!",
        expected_moves=["f3f7"],
        guided_move="f3f7",
        cm_intro=(
            "Welcome to calculation training, {username}! Calculation means visualizing moves before touching a piece. "
            "Use the C-C-T formula: 1. Checks, 2. Captures, 3. Threats. "
            "Your Bishop on c4 and Queen on f3 team up against f7. Execute the forced checkmate!"
        ),
        cm_success=(
            "MAGNIFICENT CALCULATION, {username}! You calculated the forcing sequence and delivered the final blow!"
        ),
        cm_hint="Strike f7 with your Queen to deliver checkmate.",
        educational_note="Always calculate using C-C-T: 1. Checks, 2. Captures, 3. Threats. Forcing moves are the heart of tactical calculation.",
        hints=[
            "Scan for the most forcing move on the board.",
            "f7 is defended only by the Black King and attacked twice by you.",
            "Queen takes f7 delivers checkmate!",
        ],
        theory_detail="Calculation is chess's superpower. Forcing moves (checks and captures) drastically reduce opponent choices, making victory predictable.",
        feedback_correct="Qxf7# delivers unstoppable checkmate. The complete calculation formula succeeded!",
        feedback_incorrect="Find the most forcing checkmate on f7 with your queen: Qxf7#",
        opponent_threat="Black's knight on e4 attacks White's Queen.",
        why_mistakes_fail={"f3e4": "Qxe4 captures material but misses the forced checkmate Qxf7#."},
        real_application="Grandmaster Alexander Kotov formalized candidate moves and C-C-T in his legendary book 'Think Like a Grandmaster'.",
        assessment_question="Why should you calculate forcing moves (checks and captures) first?",
        assessment_options=["Because they severely restrict the opponent's legal replies, making the calculation concrete and predictable", "Because they always win material", "Because rules require it", "Because engines say so"],
        assessment_answer_index=0,
        assessment_explanation="Forcing moves (checks, captures) narrow the opponent's legal options, drastically simplifying and clarifying the calculation tree.",
    ),
    Lesson(
        id="calc_candidate_moves",
        category="Advanced Calculation",
        level_number=5,
        level_name="Advanced Calculation",
        difficulty="Advanced",
        topic="candidate_moves",
        title="26. Finding Candidate Moves Before Calculating",
        concept="Do not calculate the first move you see! Pause, brainstorm 3-4 candidate moves across the entire board, and only then calculate lines deeply.",
        fen="r1b2rk1/pp1n1ppp/2p1p3/q2p2B1/2PP4/2PBPN2/P1Q2PPP/R4RK1 w - - 0 1",
        player_color="White",
        objective="Select the most forcing candidate move: Bxh7+ shatters Black's Kingside pawn structure with check!",
        expected_moves=["d3h7"],
        guided_move="d3h7",
        cm_intro=(
            "Broaden your vision, {username}! When you spot a good move, STOP and look for a BETTER one! "
            "Identify candidate moves: cxd5, Bf4, or Bxh7+? "
            "Calculate Bxh7+: it's a check that wins a pawn and strips the Black King of shelter! Strike!"
        ),
        cm_success=(
            "Brilliant candidate selection, {username}! 1.Bxh7+ wins a key pawn with check, exposing the enemy monarch to lethal attack!"
        ),
        cm_hint="Capture the h7 pawn with your bishop on d3.",
        educational_note="Tunnel vision is the #1 calculation defect. Always list 3 distinct candidate moves before calculating variations.",
        hints=[
            "White has a battery with Queen on c2 and Bishop on d3 aiming at h7.",
            "Capturing on h7 comes with check.",
            "Play Bishop takes h7: Bxh7+!",
        ],
        theory_detail="Candidate moves prevent hasty blunders and ensure tactical opportunities are never overlooked.",
        feedback_correct="1. Bxh7+ Kh8 claims a vital kingside pawn with check, opening lines against Black's King.",
        feedback_incorrect="Deliver check on h7 with your bishop: d3h7!",
        opponent_threat="Black threatens dxc4 followed by Nd5 with counterplay.",
        why_mistakes_fail={"c4d5": "cxd5 allows exd5 or cxd5 without exploiting the vulnerable h7 pawn."},
        real_application="Tunnel vision is the #1 cause of blunders: players calculate one line deeply without noticing a superior candidate move.",
        assessment_question="What is the biggest risk of calculating without identifying candidate moves first?",
        assessment_options=["You suffer from tunnel vision and overlook stronger moves or hidden opponent defensive resources", "You run out of pieces", "Your board flips", "The game ends automatically"],
        assessment_answer_index=0,
        assessment_explanation="Tunnel vision occurs when a player fixates on the first move seen and overlooks a far superior tactical or strategic alternative.",
    ),
    Lesson(
        id="calc_forcing_moves",
        category="Advanced Calculation",
        level_number=5,
        level_name="Advanced Calculation",
        difficulty="Advanced",
        topic="forcing_moves",
        title="27. Forcing Sequences & Eliminating Variations",
        concept="A forcing sequence gives the opponent no choices. When calculating, prefer moves that demand an immediate and unique response.",
        fen="r2q1rk1/pb3ppp/1pn1pn2/2ppN3/3P4/2PBPN2/PP3PPP/R2Q1RK1 w - - 0 1",
        player_color="White",
        objective="Eliminate defensive resources by capturing on c6 with your knight to damage Black's pawn structure!",
        expected_moves=["e5c6", "d3h7"],
        guided_move="e5c6",
        cm_intro=(
            "Master the forcing path, {username}! Look at Black's knight on c6. By trading on c6, you force Black to recapture, "
            "damaging their pawn structure and eliminating their central piece. Play Nxc6!"
        ),
        cm_success=(
            "Clean forcing exchange, {username}! Black is forced to recapture with the bishop or b-pawn, fixing their structure!"
        ),
        cm_hint="Capture Black's knight on c6 with your e5 knight.",
        educational_note="Forcing moves dramatically reduce your calculation workload because the opponent has only 1 or 2 legal replies.",
        hints=[
            "White's knight on e5 is actively posted.",
            "Take Black's c6 knight to force a recapture.",
            "Play e5 takes c6: Nxc6!",
        ],
        theory_detail="Forcing moves clarify complex positions by stripping away unnecessary branches in the calculation tree.",
        feedback_correct="1. Nxc6 forces Black to recapture, clarifying White's positional advantage.",
        feedback_incorrect="Make the forcing capture on c6: e5c6!",
        opponent_threat="Black's pieces are coordinated to break in the center with cxd4.",
        why_mistakes_fail={"d4c5": "dxc5 surrenders the center without creating any forcing threat."},
        real_application="Mikhail Tal looked for forcing complications that exceeded human calculation capacity, trusting in dynamic pressure.",
        assessment_question="What makes a move 'forcing' in chess calculation?",
        assessment_options=["It creates a direct threat (like check or capture) that requires an immediate and narrow reply", "It is played quickly", "It is a pawn move", "It threatens castling"],
        assessment_answer_index=0,
        assessment_explanation="Forcing moves (checks, captures, direct threats) compel the opponent into a narrow corridor of defensive replies.",
    ),
    Lesson(
        id="calc_king_hunt",
        category="Advanced Calculation",
        level_number=5,
        level_name="Advanced Calculation",
        difficulty="Advanced",
        topic="sacrifices",
        title="28. The Greek Gift Sacrifice (Bxh7+)",
        concept="The classic bishop sacrifice on h7 (Bxh7+ followed by Ng5+ and Qh5) shatters the castled King's pawn fortress.",
        fen="r1bq1rk1/ppp2ppp/2n1pn2/3p4/3P4/2PBPN2/PP1N1PPP/R2QK2R w KQ - 0 1",
        player_color="White",
        objective="Shatter Black's kingside shelter by executing the Greek Gift sacrifice: 1.Bxh7+!",
        expected_moves=["d3h7"],
        guided_move="d3h7",
        cm_intro=(
            "The historic Greek Gift sacrifice, {username}! When Black's King is castled and the f6 knight is absent or vulnerable, "
            "sacrificing the bishop on h7 tears open the King's shelter for a lethal follow-up attack! "
            "Sacrifice on h7 with check!"
        ),
        cm_success=(
            "SENSATIONAL SACRIFICE, {username}! 1.Bxh7+ pulls the Black King onto the open h-file where Queen and Knight will deliver mate!"
        ),
        cm_hint="Sacrifice your bishop on h7 with check: d3h7.",
        educational_note="The Greek Gift requires: a Bishop on d3, a Knight ready to jump to g5, and Queen access to h5 or g4.",
        hints=[
            "White has the classic Greek Gift attacking pieces aligned.",
            "Strike the h7 pawn with your d3 bishop.",
            "Play Bishop takes h7: Bxh7+!",
        ],
        theory_detail="Sacrificing material to expose the enemy king is sound when the resulting attack guarantees decisive material recovery or checkmate.",
        feedback_correct="1. Bxh7+ Kxh7 2. Ng5+ initiates the unstoppable Greek Gift mating attack.",
        feedback_incorrect="Execute the bishop sacrifice: d3 takes h7+!",
        opponent_threat="Black plans Re8 and e5, freeing their position if White does not strike.",
        why_mistakes_fail={"e1g1": "Standard castling gives Black time to play h6, forever preventing the Greek Gift sacrifice."},
        real_application="First documented in Gioachino Greco's manuscripts in 1619, the Greek Gift has decided thousands of master games.",
        assessment_question="What key condition is typically required for the Greek Gift (Bxh7+) sacrifice to succeed?",
        assessment_options=["A white Knight ready to jump to g5, a Queen able to reach h5, and no black Knight guarding f6", "Two queens on the board", "Opponent King in stalemate", "All rooks traded"],
        assessment_answer_index=0,
        assessment_explanation="The Greek Gift requires rapid Queen and Knight entry to h5/g5 without an enemy knight defending f6.",
    ),
    Lesson(
        id="calc_desperado",
        category="Advanced Calculation",
        level_number=5,
        level_name="Advanced Calculation",
        difficulty="Advanced",
        topic="zwischenzug",
        title="29. In-Between Moves (Zwischenzug) & Desperado",
        concept="Before making an expected response (like recapturing a piece), look for a 'Zwischenzug'—an intermediate check or threat that changes the evaluation.",
        fen="r1bqk2r/ppp2ppp/2n2n2/3P4/1bB5/2N2N2/PP3PPP/R1BQK2R b KQkq - 0 8",
        player_color="Black",
        objective="Deliver an in-between check with your bishop on c3 (Bxc3+) before saving your attacked knight on c6!",
        expected_moves=["b4c3", "d8e7"],
        guided_move="b4c3",
        cm_intro=(
            "Welcome to the Zwischenzug (in-between move), {username}! White played d5, attacking your c6 knight. "
            "Don't retreat immediately! Play the intermediate capture 1...Bxc3+ with check first! "
            "White must respond to check, damaging their pawn structure before you deal with the knight!"
        ),
        cm_success=(
            "Genius calculation, {username}! 1...Bxc3+ forces White to recapture with the b-pawn, wrecking their queenside structure!"
        ),
        cm_hint="Capture the c3 knight with your bishop to deliver an in-between check.",
        educational_note="Zwischenzug is the German word for 'intermediate move'. Inserting an in-between check frequently turns lost positions into wins.",
        hints=[
            "Before saving the knight, check if you have an active intermediate move.",
            "b4 bishop can capture c3 with check.",
            "Play Bishop takes c3 with check: Bxc3+!",
        ],
        theory_detail="Intermediate checks disrupt the opponent's planned recapture sequence, completely resetting the tactical evaluation.",
        feedback_correct="1... Bxc3+ inserts a devastating intermediate check, ruining White's queenside pawn structure.",
        feedback_incorrect="Insert the intermediate check on c3: b4xc3+!",
        opponent_threat="White's d5 pawn attacks Black's knight on c6.",
        why_mistakes_fail={"c6e7": "Moving the knight immediately allows White's bishop to maintain dominant pin and pressure."},
        real_application="World Champion Viswanathan Anand was famous for shocking opponents with lethal intermediate checks.",
        assessment_question="What is a 'Zwischenzug' (in-between move) in chess tactics?",
        assessment_options=["An unexpected intermediate move that interrupts the anticipated sequence with an urgent threat", "A move played between games", "A draw offer", "A pawn promotion"],
        assessment_answer_index=0,
        assessment_explanation="A Zwischenzug interrupts the expected move sequence (e.g. recapturing) with an intermediate threat or check that turns the tables.",
    ),
    Lesson(
        id="calc_counterattack",
        category="Defensive Skills",
        level_number=5,
        level_name="Advanced Calculation",
        difficulty="Advanced",
        topic="counterattack",
        title="30. Defensive Counterattacks & Turning the Tables",
        concept="The best defense is often a counterattack. When threatened with devastating material loss, look for a counter-check or threat against the enemy King.",
        fen="3r4/4k3/8/8/3Q4/8/8/4K3 w - - 0 1",
        player_color="White",
        objective="Black's Rook on d8 attacks your Queen on d4! Escape with check by moving the Queen to e5!",
        expected_moves=["d4e5"],
        guided_move="d4e5",
        cm_intro=(
            "Under fire, {username}! Black's Rook on d8 is skewering your Queen down the d-file. "
            "Queens must never be surrendered lightly! "
            "Evacuate your Queen to e5: escape the attack AND deliver a powerful check to the Black King!"
        ),
        cm_success=(
            "Brilliant tactical defense, {username}! You escaped the rook's crosshairs and countered with check. "
            "Counter-checks frequently extinguish the opponent's initiative entirely!"
        ),
        cm_hint="Move your Queen from d4 to e5 to escape attack and check Black's King.",
        educational_note="When defending against an attack, always ask: 'Can I counterattack with a check or threaten a more valuable piece?'",
        hints=[
            "Observe Black's rook on d8 aiming at your Queen.",
            "e5 is a safe central square that checks Black's King on e7.",
            "Move Queen to e5 with check: Qe5+!",
        ],
        theory_detail="Counter-checks combine defense and attack in a single move, immediately transferring the initiative back to you.",
        feedback_correct="Qe5+ parries the skewer threat while seizing the initiative with check.",
        feedback_incorrect="Move your queen to e5 with check: Qe5+!",
        opponent_threat="Black's rook on d8 pins and threatens White's Queen.",
        why_mistakes_fail={"d4d8": "Trading queen for rook without check surrenders White's decisive winning advantage."},
        real_application="Emanuel Lasker, World Champion for 27 years, specialized in defensive counterattacks from desperate-looking positions.",
        assessment_question="When your heavy piece is under attack, what should you calculate before passively fleeing?",
        assessment_options=["Can I counterattack with check or attack a more valuable enemy target?", "Should I resign immediately?", "Can I hide the piece off the board?", "Should I offer a draw?"],
        assessment_answer_index=0,
        assessment_explanation="Active defense through counter-threats and checks is far stronger than passive retreat in tactical struggles.",
    ),

    # -------------------------------------------------------------------------
    # LEVEL 6: ENDGAME MASTERY (Lessons 31 - 36)
    # -------------------------------------------------------------------------
    Lesson(
        id="endgame_opposition",
        category="Pro Strategies",
        level_number=6,
        level_name="Endgame Mastery",
        difficulty="Intermediate",
        topic="endgame_opposition",
        title="31. The Direct Opposition: Seizing the Critical Square",
        concept="In King and Pawn endgames, having the Kings face each other with one square between them forces the other King to yield.",
        fen="4k3/8/8/4K3/8/8/4P3/8 w - - 0 1",
        player_color="White",
        objective="Step forward with your King to e6 to take the direct opposition and force Black's King to give way!",
        expected_moves=["e5e6"],
        guided_move="e5e6",
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
            "Kings are facing each other on the e-file.",
            "Push your King into e6 with direct opposition.",
            "Play King e5 to e6: Ke6!",
        ],
        theory_detail="Seizing the opposition outflanks the opposing King, clearing an unblockable promotion lane for your passed pawn.",
        feedback_correct="1. Ke6 claims the opposition, forcing Black's King to surrender the key promotion squares.",
        feedback_incorrect="Take the opposition by stepping forward: Ke5 to e6!",
        opponent_threat="Black's King wants to maintain blockade on e7 and d8.",
        why_mistakes_fail={"e5f6": "Stepping to f6 surrenders the opposition; Ke6 forces Black's King to step aside!"},
        real_application="Understanding opposition separates master endgame players from amateurs. It is purely deterministic.",
        assessment_question="Who holds 'the opposition' when two Kings face each other with one square between them?",
        assessment_options=["The player who does NOT have to move", "The player whose turn it is to move", "The player with White pieces", "Whoever has higher rating"],
        assessment_answer_index=0,
        assessment_explanation="The player who does not have to move holds the opposition because the opponent is forced to yield ground.",
    ),
    Lesson(
        id="curr_pawn_promotion",
        category="Endgames",
        level_number=6,
        level_name="Endgame Mastery",
        difficulty="Intermediate",
        topic="pawn_promotion",
        title="32. Escorting Passed Pawns to Promotion",
        concept="A passed pawn has no enemy pawns obstructing its path to the 8th rank. In the endgame, escorting passed pawns decides the game.",
        fen="8/4P3/8/8/8/8/8/4K2k w - - 0 1",
        player_color="White",
        objective="Advance your passed pawn from e7 to e8 and promote to a Queen (e8=Q) to seal victory!",
        expected_moves=["e7e8q", "e7e8r"],
        guided_move="e7e8q",
        cm_intro=(
            "Promote to victory, {username}! When a pawn reaches the 8th rank, it transforms into a Queen, Rook, Bishop, or Knight. "
            "Push your e7 pawn to e8 and select a Queen to deliver checkmate power!"
        ),
        cm_success=(
            "All hail the new Queen, {username}! You promoted the passed pawn cleanly. The endgame is completely won!"
        ),
        cm_hint="Advance your pawn from e7 to e8 and select the Queen.",
        educational_note="Passed pawns must be pushed! Always calculate the 'Rule of the Square' to see if the enemy King can catch the pawn.",
        hints=[
            "Your pawn is on the 7th rank, one step from glory.",
            "Promoting to a Queen gives you 9 points of overwhelming material.",
            "Play e7 to e8 and promote to Queen!",
        ],
        theory_detail="Promoting a passed pawn into a Queen is the definitive conversion goal of all pawn endgames.",
        feedback_correct="1. e8=Q promotes the pawn into a Queen, sealing the victory.",
        feedback_incorrect="Advance your pawn to the 8th rank: e7e8q!",
        opponent_threat="Black King is in the corner waiting for stalemate tricks.",
        why_mistakes_fail={"e1f2": "Stalemate blunder! White must promote the passed pawn to claim the win."},
        real_application="Capablanca stated that passed pawns must be pushed; they tie down enemy pieces or queen.",
        assessment_question="What is an 'outside passed pawn' in chess endgames?",
        assessment_options=["A passed pawn on a flank far away from the main group of pieces, acting as a decoy to divert the enemy King", "A pawn outside the board", "A doubled pawn", "A pawn that cannot promote"],
        assessment_answer_index=0,
        assessment_explanation="An outside passed pawn sits on a far flank, forcing the opposing King to abandon central defenses to stop it.",
    ),
    Lesson(
        id="endgame_lucena",
        category="Endgame Mastery",
        level_number=6,
        level_name="Endgame Mastery",
        difficulty="Advanced",
        topic="lucena_position",
        title="33. The Lucena Position: Building a Bridge",
        concept="The Lucena is the golden blueprint for winning Rook and Pawn endings: cut off the enemy King, advance the Rook to the 4th rank, and build a protective bridge.",
        fen="1K1k4/1P6/8/8/8/8/r7/2R5 w - - 0 1",
        player_color="White",
        objective="Initiate the Lucena Bridge technique: check the Black King on d1 with your Rook to drive it two files away!",
        expected_moves=["c1d1"],
        guided_move="c1d1",
        cm_intro=(
            "The mother of all rook endgames, {username}! This is the legendary Lucena Position. "
            "Your pawn is on the 7th rank, but your King is trapped on b8 by Black's rook. "
            "Step 1: Check Black's King with 1.Rd1+! Drive the King away from the c-file so your King can escape!"
        ),
        cm_success=(
            "Flawless Step 1, {username}! By checking with Rd1+, you force Black's King to the e-file. Next you lift the rook to d4 to build the bridge!"
        ),
        cm_hint="Move your rook from c1 to d1 to check Black's King.",
        educational_note=(
            "The Lucena Position (first analyzed in 1497) is completely winning. The winning method is: "
            "1. Check the King away, 2. Place Rook on the 4th rank (Rd4), 3. Walk the King out, 4. Shield against checks on the 4th rank."
        ),
        hints=[
            "White needs to drive the Black King away from the c-file.",
            "c1 rook can deliver check down the d-file.",
            "Play Rook to d1: Rd1+!",
        ],
        theory_detail="Building a bridge allows White's King to escape vertical rook checks, guaranteeing pawn promotion on the next move.",
        feedback_correct="1. Rd1+ drives Black's King to the e-file, executing Phase 1 of the Lucena bridge.",
        feedback_incorrect="Deliver check with your rook on d1: c1d1!",
        opponent_threat="Black's rook on a2 cuts off White's King from stepping out of the promotion square.",
        why_mistakes_fail={"b8a7": "Ka7 walks into Ra2+ checks forever without bridge support."},
        real_application="Published by Lucena in 1497, this remains the single most important theoretical rook endgame in chess history.",
        assessment_question="In the Lucena position, what is the purpose of 'building a bridge' with the Rook on the 4th rank?",
        assessment_options=["To shield the friendly King from vertical enemy Rook checks so the pawn can promote", "To castle late in the game", "To trade Queens", "To deliver back-rank checkmate"],
        assessment_answer_index=0,
        assessment_explanation="The 4th-rank bridge intercepts vertical checks from the opponent's rook, allowing the friendly King to emerge and promote the pawn.",
    ),
    Lesson(
        id="endgame_philidor",
        category="Endgame Mastery",
        level_number=6,
        level_name="Endgame Mastery",
        difficulty="Advanced",
        topic="philidor_defense",
        title="34. The Philidor Position: 3rd Rank Defense",
        concept="The Philidor Defense is the universal drawing method in Rook endgames: hold the 3rd rank with your Rook, and drop to the 8th rank for checks when the pawn pushes.",
        fen="8/8/8/4k3/8/4r3/4K1R1/8 w - - 0 1",
        player_color="White",
        objective="Maintain defensive resilience by stepping your King to d2 or f2, keeping pressure on Black's active rook!",
        expected_moves=["e2d2", "e2f2"],
        guided_move="e2d2",
        cm_intro=(
            "The master of drawing technique, {username}! When defending against an aggressive King and Rook, "
            "Philidor's method holds the draw. Step your King to d2 or f2 to keep contact and preserve defensive stability!"
        ),
        cm_success=(
            "Solid defense, {username}! You maintained king coordination. White safely draws against Black's active pieces."
        ),
        cm_hint="Move your King to d2 or f2.",
        educational_note=(
            "Philidor analyzed this drawing technique in 1777. Keep your Rook on the 3rd (or 6th) rank until the enemy pawn pushes, "
            "then drop your Rook to the back rank to check from behind infinitely."
        ),
        hints=[
            "White King is attacked by Black's rook.",
            "Step out of check to d2 or f2.",
            "Play King to d2: Kd2!",
        ],
        theory_detail="Philidor's defense guarantees a fortress draw against passed pawns on ranks 4 and 5.",
        feedback_correct="1. Kd2 defends accurately, holding the drawing fortress.",
        feedback_incorrect="Step your king out of check: e2d2 or e2f2!",
        opponent_threat="Black's active King and Rook threaten to drive White's King away.",
        why_mistakes_fail={"e2f1": "Stepping to the back rank prematurely allows Black to advance Kd4-e4 effortlessly."},
        real_application="Francois-Andre Danican Philidor analyzed this technique in 1777; every grandmaster knows it by heart.",
        assessment_question="In Philidor's Rook endgame defense, when does the defending Rook drop back to the 8th/1st rank?",
        assessment_options=["As soon as the opponent's pawn crosses to the 6th rank, so the Rook can give infinite checks from behind", "On move 1", "When the King is checkmated", "Never"],
        assessment_answer_index=0,
        assessment_explanation="When the pawn reaches the 6th rank, it can no longer shelter its King from rear checks, allowing infinite vertical checks from behind.",
    ),
    Lesson(
        id="endgame_rook_pawn",
        category="Endgame Mastery",
        level_number=6,
        level_name="Endgame Mastery",
        difficulty="Intermediate",
        topic="rook_endgames",
        title="35. Active Rooks in Rook Endgames",
        concept="Active rooks that deliver checks and cut off the enemy King are the secret to winning rook endgames.",
        fen="1R6/8/8/8/8/8/4K1k1/7r w - - 0 1",
        player_color="White",
        objective="Deliver check with your active Rook by sliding from b8 to g8 to drive the Black King away!",
        expected_moves=["b8g8"],
        guided_move="b8g8",
        cm_intro=(
            "Active rooks rule endgames, {username}! Tarrasch's eternal rule: 'Rooks belong behind passed pawns and on active cutting files.' "
            "Slide your Rook from b8 to g8 to deliver check and isolate the Black King!"
        ),
        cm_success=(
            "Magnificent play, {username}! You cut off the enemy King and seized total rook activity!"
        ),
        cm_hint="Slide your rook horizontally along the 8th rank from b8 over to g8 to deliver check.",
        educational_note="In rook endgames, passive defense almost always loses. Keep your rook active and aggressively cut off the enemy King.",
        hints=[
            "Observe the line of the g-file: Black King on g2.",
            "b8 rook can swing across rank 8 to g8.",
            "Play Rook to g8 with check: Rg8+!",
        ],
        theory_detail="Rooks are long-range pieces. Confining them to passive defense diminishes their value by more than half.",
        feedback_correct="1. Rg8+ checks the King, forcing Black into a passive retreat.",
        feedback_incorrect="Deliver check along the 8th rank: b8g8!",
        opponent_threat="Black's rook on h1 and King on g2 threaten Rh2+ mating nets.",
        why_mistakes_fail={"b8b2": "Rb2 is passive and allows Black King to remain menacing on g2."},
        real_application="Rook endgames occur in over 50% of tournament endgames. An active Rook is often worth a full pawn or more.",
        assessment_question="Where do rooks belong in rook and pawn endgames according to Dr. Siegbert Tarrasch?",
        assessment_options=["Behind passed pawns (supporting your own or attacking the enemy's)", "On the corners of the board", "Trapped in front of your King", "Traded off immediately"],
        assessment_answer_index=0,
        assessment_explanation="Tarrasch's Rule states that rooks belong behind passed pawns—to support your own or constantly harass the enemy's.",
    ),
    Lesson(
        id="endgame_zugzwang",
        category="Endgame Mastery",
        level_number=6,
        level_name="Endgame Mastery",
        difficulty="Advanced",
        topic="zugzwang",
        title="36. Zugzwang & Triangulation",
        concept="Zugzwang occurs when any legal move a player makes damages their position. Triangulation loses a tempo to put the opponent in zugzwang.",
        fen="8/8/8/4k3/8/4K3/8/8 w - - 0 1",
        player_color="White",
        objective="Outflank the enemy King! Step your King to d3 (or f3) to take the initiative and claim the key squares!",
        expected_moves=["e3d3", "e3f3"],
        guided_move="e3d3",
        cm_intro=(
            "The magic of Zugzwang, {username}! In King endgames, passing your turn would often be ideal, but chess rules forbid it! "
            "Step your King to d3 or f3 to outflank Black's King and force them into yielding territory!"
        ),
        cm_success=(
            "Textbook outflanking, {username}! Whichever way Black moves, your King invades forward!"
        ),
        cm_hint="Move your King to d3 or f3.",
        educational_note="Triangulation is moving your King in a triangle (e.g. e3-d3-e4) to reach the same position while passing the move to the opponent.",
        hints=[
            "Direct opposition: step laterally to outflank.",
            "Kd3 or Kf3 forces Black to give ground.",
            "Play King to d3: Kd3!",
        ],
        theory_detail="Zugzwang is the unique hallmark of chess: having the move can be a lethal disadvantage.",
        feedback_correct="1. Kd3 outflanks Black, putting the opponent into zugzwang.",
        feedback_incorrect="Move your King to d3 or f3 to outflank: e3d3!",
        opponent_threat="Black holds equal space if White plays passively.",
        why_mistakes_fail={"e3e2": "Retreating loses the center; stepping to d3 or f3 demands Black yield ground."},
        real_application="Zugzwang is the unique hallmark of chess: having the move can be a lethal disadvantage.",
        assessment_question="What does the chess term 'Zugzwang' mean in practice?",
        assessment_options=["A position where any legal move the player makes will significantly worsen their position", "A winning pawn break", "A rapid tournament game", "An illegal move penalty"],
        assessment_answer_index=0,
        assessment_explanation="Zugzwang (German for 'compulsion to move') is a state where every legal move damages the player's position.",
    ),

    # -------------------------------------------------------------------------
    # LEVEL 7: COMPETITIVE CHESS (Lessons 37 - 42)
    # -------------------------------------------------------------------------
    Lesson(
        id="comp_positional_sac",
        category="Competitive Chess",
        level_number=7,
        level_name="Competitive Chess",
        difficulty="Advanced",
        topic="positional_sacrifice",
        title="37. The Positional Exchange Sacrifice",
        concept="Sacrificing a Rook for a minor piece (Knight or Bishop) to gain total positional dominance, eliminate a defender, or secure an eternal outpost.",
        fen="r4rk1/1ppq1ppp/p1np4/4p3/B2bP3/2NP1N2/PPP2PPP/R2Q1RK1 w - - 0 11",
        player_color="White",
        objective="Centralize your Knight to the dominating d5 outpost by playing 1.Nd5!",
        expected_moves=["c3d5", "a4c6"],
        guided_move="c3d5",
        cm_intro=(
            "Welcome to elite tournament strategy, {username}! Grandmasters do not fear giving up material for long-term dominance. "
            "Anchor your Knight on the magnificent d5 central square: it paralyzes Black's queenside and eyes fatal attacking outposts!"
        ),
        cm_success=(
            "Grandmaster mastery, {username}! Your Knight on d5 radiates total central authority. Black's position is cramped and passive!"
        ),
        cm_hint="Hop your knight from c3 to d5.",
        educational_note="Tigran Petrosian famously said: 'The exchange sacrifice is not a loss of material; it is the purchase of permanent positional assets.'",
        hints=[
            "d5 is an ideal central outpost.",
            "Black has no pawns able to drive the knight away.",
            "Play Knight from c3 to d5: Nd5!",
        ],
        theory_detail="A positional sacrifice does not aim for immediate checkmate, but for permanent structural control that chokes the opponent over 10-20 moves.",
        feedback_correct="1. Nd5 establishes a dominant central anchor that dictates the middlegame.",
        feedback_incorrect="Hop your knight to d5: c3d5!",
        opponent_threat="Black's bishop on d4 controls central squares and pressures White's queenside.",
        why_mistakes_fail={"f3d4": "Trading knight for bishop on d4 leaves Black with a strong pawn on d4 and easy play."},
        real_application="Tigran Petrosian famously said: 'The exchange is not a piece, it is a quality.' He won world titles with exchange sacrifices.",
        assessment_question="What is the goal of a 'positional sacrifice' as opposed to a tactical sacrifice?",
        assessment_options=["To gain long-term structural, positional, or square control rather than immediate forced checkmate or material recapture", "To blunder a piece on purpose", "To force a stalemate", "To save time on the clock"],
        assessment_answer_index=0,
        assessment_explanation="Positional sacrifices surrender material for enduring strategic advantages (outposts, light/dark square control, king safety).",
    ),
    Lesson(
        id="comp_punishing_mistakes",
        category="Competitive Chess",
        level_number=7,
        level_name="Competitive Chess",
        difficulty="Advanced",
        topic="punishing_mistakes",
        title="38. Punishing Opponent Mistakes: Immediate Retribution",
        concept="When an opponent makes a mistake, do not react with your pre-planned move. Pause, identify the defect, and strike immediately before they can recover.",
        fen="r1bqkb1r/pppp1ppp/2n5/4p3/2B1n3/2N2N2/PPPP1PPP/R1BQK2R w KQkq - 0 5",
        player_color="White",
        objective="Black blundered an overextended Knight to e4! Punish the mistake immediately by capturing on e4 with your knight!",
        expected_moves=["c3e4"],
        guided_move="c3e4",
        cm_intro=(
            "Eyes on the prize, {username}! Black overreached and hopped their knight to e4 without sufficient support. "
            "Never let a blunder pass! Strike immediately: capture the knight on e4 with your c3 knight!"
        ),
        cm_success=(
            "Clinical retribution, {username}! You captured the overextended knight cleanly and seized commanding material superiority!"
        ),
        cm_hint="Take Black's knight on e4 with your c3 knight.",
        educational_note="Fischer's rule: 'Tactics flow from a superior position.' When your opponent plays an unsound move, punish it with clinical accuracy.",
        hints=[
            "Black's e4 knight is defended only by tactics that fail.",
            "Take the knight with your c3 knight.",
            "Play c3 takes e4: Nxe4!",
        ],
        theory_detail="Refuting blunders requires objective calculation: don't assume the opponent had a secret master plan.",
        feedback_correct="1. Nxe4 claims a full minor piece, immediately punishing Black's tactical oversight.",
        feedback_incorrect="Capture Black's blunder on e4: c3xe4!",
        opponent_threat="Black jumped their Knight to e4 without sufficient tactical justification.",
        why_mistakes_fail={"c4f7": "Bxf7+ is an unsound speculative sacrifice; Nxe4 cleanly wins a piece and cements advantage."},
        real_application="Fischer's motto: 'Tactics flow from a superior position.' When opponents err, clinical execution wins.",
        assessment_question="What should you do the moment your opponent plays an unexpected, flawed move?",
        assessment_options=["Pause, recalculate, find what is left undefended, and punish the mistake directly", "Play instantly", "Follow your old plan without thinking", "Offer a draw"],
        assessment_answer_index=0,
        assessment_explanation="When an opponent blunders, pause, calculate the concrete refutation, and strike before they can repair the defect.",
    ),
    Lesson(
        id="comp_opponent_styles",
        category="Competitive Chess",
        level_number=7,
        level_name="Competitive Chess",
        difficulty="Advanced",
        topic="opponent_styles",
        title="39. Neutralizing Aggressive Attackers",
        concept="Against wild attackers: do not panic, trade off their attacking pieces, consolidate king safety, and convert the resulting superior endgame.",
        fen="r1bqk2r/pppp1ppp/2n2n2/4p3/1bB1P3/2N2N2/PPPP1PPP/R1BQK2R w KQkq - 4 5",
        player_color="White",
        objective="Neutralize Black's pin and attack by castling kingside (O-O) to consolidate total King safety!",
        expected_moves=["c3d5", "e1g1"],
        guided_move="e1g1",
        cm_intro=(
            "Facing an aggressive attacker, {username}! Aggressive players want chaos and tactical firefights. "
            "How do you neutralize them? Solid, classical development! Castle kingside (O-O): tuck your king away and remove all cheap tactical targets!"
        ),
        cm_success=(
            "Ice in your veins, {username}! By castling safely, you sucked the oxygen out of Black's attack. The initiative is yours!"
        ),
        cm_hint="Castle kingside: e1g1.",
        educational_note="Against tactical attackers, exchange pieces and steer the game toward a quiet endgame where their positional weaknesses are fatal.",
        hints=[
            "Don't compromise your pawn structure unnecessarily.",
            "Tuck the King away into safety.",
            "Play King e1 to g1 to castle: O-O!",
        ],
        theory_detail="Solid prophylaxis and King safety deflate premature attacks, leaving attackers exhausted and overextended.",
        feedback_correct="1. O-O neutralizes Black's tactical ambition and establishes a rock-solid foundation.",
        feedback_incorrect="Castle kingside to extinguish the attack: e1g1!",
        opponent_threat="Black wants to pin on c3 and launch kingside attacks; White castles safely and dampens all threats.",
        why_mistakes_fail={"d1e2": "Delaying castling plays directly into the attacker's hands."},
        real_application="Karpov famously neutralized aggressive attackers like Kasparov and Spassky by methodically trading their attacking pieces.",
        assessment_question="What is the most effective psychological and tactical counter to a wild, aggressive attacker?",
        assessment_options=["Solid defense, trading off their attacking pieces, and forcing a quiet endgame where their weaknesses show", "Attacking even more wildly without calculating", "Resigning", "Copying all their moves"],
        assessment_answer_index=0,
        assessment_explanation="Trading pieces deprives attackers of their tactical firepower and forces them into technical endgames where they struggle.",
    ),
    Lesson(
        id="comp_prophylaxis_tourney",
        category="Competitive Chess",
        level_number=7,
        level_name="Competitive Chess",
        difficulty="Advanced",
        topic="prophylaxis",
        title="40. Tournament Prophylaxis & Defensive Resourcefulness",
        concept="In competitive tournament chess, high-level players constantly eliminate future counterplay with small, patient consolidating moves like h3 or a3.",
        fen="r2q1rk1/ppp2ppp/2n1bn2/3p4/3P4/2PBPN2/PP1N1PPP/R2Q1RK1 w - - 0 1",
        player_color="White",
        objective="Play prophylactic move 1.h3 to permanently prevent Black's annoying Bg4 pin on your f3 knight!",
        expected_moves=["h2h3", "d1c2"],
        guided_move="h2h3",
        cm_intro=(
            "Tournament prophylaxis, {username}! Look at Black's light-squared bishop on e6: it wants to jump to g4, pinning your f3 knight. "
            "Play the patient master move 1.h3! You control g4 forever, denying Black any active outpost!"
        ),
        cm_success=(
            "Elite tournament technique, {username}! 1.h3 shuts down Black's active bishop jump, leaving White with undisputed harmony!"
        ),
        cm_hint="Push your h2 pawn forward one square to h3.",
        educational_note="In closed and semi-closed positions, spending one tempo on h3 or a3 to deny an outpost is worth its weight in gold.",
        hints=[
            "Observe the g4 square.",
            "A small pawn step to h3 controls g4 permanently.",
            "Play h2 to h3: h3!",
        ],
        theory_detail="Prophylactic pawn moves prevent annoying enemy pins and create a 'Luft' (escape square) for the King against back-rank mates.",
        feedback_correct="1. h3 restricts Black's bishop and secures White's Kingside harmony.",
        feedback_incorrect="Play the prophylactic pawn push: h2h3!",
        opponent_threat="Black wants to jump Bg4 pinning White's knight and seizing initiative.",
        why_mistakes_fail={"f1e1": "Re1 ignores Black's Bg4 pin; h3 controls g4 permanently."},
        real_application="Boris Spassky noted that world champions make moves that look like nothing until 10 moves later when the opponent has no counterplay.",
        assessment_question="Why do master players frequently play quiet moves like h3 or a3 in tournament games?",
        assessment_options=["To prevent annoying enemy knight and bishop pins on g4/b4 before launching their own plans", "Because they have no other moves", "To waste clock time", "Because pawns are bored"],
        assessment_answer_index=0,
        assessment_explanation="Small prophylactic moves like h3/a3 extinguish enemy pins and outposts, ensuring your pieces operate with full mobility.",
    ),
    Lesson(
        id="comp_simplification",
        category="Competitive Chess",
        level_number=7,
        level_name="Competitive Chess",
        difficulty="Advanced",
        topic="conversion",
        title="41. Converting Advantages by Simplification",
        concept="When ahead in material or position, trading pieces (especially Queens and Rooks) eliminates counterplay and produces an easily converted endgame.",
        fen="2r3k1/5ppp/8/8/4B3/8/5PPP/2R3K1 w - - 0 1",
        player_color="White",
        objective="Simplify into an easily won endgame! Capture Black's rook on c8 with your c1 rook: 1.Rxc8+!",
        expected_moves=["c1c8"],
        guided_move="c1c8",
        cm_intro=(
            "The art of conversion, {username}! You are up a full Bishop (+3). "
            "How do champions win won games? SIMPLIFY! Trade off the rooks on c8: "
            "once heavy pieces disappear, your extra Bishop will effortlessly gobble up Black's pawns!"
        ),
        cm_success=(
            "Clinical conversion, {username}! You traded rooks and transitioned into a completely winning Bishop endgame. Flawless technique!"
        ),
        cm_hint="Take Black's rook on c8 with your c1 rook.",
        educational_note="Simplification is the safest path to victory. When ahead in material, trade pieces (not pawns) to extinguish all opposing counterplay.",
        hints=[
            "White has an extra bishop.",
            "Trading rooks eliminates all Black counter-checks.",
            "Play c1 takes c8: Rxc8+!",
        ],
        theory_detail="Reducing the number of pieces on the board exponentially reduces the opponent's tactical chances.",
        feedback_correct="1. Rxc8+ cleanly exchanges the heavy pieces, leaving Black helpless against the extra bishop.",
        feedback_incorrect="Trade rooks on c8: c1xc8+!",
        opponent_threat="Black's rook on c8 threatens counter-checks or back-rank trades on Black's terms.",
        why_mistakes_fail={"e4h7": "Bxh7+ trades a bishop for a pawn but leaves Black's rook active on c8; Rxc8+ simplifies into a clean winning endgame."},
        real_application="Capablanca's technique: Up a piece? Trade everything down until you have a King and Pawn endgame that plays itself.",
        assessment_question="Why should a player who is up a piece generally trade pieces but NOT pawns?",
        assessment_options=["Trading pieces eliminates the opponent's attacking chances, while keeping pawns preserves winning promotion targets", "Pieces are worth less in the endgame", "Pawns cannot be traded", "The opponent gets bonus time"],
        assessment_answer_index=0,
        assessment_explanation="Trading pieces kills enemy counterplay and King attacks; keeping pawns gives you pawns to promote into Queens.",
    ),
    Lesson(
        id="comp_grandmaster_finish",
        category="Competitive Chess",
        level_number=7,
        level_name="Competitive Chess",
        difficulty="Advanced",
        topic="grandmaster_finish",
        title="42. The Grandmaster Finish: Flawless Execution",
        concept="The final exam: calculate the forced back-rank deflection and mating net. A grandmaster never relaxes until the scoresheet is signed.",
        fen="6k1/5ppp/8/8/8/8/1Q3PPP/5RK1 w - - 0 1",
        player_color="White",
        objective="Deliver the final checkmate! Invade Black's back rank with Qb8# to graduate from the JD Chess Academy!",
        expected_moves=["b2b8"],
        guided_move="b2b8",
        cm_intro=(
            "The Grandmaster graduation, {username}! You have mastered beginner basics, tactical weapons, opening strategy, "
            "middlegame maneuvering, deep calculation, and endgame technique. "
            "Deliver the final blow: strike Black's back rank with Qb8# and claim your Grandmaster title!"
        ),
        cm_success=(
            "CHECKMATE! CONGRATULATIONS GRANDMASTER {username}!! "
            "You have conquered the 42-lesson JD Chess Academy! "
            "You know how to think, calculate, strategize, and win. The chessboard is yours!"
        ),
        cm_hint="Slide your Queen from b2 all the way to b8 to deliver checkmate.",
        educational_note="Grandmaster mindset: Always maintain concentration and play with maximum energy until the very final move.",
        hints=[
            "Black's King is trapped on g8 behind its own pawns.",
            "b8 is an undefended entry square along the back rank.",
            "Slide Queen to b8: Qb8#!",
        ],
        theory_detail="Back-rank checkmates illustrate the fatal consequence of neglecting King escape squares (Luft).",
        feedback_correct="1. Qb8# delivers unstoppable checkmate. The complete Academy curriculum has been mastered!",
        feedback_incorrect="Deliver checkmate on the back rank with your Queen: b2b8#",
        opponent_threat="Black threatens to push h6 or g6 and escape the back-rank vulnerability.",
        why_mistakes_fail={"b2e5": "Qe5 allows Black time to play h6 and escape the mating net."},
        real_application="You have conquered all 7 levels of the JD Chess Academy. You now understand how to think, calculate, strategize, and win!",
        assessment_question="What is the ultimate mindset of a competitive chess player?",
        assessment_options=["Constant vigilance: verify opponent threats, find candidate forcing moves, and play with strategic purpose on every move", "Hoping the opponent blunders", "Memorizing openings without understanding", "Playing as fast as possible"],
        assessment_answer_index=0,
        assessment_explanation="A competitive master plays with constant vigilance: respecting opponent threats, calculating candidate moves, and applying purposeful strategy.",
    ),
]


# =============================================================================
# CURRICULUM ACCESSORS & PROGRESSION HELPERS (O(1) Indexed Lookups)
# =============================================================================

_LESSONS_BY_ID: dict[str, Lesson] = {l.id: l for l in CURRICULUM}
_LESSONS_INDEX: dict[str, int] = {l.id: i for i, l in enumerate(CURRICULUM)}
_LESSONS_BY_LEVEL: dict[int, list[Lesson]] = {
    lvl: [l for l in CURRICULUM if l.level_number == lvl] for lvl in range(1, 8)
}
_LESSONS_BY_TOPIC: dict[str, list[Lesson]] = {}
for _l in CURRICULUM:
    _LESSONS_BY_TOPIC.setdefault(_l.topic, []).append(_l)


def get_curriculum() -> list[Lesson]:
    """Return all available lessons in the structured Academy curriculum."""
    return list(CURRICULUM)


def get_academy_levels() -> list[dict[str, Any]]:
    """Return metadata for all 7 Academy tiers."""
    return list(ACADEMY_LEVELS)


def get_lesson_by_id(lesson_id: str) -> Lesson | None:
    """Find a specific lesson by its unique string ID in O(1) time."""
    return _LESSONS_BY_ID.get(lesson_id)


def get_lessons_by_level(level_number: int) -> list[Lesson]:
    """Return all lessons belonging to a specific Academy level (1-7) in O(1) time."""
    return list(_LESSONS_BY_LEVEL.get(level_number, []))


def get_lessons_by_topic(topic: str) -> list[Lesson]:
    """Return all lessons associated with a given tactical or strategic topic in O(1) time."""
    return list(_LESSONS_BY_TOPIC.get(topic, []))


def get_next_lesson(current_id: str) -> Lesson | None:
    """Retrieve the lesson following current_id in the progression path in O(1) time."""
    idx = _LESSONS_INDEX.get(current_id)
    if idx is not None and idx + 1 < len(CURRICULUM):
        return CURRICULUM[idx + 1]
    return None


def get_prev_lesson(current_id: str) -> Lesson | None:
    """Retrieve the lesson preceding current_id in the progression path in O(1) time."""
    idx = _LESSONS_INDEX.get(current_id)
    if idx is not None and idx > 0:
        return CURRICULUM[idx - 1]
    return None
